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
      const fetchOperations = async () => {
        try {
          // No MVP, usaremos dados estáticos
          operations.value = [
            {
              id: 101,
              client_name: 'João Silva',
              client_document: '123.456.789-00',
              amount: 15000,
              modality: 'Capital de Giro',
              term: 24,
              created_at: '2025-02-15T10:30:00',
              status: 'analysis'
            },
            {
              id: 102,
              client_name: 'Maria Souza',
              client_document: '987.654.321-00',
              amount: 50000,
              modality: 'Financiamento',
              term: 36,
              created_at: '2025-02-18T14:45:00',
              status: 'verification'
            },
            {
              id: 103,
              client_name: 'Tech Solutions Ltda',
              client_document: '12.345.678/0001-90',
              amount: 200000,
              modality: 'Capital de Giro',
              term: 48,
              created_at: '2025-02-20T09:15:00',
              status: 'committee'
            },
            {
              id: 104,
              client_name: 'Ana Pereira',
              client_document: '456.789.123-00',
              amount: 8000,
              modality: 'Crédito Pessoal',
              term: 12,
              created_at: '2025-02-22T16:30:00',
              status: 'pending'
            },
            {
              id: 105,
              client_name: 'Comércio Verde Ltda',
              client_document: '98.765.432/0001-10',
              amount: 150000,
              modality: 'Financiamento',
              term: 60,
              created_at: '2025-02-24T11:20:00',
              status: 'formalization'
            },
            {
              id: 106,
              client_name: 'Roberto Almeida',
              client_document: '321.654.987-00',
              amount: 30000,
              modality: 'Capital de Giro',
              term: 24,
              created_at: '2025-02-26T13:40:00',
              status: 'monitoring'
            }
          ];
          
          // Calcular paginação
          totalPages.value = Math.ceil(operations.value.length / itemsPerPage);
        } catch (error) {
          console.error('Erro ao buscar operações:', error);
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
    padding: 20px;
  }
  
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
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
  
  .operations-tabs {
    display: flex;
    overflow-x: auto;
    margin-bottom: 20px;
    border-bottom: 1px solid #ddd;
    padding-bottom: 1px;
  }
  
  .tab-button {
    padding: 10px 20px;
    background: none;
    border: none;
    cursor: pointer;
    font-size: 14px;
    color: #666;
    border-bottom: 3px solid transparent;
    position: relative;
    white-space: nowrap;
  }
  
  .tab-button.active {
    color: var(--primary-color);
    border-bottom-color: var(--primary-color);
    font-weight: 500;
  }
  
  .count-badge {
    display: inline-block;
    background-color: #f0f0f0;
    color: #333;
    font-size: 12px;
    line-height: 1;
    padding: 2px 6px;
    border-radius: 10px;
    margin-left: 5px;
  }
  
  .tab-button.active .count-badge {
    background-color: var(--primary-color);
    color: white;
  }
  
  .operations-table {
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
    display: inline-flex;
    align-items: center;
    gap: 5px;
  }
  
  .status-badge {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
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
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 40px 20px;
    text-align: center;
    margin-bottom: 20px;
  }
  
  .empty-state p {
    color: #666;
    margin-bottom: 20px;
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