# Портфолио: фронтенд

React + TypeScript, Vite, Axios. Экран продуктов работает с готовыми сервисами без локального FastAPI.

## Запуск

Скопируйте `.env.example` в `.env.local`, заполните `VITE_PROJECT_ID` и при необходимости `VITE_ACCOUNT_ID`.

```sh
npm ci
npm run dev -- --configLoader runner
```

Откройте адрес из терминала (по умолчанию http://127.0.0.1:3003).
После изменения env перезапустите Vite. Пароли и токены не записываются в env.

## Запросы

| Назначение | Запрос браузера | Готовый сервис |
| --- | --- | --- |
| Вход | POST /auth-api/auth/login | https://api.users.skroy.ru/auth/login |
| Продукты | GET /api/account/my/products/ | https://platform.skroy.ru/account/my/products/ |
| Категории | GET /directory-api/directory/product | https://directory.basis.skroy.ru/directory/product |

Vite удаляет префикс прокси и пересылает запрос готовому сервису. Все запросы продуктов/справочников передают Project-ID и полученный Authorization: Bearer.
Вход отправляет username/password/grant_type=password как application/x-www-form-urlencoded, Project-ID и необязательный Account-ID.
Токен берётся из data[0].auth_data.access_token и хранится только в памяти. После обновления страницы нужен повторный вход.

Продукты загружаются с page/per_page=50 до неполной страницы. Ответ data преобразуется в карточки.
Справочник категорий возвращает data — массив групп; каждая категория имеет title/value.
Названия и описания сохраняются с сервера, стадии переводятся, известным продуктам назначаются иконки.
Карточки с точным названием «Тест»/«test» скрыты на фронте, серверные записи не удаляются.

## Публикация

Vite proxy предназначен для разработки. На сервере сайта настройте такие же маршруты прокси
или задайте прямые VITE_API_URL/VITE_DIRECTORY_API_URL при разрешённом CORS.
Маршрут /auth-api также должен проксироваться к сервису пользователей.
Собственный сервис проектов — отдельная задача; создание, изменение, удаление продуктов в интерфейсе пока не подключены.

## Проверки

```sh
node node_modules/typescript/bin/tsc -b
npm run lint
node node_modules/vite/bin/vite.js build --configLoader runner
```
