// Public portfolio demo: all changes stay on this device; no credentials are collected.
const key = 'portfolio-demo-v1';
const focus = false;
function initial(){return focus ? [
 {id:'task-1',title:'Подготовить презентацию проекта',description:JSON.stringify({description:'Собрать основные результаты и показать команде',project:'Портфолио',type:'Задача',status:'В работе',deadline:new Date(Date.now()+86400000*3).toISOString().slice(0,10),created:new Date().toISOString()}),category:'it',stage:'idea',published:1},
 {id:'task-2',title:'Проверить адаптивную верстку',description:JSON.stringify({description:'Проверить страницы на телефоне и планшете',project:'Сайт',type:'Задача',status:'Новая',deadline:'',created:new Date().toISOString()}),category:'it',stage:'idea',published:1},
 {id:'task-3',title:'Опубликовать демо',description:JSON.stringify({description:'Добавить ссылку в README',project:'Портфолио',type:'Задача',status:'Завершена',deadline:'',created:new Date().toISOString()}),category:'it',stage:'idea',published:1}
 ] : [
 {id:'sigma',title:'Сигма',description:'Планирование задач и командная работа',stage:'implementation',category:'it',published:1},
 {id:'classhub',title:'ClassHub',description:'Образовательная платформа',stage:'mvp_development',category:'education',published:1},
 {id:'maibo',title:'Майбо',description:'Сервис заботы о здоровье',stage:'idea',category:'health',published:1}];}
export async function demoRequest(path,method='GET',body={}){
 let rows; try { rows=JSON.parse(localStorage.getItem(key)||'null')||initial(); } catch {rows=initial();}
 if(path.startsWith('/auth/')) return {token:'demo-browser',email:'demo@example.com',ok:true};
 if(path==='/categories')return {data:[{id:'it',name:'IT'},{id:'education',name:'Образование'},{id:'health',name:'Здоровье'}]};
 if(path==='/products'&&method==='GET')return {data:rows};
 let result={ok:true};
 if(path==='/products'&&method==='POST'){const id=crypto.randomUUID();rows.unshift({id,...body,published:1});result={id};}
 else if(path.startsWith('/products/')){const id=path.split('/').pop();if(!rows.some(r=>r.id===id))throw Error('Запись не найдена');if(method==='DELETE')rows=rows.filter(r=>r.id!==id);else if(method==='PATCH')rows=rows.map(r=>r.id===id?{...r,...body}:r);}
 else throw Error('Неизвестный маршрут демо');
 localStorage.setItem(key,JSON.stringify(rows));return result;
}
