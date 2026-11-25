import axios from 'axios';

export const api = axios.create({
 baseURL: import.meta.env.VITE_API_URL || '/api',
 timeout: 15000,
});

export const directoryApi = axios.create({
 baseURL: import.meta.env.VITE_DIRECTORY_API_URL || '/directory-api',
 timeout: 15000,
});

let accessToken: string | null = null;
export function setAccessToken(token: string | null) { accessToken = token; }
export function hasAccessToken() { return Boolean(accessToken); }

for (const client of [api, directoryApi]) client.interceptors.request.use(config => {
 const projectId = import.meta.env.VITE_PROJECT_ID?.trim();
 if (!projectId || !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(projectId)) {
  throw new Error('Укажите UUID проекта в VITE_PROJECT_ID и перезапустите фронтенд.');
 }
 config.headers.set('Project-ID', projectId);
 if (accessToken) config.headers.set('Authorization', `Bearer ${accessToken}`);
 return config;
});
