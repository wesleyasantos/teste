<template>
    <div class="analysis-list">
      <div class="page-header">
        <h1>Análises de Crédito</h1>
      </div>
      
      <div class="filter-section">
        <div class="filter-row">
          <div class="filter-group">
            <label for="decision">Decisão</label>
            <select id="decision" v-model="filters.decision">
              <option value="">Todas</option>
              <option value="pending">Pendente</option>
              <option value="approved">Aprovado</option>
              <option value="rejected">Reprovado</option>
              <option value="need_info">Necessita Informações</option>
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
      
      <div class="analyses-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Cliente</th>
              <th>Solicitação</th>
              <th>Analista</th>
              <th>Data</th>
              <th>Decisão</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="analysis in analyses" :key="analysis.id">
              <td>#{{ analysis.id }}</td>
              <td>{{ analysis.client_name }}</td>
              <td>#{{ analysis.application_id }}</td>
              <td>{{ analysis.analyst_name }}</td>
              <td>{{ formatDate(analysis.created_at) }}</td>
              <td>
                <span :class="'status-badge ' + analysis.decision">
                  {{ getDecisionLabel(analysis.decision) }}
                </span>
              </td>
              <td class="actions">
                <router-link :to="'/analyses/' + analysis.id" class="btn-view">Ver</router-link>
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
  
  export default {
    name: 'AnalysisList',
    setup() {
      const analyses = ref([]);
      const currentPage = ref(1);
      const totalPages = ref(1);
      
      const filters = reactive({
        decision: '',
        client: ''
      });
      
      // Buscar análises
      const fetchAnalyses = async (page = 1) => {
        try {
          // Em uma aplicação real, você buscaria do backend
          // Dados estáticos para exemplo
          analyses.value = [
            {
              id: 1,
              client_name: 'João Silva',
              application_id: 101,
              analyst_name: 'Ana Ferreira',
              created_at: '2025-02-16T14:20:00',
              decision: 'approved'
            },
            {
              id: 2,
              client_name: 'Maria Souza',
              application_id: 102,
              analyst_name: 'Carlos Gomes',
              created_at: '2025-02-18T10:15:00',
              decision: 'pending'
            },
            {
              id: 3,
              client_name: 'Roberto Almeida',
              application_id: 103,
              analyst_name: 'Ana Ferreira',
              created_at: '2025-02-20T16:30:00',
              decision: 'rejected'
            },
            {
              id: 4,
              client_name: 'Carlos Oliveira',
              application_id: 104,
              analyst_name: 'Pedro Santos',
              created_at: '2025-02-22T09:45:00',
              decision: 'need_info'
            }
          ];
          
          // Simular paginação
          totalPages.value = 2;
          currentPage.value = page;
        } catch (error) {
          console.error('Erro ao buscar análises:', error);
        }
      };
      
      // Aplicar filtros
      const applyFilters = () => {
        fetchAnalyses(1);
      };
      
      // Resetar filtros
      const resetFilters = () => {
        filters.decision = '';
        filters.client = '';
        fetchAnalyses(1);
      };
      
      // Funções de formatação
      const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('pt-BR');
      };
      
      const getDecisionLabel = (decision) => {
        const labels = {
          'pending': 'Pendente',
          'approved': 'Aprovado',
          'rejected': 'Reprovado',
          'need_info': 'Requer Informações'
        };
        return labels[decision] || decision;
      };
      
      // Paginação
      const changePage = (page) => {
        if (page >= 1 && page <= totalPages.value) {
          fetchAnalyses(page);
        }
      };
      
      onMounted(() => {
        fetchAnalyses();
      });
      
      return {
        analyses,
        filters,
        currentPage,
        totalPages,
        applyFilters,
        resetFilters,
        formatDate,
        getDecisionLabel,
        changePage
      };
    }
  }
  </script>
  
  <style scoped>
  .analysis-list {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .page-header {
    margin-bottom: 20px;
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
  
  .analyses-table {
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
  
  .btn-view {
    padding: 6px 12px;
    border-radius: 4px;
    text-decoration: none;
    font-size: 14px;
    background-color: #E3F2FD;
    color: #1976D2;
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
  
  .status-badge.approved {
    background-color: #E8F5E9;
    color: #388E3C;
  }
  
  .status-badge.rejected {
    background-color: #FFEBEE;
    color: #D32F2F;
  }
  
  .status-badge.need_info {
    background-color: #E3F2FD;
    color: #1976D2;
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