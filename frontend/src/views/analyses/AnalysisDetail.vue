<template>
  <div class="analysis-container">
    <div class="page-header">
      <h1>Análise de Crédito #{{ analysis.id }}</h1>
      <div class="status-badge" :class="analysis.decision">
        {{ getDecisionLabel(analysis.decision) }}
      </div>
    </div>
    
    <div class="content-grid">
      <!-- Informações do cliente -->
      <div class="info-card">
        <h2>Dados do Cliente</h2>
        <div v-if="client">
          <div class="info-row">
            <span class="label">Nome:</span>
            <span class="value">{{ client.name }}</span>
          </div>
          <div class="info-row">
            <span class="label">CPF:</span>
            <span class="value">{{ client.cpf }}</span>
          </div>
          <div class="info-row">
            <span class="label">Data de Nascimento:</span>
            <span class="value">{{ formatDate(client.birth_date) }}</span>
          </div>
          <div class="info-row">
            <span class="label">Profissão:</span>
            <span class="value">{{ client.profession }}</span>
          </div>
          <div class="info-row">
            <span class="label">Renda Mensal:</span>
            <span class="value">R$ {{ formatCurrency(client.monthly_income) }}</span>
          </div>
        </div>
        <div v-else>
          <p>Carregando dados do cliente...</p>
        </div>
      </div>
      
      <!-- Informações da solicitação -->
      <div class="info-card">
        <h2>Dados da Solicitação</h2>
        <div v-if="application">
          <div class="info-row">
            <span class="label">Valor Solicitado:</span>
            <span class="value">R$ {{ formatCurrency(application.amount_requested) }}</span>
          </div>
          <div class="info-row">
            <span class="label">Prazo (meses):</span>
            <span class="value">{{ application.term_months }}</span>
          </div>
          <div class="info-row">
            <span class="label">Valor da Parcela:</span>
            <span class="value">R$ {{ calculateInstallment() }}</span>
          </div>
          <div class="info-row">
            <span class="label">Comprometimento de Renda:</span>
            <span class="value">{{ calculateIncomeRatio() }}%</span>
          </div>
          <div class="info-row">
            <span class="label">Finalidade:</span>
            <span class="value">{{ application.purpose }}</span>
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
      
      <!-- Recomendação da IA -->
      <div class="info-card ai-recommendation">
        <h2>
          <span>Recomendação da IA</span>
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
            <h3>{{ aiPrediction.recommendation.split(':')[0] }}</h3>
            <p>{{ aiPrediction.recommendation.split(':')[1] }}</p>
          </div>
          
          <div class="explanation-box">
            <h3>Análise Detalhada</h3>
            <pre>{{ aiPrediction.explanation }}</pre>
          </div>
        </div>
        <div v-else>
          <p>A análise de IA ainda não foi gerada.</p>
          <button @click="generateAIPrediction" class="button primary">
            Gerar Análise de IA
          </button>
        </div>
      </div>
      
      <!-- Formulário de decisão -->
      <div class="info-card decision-form">
        <h2>Análise do Analista</h2>
        
        <form @submit.prevent="saveAnalysis">
          <div class="form-group">
            <label for="decision">Decisão:</label>
            <select v-model="analysis.decision" id="decision" required>
              <option value="pending">Pendente</option>
              <option value="approved">Aprovado</option>
              <option value="rejected">Reprovado</option>
              <option value="need_info">Necessita Informações Adicionais</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="notes">Observações:</label>
            <textarea 
              v-model="analysis.notes" 
              id="notes" 
              rows="6"
              placeholder="Adicione observações sobre sua análise..."></textarea>
          </div>
          
          <div class="form-actions">
            <button type="submit" class="button primary">Salvar Análise</button>
            <button 
              v-if="analysis.decision === 'approved'" 
              type="button" 
              class="button success"
              @click="finishProcess">
              Finalizar Processo
            </button>
          </div>
        </form>
      </div>
      
      <!-- Documentos do cliente -->
      <div class="info-card">
        <h2>Documentos do Cliente</h2>
        
        <table v-if="documents && documents.length > 0">
          <thead>
            <tr>
              <th>Tipo</th>
              <th>Data de Upload</th>
              <th>Arquivo</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="doc in documents" :key="doc.id">
              <td>{{ getDocumentTypeLabel(doc.document_type) }}</td>
              <td>{{ formatDate(doc.uploaded_at) }}</td>
              <td>
                <a :href="doc.file" target="_blank" class="button small">
                  Visualizar
                </a>
              </td>
            </tr>
          </tbody>
        </table>
        
        <div v-else class="empty-state">
          <p>Nenhum documento encontrado para este cliente.</p>
          <button class="button small" @click="navigateToClientDocs">
            Gerenciar Documentos
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

