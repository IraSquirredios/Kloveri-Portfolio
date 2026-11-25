# Portfolio. Cloveri Start

Новая версия страницы продуктов расположена в [`portfolio_frontend/`](portfolio_frontend/README.md).
Она включает React/TypeScript интерфейс по макету, авторизацию через сервис пользователей,
загрузку продуктов из Triada и категорий из сервиса справочников.

## Проверка новой версии

```sh
cd portfolio_frontend
npm ci
cp .env.example .env.local
# Заполнить VITE_PROJECT_ID и при необходимости VITE_ACCOUNT_ID.
npm run dev -- --configLoader runner
```

Для новой версии подготовлены `Dockerfile.portfolio`, nginx-прокси и официальный
тестовый CI/CD с runner `docker` и окружением стажировок. Порядок настройки и ручного
деплоя: [`deploy/README.md`](deploy/README.md). Нужны SERVICE_DOMAIN, INIT_TOKEN и ENV_FILE
в настройках проекта. Pipeline работает в нашей ветке и dev; master не развёртывает.

Локальные env-файлы, пароли и токены в репозиторий не включаются.
