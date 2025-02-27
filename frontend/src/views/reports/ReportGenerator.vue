<template>
    <div class="report-generator">
      <div class="page-header">
        <h1>Gerador de Relatórios</h1>
        <button @click="generateReport" class="btn-primary">Gerar Relatório</button>
      </div>
      
      <div class="report-form">
        <div class="form-section">
          <h2>Parâmetros do Relatório</h2>
          
          <div class="form-row">
            <div class="form-group">
              <label for="report_type">Tipo de Relatório</label>
              <select v-model="reportParams.report_type" id="report_type" required>
                <option value="">Selecione um tipo...</option>
                <option value="monthly">Relatório Mensal</option>
                <option value="client">Relatório de Cliente</option>
                <option value="performance">Desempenho de Analistas</option>
                <option value="risk">Análise de Risco</option>
                <option value="custom">Relatório Personalizado</option>
              </select>
            </div>
          </div>
          
          <!-- Parâmetros específicos para cada tipo de relatório -->
          <div v-if="reportParams.report_type === 'monthly'" class="form-row">
            <div class="form-group">
              <label for="month">Mês de Referência</label>
              <input type="month" v-model="reportParams.month" id="month" required>
            </div>
          </div>
          
          <div v-if="reportParams.report_type === 'client'" class="form-row">
            <div class="form-group">
              <label for="client_id">Cliente</label>
              <select v-model="reportParams.client_id" id="client_id" required>
                <option value="">Selecione um cliente...</option>
                <option v-for="client in clients" :key="client.id" :value="client.id">
                  {{ client.name }}
                </option>
              </select>
            </div>
          </div>
          
          <div v-if="reportParams.report_type === 'performance'" class="form-row">
            <div class="form-group">
              <label for="start_date">Data Inicial</label>
              <input type="date" v-model="reportParams.start_date" id="start_date" required>
            </div>
            
            <div class="form-group">
              <label for="end_date">Data Final</label>
              <input type="date" v-model="reportParams.end_date" id="end_date" required>
            </div>
            
            <div class="form-group">
              <label for="analyst_id">Analista</label>
              <select v-model="reportParams.analyst_id" id="analyst_id">
                <option value="">Todos os Analistas</option>
                <option v-for="analyst in analysts" :key="analyst.id" :value="analyst.id">
                  {{ analyst.name }}
                </option>
              </select>
            </div>
          </div>
          
          <div v-if="reportParams.report_type === 'risk'" class="form-row">
            <div class="form-group">
              <label for="risk_threshold">Limite de Risco</label>
              <input 
                type="number" 
                v-model="reportParams.risk_threshold" 
                id="risk_threshold" 
                min="0" 
                max="100" 
                step="1"
              >
              <small>Solicitações com score de risco acima deste valor</small>
            </div>
            
            <div class="form-group">
              <label for="period">Período</label>
              <select v-model="reportParams.period" id="period">
                <option value="7d">Últimos 7 dias</option>
                <option value="30d">Últimos 30 dias</option>
                <option value="90d">Últimos 90 dias</option>
                <option value="year">Este ano</option>
                <option value="all">Todo período</option>
              </select>
            </div>
          </div>
          
          <div v-if="reportParams.report_type === 'custom'" class="form-row">
            <div class="form-group">
              <label for="report_title">Título do Relatório</label>
              <input type="text" v-model="reportParams.report_title" id="report_title" required>
            </div>
            
            <div class="form-group">
              <label for="include_sections">Seções a Incluir</label>
              <div class="checkbox-group">
                <div class="checkbox-item">
                  <input 
                    type="checkbox" 
                    id="section_summary" 
                    v-model="reportParams.sections.summary"
                  >
                  <label for="section_summary">Resumo Executivo</label>
                </div>
                <div class="checkbox-item">
                  <input 
                    type="checkbox" 
                    id="section_applications" 
                    v-model="reportParams.sections.applications"
                  >
                  <label for="section_applications">Solicitações</label>
                </div>
                <div class="checkbox-item">
                  <input 
                    type="checkbox" 
                    id="section_clients" 
                    v-model="reportParams.sections.clients"
                  >
                  <label for="section_clients">Clientes</label>
                </div>
                <div class="checkbox-item">
                  <input 
                    type="checkbox" 
                    id="section_risk" 
                    v-model="reportParams.sections.risk"
                  >
                  <label for="section_risk">Análise de Risco</label>
                </div>
                <div class="checkbox-item">
                  <input 
                    type="checkbox" 
                    id="section_analysts" 
                    v-model="reportParams.sections.analysts"
                  >
                  <label for="section_analysts">Desempenho de Analistas</label>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Opções de formato para todos os relatórios -->
          <div class="form-row">
            <div class="form-group">
              <label for="format">Formato do Relatório</label>
              <select v-model="reportParams.format" id="format" required>
                <option value="pdf">PDF</option>
                <option value="excel">Excel</option>
                <option value="csv">CSV</option>
              </select>
            </div>
          </div>
        </div>
        
        <!-- Prévia do relatório (mockup) -->
        <div v-if="showPreview" class="preview-section">
          <h2>Prévia do Relatório</h2>
          <div class="report-preview">
            <div class="report-header">
              <h3>{{ getReportTitle() }}</h3>
              <div class="report-meta">
                <span>Gerado em: {{ formatDate(new Date()) }}</span>
                <span>Por: {{ currentUser.name }}</span>
              </div>
            </div>
            
            <div class="report-body">
              <!-- Exemplo de conteúdo para prévia -->
              <div v-if="reportParams.report_type === 'monthly'" class="report-section">
                <h4>Resumo do Mês</h4>
                <div class="stat-row">
                  <div class="stat-card">
                    <div class="stat-title">Total de Solicitações</div>
                    <div class="stat-value">35</div>
                  </div>
                  <div class="stat-card">
                    <div class="stat-title">Aprovadas</div>
                    <div class="stat-value">22 (63%)</div>
                  </div>
                  <div class="stat-card">
                    <div class="stat-title">Rejeitadas</div>
                    <div class="stat-value">13 (37%)</div>
                  </div>
                  <div class="stat-card">
                    <div class="stat-title">Valor Total Aprovado</div>
                    <div class="stat-value">R$ 325.500,00</div>
                  </div>
                </div>
                
                <div class="chart-placeholder">
                  [Gráfico: Distribuição de Solicitações por Status]
                </div>
                
                <div class="chart-placeholder">
                  [Gráfico: Volume de Solicitações por Dia]
                </div>
                
                <table class="preview-table">
                  <thead>
                    <tr>
                      <th>Métrica</th>
                      <th>Valor</th>
                      <th>vs. Mês Anterior</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Ticket Médio</td>
                      <td>R$ 14.795,45</td>
                      <td class="trend-up">+5.4%</td>
                    </tr>
                    <tr>
                      <td>Taxa de Aprovação</td>
                      <td>63%</td>
                      <td class="trend-up">+2.1%</td>
                    </tr>
                    <tr>
                      <td>Score de Risco Médio</td>
                      <td>42.3</td>
                      <td class="trend-down">-3.5%</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              
              <div v-if="reportParams.report_type === 'client'" class="report-section">
                <h4>Perfil do Cliente</h4>
                <div class="client-profile">
                  <div class="profile-header">
                    <div class="client-name">João Silva</div>
                    <div class="client-id">CPF: 123.456.789-00</div>
                  </div>
                  <div class="profile-details">
                    <div class="detail-row">
                      <span class="detail-label">Profissão:</span>
                      <span class="detail-value">Engenheiro</span>
                    </div>
                    <div class="detail-row">
                      <span class="detail-label">Renda Mensal:</span>
                      <span class="detail-value">R$ 5.000,00</span>
                    </div>
                    <div class="detail-row">
                      <span class="detail-label">Score de Crédito:</span>
                      <span class="detail-value score-value">825</span>
                    </div>
                  </div>
                </div>
                
                <h4>Histórico de Solicitações</h4>
                <table class="preview-table">
                  <thead>
                    <tr>
                      <th>Data</th>
                      <th>Valor</th>
                      <th>Finalidade</th>
                      <th>Status</th>
                      <th>Score de Risco</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>15/01/2025</td>
                      <td>R$ 8.000,00</td>
                      <td>Compra de automóvel</td>
                      <td><span class="status-approved">Aprovado</span></td>
                      <td>22.5</td>
                    </tr>
                    <tr>
                      <td>20/02/2025</td>
                      <td>R$ 3.000,00</td>
                      <td>Reforma residencial</td>
                      <td><span class="status-pending">Pendente</span></td>
                      <td>N/A</td>
                    </tr>
                  </tbody>
                </table>
                
                <div class="chart-placeholder">
                  [Gráfico: Histórico de Score de Risco]
                </div>
              </div>
              
              <!-- Outros tipos de relatório teriam previsualizações similares -->
            </div>
            
            <div class="report-footer">
              <div class="page-number">Página 1 de 5</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, computed } from 'vue';
  
  export default {
    name: 'ReportGenerator',
    setup() {
      const reportParams = reactive({
        report_type: '',
        month: '',
        client_id: '',
        start_date: '',
        end_date: '',
        analyst_id: '',
        risk_threshold: 60,
        period: '30d',
        report_title: '',
        format: 'pdf',
        sections: {
          summary: true,
          applications: true,
          clients: false,
          risk: true,
          analysts: false
        }
      });
      
      const showPreview = ref(false);
      
      // Dados mockados para o componente
      const clients = ref([
        { id: 1, name: 'João Silva' },
        { id: 2, name: 'Maria Souza' },
        { id: 3, name: 'Tech Solutions Ltda' },
        { id: 4, name: 'Comércio Verde Ltda' }
      ]);
      
      const analysts = ref([
        { id: 1, name: 'Ana Ferreira' },
        { id: 2, name: 'Carlos Gomes' },
        { id: 3, name: 'Pedro Santos' }
      ]);
      
      const currentUser = ref({
        id: 2,
        name: 'Carlos Gomes',
        role: 'manager'
      });
      
      // Detectar se tem parâmetros suficientes para mostrar prévia
      const canShowPreview = computed(() => {
        if (!reportParams.report_type) return false;
        
        switch (reportParams.report_type) {
          case 'monthly':
            return !!reportParams.month;
          case 'client':
            return !!reportParams.client_id;
          case 'performance':
            return !!reportParams.start_date && !!reportParams.end_date;
          default:
            return true;
        }
      });
      
      // Gerar título do relatório baseado nos parâmetros
      const getReportTitle = () => {
        switch (reportParams.report_type) {
          case 'monthly':
            return `Relatório Mensal - ${formatMonth(reportParams.month)}`;
          case 'client':
            const client = clients.value.find(c => c.id === parseInt(reportParams.client_id));
            return `Relatório de Cliente - ${client ? client.name : ''}`;
          case 'performance':
            return 'Relatório de Desempenho de Analistas';
          case 'risk':
            return 'Relatório de Análise de Risco';
          case 'custom':
            return reportParams.report_title || 'Relatório Personalizado';
          default:
            return 'Novo Relatório';
        }
      };
      
      // Formatar mês para exibição
      const formatMonth = (monthStr) => {
        if (!monthStr) return '';
        
        const [year, month] = monthStr.split('-');
        const date = new Date(parseInt(year), parseInt(month) - 1, 1);
        
        return date.toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' });
      };
      
      // Formatar data para exibição
      const formatDate = (date) => {
        return date.toLocaleDateString('pt-BR', { 
          day: '2-digit', 
          month: '2-digit', 
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
      };
      
      // Gerar relatório (mostrar prévia no contexto do MVP)
      const generateReport = () => {
        // Validar parâmetros
        if (!reportParams.report_type) {
          alert('Por favor, selecione um tipo de relatório.');
          return;
        }
        
        // Verificar parâmetros específicos de cada tipo
        if (reportParams.report_type === 'monthly' && !reportParams.month) {
          alert('Por favor, selecione o mês de referência.');
          return;
        }
        
        if (reportParams.report_type === 'client' && !reportParams.client_id) {
          alert('Por favor, selecione um cliente.');
          return;
        }
        
        if (reportParams.report_type === 'performance' && (!reportParams.start_date || !reportParams.end_date)) {
          alert('Por favor, defina o período para o relatório.');
          return;
        }
        
        // Em uma aplicação real, aqui chamaríamos a API para gerar o relatório
        // Para o MVP, vamos apenas mostrar a prévia
        showPreview.value = true;
        
        // Scroll suave para a prévia
        setTimeout(() => {
          const previewElement = document.querySelector('.preview-section');
          if (previewElement) {
            previewElement.scrollIntoView({ behavior: 'smooth' });
          }
        }, 100);
        
        // Simulando um relatório real que seria baixado
        if (reportParams.format === 'pdf') {
          setTimeout(() => {
            alert('Em uma versão completa, o relatório em PDF seria gerado e baixado automaticamente.');
          }, 2000);
        }
      };
      
      return {
        reportParams,
        showPreview,
        clients,
        analysts,
        currentUser,
        canShowPreview,
        getReportTitle,
        formatDate,
        formatMonth,
        generateReport
      };
    }
  }
  </script>
  
  <style scoped>
  .report-generator {
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
  
  .form-section {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-bottom: 30px;
  }
  
  .form-section h2 {
    margin-top: 0;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
    font-size: 18px;
  }
  
  .form-row {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin-bottom: 20px;
  }
  
  .form-group {
    flex: 1;
    min-width: 250px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
    color: #333;
  }
  
  input, select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
  }
  
  small {
    display: block;
    margin-top: 5px;
    color: #666;
    font-size: 12px;
  }
  
  .checkbox-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 5px;
  }
  
  .checkbox-item {
    display: flex;
    align-items: center;
    min-width: 200px;
  }
  
  .checkbox-item input {
    width: auto;
    margin-right: 8px;
  }
  
  .checkbox-item label {
    margin: 0;
    font-weight: normal;
  }
  
  .btn-primary {
    background-color: #2196F3;
    color: white;
    padding: 10px 20px;
    border-radius: 4px;
    border: none;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
  }
  
  .btn-primary:hover {
    background-color: #1976D2;
  }
  
  /* Seção de prévia */
  .preview-section {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-top: 30px;
  }
  
  .preview-section h2 {
    margin-top: 0;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
    font-size: 18px;
  }
  
  .report-preview {
    background-color: #fefefe;
    border: 1px solid #eee;
    border-radius: 4px;
    padding: 20px;
  }
  
  .report-header {
    text-align: center;
    margin-bottom: 20px;
    padding-bottom: 20px;
    border-bottom: 1px solid #ddd;
  }
  
  .report-header h3 {
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 22px;
    color: #333;
  }
  
  .report-meta {
    display: flex;
    justify-content: space-between;
    color: #666;
    font-size: 14px;
  }
  
  .report-section {
    margin-bottom: 30px;
  }
  
  .report-section h4 {
    font-size: 18px;
    margin-bottom: 15px;
    color: #444;
  }
  
  .stat-row {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin-bottom: 20px;
  }
  
  .stat-card {
    flex: 1;
    min-width: 200px;
    background-color: #f5f5f5;
    border-radius: 4px;
    padding: 15px;
    text-align: center;
  }
  
  .stat-title {
    font-size: 14px;
    color: #666;
    margin-bottom: 5px;
  }
  
  .stat-value {
    font-size: 20px;
    font-weight: 600;
    color: #333;
  }
  
  .chart-placeholder {
    background-color: #f5f5f5;
    border: 1px dashed #ccc;
    border-radius: 4px;
    padding: 30px;
    text-align: center;
    color: #666;
    margin-bottom: 20px;
  }
  
  .preview-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }
  
  .preview-table th,
  .preview-table td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #eee;
  }
  
  .preview-table th {
    background-color: #f5f5f5;
    font-weight: 500;
    color: #333;
  }
  
  .trend-up {
    color: #4CAF50;
  }
  
  .trend-down {
    color: #F44336;
  }
  
  .client-profile {
    background-color: #f9f9f9;
    border-radius: 4px;
    padding: 15px;
    margin-bottom: 20px;
  }
  
  .profile-header {
    margin-bottom: 15px;
  }
  
  .client-name {
    font-size: 18px;
    font-weight: 600;
  }
  
  .client-id {
    color: #666;
    font-size: 14px;
  }
  
  .profile-details {
    display: flex;
    flex-wrap: wrap;
  }
  
  .detail-row {
    flex: 1;
    min-width: 200px;
    margin-bottom: 10px;
  }
  
  .detail-label {
    color: #666;
    margin-right: 5px;
  }
  
  .detail-value {
    font-weight: 500;
  }
  
  .score-value {
    color: #4CAF50;
    font-weight: 600;
  }
  
  .status-approved {
    display: inline-block;
    padding: 3px 6px;
    background-color: #E8F5E9;
    color: #388E3C;
    border-radius: 3px;
    font-size: 12px;
  }
  
  .status-pending {
    display: inline-block;
    padding: 3px 6px;
    background-color: #FFF8E1;
    color: #FFA000;
    border-radius: 3px;
    font-size: 12px;
  }
  
  .report-footer {
    text-align: center;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #ddd;
    color: #666;
    font-size: 14px;
  }
  </style>