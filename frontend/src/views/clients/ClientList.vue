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
                <router-link :to="'/applications/new?client=' + client.id" class="btn-action">Nova Solicitação</router-link>
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
          // Dados estáticos para exemplo
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
            },
            {
              id: 3,
              name: 'Carlos Oliveira',
              cpf: '456.789.123-00',
              phone: '(11) 94567-8912',
              email: 'carlos.oliveira@email.com',
              monthly_income: 8000
            },
            {
              id: 4,
              name: 'Ana Pereira',
              cpf: '789.123.456-00',
              phone: '(11) 97891-2345',
              email: 'ana.pereira@email.com',
              monthly_income: 4500
            }
          ];
          
          // Simular paginação
          totalPages.value = 3;
          currentPage.value = page;
        } catch (error) {
          console.error('Erro ao buscar clientes:', error);
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
    padding: 20px;
  }
  
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .btn-primary {
    background-color: #2196F3;
    color: white;
    padding: 10px 20px;
    border-radius: 4px;
    text-decoration: none;
    font-weight: 500;
  }
  
  .search-box {
    display: flex;
    margin-bottom: 20px;
  }
  
  .search-box input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px 0 0 4px;
  }
  
  .btn-search {
    background-color: #2196F3;
    color: white;
    border: none;
    padding: 0 20px;
    border-radius: 0 4px 4px 0;
    cursor: pointer;
  }
  
  .clients-table {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    margin-bottom: 20px;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th, td {
    padding: 15px;
    text-align: left;
    border-bottom: 1px solid #eee;
  }
  
  th {
    background-color: #f5f5f5;
    font-weight: 500;
  }
  
  .actions {
    display: flex;
    gap: 10px;
  }
  
  .btn-view, .btn-edit, .btn-action {
    padding: 6px 12px;
    border-radius: 4px;
    text-decoration: none;
    font-size: 14px;
  }
  
  .btn-view {
    background-color: #E3F2FD;
    color: #1976D2;
  }
  
  .btn-edit {
    background-color: #FFF8E1;
    color: #FFA000;
  }
  
  .btn-action {
    background-color: #E8F5E9;
    color: #388E3C;
  }
  
  .pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
  }
  
  .btn-page {
    padding: 8px 16px;
    background-color: #f5f5f5;
    border: 1px solid #ddd;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn-page:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .page-info {
    color: #666;
  }
  </style>