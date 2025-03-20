// frontend/src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css'

// Importar o novo serviço API
import api from './services/api';

// Verificar autenticação
const currentRoute = router.currentRoute?.value?.path || '/';
if (!api.auth.isAuthenticated() && currentRoute !== '/login') {
  router.push('/login');
}

createApp(App)
  .use(router)
  .mount('#app')