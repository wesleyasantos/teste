import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '../views/Dashboard.vue';
import OperationsList from '../views/operations/OperationsList.vue';
import OperationForm from '../views/operations/OperationForm.vue';
import OperationDetail from '../views/operations/OperationDetail.vue';
import ClientList from '../views/clients/ClientList.vue';
import ClientDetail from '../views/clients/ClientDetail.vue';
import ClientForm from '../views/clients/ClientForm.vue';
import ReportGenerator from '../views/reports/ReportGenerator.vue';
import Settings from '../views/settings/Settings.vue';
import Login from '../views/auth/Login.vue';
import api from '../services/api';

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
  // Gestão das Operações
  {
    path: '/operations',
    name: 'OperationsList',
    component: OperationsList,
    meta: { requiresAuth: true }
  },
  // Cadastro de Operações
  {
    path: '/operations/new',
    name: 'OperationCreate',
    component: OperationForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/operations/:id',
    name: 'OperationDetail',
    component: OperationDetail,
    meta: { requiresAuth: true }
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
  // Relatórios
  {
    path: '/reports',
    name: 'Reports',
    component: ReportGenerator,
    meta: { requiresAuth: true }
  },
  // Configurações
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
    meta: { requiresAuth: true }
  },
  // Redirecionamentos de Aplicações para Operações
  {
    path: '/applications',
    redirect: '/operations'
  },
  {
    path: '/applications/new',
    redirect: '/operations/new'
  },
  {
    path: '/applications/:id',
    redirect: to => ({ path: `/operations/${to.params.id}` })
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
    if (!api.auth.isAuthenticated()) {
      // Redirecionar para o login
      next({ name: 'Login' });
    } else {
      // Prosseguir para a rota desejada
      next();
    }
  } else {
    // Para rotas que não precisam de autenticação
    
    // Se estiver na página inicial e já estiver autenticado, vá para o dashboard
    if (to.path === '/' && api.auth.isAuthenticated()) {
      next({ name: 'Dashboard' });
    } else {
      next();
    }
  }
});

export default router;