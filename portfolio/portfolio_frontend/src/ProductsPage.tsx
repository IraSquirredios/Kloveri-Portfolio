import { useEffect, useRef, useState } from 'react';
import logo from '../assets/icons/icon-logo.svg';
import categoryReset from '../assets/icons/icon-category-reset.svg';
import type { Category, Product, IconName } from './productsData';

import {api} from './api/client';
import { loadProducts } from './api/products';
import { loadCategories } from './api/categories';

const paths: Record<IconName, string> = {
 grid: 'M3 3h6v6H3ZM15 3h6v6h-6ZM3 15h6v6H3ZM15 15h6v6h-6Z',
 heart: 'M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z',
 folder: 'M3 7V5a2 2 0 0 1 2-2h5l4 4h5a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z',
 bell: 'M18 8a6 6 0 0 0-12 0c0 8-3 8-3 10h18c0-2-3-2-3-10M9 21h6',
 settings: 'M9 3h6l1 3 3-1 3 5-2 2 2 2-3 5-3-1-1 3H9l-1-3-3 1-3-5 2-2-2-2 3-5 3 1ZM12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8',
 logout: 'M10 3h7a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4h-7M14 12H2m5-5-5 5 5 5',
 sigma: 'M19 3H5l8 9-8 9h14',
 lace: 'M12 2 15 5l4-1 1 4 3 4-3 3-1 5-4-1-3 3-3-3-4 1-1-5-3-3 3-4 1-4 4 1ZM12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10',
 star: 'm12 2 3 7 7 1-5 5 1 7-6-4-6 4 1-7-5-5 7-1Z',
 bolt: 'm13 1-9 13h7l-1 9 10-14h-7Z',
 medical: 'M8 6V3h8v3M3 6h18v16H3ZM12 10v8m-4-4h8',
 school: 'm2 8 10-5 10 5-10 5ZM6 10v8q6 5 12 0v-8m4-2v10',
 food: 'm5 3 16 18M3 5l4 4 3-3-4-4M3 21l12-12m0 0c-4-4 3-9 6-6s-2 10-6 6',
 wallet: 'M3 4h18v16H3ZM21 9h-8v6h8m-5-3h1',
};
function Icon({ name }: { name: IconName }) { return <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d={paths[name]} /></svg>; }
export default function ProductsPage({ email, onLogout, isAdmin = false }: { email: string; onLogout: () => void; isAdmin?: boolean }) {
 const [editor,setEditor]=useState<{id?:string;title:string;description:string}|null>(null);
 const [saveError,setSaveError]=useState('');
 const [loadError, setLoadError] = useState('');
 const [categories, setCategories] = useState<Category[]>([]);
 const [fetchVersion, setFetchVersion] = useState(0);
 const [productsLoading, setProductsLoading] = useState(true);
 const [selected, setSelected] = useState<string[]>([]);
 const [publication] = useState<Record<string, boolean>>({});
 const [deleted] = useState<string[]>([]);
 const published = (p: Product) => publication[p.product_name] ?? p.published !== false;
 async function changePublication(names:string[],value:boolean){try{for(const name of names){const p=products.find(p=>p.product_name===name);if(p?.id)await api.patch('/products/'+p.id,{published:value});}setSelected([]);setFetchVersion(v=>v+1);}catch{window.alert('Не удалось сохранить публикацию');}}
 async function deleteProducts(names:string[]){if(!names.length||!window.confirm('Удалить выбранные продукты?'))return;try{for(const name of names){const p=products.find(p=>p.product_name===name);if(p?.id)await api.delete('/products/'+p.id);}setSelected([]);setFetchVersion(v=>v+1);}catch{window.alert('Не удалось удалить продукт');}}
 const [query, setQuery] = useState('');
 const [category, setCategory] = useState('');
 const [collapsed, setCollapsed] = useState(false);
 const [labelsHidden, setLabelsHidden] = useState(false);
 const [sidebarAnimating, setSidebarAnimating] = useState(false);
 const sidebarTimers = useRef<ReturnType<typeof setTimeout>[]>([]);
 useEffect(() => () => sidebarTimers.current.forEach(clearTimeout), []);

 const [products, setProducts] = useState<Product[]>([]);

 useEffect(() => {
  const controller = new AbortController();
  Promise.all([loadProducts(controller.signal), loadCategories(controller.signal)])
   .then(([result, directory]) => { if (controller.signal.aborted) return; setProducts(result.products.filter(product => !['тест', 'test'].includes(product.product_name.trim().toLowerCase()))); setCategories(directory); setProductsLoading(false); })
   .catch(error => {
    if (controller.signal.aborted) return;
    console.error('Ошибка загрузки продуктов:', error);
    setLoadError(error instanceof Error ? error.message : 'Не удалось загрузить продукты.'); setProductsLoading(false);
   });
  return () => controller.abort();
 }, [fetchVersion, isAdmin]);

 function toggleSidebar() {
  if (sidebarAnimating) return;
  setSidebarAnimating(true);
  if (collapsed) {
   setCollapsed(false);
   sidebarTimers.current = [setTimeout(() => setLabelsHidden(false), 500), setTimeout(() => setSidebarAnimating(false), 1000)];
  } else {
   setLabelsHidden(true);
   sidebarTimers.current = [setTimeout(() => setCollapsed(true), 500), setTimeout(() => setSidebarAnimating(false), 1000)];
  }
 }
 const [section, setSection] = useState('Продукты');
 const filtered = products.filter(p => !deleted.includes(p.product_name) && `${p.product_name} ${p.description}`.toLocaleLowerCase('ru').includes(query.trim().toLocaleLowerCase('ru')) && (!category || p.categoryIds.includes(category)));
 function renderCard(p: Product) {
  const checked = selected.includes(p.product_name);
  return <article className={`product-card${isAdmin && !published(p) ? ' product-card--draft' : ''}${checked ? ' product-card--selected' : ''}`} key={p.id || p.product_name}>
   <div className="product-card-top">
    {isAdmin && <button className="product-select" type="button" aria-label={`Выбрать ${p.product_name}`} aria-pressed={checked} onClick={() => setSelected(previous => previous.includes(p.product_name) ? previous.filter(name => name !== p.product_name) : [...previous, p.product_name])} />}
    <Icon name={p.icon} /><h2 title={p.product_name}>{p.product_name}</h2>
    <span className={`product-status ${isAdmin && !published(p) ? 'draft' : ['Реализован', 'Разработка MVP'].includes(p.status) ? 'done' : p.status === 'Остановлен' ? 'stopped' : ''}`}>{isAdmin && !published(p) ? 'Черновик' : p.status}</span>
    {isAdmin && <details className="product-menu" onKeyDown={e => { if (e.key === 'Escape') e.currentTarget.open = false; }} onBlur={e => { if (!e.currentTarget.contains(e.relatedTarget)) e.currentTarget.open = false; }}>
     <summary aria-label={`Действия: ${p.product_name}`}>⋮</summary>
     <div><button type="button" onClick={()=>{setSaveError('');setEditor({id:p.id,title:p.product_name,description:p.description});}}>Редактировать</button><button type="button" onClick={e => { changePublication([p.product_name], !published(p)); e.currentTarget.closest('details')?.removeAttribute('open'); }}>{published(p) ? 'Снять с публикации' : 'Опубликовать'}</button><button type="button" onClick={() => deleteProducts([p.product_name])}>Удалить</button></div>
    </details>}
   </div><p>{p.description}</p>
  </article>;
 }
 const draftSelection = selected.filter(name => products.some(p => p.product_name === name && !published(p)));
 return <div className={`products-page${isAdmin ? ' products-page--admin' : ''}${collapsed ? ' products-page--collapsed' : ''}${labelsHidden ? ' products-page--labels-hidden' : ''}`}>
  {editor && <div className="loading-overlay"><form className="loading-card" style={{display:'block',width:'min(500px,94vw)',padding:24}} onSubmit={async e=>{e.preventDefault();try{const body={title:editor.title.trim(),description:editor.description};if(!body.title)return;if(editor.id)await api.patch('/products/'+editor.id,body);else await api.post('/products',{...body,category:'it',stage:'idea'});setEditor(null);setFetchVersion(v=>v+1);}catch{setSaveError('Не удалось сохранить продукт');}}}><h2>{editor.id?'Редактировать продукт':'Добавить продукт'}</h2><label>Название<input required maxLength={150} value={editor.title} onChange={e=>setEditor({...editor,title:e.target.value})}/></label><label>Описание<textarea maxLength={5000} value={editor.description} onChange={e=>setEditor({...editor,description:e.target.value})}/></label><p role="alert">{saveError}</p><button type="submit">Сохранить</button><button type="button" onClick={()=>setEditor(null)}>Отмена</button></form></div>}
  <aside id="products-sidebar" className="products-sidebar">
   <div className="products-brand"><img src={logo} alt="" /><span>Портфолио проектов<br />ГК Эйтика</span></div>
   <p className="account-email" title={email}>{email}</p>
   <nav aria-label="Главное меню"><button className={section === 'Продукты' ? 'sidebar-link active' : 'sidebar-link'} onClick={() => setSection('Продукты')} title="Продукты" aria-label="Продукты"><Icon name="folder" /><span>Продукты</span></button>{isAdmin && <>{([{ name: 'Другой раздел', icon: 'grid' }, { name: 'Ещё один раздел', icon: 'heart' }] as const).map(item => <button key={item.name} className={section === item.name ? 'sidebar-link active' : 'sidebar-link'} onClick={() => setSection(item.name)} title={item.name} aria-label={item.name}><Icon name={item.icon} /><span>{item.name}</span></button>)}</>}</nav>
   <div className="sidebar-bottom">
    <button className="sidebar-link" onClick={() => setSection('Уведомления')} title="Уведомления" aria-label="Уведомления"><Icon name="bell" /><span>Уведомления</span></button>
    <button className="sidebar-link" onClick={() => setSection('Настройки')} title="Настройки" aria-label="Настройки"><Icon name="settings" /><span>Настройки</span></button>
    <button className="sidebar-link" onClick={onLogout} title="Выйти" aria-label="Выйти"><Icon name="logout" /><span>Выйти</span></button>
   </div>
   <button className="sidebar-collapse" onClick={toggleSidebar} disabled={sidebarAnimating} aria-expanded={!collapsed} aria-controls="products-sidebar" aria-label={collapsed ? 'Развернуть меню' : 'Свернуть меню'}><svg className={collapsed ? 'collapse-arrow is-collapsed' : 'collapse-arrow'} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M21 12H3m8-8-8 8 8 8" /></svg></button>
  </aside>
  <main className="products-main">
   <button className="products-back" onClick={() => section === 'Продукты' ? onLogout() : setSection('Продукты')}>‹ Назад</button>
   <div className="products-toolbar"><h1>{section}</h1>{section === 'Продукты' && (isAdmin ? <div className="admin-actions">
    <button type="button" aria-pressed={selected.length > 0} onClick={() => setSelected(previous => previous.length ? [] : filtered.map(product => product.product_name))}>Выбрать</button>
    <button type="button" className="admin-add" onClick={() => {setSaveError('');setEditor({title:'',description:''});}}><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true"><path d="M12 5v14M5 12h14" /></svg>Добавить</button>
   </div> : <div className="products-filters">
    <input type="search" aria-label="Поиск продуктов" placeholder="Поиск" value={query} onChange={e => setQuery(e.target.value)} />
    <div className={`category-filter${category ? ' category-filter--selected' : ''}`}><details className="category-dropdown" onKeyDown={e => { if (e.key === 'Escape') { e.currentTarget.open = false; e.currentTarget.querySelector('summary')?.focus(); } }} onBlur={e => { if (!e.currentTarget.contains(e.relatedTarget)) e.currentTarget.open = false; }}>
     <summary aria-label="Категория">{category ? (categories.find(item => item.id === category)?.name || category) : 'Категория'}{!category && <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true"><path d="m2 7 10 10L22 7" /></svg>}</summary>
     <div className="category-options">{categories.map(item => <button key={item.id} type="button" aria-pressed={category === item.id} onClick={e => { setCategory(category === item.id ? '' : item.id); const dropdown = e.currentTarget.closest('details'); if (dropdown) { dropdown.open = false; dropdown.querySelector('summary')?.focus(); } }}>{item.name}</button>)}</div>
    </details>
    {category && <button type="button" className="category-reset" aria-label="Сбросить категорию" onClick={e => {
     setCategory('');
     const details = e.currentTarget.parentElement?.querySelector('details');
     if (details) { details.open = false; details.querySelector('summary')?.focus(); }
    }}><img src={categoryReset} alt="" width="20" height="20" /></button>}
    </div>
   </div>)}</div>
   {section === 'Продукты' ? <>
    {productsLoading && <p role="status">Загрузка продуктов…</p>}
    {loadError && <div role="alert"><p>Не удалось загрузить продукты. {loadError}</p><button onClick={() => { setProductsLoading(true); setLoadError(''); setFetchVersion(value => value + 1); }}>Повторить</button></div>}
    <div className="products-grid">{filtered.filter(p => !isAdmin || published(p)).map(renderCard)}
    {!filtered.length && !loadError && !productsLoading && <div className="products-search-empty"><p role="status">По вашему запросу ничего не найдено</p><button type="button" onClick={() => { setQuery(''); setCategory(''); }}>Сбросить поиск</button></div>}
    </div>
    {isAdmin && <section className="admin-drafts" aria-labelledby="drafts-title"><div className="admin-drafts-heading"><h2 id="drafts-title">Не опубликованы</h2><button disabled={!draftSelection.length} onClick={() => changePublication(draftSelection, true)}>Опубликовать</button></div><div className="products-grid">{filtered.filter(p => !published(p)).map(renderCard)}</div></section>}
   </> : <p className="products-empty">{section === 'Уведомления' ? 'Новых уведомлений нет' : section === 'Настройки' ? 'Настройки пока не подключены' : 'Раздел пока не подключён'}</p>}
  </main>
 </div>;
}
