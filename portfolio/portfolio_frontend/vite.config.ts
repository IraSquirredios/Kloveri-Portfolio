import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig(({ mode }) => {
 const env = loadEnv(mode, process.cwd(), '');
 return {
  plugins: [react()],
  server: {
   host: '127.0.0.1', port: 3003,
   proxy: {
    '/auth-api': {
     target: env.AUTH_PROXY_TARGET || 'https://api.users.skroy.ru', changeOrigin: true,
     rewrite: path => path.replace(/^\/auth-api/, ''),
    },
    '/directory-api': {
     target: env.DIRECTORY_PROXY_TARGET || 'https://directory.basis.skroy.ru', changeOrigin: true,
     rewrite: path => path.replace(/^\/directory-api/, ''),
    },
    '/api': {
     target: env.API_PROXY_TARGET || 'https://platform.skroy.ru', changeOrigin: true,
     rewrite: path => path.replace(/^\/api/, ''),
    },
   },
  },
 };
});
