import json,sqlite3,os,secrets,hashlib,hmac,time
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
DB=os.environ.get('DATABASE_PATH','data/portfolio.sqlite3');os.makedirs(os.path.dirname(os.path.abspath(DB)),exist_ok=True)
def connect():
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row;return c
with connect() as c:
 c.executescript('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,email TEXT UNIQUE,password TEXT,salt TEXT);CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY,user_id INTEGER,expires REAL);CREATE TABLE IF NOT EXISTS products(id TEXT PRIMARY KEY,user_id INTEGER,title TEXT,description TEXT,stage TEXT,category TEXT,published INTEGER);')
def password(p,s):return hashlib.pbkdf2_hmac('sha256',p.encode(),s.encode(),200000).hex()
class Handler(BaseHTTPRequestHandler):
 def reply(self,status,data):
  b=json.dumps(data,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
 def do_GET(self):self.handle_request()
 def do_POST(self):self.handle_request()
 def do_PATCH(self):self.handle_request()
 def do_DELETE(self):self.handle_request()
 def handle_request(self):
  try:self.dispatch()
  except (ValueError,KeyError,json.JSONDecodeError):self.reply(400,{'message':'Проверьте данные запроса'})
  except sqlite3.IntegrityError:self.reply(409,{'message':'Этот email уже зарегистрирован'})
 def dispatch(self):
  path=urlparse(self.path).path;body={};size=int(self.headers.get('Content-Length','0'))
  if size>100000:return self.reply(413,{'message':'Слишком большой запрос'})
  if size:body=json.loads(self.rfile.read(size))
  if path=='/health':return self.reply(200,{'ok':True})
  with connect() as c:
   if path in ['/auth/register','/auth/login'] and self.command=='POST':
    email=str(body.get('email','')).strip().lower();pw=str(body.get('password',''))
    if '@' not in email or len(email)>254 or len(pw)<8 or len(pw)>200:return self.reply(400,{'message':'Введите email и пароль от 8 до 200 символов'})
    if path.endswith('register'):
     salt=secrets.token_hex(16);u=c.execute('INSERT INTO users(email,password,salt) VALUES(?,?,?)',(email,password(pw,salt),salt));uid=u.lastrowid
     for title,desc,cat in [('Сигма','Планирование задач и командная работа','it'),('ClassHub','Образовательная платформа','education'),('Майбо','Сервис заботы о здоровье','health')]:c.execute('INSERT INTO products VALUES(?,?,?,?,?,?,?)',(secrets.token_hex(12),uid,title,desc,'idea',cat,1))
    else:
     u=c.execute('SELECT * FROM users WHERE email=?',(email,)).fetchone()
     if not u or not hmac.compare_digest(u['password'],password(pw,u['salt'])):return self.reply(401,{'message':'Неверный email или пароль'})
     uid=u['id']
    token=secrets.token_urlsafe(32);c.execute('INSERT INTO sessions VALUES(?,?,?)',(hashlib.sha256(token.encode()).hexdigest(),uid,time.time()+86400));return self.reply(200,{'token':token,'email':email})
   raw=self.headers.get('Authorization','').removeprefix('Bearer ');token=hashlib.sha256(raw.encode()).hexdigest();u=c.execute('SELECT user_id FROM sessions WHERE token=? AND expires>?',(token,time.time())).fetchone()
   if not u:return self.reply(401,{'message':'Войдите в аккаунт'})
   uid=u['user_id']
   if path=='/auth/logout':c.execute('DELETE FROM sessions WHERE token=?',(token,));return self.reply(200,{'ok':True})
   if path=='/categories':return self.reply(200,{'data':[{'id':k,'name':v} for k,v in [('it','IT'),('education','Образование'),('health','Здоровье')]]})
   if path=='/products' and self.command=='GET':return self.reply(200,{'data':[dict(r) for r in c.execute('SELECT * FROM products WHERE user_id=? ORDER BY rowid DESC',(uid,))]})
   if path=='/products' and self.command=='POST':
    title=str(body.get('title','')).strip();desc=str(body.get('description',''));cat=body.get('category','it');stage=body.get('stage','idea')
    if not title or len(title)>150 or len(desc)>5000 or cat not in ['it','education','health'] or stage not in ['idea','mvp_development','implementation','implemented','stopped']:return self.reply(400,{'message':'Проверьте название, категорию и стадию'})
    id=secrets.token_hex(12);c.execute('INSERT INTO products VALUES(?,?,?,?,?,?,?)',(id,uid,title,desc,stage,cat,1));return self.reply(201,{'id':id})
   if path.startswith('/products/'):
    id=path.split('/')[-1]
    if not c.execute('SELECT id FROM products WHERE id=? AND user_id=?',(id,uid)).fetchone():return self.reply(404,{'message':'Продукт не найден'})
    if self.command=='DELETE':c.execute('DELETE FROM products WHERE id=? AND user_id=?',(id,uid));return self.reply(200,{'ok':True})
    if self.command=='PATCH':
     for key in ['title','description','stage','category','published']:
      if key not in body:continue
      value=body[key]
      if key=='title' and (not isinstance(value,str) or not value.strip() or len(value)>150):return self.reply(400,{'message':'Неверное название'})
      if key=='description' and (not isinstance(value,str) or len(value)>5000):return self.reply(400,{'message':'Слишком длинное описание'})
      if key=='category' and value not in ['it','education','health']:return self.reply(400,{'message':'Неверная категория'})
      if key=='stage' and value not in ['idea','mvp_development','implementation','implemented','stopped']:return self.reply(400,{'message':'Неверная стадия'})
      if key=='published' and not isinstance(value,bool):return self.reply(400,{'message':'Неверный статус'})
     for key in ['title','description','stage','category','published']:
      if key in body:c.execute(f'UPDATE products SET {key}=? WHERE id=? AND user_id=?',(body[key],id,uid))
     return self.reply(200,{'ok':True})
   return self.reply(404,{'message':'Маршрут не найден'})
if __name__=='__main__':ThreadingHTTPServer(('0.0.0.0',8000),Handler).serve_forever()
