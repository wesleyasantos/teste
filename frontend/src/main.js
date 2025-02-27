import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css'

// Iniciar a aplicação MVP
import dataService from './services/data-service';

// Garantir que os dados do MVP estejam inicializados
dataService.initializeData();

// Se não houver usuário logado, redirecionar para login
const currentRoute = router.currentRoute?.value?.path || '/';
if (!dataService.isAuthenticated() && currentRoute !== '/login') {
  router.push('/login');
}

createApp(App)
  .use(router)
  .mount('#app')