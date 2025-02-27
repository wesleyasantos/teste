<template>
  <div class="dashboard">
    <div class="welcome-banner">
      <div class="container">
        <h1>Bem-vindo a W2M Finance</h1>
        <p class="mvp-notice">Este é um ambiente de demonstração (MVP) com dados pré-carregados</p>
      </div>
    </div>
    
    <div class="container">
      <div class="dashboard-stats">
        <div class="stat-card">
          <div class="stat-icon pending-icon">
            <i class="fas fa-clock"></i>
          </div>
          <div class="stat-content">
            <h3>Solicitações Pendentes</h3>
            <div class="stat-value">{{ stats.pendingCount }}</div>
            <div class="stat-trend up" v-if="stats.pendingCount > 0">
              <span>+{{ stats.pendingCount }}</span> novas hoje
            </div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon approved-icon">
            <i class="fas fa-check-circle"></i>
          </div>
          <div class="stat-content">
            <h3>Aprovadas este mês</h3>
            <div class="stat-value">{{ stats.approvedCount }}</div>
            <div class="stat-amount">R$ {{ formatCurrency(stats.approvedAmount) }}</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon analysis-icon">
            <i class="fas fa-search-dollar"></i>
          </div>
          <div class="stat-content">
            <h3>Em Análise</h3>
            <div class="stat-value">{{ stats.inAnalysisCount }}</div>
            <div class="stat-info">{{ stats.analysisRemainingToday }} pendentes para hoje</div>
          </div>
        </div>
        
        <div class="stat-card">
          <div class="stat-icon rate-icon">
            <i class="fas fa-chart-line"></i>
          </div>
          <div class="stat-content">
            <h3>Taxa de Aprovação</h3>
            <div class="stat-value">{{ stats.approvalRate }}%</div>
            <div class="stat-trend" :class="stats.approvalTrend">
              <span>{{ stats.approvalTrend === 'up' ? '+' : '-' }}2.5%</span> vs. semana anterior
            </div>
          </div>
        </div>
      </div>
      
      <div class="dashboard-row">
        <div class="dashboard-col">
          <div class="dashboard-card">
            <div class="card-header">
              <h2>Solicitações Recentes</h2>
              <router-link to="/applications" class="view-all">Ver Todas</router-link>
            </div>
            <table class="data-table">
              <thead>
                <tr>
                  <th>Cliente</th>
                  <th>Data</th>
                  <th>Valor</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="app in recentApplications" :key="app.id">
                  <td>{{ app.client_name }}</td>
                  <td>{{ formatDate(app.created_at) }}</td>
                  <td>R$ {{ formatCurrency(app.amount_requested) }}</td>
                  <td>
                    <span :class="'status-badge ' + app.status">
                      {{ getStatusLabel(app.status) }}
                    </span>
                  </td>
                  <td>
                    <router-link :to="'/applications/' + app.id" class="btn-view">Ver</router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <div class="dashboard-col">
          <div class="dashboard-card">
            <div class="card-header">
              <h2>Análises Pendentes</h2>
              <router-link to="/analyses" class="view-all">Ver Todas</router-link>
            </div>
            <div v-if="pendingAnalyses.length > 0">
              <div v-for="analysis in pendingAnalyses" :key="analysis.id" class="analysis-item">
                <div class="analysis-header">
                  <h3>{{ analysis.client_name }}</h3>
                  <span :class="'status-badge ' + analysis.decision">
                    {{ getDecisionLabel(analysis.decision) }}
                  </span>
                </div>
                <div class="analysis-details">
                  <div class="analysis-meta">
                    <div><strong>Solicitação:</strong> #{{ analysis.application_id }}</div>
                    <div><strong>Data:</strong> {{ formatDate(analysis.created_at) }}</div>
                  </div>
                  <router-link :to="'/analyses/' + analysis.id" class="btn-primary">Continuar Análise</router-link>
                </div>
              </div>
            </div>
            <div v-else class="empty-state">
              <p>Não há análises pendentes no momento.</p>
            </div>
          </div>
        </div>
      </div>
      
      <div class="dashboard-row">
        <div class="dashboard-col-full">
          <div class="dashboard-card">
            <div class="card-header">
              <h2>Novos Clientes</h2>
              <router-link to="/clients" class="view-all">Ver Todos</router-link>
            </div>
            <div class="clients-grid">
              <div v-for="client in recentClients" :key="client.id" class="client-card">
                <div class="client-type-badge" :class="client.type === 'PF' ? 'pf' : 'pj'">
                  {{ client.type === 'PF' ? 'Pessoa Física' : 'Pessoa Jurídica' }}
                </div>
                <div class="client-info">
                  <h3>{{ client.name }}</h3>
                  <div class="client-meta">
                    <span v-if="client.type === 'PF'">{{ client.cpf }}</span>
                    <span v-else>{{ client.cnpj }}</span>
                  </div>
                </div>
                <div class="client-actions">
                  <router-link :to="'/clients/' + client.id" class="btn-view">Perfil</router-link>
                  <router-link :to="'/applications/new?client=' + client.id" class="btn-action">Nova Solicitação</router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="dashboard-footer">
        <div class="mvp-actions">
          <h3>Ações Rápidas</h3>
          <div class="action-buttons">
            <router-link to="/clients/new" class="demo-btn">
              <i class="fas fa-user-plus"></i>
              Criar Novo Cliente
            </router-link>
            <router-link to="/applications/new" class="demo-btn">
              <i class="fas fa-file-invoice-dollar"></i>
              Nova Solicitação
            </router-link>
            <button @click="resetMVP" class="demo-btn">
              <i class="fas fa-sync-alt"></i>
              Reiniciar Dados Demo
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import api from '../services/api';

