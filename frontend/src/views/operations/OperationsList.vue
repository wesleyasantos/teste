<template>
  <div class="operations-list">
    <div class="page-header">
      <h1>Gestão das Operações</h1>
      <router-link to="/operations/new" class="btn-primary">Nova Operação</router-link>
    </div>
    
    <div class="filter-section">
      <div class="filter-row">
        <div class="filter-group">
          <label for="status">Status da Operação</label>
          <select id="status" v-model="filters.status">
            <option value="">Todos</option>
            <option value="pending">Cadastro Pendente</option>
            <option value="verification">Em Conferência</option>
            <option value="analysis">Em Análise</option>
            <option value="committee">Em Comitê</option>
            <option value="formalization">Em Formalização</option>
            <option value="monitoring">Em Acompanhamento</option>
            <option value="approved">Aprovado</option>
            <option value="rejected">Reprovado</option>
            <option value="cancelled">Cancelado</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label for="client">Cliente</label>
          <input type="text" id="client" v-model="filters.client" placeholder="Nome ou CPF/CNPJ" />
        </div>
        
        <div class="filter-group">
          <label for="date_range">Período</label>
          <select id="date_range" v-model="filters.date_range">
            <option value="7d">Últimos 7 dias</option>
            <option value="30d">Últimos 30 dias</option>
            <option value="90d">Últimos 90 dias</option>
            <option value="all">Todos</option>
          </select>
        </div>
        
        <button @click="applyFilters" class="btn-filter">Filtrar</button>
        <button @click="resetFilters" class="btn-reset">Limpar</button>
      </div>
    </div>
    
    <div class="operations-tabs">
      <button 
        v-for="(tab, index) in tabs" 
        :key="index"
        @click="currentTab = tab.value"
        :class="{ active: currentTab === tab.value }"
        class="tab-button"
      >
        {{ tab.label }}
        <span v-if="getOperationsByStatus(tab.value).length > 0" class="count-badge">
          {{ getOperationsByStatus(tab.value).length }}
        </span>
      </button>
    </div>
    
    <div class="operations-table">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Cliente</th>
            <th>CPF/CNPJ</th>
            <th>Valor</th>
            <th>Modalidade</th>
            <th>Prazo</th>
            <th>Data</th>
            <th>Status</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="operation in filteredOperations" :key="operation.id">
            <td>#{{ operation.id }}</td>
            <td>{{ operation.client_name }}</td>
            <td>{{ operation.client_document }}</td>
            <td>R$ {{ formatCurrency(operation.amount) }}</td>
            <td>{{ operation.modality }}</td>
            <td>{{ operation.term }} meses</td>
            <td>{{ formatDate(operation.created_at) }}</td>
            <td>
              <span :class="'status-badge ' + operation.status">
                {{ getStatusLabel(operation.status) }}
              </span>
            </td>
            <td class="actions">
              <router-link :to="`/operations/${operation.id}`" class="btn-view">
                <i class="fas fa-eye"></i> Ver
              </router-link>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div v-if="filteredOperations.length === 0" class="empty-state">
      <p>Nenhuma operação encontrada com os filtros selecionados.</p>
      <router-link to="/operations/new" class="btn-primary">Criar Nova Operação</router-link>
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
import { ref, reactive, computed, onMounted } from 'vue';

