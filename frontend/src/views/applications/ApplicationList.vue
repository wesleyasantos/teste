<template>
    <div class="application-list">
      <div class="page-header">
        <h1>Solicitações de Crédito</h1>
        <router-link to="/applications/new" class="btn-primary">Nova Solicitação</router-link>
      </div>
      
      <div class="filter-section">
        <div class="filter-row">
          <div class="filter-group">
            <label for="status">Status</label>
            <select id="status" v-model="filters.status">
              <option value="">Todos</option>
              <option value="pending">Pendente</option>
              <option value="in_analysis">Em Análise</option>
              <option value="approved">Aprovado</option>
              <option value="rejected">Reprovado</option>
              <option value="cancelled">Cancelado</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label for="client">Cliente</label>
            <input type="text" id="client" v-model="filters.client" placeholder="Nome ou CPF" />
          </div>
          
          <button @click="applyFilters" class="btn-filter">Filtrar</button>
          <button @click="resetFilters" class="btn-reset">Limpar</button>
        </div>
      </div>
      
      <div class="applications-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Cliente</th>
              <th>Data</th>
              <th>Valor</th>
              <th>Prazo</th>
              <th>Finalidade</th>
              <th>Status</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="app in applications" :key="app.id">
              <td>#{{ app.id }}</td>
              <td>{{ app.client_name }}</td>
              <td>{{ formatDate(app.created_at) }}</td>
              <td>R$ {{ formatCurrency(app.amount_requested) }}</td>
              <td>{{ app.term_months }} meses</td>
              <td>{{ app.purpose }}</td>
              <td>
                <span :class="'status-badge ' + app.status">
                  {{ getStatusLabel(app.status) }}
                </span>
              </td>
              <td class="actions">
                <router-link :to="'/applications/' + app.id" class="btn-view">Ver</router-link>
                <button v-if="app.status === 'pending'" @click="startAnalysis(app.id)" class="btn-analyze">
                  Analisar
                </button>
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
  import { ref, reactive, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  
  export default {
    name: 'ApplicationList',
    setup() {
      const router = useRouter();
      
      const applications = ref([]);
      const currentPage = ref(1);
      const totalPages = ref(1);
      
      const filters = reactive({
        status: '',
        client: ''
      });
      
      // Buscar solicitações
      const fetchApplications = async (page = 1) => {
        try {
          // Em uma aplicação real, você buscaria do backend
          // Dados estáticos para exemplo
          applications.value = [
            {
              id: 101,
              client_name: 'João Silva',
              created_at: '2025-02-15T10:30:00',
              amount_requested: 5000,
              term_months: 12,
              purpose: 'Compra de automóvel',
              status: 'approved'
            },
            {
              id: 102,
              client_name: 'Maria Souza',
              created_at: '2025-02-18T14:45:00',
              amount_requested: 3000,
              term_months: 6,
              purpose: 'Reforma residencial',
              status: 'pending'
            },
            {
              id: 103,
              client_name: 'Carlos Oliveira',
              created_at: '2025-02-20T09:15:00',
              amount_requested: 12000,
              term_months: 24,
              purpose: 'Investimento em negócio',
              status: 'in_analysis'
            },
            {
              id: 104,
              client_name: 'Ana Pereira',
              created_at: '2025-02-22T16:30:00',
              amount_requested: 2500,
              term_months: 6,
              purpose: 'Educação',
              status: 'rejected'
            }
          ];
          
          // Simular paginação
          totalPages.value = 2;
          currentPage.value = page;
        } catch (error) {
          console.error('Erro ao buscar solicitações:', error);
        }
      };
      
      // Aplicar filtros
      const applyFilters = () => {
        fetchApplications(1);
      };
      
      // Resetar filtros
      const resetFilters = () => {
        filters.status = '';
        filters.client = '';
        fetchApplications(1);
      };
      
      // Iniciar análise
      const startAnalysis = (id) => {
        router.push(`/analyses/${id}`);
      };
      
      // Funções de formatação
      const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('pt-BR');
      };
      
      const formatCurrency = (value) => {
        return parseFloat(value).toLocaleString('pt-BR', {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2
        });
      };
      
      const getStatusLabel = (status) => {
        const labels = {
          'pending': 'Pendente',
          'in_analysis': 'Em Análise',
          'approved': 'Aprovado',
          'rejected': 'Reprovado',
          'cancelled': 'Cancelado'
        };
        return labels[status] || status;
      };
      
      // Paginação
      const changePage = (page) => {
        if (page >= 1 && page <= totalPages.value) {
          fetchApplications(page);
        }
      };
      
      onMounted(() => {
        fetchApplications();
      });
      
      return {
        applications,
        filters,
        currentPage,
        totalPages,
        applyFilters,
        resetFilters,
        startAnalysis,
        formatDate,
        formatCurrency,
        getStatusLabel,
        changePage
      };
    }
  }
  </script>
  
  <style scoped>
  .application-list {
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
  
  .filter-section {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-bottom: 20px;
  }
  
  .filter-row {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    align-items: flex-end;
  }
  
  .filter-group {
    flex: 1;
    min-width: 200px;
  }
  
  .filter-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
    color: #555;
  }
  
  .filter-group input,
  .filter-group select {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  .btn-filter, .btn-reset {
    padding: 8px 15px;
    border-radius: 4px;
    cursor: pointer;
    border: none;
    font-weight: 500;
  }
  
  .btn-filter {
    background-color: #2196F3;
    color: white;
  }
  
  .btn-reset {
    background-color: #f5f5f5;
    color: #333;
  }
  
  .applications-table {
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
    padding: 12px 15px;
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
  
  .btn-view, .btn-analyze {
    padding: 6px 12px;
    border-radius: 4px;
    text-decoration: none;
    font-size: 14px;
    border: none;
    cursor: pointer;
  }
  
  .btn-view {
    background-color: #E3F2FD;
    color: #1976D2;
  }
  
  .btn-analyze {
    background-color: #E8F5E9;
    color: #388E3C;
  }
  
  .status-badge {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
  }
  
  .status-badge.pending {
    background-color: #FFF8E1;
    color: #FFA000;
  }
  
  .status-badge.in_analysis {
    background-color: #E3F2FD;
    color: #1976D2;
  }
  
  .status-badge.approved {
    background-color: #E8F5E9;
    color: #388E3C;
  }
  
  .status-badge.rejected {
    background-color: #FFEBEE;
    color: #D32F2F;
  }
  
  .status-badge.cancelled {
    background-color: #EEEEEE;
    color: #616161;
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