export default {
  name: 'Dashboard',
  setup() {
    const recentApplications = ref([]);
    const pendingAnalyses = ref([]);
    const recentClients = ref([]);
    
    const stats = ref({
      pendingCount: 0,
      approvedCount: 0,
      approvedAmount: 0,
      inAnalysisCount: 0,
      analysisRemainingToday: 0,
      approvalRate: 0,
      approvalTrend: 'up' // 'up' ou 'down'
    });
    
    // Buscar dados do dashboard
    const fetchDashboardData = async () => {
      try {
        // Buscar solicitações recentes
        const applicationsResponse = await api.getApplications();
        const applications = applicationsResponse.data.results;
        
        // Processar dados para estatísticas
        const pending = applications.filter(a => a.status === 'pending');
        const inAnalysis = applications.filter(a => a.status === 'in_analysis');
        const approved = applications.filter(a => a.status === 'approved');
        const rejected = applications.filter(a => a.status === 'rejected');
        
        const approvedAmount = approved.reduce((sum, app) => sum + parseFloat(app.amount_requested), 0);
        
        stats.value = {
          pendingCount: pending.length,
          approvedCount: approved.length,
          approvedAmount: approvedAmount,
          inAnalysisCount: inAnalysis.length,
          analysisRemainingToday: inAnalysis.length,
          approvalRate: applications.length > 0 
            ? Math.round((approved.length / (approved.length + rejected.length)) * 100) 
            : 0,
          approvalTrend: Math.random() > 0.5 ? 'up' : 'down' // Simulação para demo
        };
        
        // Obter aplicações recentes
        recentApplications.value = applications
          .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
          .slice(0, 5);
        
        // Buscar análises pendentes
        const analysesResponse = await api.getAnalyses({ decision: 'pending' });
        pendingAnalyses.value = analysesResponse.data.results.slice(0, 3);
        
        // Buscar clientes recentes
        const clientsResponse = await api.getClients();
        recentClients.value = clientsResponse.data.results
          .sort((a, b) => new Date(b.created_at || '2025-01-01') - new Date(a.created_at || '2025-01-01'))
          .slice(0, 4);
      } catch (error) {
        console.error('Erro ao buscar dados do dashboard:', error);
      }
    };
    
    // Formatações
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
    
    const getDecisionLabel = (decision) => {
      const labels = {
        'pending': 'Pendente',
        'approved': 'Aprovado',
        'rejected': 'Reprovado',
        'need_info': 'Requer Informações'
      };
      return labels[decision] || decision;
    };
    
    // Reiniciar dados demo
    const resetMVP = async () => {
      try {
        await api.resetMVPData();
        alert('Dados de demonstração reiniciados com sucesso!');
        fetchDashboardData();
      } catch (error) {
        alert('Erro ao reiniciar dados. Tente novamente.');
      }
    };
    
    onMounted(() => {
      fetchDashboardData();
    });
    
    return {
      recentApplications,
      pendingAnalyses,
      recentClients,
      stats,
      formatDate,
      formatCurrency,
      getStatusLabel,
      getDecisionLabel,
      resetMVP
    };
  }
}
</script>

<style scoped>
.dashboard {
  padding-bottom: 40px;
}

