<template>
    <div class="application-detail">
      <div class="page-header">
        <h1>Solicitação de Crédito #{{ applicationId }}</h1>
        <div class="status-badge" :class="application.status">
          {{ getStatusLabel(application.status) }}
        </div>
      </div>
      
      <div class="content-grid">
        <!-- Informações da solicitação -->
        <div class="info-card">
          <h2>Detalhes da Solicitação</h2>
          <div v-if="application.id">
            <div class="info-row">
              <span class="label">Valor Solicitado:</span>
              <span class="value">R$ {{ formatCurrency(application.amount_requested) }}</span>
            </div>
            <div class="info-row">
              <span class="label">Prazo (meses):</span>
              <span class="value">{{ application.term_months }}</span>
            </div>
            <div class="info-row">
              <span class="label">Finalidade:</span>
              <span class="value">{{ application.purpose }}</span>
            </div>
            <div class="info-row">
              <span class="label">Taxa de Juros:</span>
              <span class="value">{{ application.interest_rate }}% ao mês</span>
            </div>
            <div class="info-row">
              <span class="label">Data da Solicitação:</span>
              <span class="value">{{ formatDate(application.created_at) }}</span>
            </div>
          </div>
          <div v-else>
            <p>Carregando dados da solicitação...</p>
          </div>
        </div>
        
        <!-- Informações do cliente -->
        <div class="info-card">
          <h2>Dados do Cliente</h2>
          <div v-if="client.id">
            <div class="info-row">
              <span class="label">Nome:</span>
              <span class="value">{{ client.name }}</span>
            </div>
            <div class="info-row">
              <span class="label">CPF:</span>
              <span class="value">{{ client.cpf }}</span>
            </div>
            <div class="info-row">
              <span class="label">Email:</span>
              <span class="value">{{ client.email }}</span>
            </div>
            <div class="info-row">
              <span class="label">Telefone:</span>
              <span class="value">{{ client.phone }}</span>
            </div>
            <div class="info-row">
              <span class="label">Renda Mensal:</span>
              <span class="value">R$ {{ formatCurrency(client.monthly_income) }}</span>
            </div>
            <div class="info-actions">
              <router-link :to="`/clients/${client.id}`" class="btn-view">Ver Perfil Completo</router-link>
            </div>
          </div>
          <div v-else>
            <p>Carregando dados do cliente...</p>
          </div>
        </div>
        
        <!-- Status e Análise -->
        <div class="info-card status-card">
          <h2>Status da Solicitação</h2>
          <div class="status-timeline">
            <div class="timeline-step" :class="{ active: isStatusActive('pending') }">
              <div class="step-icon pending-icon"></div>
              <div class="step-label">Pendente</div>
              <div class="step-date" v-if="isStatusActive('pending')">{{ formatDate(application.created_at) }}</div>
            </div>
            <div class="timeline-connector" :class="{ active: isStatusActive('in_analysis') }"></div>
            <div class="timeline-step" :class="{ active: isStatusActive('in_analysis') }">
              <div class="step-icon analysis-icon"></div>
              <div class="step-label">Em Análise</div>
              <div class="step-date" v-if="isStatusActive('in_analysis')">{{ formatDate(statusDates.in_analysis) }}</div>
            </div>
            <div class="timeline-connector" :class="{ active: isFinalStatus() }"></div>
            <div class="timeline-step" :class="{ active: isFinalStatus(), approved: application.status === 'approved', rejected: application.status === 'rejected' }">
              <div class="step-icon" :class="getFinalStepIconClass()"></div>
              <div class="step-label">{{ getFinalStepLabel() }}</div>
              <div class="step-date" v-if="isFinalStatus()">{{ formatDate(statusDates.final) }}</div>
            </div>
          </div>
          
          <div v-if="canStartAnalysis" class="status-actions">
            <button @click="startAnalysis" class="btn-analyze">Iniciar Análise</button>
          </div>
        </div>
        
        <!-- Análise de IA -->
        <div class="info-card" v-if="hasAiPrediction">
          <h2>
            <span>Análise de IA</span>
            <span class="ai-badge">IA</span>
          </h2>
          
          <div v-if="aiPrediction">
            <div class="risk-score">
              <div class="risk-meter">
                <div class="risk-bar" :style="{ width: aiPrediction.risk_score + '%' }"></div>
              </div>
              <div class="risk-label">
                Score de Risco: {{ aiPrediction.risk_score.toFixed(1) }}/100
                <span class="risk-help">(quanto menor, melhor)</span>
              </div>
            </div>
            
            <div class="recommendation-box" :class="getRecommendationClass()">
              <h3>{{ getRecommendationTitle() }}</h3>
              <p>{{ getRecommendationDetail() }}</p>
            </div>
            
            <div class="explanation-box">
              <h3>Análise Detalhada</h3>
              <pre>{{ aiPrediction.explanation }}</pre>
            </div>
          </div>
          <div v-else>
            <p>Carregando análise de IA...</p>
          </div>
        </div>
        
        <!-- Análise do Analista -->
        <div class="info-card" v-if="hasAnalysis">
          <h2>Análise do Avaliador</h2>
          <div v-if="analysis">
            <div class="info-row">
              <span class="label">Analista:</span>
              <span class="value">{{ analysis.analyst_name }}</span>
            </div>
            <div class="info-row">
              <span class="label">Decisão:</span>
              <span class="value">
                <span :class="'status-badge ' + analysis.decision">
                  {{ getDecisionLabel(analysis.decision) }}
                </span>
              </span>
            </div>
            <div class="info-row">
              <span class="label">Data da Análise:</span>
              <span class="value">{{ formatDate(analysis.created_at) }}</span>
            </div>
            <div class="info-row notes-row" v-if="analysis.notes">
              <span class="label">Observações:</span>
              <span class="value notes-value">{{ analysis.notes }}</span>
            </div>
            
            <div class="analysis-actions">
              <router-link :to="`/analyses/${analysis.id}`" class="btn-view">Ver Análise Completa</router-link>
            </div>
          </div>
          <div v-else>
            <p>Carregando dados da análise...</p>
          </div>
        </div>
      </div>
      
      <!-- Ações da solicitação -->
      <div class="application-actions">
        <div v-if="application.status === 'pending'" class="action-card">
          <h3>Ações Disponíveis</h3>
          <div class="action-buttons">
            <button @click="startAnalysis" class="btn-analyze">Iniciar Análise</button>
            <button @click="cancelApplication" class="btn-cancel">Cancelar Solicitação</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, computed, onMounted } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import api from '../../services/api';
  
  export default {
    name: 'ApplicationDetail',
    setup() {
      const route = useRoute();
      const router = useRouter();
      
      const applicationId = ref(parseInt(route.params.id));
      const application = ref({});
      const client = ref({});
      const analysis = ref(null);
      const aiPrediction = ref(null);
      
      // Datas de status para timeline
      const statusDates = ref({
        in_analysis: null,
        final: null
      });
      
      // Buscar dados da solicitação
      const fetchApplication = async () => {
        try {
          const response = await api.getApplication(applicationId.value);
          application.value = response.data;
          
          // Buscar cliente relacionado
          fetchClient(application.value.client_id);
          
          // Buscar análise se existir
          checkForAnalysis();
          
          // Definir datas para a timeline
          if (application.value.status === 'in_analysis' || 
              application.value.status === 'approved' || 
              application.value.status === 'rejected') {
            statusDates.value.in_analysis = application.value.updated_at;
          }
          
          if (application.value.status === 'approved' || 
              application.value.status === 'rejected') {
            statusDates.value.final = application.value.updated_at;
          }
        } catch (error) {
          console.error('Erro ao buscar solicitação:', error);
        }
      };
      
      // Buscar cliente
      const fetchClient = async (clientId) => {
        try {
          const response = await api.getClient(clientId);
          client.value = response.data;
        } catch (error) {
          console.error('Erro ao buscar cliente:', error);
        }
      };
      
      // Verificar se existe análise
      const checkForAnalysis = async () => {
        try {
          // Buscar análises associadas à solicitação
          const response = await api.getAnalyses({ application_id: applicationId.value });
          if (response.data.results && response.data.results.length > 0) {
            analysis.value = response.data.results[0];
            // Buscar predição da IA
            fetchAIPrediction();
          }
        } catch (error) {
          console.error('Erro ao buscar análise:', error);
        }
      };
      
      // Buscar predição da IA
      const fetchAIPrediction = async () => {
        try {
          const response = await api.getAIPrediction(applicationId.value);
          aiPrediction.value = response.data;
        } catch (error) {
          console.error('Erro ao buscar predição de IA:', error);
        }
      };
      
      // Iniciar análise
      const startAnalysis = async () => {
        try {
          await api.analyzeApplication(applicationId.value);
          router.push(`/analyses/${analysis.value.id}`);
        } catch (error) {
          console.error('Erro ao iniciar análise:', error);
        }
      };
      
      // Cancelar solicitação
      const cancelApplication = async () => {
        if (confirm('Tem certeza que deseja cancelar esta solicitação?')) {
          try {
            const updatedApp = { ...application.value, status: 'cancelled' };
            await api.updateApplication(applicationId.value, updatedApp);
            fetchApplication(); // Recarregar dados
          } catch (error) {
            console.error('Erro ao cancelar solicitação:', error);
          }
        }
      };
      
      // Verificar se status está ativo
      const isStatusActive = (status) => {
        if (application.value.status === status) return true;
        
        // Se o status atual é posterior ao status verificado na timeline
        const statusOrder = ['pending', 'in_analysis', 'approved', 'rejected', 'cancelled'];
        const currentIndex = statusOrder.indexOf(application.value.status);
        const checkIndex = statusOrder.indexOf(status);
        
        return currentIndex > checkIndex;
      };
      
      // Verificar se está no status final
      const isFinalStatus = () => {
        return ['approved', 'rejected', 'cancelled'].includes(application.value.status);
      };
      
      // Classes e labels para o último passo da timeline
      const getFinalStepIconClass = () => {
        if (application.value.status === 'approved') return 'approved-icon';
        if (application.value.status === 'rejected') return 'rejected-icon';
        return 'final-icon';
      };
      
      const getFinalStepLabel = () => {
        if (application.value.status === 'approved') return 'Aprovado';
        if (application.value.status === 'rejected') return 'Reprovado';
        if (application.value.status === 'cancelled') return 'Cancelado';
        return 'Decisão Final';
      };
      
      // Classe para recomendação da IA
      const getRecommendationClass = () => {
        if (!aiPrediction.value) return '';
        
        const rec = aiPrediction.value.recommendation.toLowerCase();
        if (rec.includes('aprovado com condições')) return 'warning';
        if (rec.includes('aprovado')) return 'success';
        if (rec.includes('reprovado')) return 'danger';
        if (rec.includes('análise manual')) return 'info';
        
        return '';
      };
      
      // Título da recomendação da IA
      const getRecommendationTitle = () => {
        if (!aiPrediction.value) return '';
        const parts = aiPrediction.value.recommendation.split(':');
        return parts[0];
      };
      
      // Detalhes da recomendação da IA
      const getRecommendationDetail = () => {
        if (!aiPrediction.value) return '';
        const parts = aiPrediction.value.recommendation.split(':');
        return parts.length > 1 ? parts[1].trim() : '';
      };
      
      // Formatações
      const formatDate = (dateString) => {
        if (!dateString) return '-';
        return new Date(dateString).toLocaleDateString('pt-BR');
      };
      
      const formatCurrency = (value) => {
        return parseFloat(value).toLocaleString('pt-BR', {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2
        });
      };
      
      // Labels
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
      
      // Computed properties
      const hasAnalysis = computed(() => {
        return analysis.value !== null;
      });
      
      const hasAiPrediction = computed(() => {
        return application.value.status === 'in_analysis' || 
               application.value.status === 'approved' || 
               application.value.status === 'rejected';
      });
      
      const canStartAnalysis = computed(() => {
        return application.value.status === 'pending';
      });
      
      onMounted(() => {
        fetchApplication();
      });
      
      return {
        applicationId,
        application,
        client,
        analysis,
        aiPrediction,
        statusDates,
        hasAnalysis,
        hasAiPrediction,
        canStartAnalysis,
        formatDate,
        formatCurrency,
        getStatusLabel,
        getDecisionLabel,
        isStatusActive,
        isFinalStatus,
        getFinalStepIconClass,
        getFinalStepLabel,
        getRecommendationClass,
        getRecommendationTitle,
        getRecommendationDetail,
        startAnalysis,
        cancelApplication
      };
    }
  }
  </script>
  
  <style scoped>
  .application-detail {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
  }
  
  .content-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
  }
  
  .info-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
  }
  
  .info-card h2 {
    margin-top: 0;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
    font-size: 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .info-row {
    display: flex;
    margin-bottom: 12px;
  }
  
  .label {
    flex: 1;
    color: #666;
    font-weight: 500;
  }
  
  .value {
    flex: 2;
  }
  
  .notes-row {
    flex-direction: column;
  }
  
  .notes-value {
    margin-top: 8px;
    padding: 10px;
    background-color: #f9f9f9;
    border-radius: 4px;
    white-space: pre-line;
  }
  
  .status-badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 14px;
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
  
  .status-timeline {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 30px 0;
  }
  
  .timeline-step {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex: 1;
    position: relative;
    opacity: 0.5;
  }
  
  .timeline-step.active {
    opacity: 1;
  }
  
  .timeline-connector {
    height: 2px;
    background-color: #ddd;
    flex-grow: 1;
    margin: 0 5px;
    position: relative;
    top: -20px;
  }
  
  .timeline-connector.active {
    background-color: #2196F3;
  }
  
  .step-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #ddd;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 10px;
  }
  
  .step-icon::before {
    font-family: 'Arial', sans-serif;
    color: white;
    font-weight: bold;
  }
  
  .pending-icon {
    background-color: #FFA000;
  }
  
  .pending-icon::before {
    content: "1";
  }
  
  .analysis-icon {
    background-color: #1976D2;
  }
  
  .analysis-icon::before {
    content: "2";
  }
  
  .approved-icon {
    background-color: #388E3C;
  }
  
  .approved-icon::before {
    content: "✓";
  }
  
  .rejected-icon {
    background-color: #D32F2F;
  }
  
  .rejected-icon::before {
    content: "✕";
  }
  
  .final-icon {
    background-color: #616161;
  }
  
  .final-icon::before {
    content: "3";
  }
  
  .step-label {
    font-weight: 500;
    text-align: center;
    margin-bottom: 5px;
  }
  
  .step-date {
    font-size: 12px;
    color: #666;
  }
  
  .info-actions, .status-actions, .analysis-actions {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
  
  .btn-view, .btn-analyze, .btn-cancel {
    padding: 8px 16px;
    border-radius: 4px;
    text-decoration: none;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    border: none;
  }
  
  .btn-view {
    background-color: #E3F2FD;
    color: #1976D2;
  }
  
  .btn-analyze {
    background-color: #E8F5E9;
    color: #388E3C;
  }
  
  .btn-cancel {
    background-color: #FFEBEE;
    color: #D32F2F;
  }
  
  .application-actions {
    margin-top: 20px;
  }
  
  .action-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
  }
  
  .action-card h3 {
    margin-top: 0;
    margin-bottom: 20px;
    font-size: 18px;
  }
  
  .action-buttons {
    display: flex;
    gap: 10px;
    justify-content: flex-end;
  }
  
  .ai-badge {
    background-color: #E1F5FE;
    color: #0288D1;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
  }
  
  .risk-score {
    margin-bottom: 20px;
  }
  
  .risk-meter {
    height: 10px;
    background-color: #ECEFF1;
    border-radius: 5px;
    overflow: hidden;
    margin-bottom: 5px;
  }
  
  .risk-bar {
    height: 100%;
    background: linear-gradient(to right, #4CAF50, #FFC107, #F44336);
    border-radius: 5px;
  }
  
  .risk-label {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    font-weight: 500;
  }
  
  .risk-help {
    color: #777;
    font-size: 12px;
    font-weight: normal;
  }
  
  .recommendation-box {
    padding: 15px;
    border-radius: 6px;
    margin-bottom: 20px;
  }
  
  .recommendation-box h3 {
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 16px;
    font-weight: 600;
  }
  
  .recommendation-box.success {
    background-color: #E8F5E9;
    border-left: 4px solid #4CAF50;
  }
  
  .recommendation-box.warning {
    background-color: #FFF8E1;
    border-left: 4px solid #FFC107;
  }
  
  .recommendation-box.danger {
    background-color: #FFEBEE;
    border-left: 4px solid #F44336;
  }
  
  .recommendation-box.info {
    background-color: #E3F2FD;
    border-left: 4px solid #2196F3;
  }
  
  .explanation-box {
    background-color: #F5F5F5;
    border-radius: 6px;
    padding: 15px;
  }
  
  .explanation-box h3 {
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 16px;
  }
  
  .explanation-box pre {
    white-space: pre-wrap;
    font-family: inherit;
    font-size: 14px;
    line-height: 1.5;
    color: #555;
  }
  </style>