import {demoRequest} from '../demoApi';
import axios from 'axios';
export const api = axios.create({baseURL:'/api',timeout:15000});
export const directoryApi = api;
let accessToken: string | null = null;
export function setAccessToken(token: string | null){accessToken=token;}
export function hasAccessToken(){return Boolean(accessToken);}
api.interceptors.request.use(config=>{if(accessToken)config.headers.set('Authorization',`Bearer ${accessToken}`);return config;});

if(import.meta.env.VITE_DEMO==='true')api.defaults.adapter=async config=>({data:await demoRequest(config.url||'/',(config.method||'get').toUpperCase(),typeof config.data==='string'?JSON.parse(config.data):config.data),status:200,statusText:'OK',headers:{},config});
