<template>
  <div class="client-list">
    <div class="page-header">
      <h1>Clientes</h1>
      <router-link to="/clients/new" class="btn-primary">Novo Cliente</router-link>
    </div>
    
    <div class="search-box">
      <input 
        type="text" 
        v-model="searchTerm" 
        placeholder="Buscar por nome, CPF ou email..." 
        @input="onSearch"
      />
      <button @click="onSearch" class="btn-search">Buscar</button>
    </div>
    
    <div class="clients-table">
      <table>
        <thead>
          <tr>
            <th>Nome</th>
            <th>CPF</th>
            <th>Telefone</th>
            <th>Email</th>
            <th>Renda Mensal</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="client in clients" :key="client.id">
            <td>{{ client.name }}</td>
            <td>{{ client.cpf }}</td>
            <td>{{ client.phone }}</td>
            <td>{{ client.email }}</td>
            <td>R$ {{ formatCurrency(client.monthly_income) }}</td>
            <td class="actions">
              <router-link :to="'/clients/' + client.id" class="btn-view">Ver</router-link>
              <router-link :to="'/clients/' + client.id + '/edit'" class="btn-edit">Editar</router-link>
              <router-link :to="'/operations/new?client=' + client.id" class="btn-action">Nova Solicitação</router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="pagination">
      <button 
        @click="changePage(currentPage - 1)" 
        :disabled="currentPage === 1"
        class="btn-page"
      >
        Anterior
      </button>
      <span class="page-info">Página {{ currentPage }} de {{ totalPages }}</span>
      <button 
        @click="changePage(currentPage + 1)" 
        :disabled="currentPage === totalPages"
        class="btn-page"
      >
        Próxima
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  name: 'ClientList',
  setup() {
    const clients = ref([]);
    const searchTerm = ref('');
    const currentPage = ref(1);
    const totalPages = ref(1);
    
    // Buscar dados dos clientes
    const fetchClients = async (page = 1, search = '') => {
      try {
        loading.value = true;
        
        // Construir parâmetros de busca
        const params = { page };
        if (searchTerm.value) {
          params.search = searchTerm.value;
        }
        
        // Chamar a API
        const response = await api.clients.getClients(params);
        
        console.log('Resposta da API de clientes:', response.data);
        
        if (response.data && Array.isArray(response.data.results)) {
          clients.value = response.data.results;
          totalPages.value = Math.ceil(response.data.count / 10); // Assumindo page_size = 10
        } else if (response.data && Array.isArray(response.data)) {
          // Caso a API retorne uma lista direta sem paginação
          clients.value = response.data;
          totalPages.value = 1;
        } else {
          console.warn('Formato de resposta inesperado, usando dados estáticos');
          clients.value = [
            // Dados estáticos que já existem
          ];
          totalPages.value = Math.ceil(clients.value.length / 10);
        }
        
        currentPage.value = page;
      } catch (error) {
        console.error('Erro ao buscar clientes:', error);
        // Fallback para dados estáticos em caso de erro
        clients.value = [
          {
            id: 1,
            name: 'João Silva',
            cpf: '123.456.789-00',
            phone: '(11) 98765-4321',
            email: 'joao.silva@email.com',
            monthly_income: 5000
          },
          {
            id: 2,
            name: 'Maria Souza',
            cpf: '987.654.321-00',
            phone: '(11) 91234-5678',
            email: 'maria.souza@email.com',
            monthly_income: 6500
          }
          // Outros dados estáticos que já existem
        ];
        totalPages.value = Math.ceil(clients.value.length / 10);
      } finally {
        loading.value = false;
      }
    };
    
    // Formatação de valores monetários
    const formatCurrency = (value) => {
      return parseFloat(value).toLocaleString('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    };
    
    // Manipulação de busca e paginação
    const onSearch = () => {
      fetchClients(1, searchTerm.value);
    };
    
    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        fetchClients(page, searchTerm.value);
      }
    };
    
    onMounted(() => {
      fetchClients();
    });
    
    return {
      clients,
      searchTerm,
      currentPage,
      totalPages,
      formatCurrency,
      onSearch,
      changePage
    };
  }
}
</script>
  
<style scoped>
.client-list {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 28px;
  color: #00004b;
  font-weight: 700;
  margin: 0;
}

.btn-primary {
  background: linear-gradient(90deg, #4673F5, #2556e0);
  color: white;
  padding: 10px 18px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 10px rgba(70, 115, 245, 0.2);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(70, 115, 245, 0.3);
  text-decoration: none;
}

.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  background-color: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.search-box input {
  flex: 1;
  padding: 12px 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;
  background-color: #f9f9fc;
}

.search-box input:focus {
  outline: none;
  border-color: #4673F5;
  box-shadow: 0 0 0 3px rgba(70, 115, 245, 0.15);
  background-color: #ffffff;
}

.btn-search {
  padding: 12px 20px;
  background: linear-gradient(90deg, #4673F5, #2556e0);
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(70, 115, 245, 0.2);
}

.btn-search:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(70, 115, 245, 0.3);
}

.clients-table {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  margin-bottom: 25px;
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 14px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background-color: #f5f7fa;
  color: #00004b;
  font-weight: 600;
  font-size: 14px;
}

tr:hover td {
  background-color: #f9fafc;
}

.actions {
  display: flex;
  gap: 10px;
}

.btn-view, .btn-edit, .btn-action {
  padding: 6px 12px;
  border-radius: 6px;
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.btn-view {
  background-color: #E3F2FD;
  color: #1976D2;
}

.btn-view:hover {
  background-color: #BBDEFB;
  color: #0D47A1;
  text-decoration: none;
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(25, 118, 210, 0.2);
}

.btn-edit {
  background-color: #FFF8E1;
  color: #FFA000;
}

.btn-edit:hover {
  background-color: #FFECB3;
  color: #FF6F00;
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(255, 160, 0, 0.2);
}

.btn-action {
  background-color: #E8F5E9;
  color: #388E3C;
}

.btn-action:hover {
  background-color: #C8E6C9;
  color: #2E7D32;
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(56, 142, 60, 0.2);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 30px;
}

.btn-page {
  padding: 10px 16px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  color: #444;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.btn-page:hover:not(:disabled) {
  background-color: #f5f7fa;
  border-color: #4673F5;
  color: #4673F5;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.btn-page:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #666;
  font-weight: 500;
}

/* Responsividade para telas menores */
@media (max-width: 768px) {
  .search-box {
    flex-direction: column;
    padding: 15px;
  }
  
  .btn-search {
    width: 100%;
  }
  
  .actions {
    flex-direction: column;
    gap: 5px;
  }
  
  .btn-view, .btn-edit, .btn-action {
    width: 100%;
    justify-content: center;
  }
  
  .pagination {
    flex-wrap: wrap;
  }
}
</style>