import axios from 'axios';
import { setAccessToken } from './client';

export async function signIn(username: string, password: string) {
 const projectId = import.meta.env.VITE_PROJECT_ID?.trim();
 if (!projectId) throw new Error('Укажите VITE_PROJECT_ID и перезапустите фронтенд.');
 const headers: Record<string, string> = { 'Project-ID': projectId };
 const accountId = import.meta.env.VITE_ACCOUNT_ID?.trim();
 if (accountId) headers['Account-ID'] = accountId;
 const body = new URLSearchParams({ username, password, grant_type: 'password' });
 const response = await axios.post('/auth-api/auth/login', body, { headers, timeout: 15000 });
 const token = response.data?.data?.[0]?.auth_data?.access_token;
 if (typeof token !== 'string' || !token) throw new Error('Сервис авторизации не вернул access_token.');
 setAccessToken(token);
}

export function signInErrorMessage(error: unknown): string {
 if (!axios.isAxiosError(error)) return error instanceof Error ? error.message : 'Не удалось выполнить вход.';
 if (error.code === 'ECONNABORTED' || error.code === 'ETIMEDOUT') {
  return 'Сервис входа не ответил за 15 секунд. Повторите попытку.';
 }
 const status = error.response?.status;
 if (status === 401 || status === 400) return 'Неверный логин или пароль. Проверьте введённые данные.';
 if (status === 403) return 'Сервис входа запретил доступ к этому проекту (HTTP 403).';
 if (status === 404) return 'Маршрут входа не найден (HTTP 404). Требуется перезапуск локального фронта.';
 if (status) return `Сервис входа вернул ошибку HTTP ${status}. Повторите попытку позже.`;
 return 'Нет ответа от локального сервера. Проверьте адрес страницы и доступность сервера разработки.';
}
