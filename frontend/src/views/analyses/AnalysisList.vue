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
  padding: 30px 20px;
}

.page-header {
  margin-bottom: 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header h1 {
  color: #00004b;
  font-size: 28px;
  font-weight: 700;
  margin: 0;
}

.filter-section {
  background: white;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  padding: 20px 25px;
  margin-bottom: 25px;
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
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
  margin-bottom: 8px;
  font-weight: 500;
  color: #444;
  font-size: 14px;
}

.filter-group input,
.filter-group select {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;
  background-color: #f9f9fc;
}

.filter-group input:focus,
.filter-group select:focus {
  outline: none;
  border-color: #4673F5;
  box-shadow: 0 0 0 3px rgba(70, 115, 245, 0.15);
  background-color: #ffffff;
}

.btn-filter, .btn-reset {
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  border: none;
  font-weight: 600;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-filter {
  background: linear-gradient(90deg, #2196F3, #1976D2);
  color: white;
  box-shadow: 0 4px 10px rgba(33, 150, 243, 0.2);
}

.btn-filter:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(33, 150, 243, 0.3);
}

.btn-reset {
  background-color: #f5f5f7;
  color: #444;
}

.btn-reset:hover {
  background-color: #e5e5e7;
}

.analyses-table {
  background: white;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
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
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #eef0f5;
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

.btn-view {
  padding: 8px 14px;
  border-radius: 6px;
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  background-color: #E3F2FD;
  color: #1976D2;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-view:hover {
  background-color: #BBDEFB;
  color: #0D47A1;
  text-decoration: none;
  transform: translateY(-2px);
}

.status-badge {
  display: inline-flex;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  align-items: center;
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
}

.btn-page:hover:not(:disabled) {
  background-color: #f5f7fa;
  border-color: #4673F5;
  color: #4673F5;
}

.btn-page:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #666;
  font-weight: 500;
}

.empty-state {
  text-align: center;
  padding: 60px 30px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  color: #666;
}

.empty-state p {
  margin-bottom: 20px;
  font-size: 16px;
}

.btn-primary {
  background: linear-gradient(90deg, #2196F3, #1976D2);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 10px rgba(33, 150, 243, 0.2);
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(33, 150, 243, 0.3);
  text-decoration: none;
}
</style>