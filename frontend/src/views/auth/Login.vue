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
      </form>
      
      <div class="version-info">
        <p>W2M Finance v1.0 - Ambiente de Testes</p>
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
        // No ambiente de testes, permitimos o login simulado com credenciais de teste
        if (username.value === 'wesley.sobreira' && password.value === 'admin123') {
          // Tenta autenticar via API primeiro
          try {
            const response = await api.auth.login({
              username: username.value,
              password: password.value
            });
            
            // Armazenar token
            localStorage.setItem('token', response.data.token);
            
            // Obter dados do usuário
            const userData = {
              id: 1,
              username: username.value,
              name: 'Administrador',
              email: 'admin@w2mfinance.com',
              role: 'admin',
              is_analyst: true,
              is_manager: true
            };
            
            localStorage.setItem('user', JSON.stringify(userData));
            
            // Redirecionar para o dashboard
            router.push('/');
          } catch (apiError) {
            console.log('Erro na API, usando login simulado', apiError);
            // Simulação de login para testes
            const userData = {
              id: 1,
              username: 'admin',
              name: 'Administrador',
              email: 'admin@w2mfinance.com',
              role: 'admin',
              is_analyst: true,
              is_manager: true
            };
            
            // Armazenar dados de autenticação localmente
            localStorage.setItem('token', 'token_simulado_123456');
            localStorage.setItem('user', JSON.stringify(userData));
            
            // Redirecionar para o dashboard
            router.push('/');
          }
        } else {
          // Mostrar erro para credenciais incorretas
          throw new Error('Credenciais inválidas');
        }
      } catch (err) {
        error.value = 'Usuário ou senha inválidos. Tente novamente.';
      } finally {
        loading.value = false;
      }
    };
    
    return {
      username,
      password,
      error,
      loading,
      login
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
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ef 100%);
  position: relative;
  overflow: hidden;
}

.login-container::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23000000' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

.login-card {
  width: 450px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 15px 35px rgba(0, 0, 75, 0.1);
  overflow: hidden;
  position: relative;
  z-index: 1;
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.login-header {
  background: linear-gradient(120deg, #00004b, #000075);
  padding: 40px 30px;
  text-align: center;
  color: white;
}

.login-logo {
  height: 120px;
  margin: 0 auto;
  transform: scale(1.6);
  filter: drop-shadow(0 5px 15px rgba(0, 0, 0, 0.2));
  transition: all 0.5s ease;
}

.login-logo:hover {
  transform: scale(1.7);
}

.login-form {
  padding: 40px 30px;
}

.form-group {
  margin-bottom: 25px;
}

label {
  display: block;
  margin-bottom: 10px;
  font-weight: 600;
  color: #00004b;
  font-size: 15px;
}

input {
  width: 100%;
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  font-size: 16px;
  transition: all 0.3s ease;
  background-color: #f9f9fc;
}

input:focus {
  border-color: #4673F5;
  box-shadow: 0 0 0 4px rgba(70, 115, 245, 0.15);
  background-color: #ffffff;
  outline: none;
}

.error-message {
  background-color: #FFEBEE;
  color: #D32F2F;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 25px;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  animation: shake 0.5s ease;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
  20%, 40%, 60%, 80% { transform: translateX(5px); }
}

.error-message::before {
  content: "⚠️";
  font-size: 16px;
}

.form-actions {
  margin-top: 35px;
}

.btn-login {
  width: 100%;
  padding: 16px;
  background: linear-gradient(90deg, #00004b, #000075);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(0, 0, 120, 0.15);
  position: relative;
  overflow: hidden;
}

.btn-login::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transform: translateX(-100%);
}

.btn-login:hover {
  background: linear-gradient(90deg, #000075, #00004b);
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 120, 0.25);
}

.btn-login:hover::before {
  animation: shine 1.5s infinite;
}

@keyframes shine {
  100% { transform: translateX(100%); }
}

.btn-login:active {
  transform: translateY(1px);
  box-shadow: 0 3px 10px rgba(0, 0, 120, 0.15);
}

.btn-login:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}

.version-info {
  text-align: center;
  padding: 15px;
  font-size: 12px;
  color: #999;
  background-color: #f7f7fa;
  border-top: 1px solid #f0f0f0;
}
</style>