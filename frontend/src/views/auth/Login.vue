<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <img src="../../assets/logo.svg" alt="Análise de Crédito" class="login-logo" />
      </div>
      
      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label for="username">Usuário</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            required 
            autofocus
          />
        </div>
        
        <div class="form-group">
          <label for="password">Senha</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            required
          />
        </div>
        
        <div v-if="error" class="error-message">
          {{ error }}
        </div>
        
        <div class="form-actions">
          <button type="submit" class="btn-login" :disabled="loading">
            {{ loading ? 'Entrando...' : 'Entrar' }}
          </button>
        </div>
        
        <div class="demo-accounts">
          <h3>Contas para demonstração</h3>
          <div class="account" @click="fillCredentials('admin', 'admin123')">
            <div class="account-icon admin">A</div>
            <div class="account-info">
              <div class="account-role">Administrador</div>
              <div class="account-creds">admin / admin123</div>
            </div>
          </div>
          <div class="account" @click="fillCredentials('analista', 'analista123')">
            <div class="account-icon analyst">A</div>
            <div class="account-info">
              <div class="account-role">Analista</div>
              <div class="account-creds">analista / analista123</div>
            </div>
          </div>
          <div class="account" @click="fillCredentials('gerente', 'gerente123')">
            <div class="account-icon manager">G</div>
            <div class="account-info">
              <div class="account-role">Gerente</div>
              <div class="account-creds">gerente / gerente123</div>
            </div>
          </div>
        </div>
      </form>
      
      <div class="demo-actions">
        <button @click="resetMVP" class="btn-reset-demo">
          Reiniciar Dados de Demonstração
        </button>
      </div>
      
      <div class="version-info">
        <p>MVP v1.0 - Demonstração</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '../../services/api';

export default {
  name: 'Login',
  setup() {
    const router = useRouter();
    
    const username = ref('');
    const password = ref('');
    const error = ref('');
    const loading = ref(false);
    
    const login = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        const response = await api.login({
          username: username.value,
          password: password.value
        });
        
        // Armazenar o token
        localStorage.setItem('token', response.data.token);
        
        // Redirecionar para o dashboard
        router.push('/');
      } catch (err) {
        error.value = 'Usuário ou senha inválidos. Tente novamente.';
      } finally {
        loading.value = false;
      }
    };
    
    const fillCredentials = (user, pass) => {
      username.value = user;
      password.value = pass;
    };
    
    const resetMVP = async () => {
      try {
        await api.resetMVPData();
        alert('Dados de demonstração reiniciados com sucesso!');
        window.location.reload();
      } catch (err) {
        alert('Erro ao reiniciar dados. Tente novamente.');
      }
    };
    
    return {
      username,
      password,
      error,
      loading,
      login,
      fillCredentials,
      resetMVP
    };
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  background-image: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
}

.login-card {
  width: 450px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 8px 30px rgba(0, 0, 75, 0.1);
  overflow: hidden;
}

.login-header {
  background-color: #00004b;
  padding: 30px;
  text-align: center;
}

.login-logo {
  height: 120px;
  margin: 0 auto;
}

.login-form {
  padding: 30px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  transition: all 0.3s ease;
}

input:focus {
  border-color: #00004b;
  box-shadow: 0 0 0 3px rgba(0, 0, 75, 0.1);
  outline: none;
}

.error-message {
  background-color: #FFEBEE;
  color: #D32F2F;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 20px;
  font-size: 14px;
}

.form-actions {
  margin-top: 30px;
}

.btn-login {
  width: 100%;
  padding: 14px;
  background-color: #00004b;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-login:hover {
  background-color: #000075;
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.demo-accounts {
  margin-top: 40px;
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.demo-accounts h3 {
  font-size: 16px;
  margin-top: 0;
  margin-bottom: 15px;
  color: #666;
  text-align: center;
}

.account {
  display: flex;
  align-items: center;
  padding: 12px;
  background-color: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.account:hover {
  background-color: #f0f0f0;
  transform: translateY(-2px);
}

.account-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: white;
  margin-right: 15px;
}

.account-icon.admin {
  background-color: #FF9F1C;
}

.account-icon.analyst {
  background-color: #2196F3;
}

.account-icon.manager {
  background-color: #4CAF50;
}

.account-info {
  flex: 1;
}

.account-role {
  font-weight: 600;
  color: #333;
  margin-bottom: 2px;
}

.account-creds {
  font-size: 14px;
  color: #666;
}

.demo-actions {
  padding: 0 30px 20px;
  text-align: center;
}

.btn-reset-demo {
  background-color: #f5f5f5;
  color: #666;
  border: 1px solid #ddd;
  padding: 10px 20px;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-reset-demo:hover {
  background-color: #eee;
  border-color: #ccc;
}

.version-info {
  text-align: center;
  padding: 12px;
  font-size: 12px;
  color: #999;
  background-color: #f5f5f5;
  border-top: 1px solid #eee;
}
</style>