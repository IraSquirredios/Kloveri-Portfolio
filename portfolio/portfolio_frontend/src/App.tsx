import { useEffect, useState } from 'react';
import type { FormEvent } from 'react';
import logo from '../assets/icons/icon-logo.svg';
import eye from '../assets/icons/icon-eye.svg';
import close from '../assets/icons/icon-close.svg';
import closeBlack from '../assets/icons/icon-close-black.svg';
import ProductsPage from './ProductsPage';
import './styles/products.scss';
import { api, hasAccessToken, setAccessToken } from './api/client';
import { signIn, signUp, signInErrorMessage } from './api/auth';
import axios from 'axios';

export default function App() {
  const [page, setPage] = useState(window.location.hash === '#products' && hasAccessToken() ? 'products' : 'login');
  useEffect(() => {
    const update = () => setPage(window.location.hash === '#products' && hasAccessToken() ? 'products' : 'login');
    window.addEventListener('hashchange', update);
    return () => window.removeEventListener('hashchange', update);
  }, []);
  const [register, setRegister] = useState(false);
  const [loading, setLoading] = useState(false);
  const [loginMessage, setLoginMessage] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [visible, setVisible] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [authError, setAuthError] = useState(false);
  const [alertVisible, setAlertVisible] = useState(false);
  const validEmail = Boolean(email.trim());
  const emailError = submitted && !email.trim() ? 'Введите логин или email' : '';
  const passwordError = submitted && !password ? 'Введите пароль' : '';

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (loading) return;
    setSubmitted(true);
    setAuthError(false); setAlertVisible(false);
    if (!validEmail || !password) return;
    setLoading(true);
    try {
      await (register ? signUp : signIn)(email.trim(), password);
      setPassword('');
      window.location.hash = 'products';
      setPage('products');
    } catch (error) {
      const rejected = axios.isAxiosError(error) && [400, 401, 403].includes(error.response?.status || 0);
      setAuthError(rejected);
      setLoginMessage(signInErrorMessage(error));
      setAlertVisible(true);
    } finally {
      setLoading(false);
    }
  }

  if (page === 'products') return <ProductsPage isAdmin={true} email={email.trim().toLowerCase() === 'demo_focus' ? 'pochta@mail.ru' : email || 'pochta@mail.ru'} onLogout={async () => {
    try { await api.post('/auth/logout'); } catch { /* Local logout still clears the session. */ }
    setAccessToken(null);
    window.location.hash = '';
    setPage('login');
    setPassword('');
    setSubmitted(false);
    setAuthError(false);
    setAlertVisible(false);
  }} />;

  return (
    <main className="login-page">
      <section className="login-panel" aria-label="Авторизация" inert={loading}>
        {alertVisible && <div className="auth-alert" id="auth-error" role="alert">
          <p>{loginMessage}</p>
          <button type="button" aria-label="Закрыть сообщение об ошибке" onClick={() => setAlertVisible(false)}><img src={closeBlack} alt="" width="24" height="24" /></button>
        </div>}
        <a className="brand" href="/" aria-label="Портфолио проектов ГК Эйтика">
          <img src={logo} alt="" width="34" height="48" />
          <span>Портфолио проектов<br />ГК Эйтика</span>
        </a>
        <form className="login-form" onSubmit={submit} noValidate>
          {import.meta.env.VITE_DEMO==='true'&&<><p>Демо: изменения сохраняются только в этом браузере.</p><button type="button" className="login-button" onClick={()=>{setAccessToken('demo-browser');setEmail('demo@example.com');window.location.hash='products';setPage('products')}}>Посмотреть демо</button></>}<h1>{register ? 'Создать аккаунт' : 'Введите учётные данные'}</h1>
          <div className={`form-field${emailError ? " form-field--error" : ""}`}>
            <label htmlFor="email">Логин или email</label>
            <div className="email-input">
            <input id="email" name="email" type="text" autoComplete="username" placeholder="demo_focus или email" value={email} onChange={(event) => { setEmail(event.target.value); setAuthError(false); setAlertVisible(false); }} aria-invalid={Boolean(emailError) || authError} aria-describedby={emailError ? 'email-error' : authError && alertVisible ? 'auth-error' : undefined} />
            {email && <button className="visibility-button" type="button" aria-label="Очистить логин" onClick={() => { setEmail(''); setSubmitted(false); setAuthError(false); setAlertVisible(false); document.getElementById('email')?.focus(); }}><img src={close} alt="" width="20" height="20" /></button>}
            </div>
            {emailError && <p id="email-error" className="field-error" aria-live="polite">{emailError}</p>}
          </div>
          <div className="form-field">
            <label htmlFor="password">Пароль</label>
            <div className="password-input">
              <input id="password" name="password" type={visible ? 'text' : 'password'} autoComplete="current-password" placeholder="Введите пароль" value={password} onChange={(event) => { setPassword(event.target.value); setAuthError(false); setAlertVisible(false); }} aria-invalid={Boolean(passwordError) || authError} aria-describedby={passwordError ? 'password-error' : authError && alertVisible ? 'auth-error' : undefined} />
              <button type="button" className="visibility-button" onClick={() => setVisible(!visible)} aria-label={visible ? 'Скрыть пароль' : 'Показать пароль'} aria-pressed={visible}><img src={eye} alt="" width="21" height="21" /></button>
            </div>
            {passwordError && <p id="password-error" className="field-error">{passwordError}</p>}
          </div>
          <button className="login-button" type="submit" disabled={!validEmail || !password || authError || loading}>{register ? 'Зарегистрироваться' : 'Войти'}</button><button type="button" onClick={() => setRegister(!register)}>{register ? 'Уже есть аккаунт' : 'Создать аккаунт'}</button>
        </form>
      </section>
      <div className="login-image" role="img" aria-label="Папки проектов на полках" />
      {loading && <div className="loading-overlay">
        <div className="loading-card" role="status" aria-live="polite" aria-label="Загрузка">
          <span className="loading-spinner" aria-hidden="true" />
          <span>Загрузка</span>
        </div>
      </div>}
    </main>
  );
}
