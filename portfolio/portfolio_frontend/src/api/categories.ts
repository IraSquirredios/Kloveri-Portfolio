import { directoryApi } from './client';
import type { Category } from '../productsData';

// The directory service wraps its array of category groups in data.
export function mapCategories(data: unknown): Category[] {
 if (!Array.isArray(data)) throw new Error('Неверный формат справочника категорий.');
 const result = new Map<string, Category>();
 for (const group of data) {
  if (!group || typeof group !== 'object' || Array.isArray(group)) {
   throw new Error('Неверный формат справочника категорий.');
  }
  for (const entry of Object.values(group)) {
   if (!entry || typeof entry !== 'object' || !('value' in entry) || !('title' in entry) ||
       typeof entry.value !== 'string' || typeof entry.title !== 'string') {
    throw new Error('Неверный формат категории.');
   }
   result.set(entry.value, { id: entry.value, name: entry.title });
  }
 }
 return [...result.values()];
}

export async function loadCategories(signal: AbortSignal) {
 const response = await directoryApi.get<{ data: unknown }>('/directory/product', { signal });
 return mapCategories(response.data?.data);
}
