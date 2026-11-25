"""
Работа с HTTP/HTTPS-запросами

Работает поверх библиотеки HTTPX, добавляя функции:
    - логирование DNS-обращений
    - логирование ответов
    - обращение по IP-адресу и заголовку Host
    - Установка User-Agent по умолчанию
"""
import logging
import httpx
import socket
import random
from typing import Optional, Dict, Any, Union, List, Tuple
from enum import Enum

# Функция получения session_id из контекста
from .session_context import get_session_id_str

__version__ = '1.0.1'

# Константы библиотеки
DEFAULT_TIMEOUT = 30.0
DEFAULT_USER_AGENT = "EiticaPuzzle/1.0"
DEFAULT_LOGGER_NAME = "HTTPClient"


class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class HTTPClient:
    def __init__(
        self,
        *,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str = DEFAULT_USER_AGENT,
        log_dns: bool = False,
        log_responses: bool = False,
        resolve_ip: bool = False,
        verify_ssl: bool = True,
    ):
        """
        Инициализация HTTP клиента.

        :param timeout: Таймаут запроса в секундах
        :param user_agent: User-Agent для запросов
        :param log_dns: Логировать DNS запросы
        :param log_responses: Логировать ответы серверов
        :param resolve_ip: Использовать IP адрес из DNS вместо домена
        :param verify_ssl: Проверять SSL сертификаты
        """
        self.timeout = timeout
        self.user_agent = user_agent
        self.log_dns = log_dns
        self.log_responses = log_responses
        self.resolve_ip = resolve_ip
        self.verify_ssl = verify_ssl
        self._client = None  #  Здесь храним клиент, чтобы корректно закрыть все соединения при выходе

        if self.log_dns or self.log_responses:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(DEFAULT_LOGGER_NAME)
            self.logger.setLevel(logging.INFO)

    def _log(self, level):
        if self.log_dns or self.log_responses:
            self.logger.setLevel(level)

    def log_info(self):
        self._log(logging.INFO)

    def log_debug(self):
        self._log(logging.DEBUG)

    def _resolve_domain_to_ip(self, domain: str) -> Optional[Tuple[str, List[str]]]:
        """
        Разрешает доменное имя в IP адрес(а), возвращает случайный выбранный IP и список всех IP.

        :param domain: Доменное имя для разрешения
        :return: Кортеж (выбранный IP, список всех IP) или None при ошибке
        """
        try:
            # Получаем все IPv4 адреса для домена
            addr_info = socket.getaddrinfo(domain, None, family=socket.AF_INET, proto=socket.IPPROTO_TCP)
            ip_addresses = list({info[4][0] for info in addr_info})  # Уникальные IP
            
            if not ip_addresses:
                if self.log_dns:
                    self.logger.warning(f"No IP addresses found for domain: {domain}")
                return None
            
            # Выбираем случайный IP из списка
            selected_ip = random.choice(ip_addresses)
            
            if self.log_dns:
                self.logger.info(f"DNS lookup: {domain} -> {ip_addresses} (selected: {selected_ip})")
            
            return selected_ip, ip_addresses
        except Exception as e:
            if self.log_dns:
                self.logger.error(f"DNS lookup failed for {domain}: {e}")
            return None

    def _add_session_header(self, headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        """
        Добавляет X-Session-ID в заголовки, если он доступен.

        Args:
            headers: Исходные заголовки

        Returns:
            Dict[str, str]: Заголовки с добавленным X-Session-ID
        """
        if headers is None:
            headers = {}

        # Не перезаписываем, если заголовок уже установлен явно
        if 'X-Session-ID' not in headers:
            session_id = get_session_id_str()
            if session_id:
                headers['X-Session-ID'] = session_id

        return headers


    async def _get_client(self) -> httpx.AsyncClient:
        """Получаем или создаем клиент"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self.timeout,
                verify=self.verify_ssl,
            )
        return self._client

    async def close(self):
        """Явное закрытие клиента"""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def _make_request(
        self,
        method: HTTPMethod,
        url: str,
        endpoint: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Union[Dict[str, Any], List[Any]]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> httpx.Response:
        """
        Универсальный метод для выполнения HTTP запросов.

        :param method: HTTP метод
        :param url: Базовый URL
        :param endpoint: Endpoint (будет объединен с URL)
        :param params: Параметры запроса
        :param json: Данные для отправки в формате JSON
        :param headers: Заголовки запроса
        :param kwargs: Дополнительные параметры для httpx
        :return: Объект ответа httpx
        """
        # Объединяем URL и endpoint
        full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}" if endpoint else url

        # Подготовка заголовков
        final_headers = headers or {}
        # Добавим заголовок для отслеживания сквозной сессии
        final_headers = self._add_session_header( final_headers )
        final_headers.setdefault("User-Agent", self.user_agent)

        # Настройки для использования IP из DNS
        if self.resolve_ip:
            try:
                from urllib.parse import urlparse

                parsed_url = urlparse(full_url)
                domain = parsed_url.hostname

                if domain:
                    # Получаем IP адрес(а)
                    resolution = self._resolve_domain_to_ip(domain)
                    if resolution:
                        ip, all_ips = resolution
                        
                        # Модифицируем URL и заголовки
                        full_url = full_url.replace(domain, ip)
                        final_headers["Host"] = domain
                        
                        if self.log_dns:
                            self.logger.info(f"Using IP: {ip} from available: {all_ips} for domain: {domain}")
            except Exception as e:
                if self.log_dns:
                    self.logger.error(f"DNS resolution failed: {e}")

        #   Получаем клиент через _get_client()
        client = await self._get_client()

        try:
            response = await client.request(
                method=method.value,
                url=full_url,
                params=params,
                json=json,
                headers=final_headers,
                **kwargs,
            )

            if self.log_responses:
                self.logger.info(
                    f"Response: {method.value} {full_url} - {response.status_code}"
                )
                #   Пытаемся распарсить JSON из тела ответа
                try:
                    parsed_json = response.json()
                    self.logger.debug(f"Response JSON: {parsed_json}")  # Если JSON-валиден, логируем его
                except Exception:
                    #   Во всех остальных случаях, посмотрим на ответ как есть
                    if response.content:
                        self.logger.debug(f"Response content: {response.text}")

            return response

        except Exception as e:
            #   Логируем ошибки запроса, если нужно
            if self.log_responses:
                self.logger.error(f"Request failed: {str(e)}")
            raise


    async def get(
        self,
        url: str,
        endpoint: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> httpx.Response:
        return await self._make_request(
            HTTPMethod.GET, url, endpoint, params=params, headers=headers, **kwargs
        )

    async def post(
        self,
        url: str,
        endpoint: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Union[Dict[str, Any], List[Any]]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> httpx.Response:
        return await self._make_request(
            HTTPMethod.POST,
            url,
            endpoint,
            params=params,
            json=json,
            headers=headers,
            **kwargs,
        )

    async def put(
        self,
        url: str,
        endpoint: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Union[Dict[str, Any], List[Any]]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> httpx.Response:
        return await self._make_request(
            HTTPMethod.PUT,
            url,
            endpoint,
            params=params,
            json=json,
            headers=headers,
            **kwargs,
        )

    async def delete(
        self,
        url: str,
        endpoint: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> httpx.Response:
        return await self._make_request(
            HTTPMethod.DELETE, url, endpoint, params=params, headers=headers, **kwargs
        )

    async def patch(
        self,
        url: str,
        endpoint: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Union[Dict[str, Any], List[Any]]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> httpx.Response:
        return await self._make_request(
            HTTPMethod.PATCH,
            url,
            endpoint,
            params=params,
            json=json,
            headers=headers,
            **kwargs,
        )
