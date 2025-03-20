<template>
  <div id="app">
    <header v-if="isAuthenticated && !isLoginPage">
      <nav class="navbar">
        <div class="logo">
          <router-link to="/">
            <img src="./assets/logo.svg" alt="Análise de Crédito" class="logo-image" />
          </router-link>
        </div>
        <ul class="nav-links">
          <li><router-link to="/">Dashboard</router-link></li>
          <li><router-link to="/operations/new">Cadastro de Operação</router-link></li>
          <li><router-link to="/operations">Gestão das Operações</router-link></li>
          <li><router-link to="/clients">Cadastro e Gestão de Clientes</router-link></li>
          <li><router-link to="/reports">Relatórios</router-link></li>
          <li><router-link to="/settings">Configurações</router-link></li>
        </ul>
        <div class="user-menu">
          <span class="user-role">{{ userRole }}</span>
          <span class="username">{{ userName }}</span>
          <button @click="logout" class="logout-btn">Sair</button>
        </div>
      </nav>
    </header>
    
    <main :class="{'auth-page': isLoginPage}">
      <router-view></router-view>
    </main>
    
    <footer v-if="isAuthenticated && !isLoginPage">
      <div class="footer-content">
        <div class="footer-logo">
          <img src="./assets/logo.svg" alt="Análise de Crédito" class="footer-logo-image" />
        </div>
        <div class="footer-info">
          <p>&copy; 2025 W2M Finance - <span class="demo-tag">Versão MVP</span></p>
          <p class="footer-contact">Suporte: suporte@w2msolucoes.com | (45) 0123-0123</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from './services/api';

window.debugApp = {
  checkApiConnection: async () => {
    try {
      const result = await fetch('http://localhost:8000/api/');
      console.log('API Connection Status:', result.status);
      return result.ok;
    } catch (error) {
      console.error('API Connection Error:', error);
      return false;
    }
  },
  
  testCreateOperation: async () => {
    try {
      const testData = {
        client: 1, // Considere o primeiro cliente
        amount: 10000,
        term_months: 12,
        modality: 'Capital de Giro',
        payment_frequency: 'monthly',
        interest_rate: 1.5,
        interest_frequency: 'monthly',
        amortization_system: 'price',
        first_payment_date: new Date().toISOString().split('T')[0],
        purpose: 'Teste',
        status: 'pending'
      };
      
      const result = await apiClient.post('/operations/', testData);
      console.log('Test Create Operation Result:', result.data);
      return result.data;
    } catch (error) {
      console.error('Test Create Operation Error:', error);
      throw error;
    }
  },
  
  getLocalOperations: () => {
    return JSON.parse(localStorage.getItem('operations') || '[]');
  },
  
  clearLocalOperations: () => {
    localStorage.removeItem('operations');
    console.log('Local operations cleared');
  }
};

export default {
  name: 'App',
  setup() {
    const router = useRouter();
    const route = useRoute();
    const currentUser = ref(null);
    
    const isAuthenticated = computed(() => {
      return api.auth.isAuthenticated()
    });
    
    const isLoginPage = computed(() => {
      return route.path === '/login';
    });
    
    const userName = computed(() => {
      return currentUser.value ? currentUser.value.name : 'Usuário';
    });
    
    const userRole = computed(() => {
      if (!currentUser.value) return '';
      
      const roles = {
        'admin': 'Administrador',
        'analyst': 'Analista',
        'manager': 'Gerente'
      };
      
      return roles[currentUser.value.role] || currentUser.value.role;
    });
    
    const logout = async () => {
      try {
        await api.logout();
        router.push('/login');
      } catch (error) {
        console.error('Erro ao fazer logout:', error);
      }
    };
    
    const checkAuth = () => {
      if (api.auth.isAuthenticated()) {
        const currentUser = api.auth.getCurrentUser();
      } else if (!isLoginPage.value) {
        router.push('/login');
      }
    };
    
    // Verificar autenticação quando a rota muda
    watch(() => route.path, () => {
      checkAuth();
    });
    
    onMounted(() => {
      checkAuth();
    });
    
    return {
      isAuthenticated,
      isLoginPage,
      userName,
      userRole,
      logout
    };
  }
}
</script>

