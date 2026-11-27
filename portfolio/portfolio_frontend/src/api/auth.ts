import {api,setAccessToken} from './client';
export async function signIn(email:string,password:string){const r=await api.post('/auth/login',{email,password});setAccessToken(r.data.token);}
export async function signUp(email:string,password:string){const r=await api.post('/auth/register',{email,password});setAccessToken(r.data.token);}
export function signInErrorMessage(error:unknown):string{const e=error as {response?:{data?:{message?:string}}};return e.response?.data?.message||'Не удалось подключиться к локальному сервису.';}
