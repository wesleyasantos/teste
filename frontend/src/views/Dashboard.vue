<template>
  <div class="dashboard">
    <div class="welcome-banner">
      <div class="container">
        <h1>Bem-vindo a W2M Finance</h1>
        <p class="mvp-notice">Este é um ambiente de demonstração (MVP)</p>
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
              <router-link to="/operations" class="view-all">Ver Todas</router-link>
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
                    <router-link :to="'/operations/' + app.id" class="btn-view">Ver</router-link>
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
                  <router-link :to="'/operations/new?client=' + client.id" class="btn-action">Nova Solicitação</router-link>
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
            <router-link to="/operations/new" class="demo-btn">
              <i class="fas fa-file-invoice-dollar"></i>
              Nova Operação
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
  padding-bottom: 50px;
}

.welcome-banner {
  background: linear-gradient(135deg, #00004b 0%, #000075 100%);
  color: white;
  padding: 40px 0;
  margin-bottom: 40px;
  box-shadow: 0 5px 20px rgba(0, 0, 75, 0.2);
  position: relative;
  overflow: hidden;
}

.welcome-banner::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
  border-radius: 50%;
  transform: translate(50%, -50%);
}

.welcome-banner h1 {
  margin: 0 0 15px;
  font-size: 32px;
  font-weight: 700;
  animation: fadeIn 0.8s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.mvp-notice {
  background-color: #FF9F1C;
  color: #00004b;
  display: inline-block;
  padding: 6px 15px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  animation: fadeIn 1s ease-out 0.3s both;
}

.dashboard-stats {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
  gap: 25px;
  margin-bottom: 40px;
}

.stat-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  padding: 25px;
  display: flex;
  transition: all 0.3s ease;
  overflow: hidden;
  position: relative;
  animation: fadeIn 0.5s ease-out forwards;
  animation-delay: calc(var(--animation-order, 0) * 0.1s);
  opacity: 0;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  color: white;
  margin-right: 20px;
  position: relative;
  z-index: 1;
}

.stat-icon::before {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 12px;
  opacity: 0.2;
  background-color: currentColor;
  z-index: -1;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
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
  background-color: #FF9F1C;
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
  font-size: 32px;
  font-weight: 700;
  color: #00004b;
  margin-bottom: 5px;
  background: linear-gradient(90deg, #00004b, #4673F5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
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
  margin-top: 8px;
  font-weight: 500;
}

.stat-trend.up {
  color: #4CAF50;
}

.stat-trend.up::before {
  content: '↑';
  margin-right: 5px;
}

.stat-trend.down {
  color: #F44336;
}

.stat-trend.down::before {
  content: '↓';
  margin-right: 5px;
}

.dashboard-row {
  display: flex;
  margin-bottom: 30px;
  gap: 25px;
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
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  padding: 25px;
  height: 100%;
  animation: fadeIn 0.5s ease-out forwards;
  animation-delay: calc(var(--animation-order, 0) * 0.1s);
  opacity: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.card-header h2 {
  margin: 0;
  font-size: 20px;
  color: #00004b;
  font-weight: 600;
}

.view-all {
  color: #4673F5;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.view-all:hover {
  color: #8237DC;
  text-decoration: none;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 8px;
  overflow: hidden;
}

.data-table th, .data-table td {
  padding: 14px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.data-table th {
  font-weight: 600;
  color: #555;
  background-color: #f9f9fc;
}

.data-table tr:hover {
  background-color: #f5f7fa;
}

.data-table tr:last-child td {
  border-bottom: none;
}

.btn-view {
  padding: 6px 12px;
  background-color: #E3F2FD;
  color: #1976D2;
  border-radius: 6px;
  font-size: 13px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.btn-view:hover {
  background-color: #BBDEFB;
  color: #0D47A1;
  text-decoration: none;
}

.analysis-item {
  background-color: #f9f9fc;
  border-radius: 10px;
  padding: 18px;
  margin-bottom: 15px;
  transition: all 0.3s ease;
  border-left: 4px solid #4673F5;
}

.analysis-item:hover {
  transform: translateX(5px);
  background-color: #f5f7fa;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.analysis-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.analysis-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #00004b;
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
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  transition: all 0.3s ease;
  position: relative;
  border: 1px solid #eee;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.03);
  overflow: hidden;
}

.client-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  border-color: #e5e5e5;
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
  color: #00004b;
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

.btn-action {
  padding: 6px 12px;
  background-color: #E8F5E9;
  color: #388E3C;
  border-radius: 6px;
  font-size: 13px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.btn-action:hover {
  background-color: #C8E6C9;
  color: #2E7D32;
  text-decoration: none;
}

.empty-state {
  text-align: center;
  padding: 30px 20px;
  color: #666;
  background-color: #f9f9fc;
  border-radius: 10px;
  margin-top: 15px;
}

.btn-primary {
  background-color: #4673F5;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 10px rgba(70, 115, 245, 0.2);
}

.btn-primary:hover {
  background-color: #2556e0;
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(70, 115, 245, 0.3);
  text-decoration: none;
}

.dashboard-footer {
  margin-top: 50px;
  padding-top: 30px;
}

.mvp-actions {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  padding: 30px;
  text-align: center;
}

.mvp-actions h3 {
  margin-bottom: 25px;
  font-size: 20px;
  color: #00004b;
  position: relative;
  display: inline-block;
}

.mvp-actions h3:after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, #4673F5, #8237DC);
  border-radius: 1.5px;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
  margin-top: 20px;
}

.demo-btn {
  background: linear-gradient(135deg, #00004b, #000075);
  color: white;
  padding: 15px 25px;
  border-radius: 10px;
  border: none;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 75, 0.15);
}

.demo-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 75, 0.2);
  background: linear-gradient(135deg, #000075, #00004b);
  text-decoration: none;
}

.demo-btn i {
  font-size: 18px;
}

/* Status badges */
.status-badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
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
</style>