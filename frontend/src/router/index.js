import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '../views/Dashboard.vue';
import ClientList from '../views/clients/ClientList.vue';
import ClientDetail from '../views/clients/ClientDetail.vue';
import ClientForm from '../views/clients/ClientForm.vue';
import AnalysisList from '../views/analyses/AnalysisList.vue';
import AnalysisDetail from '../views/analyses/AnalysisDetail.vue';
import Login from '../views/auth/Login.vue';  // Importar diretamente para melhor desempenho
import dataService from '../services/data-service';

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  // Clientes
  {
    path: '/clients',
    name: 'ClientList',
    component: ClientList,
    meta: { requiresAuth: true }
  },
  {
    path: '/clients/new',
    name: 'ClientCreate',
    component: ClientForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/clients/:id',
    name: 'ClientDetail',
    component: ClientDetail,
    meta: { requiresAuth: true }
  },
  {
    path: '/clients/:id/edit',
    name: 'ClientEdit',
    component: ClientForm,
    meta: { requiresAuth: true }
  },
  // Aplicações
  {
    path: '/applications',
    name: 'ApplicationList',
    component: () => import('../views/applications/ApplicationList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/applications/new',
    name: 'ApplicationCreate',
    component: () => import('../views/applications/ApplicationForm.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/applications/:id',
    name: 'ApplicationDetail',
    component: () => import('../views/applications/ApplicationDetail.vue'),
    meta: { requiresAuth: true }
  },
  // Análises
  {
    path: '/analyses',
    name: 'AnalysisList',
    component: AnalysisList,
    meta: { requiresAuth: true }
  },
  {
    path: '/analyses/:id',
    name: 'AnalysisDetail',
    component: AnalysisDetail,
    meta: { requiresAuth: true }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue')
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Navegação protegida
router.beforeEach((to, from, next) => {
  // Se a rota requer autenticação
  if (to.meta.requiresAuth) {
    // Verificar se o usuário está autenticado
    if (!dataService.isAuthenticated()) {
      // Redirecionar para o login
      next({ name: 'Login' });
    } else {
      // Prosseguir para a rota desejada
      next();
    }
  } else {
    // Para rotas que não precisam de autenticação
    
    // Se estiver na página inicial e já estiver autenticado, vá para o dashboard
    if (to.path === '/' && dataService.isAuthenticated()) {
      next({ name: 'Dashboard' });
    } else {
      next();
    }
  }
});

export default router;