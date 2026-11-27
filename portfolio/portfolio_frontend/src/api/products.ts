import { api } from './client';
import type { Category, Product, IconName } from '../productsData';

export type PlatformProduct = {
 product_id: string | null;
 title: string | null;
 description?: { preview?: string | null; full?: string | null } | null;
 categories?: { title?: string | null; value?: string | null }[] | null;
 stage: string | null;
 status: string | null;
};



const stageLabels: Record<string, string> = {
 idea: 'Идея', mvp_development: 'Разработка MVP',
 implementation: 'Реализация', implemented: 'Реализован', stopped: 'Остановлен',
};
const productIcons: Record<string, IconName> = {
 'Сигма': 'sigma', 'Кружева': 'lace', 'Кловери': 'star', 'Тренды': 'bolt',
 'Майбо': 'medical', 'ClassHub': 'school', 'OmniNotice': 'bell',
 'Ресторатика': 'food', 'Цены в магазинах': 'wallet',
};

export function mapProducts(items: PlatformProduct[]): { products: Product[]; categories: Category[] } {
 const categories = new Map<string, Category>();
 const products = items.map(item => {
  const categoryIds = (item.categories || []).flatMap(category => {
   if (!category.value) return [];
   categories.set(category.value, { id: category.value, name: category.title || category.value });
   return [category.value];
  });
  return {
   id: item.product_id || undefined,
   product_name: item.title || 'Без названия',
   description: item.description?.preview || item.description?.full || '',
   status: stageLabels[item.stage || ''] || item.stage || item.status || '',
   icon: productIcons[item.title || ''] || 'folder',
   categoryIds,
  };
 });
 return { products, categories: [...categories.values()] };
}

export async function loadProducts(signal: AbortSignal) {
 const r=await api.get('/products',{signal});
 const raw=r.data.data as {id:string;title:string;description:string;stage:string;category:string;published:number}[];
 const mapped=mapProducts(raw.map(p=>({product_id:p.id,title:p.title,description:{preview:p.description},stage:p.stage,status:null,categories:[{title:p.category,value:p.category}]})));
 return {...mapped,products:mapped.products.map(p=>({...p,published:Boolean(raw.find(item=>item.id===p.id)?.published)}))};
}
