<template>
    <div class="application-form">
      <div class="page-header">
        <h1>Nova Solicitação de Crédito</h1>
      </div>
      
      <form @submit.prevent="saveApplication">
        <!-- Seleção de Cliente -->
        <div class="form-section">
          <h2>Cliente</h2>
          
          <div v-if="!selectedClientId">
            <div class="search-box">
              <input 
                type="text" 
                v-model="clientSearch" 
                placeholder="Buscar cliente por nome ou CPF..." 
                @input="searchClients"
              />
              <button type="button" class="btn-search">Buscar</button>
            </div>
            
            <div v-if="clients.length > 0" class="client-results">
              <table>
                <thead>
                  <tr>
                    <th>Nome</th>
                    <th>CPF</th>
                    <th>Telefone</th>
                    <th>Email</th>
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="client in clients" :key="client.id">
                    <td>{{ client.name }}</td>
                    <td>{{ client.cpf }}</td>
                    <td>{{ client.phone }}</td>
                    <td>{{ client.email }}</td>
                    <td>
                      <button 
                        type="button" 
                        @click="selectClient(client)" 
                        class="btn-select"
                      >
                        Selecionar
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <div v-else-if="clientSearch" class="empty-state">
              <p>Nenhum cliente encontrado com esses critérios.</p>
              <router-link to="/clients/new" class="btn-create">Cadastrar Novo Cliente</router-link>
            </div>
          </div>
          
          <div v-else class="selected-client">
            <div class="client-info">
              <div class="info-row">
                <span class="label">Nome:</span>
                <span class="value">{{ selectedClient.name }}</span>
              </div>
              <div class="info-row">
                <span class="label">CPF:</span>
                <span class="value">{{ selectedClient.cpf }}</span>
              </div>
              <div class="info-row">
                <span class="label">Telefone:</span>
                <span class="value">{{ selectedClient.phone }}</span>
              </div>
              <div class="info-row">
                <span class="label">Email:</span>
                <span class="value">{{ selectedClient.email }}</span>
              </div>
              <div class="info-row">
                <span class="label">Renda Mensal:</span>
                <span class="value">R$ {{ formatCurrency(selectedClient.monthly_income) }}</span>
              </div>
            </div>
            <button type="button" @click="clearSelectedClient" class="btn-change">
              Trocar Cliente
            </button>
          </div>
        </div>
        
        <!-- Detalhes da Solicitação -->
        <div v-if="selectedClientId" class="form-section">
          <h2>Detalhes da Solicitação</h2>
          
          <div class="form-row">
            <div class="form-group">
              <label for="amount">Valor Solicitado (R$) *</label>
              <input 
                type="number" 
                id="amount" 
                v-model="application.amount_requested" 
                min="500" 
                step="100" 
                required
              />
            </div>
            
            <div class="form-group">
              <label for="term">Prazo (meses) *</label>
              <select 
                id="term" 
                v-model="application.term_months" 
                required
              >
                <option value="">Selecione...</option>
                <option value="6">6 meses</option>
                <option value="12">12 meses</option>
                <option value="18">18 meses</option>
                <option value="24">24 meses</option>
                <option value="36">36 meses</option>
                <option value="48">48 meses</option>
                <option value="60">60 meses</option>
              </select>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="purpose">Finalidade *</label>
              <select 
                id="purpose" 
                v-model="application.purpose" 
                required
              >
                <option value="">Selecione...</option>
                <option value="Automóvel">Compra de Automóvel</option>
                <option value="Imóvel">Compra de Imóvel</option>
                <option value="Reforma">Reforma Residencial</option>
                <option value="Educação">Educação</option>
                <option value="Negócio">Investimento em Negócio</option>
                <option value="Dívidas">Pagamento de Dívidas</option>
                <option value="Outro">Outro</option>
              </select>
            </div>
          </div>
          
          <div v-if="application.purpose === 'Outro'" class="form-row">
            <div class="form-group">
              <label for="other_purpose">Descreva a Finalidade *</label>
              <textarea 
                id="other_purpose" 
                v-model="application.purpose_description" 
                rows="3" 
                required
              ></textarea>
            </div>
          </div>
          
          <div class="simulation-box" v-if="canShowSimulation">
            <h3>Simulação</h3>
            <div class="simulation-details">
              <div class="sim-row">
                <span class="sim-label">Valor Solicitado:</span>
                <span class="sim-value">R$ {{ formatCurrency(application.amount_requested) }}</span>
              </div>
              <div class="sim-row">
                <span class="sim-label">Prazo:</span>
                <span class="sim-value">{{ application.term_months }} meses</span>
              </div>
              <div class="sim-row">
                <span class="sim-label">Taxa de Juros (estimada):</span>
                <span class="sim-value">{{ estimatedRate }}% ao mês</span>
              </div>
              <div class="sim-row highlight">
                <span class="sim-label">Valor da Parcela (estimado):</span>
                <span class="sim-value">R$ {{ calculateInstallment() }}</span>
              </div>
              <div class="sim-row">
                <span class="sim-label">Comprometimento de Renda:</span>
                <span class="sim-value" :class="incomeRatioClass">{{ calculateIncomeRatio() }}%</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Botões de Ação -->
        <div v-if="selectedClientId" class="form-actions">
          <button type="button" @click="cancel" class="btn-cancel">Cancelar</button>
          <button type="submit" class="btn-save" :disabled="!isFormValid">Enviar Solicitação</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  import { ref, reactive, computed, onMounted } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  
  export default {
    name: 'ApplicationForm',
    setup() {
      const route = useRoute();
      const router = useRouter();
      
      const clientSearch = ref('');
      const clients = ref([]);
      const selectedClientId = ref(null);
      const selectedClient = ref({});
      
      const application = reactive({
        amount_requested: '',
        term_months: '',
        purpose: '',
        purpose_description: ''
      });
      
      // Verificar se há um cliente pré-selecionado na URL
      const checkQueryParams = () => {
        const clientId = route.query.client;
        if (clientId) {
          fetchClient(clientId);
        }
      };
      
      // Buscar cliente específico
      const fetchClient = async (id) => {
        try {
          // Em uma aplicação real, você buscaria do backend
          // Dados estáticos para exemplo
          selectedClient.value = {
            id: parseInt(id),
            name: 'João Silva',
            cpf: '123.456.789-00',
            phone: '(11) 98765-4321',
            email: 'joao.silva@email.com',
            monthly_income: 5000
          };
          selectedClientId.value = parseInt(id);
        } catch (error) {
          console.error('Erro ao buscar cliente:', error);
        }
      };
      
      // Buscar clientes com base na pesquisa
      const searchClients = async () => {
        if (clientSearch.value.length < 3) {
          clients.value = [];
          return;
        }
        
        try {
          // Em uma aplicação real, você buscaria do backend
          // Dados estáticos para exemplo
          clients.value = [
            {
              id: 1,
              name: 'João Silva',
              cpf: '123.456.789-00',
              phone: '(11) 98765-4321',
              email: 'joao.silva@email.com',
              monthly_income: 5000
            },
            {
              id: 2,
              name: 'Maria Souza',
              cpf: '987.654.321-00',
              phone: '(11) 91234-5678',
              email: 'maria.souza@email.com',
              monthly_income: 6500
            }
          ];
        } catch (error) {
          console.error('Erro ao buscar clientes:', error);
        }
      };
      
      // Selecionar cliente
      const selectClient = (client) => {
        selectedClient.value = client;
        selectedClientId.value = client.id;
        clientSearch.value = '';
        clients.value = [];
      };
      
      // Limpar cliente selecionado
      const clearSelectedClient = () => {
        selectedClient.value = {};
        selectedClientId.value = null;
        application.amount_requested = '';
        application.term_months = '';
        application.purpose = '';
        application.purpose_description = '';
      };
      
      // Taxa de juros estimada baseada no prazo
      const estimatedRate = computed(() => {
        if (!application.term_months) return '-';
        
        const term = parseInt(application.term_months);
        if (term <= 12) return 1.5;
        if (term <= 24) return 1.8;
        if (term <= 36) return 2.0;
        return 2.2;
      });
      
      // Cálculo do valor da parcela
      const calculateInstallment = () => {
        if (application.amount_requested && application.term_months && estimatedRate.value !== '-') {
          const principal = parseFloat(application.amount_requested);
          const months = parseInt(application.term_months);
          const rate = parseFloat(estimatedRate.value) / 100;
          
          // Cálculo com juros compostos
          const installment = (principal * rate * Math.pow(1 + rate, months)) / (Math.pow(1 + rate, months) - 1);
          return formatCurrency(installment);
        }
        return '-';
      };
      
      // Cálculo do comprometimento de renda
      const calculateIncomeRatio = () => {
        if (application.amount_requested && application.term_months && selectedClient.value.monthly_income) {
          const principal = parseFloat(application.amount_requested);
          const months = parseInt(application.term_months);
          const rate = parseFloat(estimatedRate.value) / 100;
          
          // Cálculo com juros compostos
          const installment = (principal * rate * Math.pow(1 + rate, months)) / (Math.pow(1 + rate, months) - 1);
          const ratio = (installment / parseFloat(selectedClient.value.monthly_income)) * 100;
          return ratio.toFixed(1);
        }
        return '-';
      };
      
      // Classe CSS baseada no comprometimento de renda
      const incomeRatioClass = computed(() => {
        const ratio = calculateIncomeRatio();
        if (ratio === '-') return '';
        
        const ratioNum = parseFloat(ratio);
        if (ratioNum <= 20) return 'ratio-good';
        if (ratioNum <= 30) return 'ratio-moderate';
        return 'ratio-high';
      });
      
      // Verificar se pode mostrar simulação
      const canShowSimulation = computed(() => {
        return application.amount_requested && application.term_months;
      });
      
      // Verificar se o formulário é válido
      const isFormValid = computed(() => {
        if (!selectedClientId.value) return false;
        if (!application.amount_requested || !application.term_months || !application.purpose) return false;
        if (application.purpose === 'Outro' && !application.purpose_description) return false;
        return true;
      });
      
      // Salvar solicitação
      const saveApplication = async () => {
        try {
          // Em uma aplicação real, você enviaria para o backend
          const applicationData = {
            client_id: selectedClientId.value,
            amount_requested: parseFloat(application.amount_requested),
            term_months: parseInt(application.term_months),
            purpose: application.purpose === 'Outro' ? application.purpose_description : application.purpose,
            status: 'pending'
          };
          
          console.log('Salvando solicitação:', applicationData);
          
          // Simular sucesso
          alert('Solicitação enviada com sucesso!');
          router.push('/applications');
        } catch (error) {
          console.error('Erro ao salvar solicitação:', error);
        }
      };
      
      // Cancelar e voltar
      const cancel = () => {
        router.push('/applications');
      };
      
      // Formatação de valores monetários
      const formatCurrency = (value) => {
        return parseFloat(value).toLocaleString('pt-BR', {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2
        });
      };
      
      onMounted(() => {
        checkQueryParams();
      });
      
      return {
        clientSearch,
        clients,
        selectedClientId,
        selectedClient,
        application,
        estimatedRate,
        incomeRatioClass,
        canShowSimulation,
        isFormValid,
        searchClients,
        selectClient,
        clearSelectedClient,
        calculateInstallment,
        calculateIncomeRatio,
        saveApplication,
        cancel,
        formatCurrency
      };
    }
  }
  </script>
  
  <style scoped>
  .application-form {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .page-header {
    margin-bottom: 30px;
  }
  
  .form-section {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-bottom: 20px;
  }
  
  .form-section h2 {
    margin-top: 0;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
    font-size: 18px;
  }
  
  .search-box {
    display: flex;
    margin-bottom: 20px;
  }
  
  .search-box input {
    flex: 1;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px 0 0 4px;
  }
  
  .btn-search {
    background-color: #2196F3;
    color: white;
    border: none;
    padding: 0 20px;
    border-radius: 0 4px 4px 0;
    cursor: pointer;
  }
  
  .client-results {
    margin-bottom: 20px;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th, td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #eee;
  }
  
  th {
    background-color: #f5f5f5;
    font-weight: 500;
  }
  
  .btn-select {
    background-color: #2196F3;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .empty-state {
    text-align: center;
    padding: 20px;
  }
  
  .btn-create {
    display: inline-block;
    background-color: #4CAF50;
    color: white;
    padding: 8px 16px;
    border-radius: 4px;
    margin-top: 10px;
    text-decoration: none;
  }
  
  .selected-client {
    display: flex;
    justify-content: space-between;
    background-color: #f5f5f5;
    padding: 15px;
    border-radius: 4px;
  }
  
  .client-info {
    flex: 1;
  }
  
  .info-row {
    display: flex;
    margin-bottom: 8px;
  }
  
  .label {
    flex: 1;
    color: #666;
    font-weight: 500;
  }
  
  .value {
    flex: 2;
  }
  
  .btn-change {
    align-self: center;
    background-color: #f5f5f5;
    color: #2196F3;
    border: 1px solid #2196F3;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .form-row {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    margin-bottom: 15px;
  }
  
  .form-group {
    flex: 1;
    min-width: 200px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
    color: #333;
  }
  
  input, select, textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
  }
  
  textarea {
    resize: vertical;
  }
  
  .simulation-box {
    background-color: #f5f5f5;
    border-radius: 4px;
    padding: 15px;
    margin-top: 20px;
  }
  
  .simulation-box h3 {
    margin-top: 0;
    font-size: 16px;
    margin-bottom: 15px;
  }
  
  .sim-row {
    display: flex;
    margin-bottom: 10px;
    padding: 8px;
    border-bottom: 1px solid #eee;
  }
  
  .sim-row:last-child {
    border-bottom: none;
  }
  
  .sim-label {
    flex: 1;
    color: #666;
    font-weight: 500;
  }
  
  .sim-value {
    text-align: right;
    font-weight: 600;
  }
  
  .sim-row.highlight {
    background-color: #E3F2FD;
    border-radius: 4px;
  }
  
  .ratio-good {
    color: #388E3C;
  }
  
  .ratio-moderate {
    color: #FFA000;
  }
  
  .ratio-high {
    color: #F44336;
  }
  
  .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
  }
  
  .btn-cancel, .btn-save {
    padding: 10px 20px;
    border-radius: 4px;
    font-size: 16px;
    cursor: pointer;
    border: none;
  }
  
  .btn-cancel {
    background-color: #f5f5f5;
    color: #333;
  }
  
  .btn-save {
    background-color: #2196F3;
    color: white;
  }
  
  .btn-save:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  </style>