export default {
  name: 'OperationsList',
  setup() {
    const operations = ref([]);
    const currentPage = ref(1);
    const totalPages = ref(1);
    const itemsPerPage = 10;
    
    const filters = reactive({
      status: '',
      client: '',
      date_range: '30d'
    });
    
    const currentTab = ref('all');
    
    const tabs = [
      { label: 'Todas', value: 'all' },
      { label: 'Cadastro', value: 'pending' },
      { label: 'Conferência', value: 'verification' },
      { label: 'Análise', value: 'analysis' },
      { label: 'Comitê', value: 'committee' },
      { label: 'Formalização', value: 'formalization' },
      { label: 'Acompanhamento', value: 'monitoring' }
    ];
    
    // Buscar operações
    const fetchOperations = async (page = 1) => {
      try {
        loading.value = true;
        
        // Construir parâmetros de filtro
        const params = {
          page,
          status: filters.status || undefined,
          search: filters.client || undefined
        };
        
        if (filters.date_range !== 'all') {
          // Adicionar filtragem por data se necessário
          params.date_range = filters.date_range;
        }
        
        // Chamar a API para obter operações
        const response = await api.operations.getOperations(params);
        
        console.log('Resposta da API de operações:', response.data);
        
        if (response.data && Array.isArray(response.data.results)) {
          operations.value = response.data.results;
          totalPages.value = Math.ceil(response.data.count / itemsPerPage);
        } else if (response.data && Array.isArray(response.data)) {
          // Caso a API retorne uma lista direta sem paginação
          operations.value = response.data;
          totalPages.value = 1;
        } else {
          console.warn('Formato de resposta inesperado, usando dados estáticos');
          operations.value = [
            // Dados estáticos que já existem
          ];
          totalPages.value = Math.ceil(operations.value.length / itemsPerPage);
        }
        
        currentPage.value = page;
      } catch (error) {
        console.error('Erro ao buscar operações:', error);
        // Fallback para dados estáticos em caso de erro
        operations.value = [
          // Dados estáticos que já existem
        ];
        totalPages.value = Math.ceil(operations.value.length / itemsPerPage);
      } finally {
        loading.value = false;
      }
    };
    
    // Filtrar operações
    const filteredOperations = computed(() => {
      let result = operations.value;
      
      // Filtrar por tab (status)
      if (currentTab.value !== 'all') {
        result = result.filter(op => op.status === currentTab.value);
      }
      
      // Aplicar filtros adicionais
      if (filters.status) {
        result = result.filter(op => op.status === filters.status);
      }
      
      if (filters.client) {
        const searchTerm = filters.client.toLowerCase();
        result = result.filter(
          op => op.client_name.toLowerCase().includes(searchTerm) || 
                op.client_document.includes(searchTerm)
        );
      }
      
      // Filtrar por data
      if (filters.date_range !== 'all') {
        const now = new Date();
        let daysAgo;
        
        switch (filters.date_range) {
          case '7d':
            daysAgo = 7;
            break;
          case '30d':
            daysAgo = 30;
            break;
          case '90d':
            daysAgo = 90;
            break;
          default:
            daysAgo = 0;
        }
        
        if (daysAgo > 0) {
          const cutoffDate = new Date(now.setDate(now.getDate() - daysAgo));
          result = result.filter(op => new Date(op.created_at) >= cutoffDate);
        }
      }
      
      // Aplicar paginação
      const startIndex = (currentPage.value - 1) * itemsPerPage;
      const endIndex = startIndex + itemsPerPage;
      return result.slice(startIndex, endIndex);
    });
    
    // Obter operações por status para as contagens de abas
    const getOperationsByStatus = (status) => {
      if (status === 'all') return operations.value;
      return operations.value.filter(op => op.status === status);
    };
    
    // Aplicar filtros
    const applyFilters = () => {
      currentPage.value = 1; // Resetar para a primeira página
    };
    
    // Resetar filtros
    const resetFilters = () => {
      filters.status = '';
      filters.client = '';
      filters.date_range = '30d';
      currentPage.value = 1;
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
        'pending': 'Cadastro Pendente',
        'verification': 'Em Conferência',
        'analysis': 'Em Análise',
        'committee': 'Em Comitê',
        'formalization': 'Em Formalização',
        'monitoring': 'Em Acompanhamento',
        'approved': 'Aprovado',
        'rejected': 'Reprovado',
        'cancelled': 'Cancelado'
      };
      return labels[status] || status;
    };
    
    // Paginação
    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page;
      }
    };
    
    onMounted(() => {
      fetchOperations();
    });
    
    return {
      operations,
      filters,
      currentPage,
      totalPages,
      currentTab,
      tabs,
      filteredOperations,
      getOperationsByStatus,
      applyFilters,
      resetFilters,
      formatDate,
      formatCurrency,
      getStatusLabel,
      changePage
    };
  }
}
</script>
 
<style scoped>
.operations-list {
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

.filter-section {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  padding: 25px;
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
  background: linear-gradient(90deg, #4673F5, #2556e0);
  color: white;
  box-shadow: 0 4px 10px rgba(70, 115, 245, 0.2);
}

.btn-filter:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(70, 115, 245, 0.3);
}

.btn-reset {
  background-color: #f5f5f7;
  color: #555;
}

.btn-reset:hover {
  background-color: #e5e5e7;
}

.operations-tabs {
  display: flex;
  overflow-x: auto;
  margin-bottom: 25px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 1px;
  position: sticky;
  top: 80px;
  background-color: #f5f7fa;
  z-index: 3;
  padding-top: 10px;
  border-radius: 8px 8px 0 0;
}

.tab-button {
  padding: 12px 20px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  border-bottom: 3px solid transparent;
  white-space: nowrap;
  transition: all 0.3s ease;
  position: relative;
  font-weight: 500;
}

.tab-button.active {
  color: #4673F5;
  border-bottom-color: #4673F5;
  font-weight: 600;
}

.tab-button:hover {
  color: #4673F5;
}

.count-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: #f0f0f0;
  color: #333;
  font-size: 12px;
  width: 20px;
  height: 20px;
  border-radius: 10px;
  margin-left: 6px;
  font-weight: 600;
}

.tab-button.active .count-badge {
  background-color: #4673F5;
  color: white;
}

.operations-table {
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

.btn-view {
  padding: 8px 14px;
  border-radius: 6px;
  text-decoration: none;
  font-size: 13px;
  background-color: #E3F2FD;
  color: #1976D2;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-weight: 500;
}

.btn-view:hover {
  background-color: #BBDEFB;
  color: #0D47A1;
  text-decoration: none;
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(25, 118, 210, 0.2);
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
  background-color: #E3F2FD;
  color: #1976D2;
}

.status-badge.verification {
  background-color: #EDE7F6;
  color: #7E57C2;
}

.status-badge.analysis {
  background-color: #FFF8E1;
  color: #FFA000;
}

.status-badge.committee {
  background-color: #E8F5E9;
  color: #388E3C;
}

.status-badge.formalization {
  background-color: #E1F5FE;
  color: #0288D1;
}

.status-badge.monitoring {
  background-color: #F3E5F5;
  color: #AB47BC;
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

.empty-state {
  text-align: center;
  padding: 60px 30px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  margin-bottom: 25px;
  color: #666;
}

.empty-state p {
  margin-bottom: 20px;
  font-size: 16px;
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

.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
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

/* Responsividade para telas menores */
@media (max-width: 768px) {
  .filter-section {
    padding: 20px;
  }
  
  .filter-row {
    flex-direction: column;
    gap: 15px;
  }
  
  .filter-group {
    min-width: 100%;
  }
  
  .operations-tabs {
    padding: 10px;
  }
  
  .tab-button {
    padding: 10px 15px;
    font-size: 13px;
  }
  
  .btn-filter, .btn-reset {
    width: 100%;
  }
  
  .search-box {
    flex-direction: column;
  }
  
  .pagination {
    flex-direction: column;
    gap: 10px;
  }
}
</style>