import {api} from './client';
import type {Category} from '../productsData';
export async function loadCategories(signal:AbortSignal):Promise<Category[]>{return (await api.get('/categories',{signal})).data.data;}