.welcome-banner {
  background-color: var(--primary-color, #00004b);
  background-image: linear-gradient(120deg, #00004b 0%, #000075 100%);
  color: white;
  padding: 40px 0;
  margin-bottom: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 75, 0.15);
}

.welcome-banner h1 {
  margin: 0 0 15px;
  font-size: 28px;
  font-weight: 700;
}

.mvp-notice {
  background-color: var(--secondary-color, #FF9F1C);
  color: var(--primary-color, #00004b);
  display: inline-block;
  padding: 6px 15px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  padding: 20px;
  display: flex;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  overflow: hidden;
  position: relative;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: white;
  margin-right: 20px;
}

.pending-icon {
  background-color: #FFA000;
}

.approved-icon {
  background-color: #4CAF50;
}

.analysis-icon {
  background-color: #2196F3;
}

.rate-icon {
  background-color: var(--secondary-color, #FF9F1C);
}

.stat-content {
  flex: 1;
}

.stat-card h3 {
  margin-top: 0;
  margin-bottom: 10px;
  color: #555;
  font-size: 16px;
  font-weight: 500;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--primary-color, #00004b);
  margin-bottom: 5px;
}

.stat-amount {
  color: #4CAF50;
  font-weight: 600;
  font-size: 16px;
}

.stat-info {
  color: #666;
  font-size: 14px;
}

.stat-trend {
  font-size: 14px;
  display: flex;
  align-items: center;
  margin-top: 5px;
  font-weight: 500;
}

.stat-trend.up {
  color: #4CAF50;
}

.stat-trend.down {
  color: #F44336;
}

.dashboard-row {
  display: flex;
  margin-bottom: 20px;
  gap: 20px;
  flex-wrap: wrap;
}

.dashboard-col {
  flex: 1;
  min-width: 300px;
}

.dashboard-col-full {
  width: 100%;
}

.dashboard-card {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  padding: 20px;
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.card-header h2 {
  margin: 0;
  font-size: 18px;
  color: var(--primary-color, #00004b);
  font-weight: 600;
}

.view-all {
  color: var(--secondary-color, #FF9F1C);
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.view-all:hover {
  color: var(--primary-color, #00004b);
  text-decoration: none;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th, .data-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.data-table th {
  font-weight: 600;
  color: #555;
  background-color: #f9f9f9;
}

.data-table tr:hover {
  background-color: #f5f5f5;
}

.btn-view {
  padding: 5px 12px;
  background-color: #E3F2FD;
  color: #1976D2;
  border-radius: 4px;
  font-size: 12px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-view:hover {
  background-color: #1976D2;
  color: white;
  text-decoration: none;
}

.btn-action {
  padding: 5px 12px;
  background-color: #E8F5E9;
  color: #388E3C;
  border-radius: 4px;
  font-size: 12px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-action:hover {
  background-color: #388E3C;
  color: white;
  text-decoration: none;
}

.btn-primary {
  padding: 8px 16px;
  background-color: var(--primary-color, #00004b);
  color: white;
  border-radius: 4px;
  font-size: 13px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
}

.btn-primary:hover {
  background-color: #000075;
  color: white;
  text-decoration: none;
}

.analysis-item {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  transition: transform 0.2s ease;
  border-left: 4px solid var(--primary-color, #00004b);
}

.analysis-item:hover {
  transform: translateX(5px);
  background-color: #f5f5f5;
}

.analysis-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.analysis-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--primary-color, #00004b);
}

.analysis-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.analysis-meta {
  font-size: 14px;
  color: #666;
}

.clients-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.client-card {
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
  border: 1px solid #eee;
  overflow: hidden;
}

.client-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.client-type-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.client-type-badge.pf {
  background-color: #E3F2FD;
  color: #1976D2;
}

.client-type-badge.pj {
  background-color: #E8F5E9;
  color: #388E3C;
}

.client-info h3 {
  margin: 15px 0 5px;
  font-size: 18px;
  color: var(--primary-color, #00004b);
  font-weight: 600;
}

.client-meta {
  font-size: 14px;
  color: #666;
  margin-bottom: 20px;
}

.client-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.empty-state {
  text-align: center;
  padding: 30px 20px;
  color: #666;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.dashboard-footer {
  margin-top: 40px;
  padding-top: 20px;
}

.mvp-actions {
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  padding: 25px;
  text-align: center;
}

.mvp-actions h3 {
  margin-bottom: 20px;
  font-size: 18px;
  color: var(--primary-color, #00004b);
  position: relative;
  display: inline-block;
}

.mvp-actions h3:after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 100%;
  height: 3px;
  background-color: var(--secondary-color, #FF9F1C);
  border-radius: 1.5px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

.demo-btn {
  background-color: var(--primary-color, #00004b);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.demo-btn:hover {
  background-color: #000075;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
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

.status-badge.need_info {
  background-color: #E1F5FE;
  color: #0288D1;
}

/* Adicione a referência ao Font Awesome no seu index.html ou instale via npm */
/* Para ter os ícones "fas" funcionando */
</style>