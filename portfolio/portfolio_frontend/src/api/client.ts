import axios from 'axios';
export const api = axios.create({baseURL:'/api',timeout:15000});
export const directoryApi = api;
let accessToken: string | null = null;
export function setAccessToken(token: string | null){accessToken=token;}
export function hasAccessToken(){return Boolean(accessToken);}
api.interceptors.request.use(config=>{if(accessToken)config.headers.set('Authorization',`Bearer ${accessToken}`);return config;});