export default {
  name: 'AnalysisDetail',
  
  setup() {
    const route = useRoute();
    const router = useRouter();
    
    const analysis = ref({
      id: null,
      application: null,
      analyst: null,
      decision: 'pending',
      notes: '',
      ai_recommendation: null,
      created_at: null,
      updated_at: null
    });
    
    const application = ref(null);
    const client = ref(null);
    const documents = ref([]);
    const aiPrediction = ref(null);
    
    // Carregar dados da análise
    const fetchAnalysis = async () => {
      try {
        const id = route.params.id;
        // Em uma aplicação real, você buscaria do backend
        analysis.value = {
          id: parseInt(id),
          application: 101,
          analyst: 'Ana Ferreira',
          decision: 'pending',
          notes: '',
          created_at: '2025-02-16T14:20:00',
          updated_at: '2025-02-16T14:20:00'
        };
        
        // Carregar dados relacionados
        await fetchApplication(analysis.value.application);
      } catch (error) {
        console.error('Erro ao buscar análise:', error);
      }
    };
    
    // Carregar aplicação
    const fetchApplication = async (applicationId) => {
      try {
        // Em uma aplicação real, você buscaria do backend
        application.value = {
          id: applicationId,
          client_id: 1,
          amount_requested: 5000,
          term_months: 12,
          interest_rate: 1.5,
          purpose: 'Compra de automóvel',
          status: 'in_analysis',
          created_at: '2025-02-15T10:30:00'
        };
        
        // Carregar dados do cliente
        if (application.value.client_id) {
          await fetchClient(application.value.client_id);
        }
        
        // Carregar predição de IA
        await fetchAIPrediction(applicationId);
      } catch (error) {
        console.error('Erro ao buscar aplicação:', error);
      }
    };
    
    // Carregar cliente
    const fetchClient = async (clientId) => {
      try {
        // Em uma aplicação real, você buscaria do backend
        client.value = {
          id: clientId,
          name: 'João Silva',
          cpf: '123.456.789-00',
          birth_date: '1985-05-15',
          profession: 'Engenheiro',
          monthly_income: 5000
        };
        
        // Carregar documentos
        documents.value = [
          {
            id: 1,
            document_type: 'income',
            uploaded_at: '2025-01-10T14:30:00',
            file: '#'
          },
          {
            id: 2,
            document_type: 'bank_statement',
            uploaded_at: '2025-01-10T14:35:00',
            file: '#'
          }
        ];
      } catch (error) {
        console.error('Erro ao buscar cliente:', error);
      }
    };
    
    // Carregar predição de IA
    const fetchAIPrediction = async (applicationId) => {
      try {
        // Em uma aplicação real, você buscaria do backend
        if (application.value) {
          aiPrediction.value = {
            risk_score: 35.8,
            default_probability: 0.358,
            recommendation: "APROVADO COM CONDIÇÕES: Bom candidato, mas considerar redução do valor ou aumento do prazo.",
            explanation: "Score de risco: 35.80/100 (quanto menor, melhor)\n\n" +
              "Análise de capacidade de pagamento:\n" +
              "- Valor da parcela: R$ 833.33\n" +
              "- Comprometimento da renda: 27.78% da renda mensal\n\n" +
              "Principais fatores para a decisão:\n" +
              "- POSITIVO: Bom comprometimento da renda (abaixo de 30%)\n" +
              "- POSITIVO: Score de crédito adequado\n"
          };
        }
      } catch (error) {
        console.error('Erro ao buscar predição de IA:', error);
      }
    };
    
    // Gerar predição de IA
    const generateAIPrediction = async () => {
      try {
        // Em uma aplicação real, você chamaria a API
        aiPrediction.value = {
          risk_score: 35.8,
          default_probability: 0.358,
          recommendation: "APROVADO COM CONDIÇÕES: Bom candidato, mas considerar redução do valor ou aumento do prazo.",
          explanation: "Score de risco: 35.80/100 (quanto menor, melhor)\n\n" +
            "Análise de capacidade de pagamento:\n" +
            "- Valor da parcela: R$ 833.33\n" +
            "- Comprometimento da renda: 27.78% da renda mensal\n\n" +
            "Principais fatores para a decisão:\n" +
            "- POSITIVO: Bom comprometimento da renda (abaixo de 30%)\n" +
            "- POSITIVO: Score de crédito adequado\n"
        };
      } catch (error) {
        console.error('Erro ao gerar predição de IA:', error);
      }
    };
    
    // Salvar análise
    const saveAnalysis = async () => {
      try {
        // Em uma aplicação real, você chamaria a API
        console.log('Salvando análise:', analysis.value);
        alert('Análise salva com sucesso!');
      } catch (error) {
        console.error('Erro ao salvar análise:', error);
        alert('Erro ao salvar análise. Tente novamente.');
      }
    };
    
    // Finalizar processo
    const finishProcess = async () => {
      try {
        if (application.value) {
          // Em uma aplicação real, você chamaria a API
          console.log('Finalizando processo, aplicação:', application.value.id);
          alert('Processo finalizado com sucesso!');
          router.push('/applications');
        }
      } catch (error) {
        console.error('Erro ao finalizar processo:', error);
        alert('Erro ao finalizar processo. Tente novamente.');
      }
    };
    
    // Navegar para documentos do cliente
    const navigateToClientDocs = () => {
      if (client.value) {
        router.push(`/clients/${client.value.id}`);
      }
    };
    
    // Formatações e cálculos
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('pt-BR');
    };
    
    const formatCurrency = (value) => {
      return parseFloat(value).toLocaleString('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    };
    
    const calculateInstallment = () => {
      if (application.value) {
        return formatCurrency(parseFloat(application.value.amount_requested) / application.value.term_months);
      }
      return '-';
    };
    
    const calculateIncomeRatio = () => {
      if (application.value && client.value) {
        const installment = parseFloat(application.value.amount_requested) / application.value.term_months;
        const ratio = (installment / parseFloat(client.value.monthly_income)) * 100;
        return ratio.toFixed(2);
      }
      return '-';
    };
    
    const getDocumentTypeLabel = (type) => {
      const labels = {
        'income': 'Comprovante de Renda',
        'bank_statement': 'Extrato Bancário',
        'tax_return': 'Declaração de IR',
        'other': 'Outro'
      };
      return labels[type] || type;
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
    
    const getRecommendationClass = () => {
      if (!aiPrediction.value) return '';
      
      const rec = aiPrediction.value.recommendation.toLowerCase();
      if (rec.includes('aprovado com condições')) return 'warning';
      if (rec.includes('aprovado')) return 'success';
      if (rec.includes('reprovado')) return 'danger';
      if (rec.includes('análise manual')) return 'info';
      
      return '';
    };
    
    onMounted(() => {
      fetchAnalysis();
    });
    
    return {
      analysis,
      application,
      client,
      documents,
      aiPrediction,
      formatDate,
      formatCurrency,
      calculateInstallment,
      calculateIncomeRatio,
      getDocumentTypeLabel,
      getDecisionLabel,
      getRecommendationClass,
      saveAnalysis,
      finishProcess,
      generateAIPrediction,
      navigateToClientDocs
    };
  }
}
</script>

<style scoped>
.analysis-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
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
}

.info-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.info-card h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
  font-size: 18px;
  font-weight: 600;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
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
  color: #333;
}

.status-badge {
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 14px;
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

form .form-group {
  margin-bottom: 20px;
}

form label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

form select, form textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

form textarea {
  resize: vertical;
  min-height: 120px;
}

.form-actions {
  display: flex;
  gap: 10px;
}

.button {
  display: inline-block;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  background-color: #eee;
  color: #333;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.button.primary {
  background-color: #2196F3;
  color: white;
}

.button.success {
  background-color: #4CAF50;
  color: white;
}

.button.small {
  padding: 6px 12px;
  font-size: 12px;
}

.button:hover {
  opacity: 0.9;
}

table {
  width: 100%;
  border-collapse: collapse;
}

table th, table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.empty-state {
  text-align: center;
  padding: 20px;
  color: #777;
}
</style>