<style>
/* Estilos globais */
:root {
  --primary-color: #00004b;
  --secondary-color: #FF9F1C;
  --text-light: #ffffff;
  --text-dark: #333333;
  --background-light: #f5f5f5;
  --border-color: #dddddd;
  --success-color: #388E3C;
  --warning-color: #FFA000;
  --danger-color: #D32F2F;
  --info-color: #1976D2;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: var(--background-light);
  color: var(--text-dark);
  line-height: 1.6;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

header {
  background-color: var(--primary-color);
  color: var(--text-light);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

/* Estilos para o menu de navegação - ajustes */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 85px;
  max-width: 1300px; /* Aumentado para acomodar mais itens */
  margin: 0 auto;
}

.logo {
  flex-shrink: 0; /* Impede que o logo diminua */
  margin-right: 10px;
  height: 50px;
  transform: scale(2.1)
}

.logo-image {
  height: 50px; /* Reduzido para dar mais espaço ao menu */
}

.nav-links {
  display: flex;
  list-style: none;
  flex-wrap: nowrap; /* Evita quebra de linha */
  /* overflow-x: auto; Permite rolagem horizontal em telas menores */
  padding: 0 20px;
  margin: 0;
  flex: 1; /* Toma o espaço disponível */
  justify-content: center; /* Centraliza os itens */
}

.nav-links li {
  margin: 0 10px; /* Reduzido o espaçamento lateral */
  white-space: nowrap; /* Evita quebra de texto */
}

.nav-links a {
  color: var(--text-light);
  text-decoration: none;
  padding: 5px 0;
  font-weight: 500;
  position: relative;
  transition: all 0.3s ease;
  font-size: 14px; /* Tamanho da fonte reduzido */
}

.user-menu {
  display: flex;
  align-items: center;
  flex-shrink: 0; /* Não permite que encolha */
  margin-left: 15px;
}

/* Para telas menores - menu responsivo */
@media (max-width: 992px) {
  .navbar {
    flex-direction: column;
    height: auto;
    padding: 10px 20px;
  }
  
  .logo {
    margin-bottom: 10px;
  }
  
  .nav-links {
    width: 100%;
    justify-content: flex-start;
    padding-bottom: 5px;
  }
  
  .user-menu {
    width: 100%;
    justify-content: flex-end;
    margin-top: 10px;
    margin-left: 0;
  }
}

.user-role {
  background-color: var(--secondary-color);
  color: var(--primary-color);
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
  margin-right: 12px;
}

.username {
  margin-right: 15px;
  color: var(--text-light);
}

.logout-btn {
  background-color: rgba(255, 255, 255, 0.2);
  color: var(--text-light);
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-btn:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

main {
  flex: 1;
  padding: 20px 0;
  background-color: var(--background-light);
}

main.auth-page {
  padding: 0;
}

footer {
  background-color: var(--primary-color);
  color: var(--text-light);
  padding: 30px 0;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-logo-image {
  height: 120px;
  transform: scale(1.3)
}

.footer-info {
  text-align: right;
}

.footer-contact {
  font-size: 14px;
  margin-top: 5px;
  color: rgba(255, 255, 255, 0.7);
}

.demo-tag {
  background-color: var(--secondary-color);
  color: var(--primary-color);
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 12px;
  font-weight: bold;
  margin-left: 5px;
}

/* Utility classes */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

a {
  color: var(--primary-color);
  text-decoration: none;
  transition: all 0.2s ease;
}

a:hover {
  text-decoration: underline;
  color: var(--secondary-color);
}

/* Botões padrão */
.btn-primary {
  background-color: var(--primary-color);
  color: var(--text-light);
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background-color: #000075;
  text-decoration: none;
}

.btn-secondary {
  background-color: var(--text-light);
  color: var(--primary-color);
  padding: 8px 16px;
  border-radius: 4px;
  border: 1px solid var(--primary-color);
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background-color: #f0f0f0;
  text-decoration: none;
}

/* Status badges */
.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.pending {
  background-color: #FFF8E1;
  color: var(--warning-color);
}

.status-badge.in_analysis {
  background-color: #E3F2FD;
  color: var(--info-color);
}

.status-badge.approved {
  background-color: #E8F5E9;
  color: var(--success-color);
}

.status-badge.rejected {
  background-color: #FFEBEE;
  color: var(--danger-color);
}

.status-badge.cancelled {
  background-color: #EEEEEE;
  color: #616161;
}

.status-badge.need_info {
  background-color: #E1F5FE;
  color: #0288D1;
}

/* Form elements */
input, select, textarea {
  font-family: inherit;
  font-size: 14px;
  padding: 10px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  transition: border-color 0.3s ease;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(0, 0, 75, 0.1);
}

button {
  cursor: pointer;
  font-family: inherit;
}

/* Cards padrão */
.card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.card-header {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-color);
}

.card-header h2 {
  margin: 0;
  color: var(--primary-color);
  font-size: 18px;
}
</style>