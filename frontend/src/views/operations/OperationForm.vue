<template>
  <div class="operation-form">
    <div class="page-header">
      <h1>Simulação de Operação de Crédito</h1>
    </div>
    
    <form @submit.prevent="nextStep">
      <!-- Etapa 1: Dados do Cliente -->
      <div v-if="currentStep === 1" class="form-section client-section">
        <h2>Dados do Cliente</h2>
        
        <div class="form-row">
          <div class="form-group">
            <label for="document">CPF / CNPJ *</label>
            <input 
              type="text" 
              id="document" 
              v-model="formData.document"
              @blur="searchClient"
              required
            />
            <small>Digite apenas números</small>
          </div>
          
          <div class="form-group">
            <label for="client_type">Tipo de Cliente *</label>
            <select id="client_type" v-model="formData.client_type" required>
              <option value="PF">Pessoa Física</option>
              <option value="PJ">Pessoa Jurídica</option>
            </select>
          </div>
        </div>
        
        <div v-if="clientFound" class="alert alert-success">
          <i class="fas fa-check-circle"></i> Cliente encontrado! Alguns campos foram preenchidos automaticamente.
        </div>
        
        <div v-if="clients.length > 0" class="client-results">
          <h3>Clientes Encontrados</h3>
          <table>
            <thead>
              <tr>
                <th>Nome</th>
                <th>CPF/CNPJ</th>
                <th>Telefone</th>
                <th>Email</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="client in clients" :key="client.id">
                <td>{{ client.name }}</td>
                <td>{{ client.cpf || client.cnpj }}</td>
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
        
        <div class="form-row">
          <div class="form-group">
            <label for="name">Nome / Razão Social *</label>
            <input type="text" id="name" v-model="formData.name" required />
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="contact_phone">Celular / WhatsApp *</label>
            <input type="text" id="contact_phone" v-model="formData.contact_phone" required />
          </div>
          
          <div class="form-group">
            <label for="email">E-mail do Cliente / Sócio Administrador *</label>
            <input type="email" id="email" v-model="formData.email" required />
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="marital_status">Estado Civil</label>
            <select id="marital_status" v-model="formData.marital_status">
              <option value="">Selecione...</option>
              <option value="single">Solteiro(a)</option>
              <option value="married">Casado(a)</option>
              <option value="divorced">Divorciado(a)</option>
              <option value="widowed">Viúvo(a)</option>
              <option value="stable_union">União Estável</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="zipcode">CEP *</label>
            <input 
              type="text" 
              id="zipcode" 
              v-model="formData.zipcode"
              @blur="searchZipcode"
              required
            />
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="street">Logradouro</label>
            <input type="text" id="street" v-model="formData.street" readonly />
          </div>
          
          <div class="form-group" style="flex: 0 0 150px;">
            <label for="number">Número *</label>
            <input type="text" id="number" v-model="formData.number" required />
          </div>
          
          <div class="form-group">
            <label for="complement">Complemento</label>
            <input type="text" id="complement" v-model="formData.complement" />
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="neighborhood">Bairro</label>
            <input type="text" id="neighborhood" v-model="formData.neighborhood" readonly />
          </div>
          
          <div class="form-group">
            <label for="city">Cidade</label>
            <input type="text" id="city" v-model="formData.city" readonly />
          </div>
          
          <div class="form-group" style="flex: 0 0 100px;">
            <label for="state">Estado</label>
            <input type="text" id="state" v-model="formData.state" readonly />
          </div>
        </div>
      </div>
      
      <!-- Etapa 2: Dados do Crédito -->
      <div v-if="currentStep === 2" class="form-section credit-section">
        <h2>Informações do Crédito Pleiteado</h2>
        
        <div class="form-row">
          <div class="form-group">
            <label for="amount">Valor do Crédito (R$) *</label>
            <input 
              type="number" 
              id="amount" 
              v-model="formData.amount" 
              min="1000"
              step="100"
              @input="calculatePayment"
              required
            />
          </div>
          
          <div class="form-group">
            <label for="modality">Modalidade do Crédito *</label>
            <select id="modality" v-model="formData.modality" required>
              <option value="">Selecione...</option>
              <option value="capital_giro">Capital de Giro</option>
              <option value="financiamento">Financiamento</option>
              <option value="credito_pessoal">Crédito Pessoal</option>
              <option value="credito_imobiliario">Crédito Imobiliário</option>
              <option value="consignado">Empréstimo Consignado</option>
            </select>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="term">Prazo de Amortização (meses) *</label>
            <input 
              type="number" 
              id="term" 
              v-model="formData.term_months" 
              min="1"
              max="120"
              @input="calculatePayment"
              required
            />
          </div>
          
          <div class="form-group">
            <label for="payment_frequency">Periodicidade das Parcelas *</label>
            <select id="payment_frequency" v-model="formData.payment_frequency" @change="calculatePayment" required>
              <option value="monthly">Mensal</option>
              <option value="quarterly">Trimestral</option>
              <option value="semiannually">Semestral</option>
              <option value="annually">Anual</option>
            </select>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="interest_rate">Taxa de Juros *</label>
            <input 
              type="number" 
              id="interest_rate" 
              v-model="formData.interest_rate" 
              min="0.01"
              step="0.01"
              @input="calculatePayment"
              required
            />
          </div>
          
          <div class="form-group">
            <label for="interest_frequency">Periodicidade da Taxa *</label>
            <select id="interest_frequency" v-model="formData.interest_frequency" @change="calculatePayment" required>
              <option value="monthly">Mensal</option>
              <option value="annually">Anual</option>
            </select>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="grace_period">Carência (meses)</label>
            <input 
              type="number" 
              id="grace_period" 
              v-model="formData.grace_period" 
              min="0"
              @input="calculatePayment"
            />
          </div>
          
          <div class="form-group">
            <label for="grace_frequency">Periodicidade da Carência</label>
            <select id="grace_frequency" v-model="formData.grace_frequency" @change="calculatePayment">
              <option value="monthly">Mensal</option>
              <option value="quarterly">Trimestral</option>
              <option value="semiannually">Semestral</option>
            </select>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="amortization_system">Sistema de Amortização *</label>
            <select id="amortization_system" v-model="formData.amortization_system" @change="calculatePayment" required>
              <option value="price">PRICE (Parcelas Fixas)</option>
              <option value="sac">SAC (Amortização Constante)</option>
              <option value="pricemix">PRICEMIX (Sistema Misto)</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="first_payment_date">Data da Primeira Parcela *</label>
            <input 
              type="date" 
              id="first_payment_date" 
              v-model="formData.first_payment_date" 
              :min="minFirstPaymentDate"
              required
            />
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="indexation">Índice de Indexação</label>
            <select id="indexation" v-model="formData.indexation" @change="calculatePayment">
              <option value="">Sem Indexação</option>
              <option value="cdi">CDI</option>
              <option value="selic">SELIC</option>
              <option value="fixed">Custo Fixo</option>
              <option value="tlp">TLP</option>
            </select>
          </div>
          
          <div class="form-group" v-if="formData.indexation">
            <label for="index_value">Valor do Índice (%)</label>
            <input 
              type="number" 
              id="index_value" 
              v-model="formData.index_value"
              min="0"
              step="0.01"
              @input="calculatePayment"
            />
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="purpose">Finalidade *</label>
            <select id="purpose" v-model="formData.purpose" required>
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
          
          <div class="form-group" v-if="formData.purpose === 'Outro'" style="flex: 100%;">
            <label for="purpose_description">Descreva a Finalidade *</label>
            <textarea id="purpose_description" v-model="formData.purpose_description" rows="3" required></textarea>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group" style="flex: 100%;">
            <label for="observations">Observações</label>
            <textarea id="observations" v-model="formData.observations" rows="3"></textarea>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group" style="flex: 100%;">
            <label>Termo de Autorização e Documentos</label>
            <div class="file-upload">
              <input type="file" id="documents" multiple @change="handleFileUpload" />
              <label for="documents" class="file-upload-btn">
                <i class="fas fa-upload"></i> Selecionar Arquivos
              </label>
              <span class="file-info">{{ fileUploadInfo }}</span>
            </div>
          </div>
        </div>
      
        <!-- Previsão da Parcela -->
        <div class="payment-preview-section">
          <h2>Previsão de Pagamento</h2>
          
          <div class="payment-preview">
            <div class="payment-header">
              <div class="payment-title">
                {{ getPaymentTitle() }}
              </div>
              <div class="payment-subtitle">
                {{ getPaymentSubtitle() }}
              </div>
            </div>
            
            <div class="payment-details">
              <div class="payment-info-card">
                <div class="info-label">Valor Solicitado</div>
                <div class="info-value">R$ {{ formatCurrency(formData.amount) }}</div>
              </div>
              
              <div class="payment-info-card">
                <div class="info-label">Prazo</div>
                <div class="info-value">{{ formData.term_months }} meses</div>
              </div>
              
              <div class="payment-info-card">
                <div class="info-label">Taxa de Juros</div>
                <div class="info-value">{{ formData.interest_rate }}% {{ getInterestFrequencyLabel() }}</div>
              </div>
              
              <div class="payment-info-card">
                <div class="info-label">Primeira Parcela</div>
                <div class="info-value highlighted">R$ {{ firstInstallment }}</div>
              </div>
              
              <div class="payment-info-card">
                <div class="info-label">Valor Total</div>
                <div class="info-value">R$ {{ totalAmount }}</div>
              </div>
              
              <div class="payment-info-card">
                <div class="info-label">Custo Efetivo</div>
                <div class="info-value">{{ effectiveCost }}%</div>
              </div>
            </div>
            
            <div class="payment-note">
              * Os valores apresentados são estimativas. Consulte a tabela completa para mais detalhes.
            </div>
            
            <div class="payment-actions">
              <button type="button" @click="showPaymentPlan = !showPaymentPlan" class="btn-secondary">
                {{ showPaymentPlan ? 'Ocultar Tabela' : 'Ver Tabela Completa' }}
              </button>
            </div>
          </div>
          
          <!-- Tabela de Amortização -->
          <div v-if="showPaymentPlan" class="payment-plan">
            <h3>Plano de Pagamento</h3>
            
            <div class="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Parcela</th>
                    <th>Data</th>
                    <th>Prestação</th>
                    <th>Amortização</th>
                    <th>Juros</th>
                    <th>Saldo Devedor</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, index) in paymentPlan" :key="index">
                    <td>{{ row.installment }}</td>
                    <td>{{ formatDate(row.date) }}</td>
                    <td>R$ {{ formatCurrency(row.payment) }}</td>
                    <td>R$ {{ formatCurrency(row.amortization) }}</td>
                    <td>R$ {{ formatCurrency(row.interest) }}</td>
                    <td>R$ {{ formatCurrency(row.balance) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Botões de navegação -->
      <div class="form-actions">
        <button 
          v-if="currentStep > 1" 
          type="button" 
          @click="prevStep" 
          class="btn-secondary"
        >
          Voltar
        </button>
        
        <button 
          v-if="currentStep < totalSteps" 
          type="submit" 
          class="btn-primary"
        >
          Próximo
        </button>
        
        <button 
          v-if="currentStep === totalSteps" 
          type="submit" 
          class="btn-success"
        >
          Cadastrar Operação
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../../services/api';

export default {
  name: 'OperationForm',
  setup() {
    const route = useRoute();
    const router = useRouter();
    
    const currentStep = ref(1);
    const totalSteps = 2;
    const clientFound = ref(false);
    const clients = ref([]);
    const fileUploadInfo = ref('Nenhum arquivo selecionado');
    const showPaymentPlan = ref(false);
    const loading = ref(false);
    const error = ref('');
    
    // Dados do formulário
    const formData = reactive({
      document: '',
      client_type: 'PF',
      name: '',
      contact_phone: '',
      email: '',
      marital_status: '',
      zipcode: '',
      street: '',
      number: '',
      complement: '',
      neighborhood: '',
      city: '',
      state: '',
      
      // Dados do crédito
      amount: 10000,
      modality: '',
      term_months: 24,
      payment_frequency: 'monthly',
      interest_rate: 1.5,
      interest_frequency: 'monthly',
      grace_period: 0,
      grace_frequency: 'monthly',
      amortization_system: 'price',
      first_payment_date: new Date().toISOString().split('T')[0],
      indexation: '',
      index_value: 0,
      purpose: '',
      purpose_description: '',
      observations: '',
      files: []
    });
    
    // Cliente selecionado
    const selectedClientId = ref(null);
    const selectedClient = ref(null);
    
    // Previsão de pagamento
    const firstInstallment = ref('0,00');
    const totalAmount = ref('0,00');
    const effectiveCost = ref('0,00');
    const paymentPlan = ref([]);
    
    // Data mínima para primeira parcela (hoje + 1 mês)
    const minFirstPaymentDate = computed(() => {
      const today = new Date();
      today.setMonth(today.getMonth() + 1);
      return today.toISOString().split('T')[0];
    });
    
    // Verificar se há um cliente pré-selecionado na URL
    const checkQueryParams = () => {
      const clientId = route.query.client;
      if (clientId) {
        fetchClient(clientId);
      }
    };
    
    // Buscar cliente pelo documento
    const searchClient = async () => {
      if (formData.document && formData.document.length >= 8) {
        try {
          loading.value = true;
          const cleanDocument = formData.document.replace(/[^\d]/g, '');
          
          let params = {};
          if (formData.client_type === 'PF') {
            params = { cpf: cleanDocument };
          } else {
            params = { cnpj: cleanDocument };
          }
          
          console.log('Buscando cliente com parâmetros:', params);
          
          try {
            // Tentar buscar no backend
            const response = await api.clients.getClients(params);
            
            if (response.data && Array.isArray(response.data.results) && response.data.results.length > 0) {
              clients.value = response.data.results;
              console.log('Clientes encontrados:', clients.value);
            } else if (response.data && Array.isArray(response.data) && response.data.length > 0) {
              clients.value = response.data;
              console.log('Clientes encontrados (formato alternativo):', clients.value);
            } else {
              console.log('Nenhum cliente encontrado na API. Verificando cache local...');
              
              // Tentar buscar no localStorage como fallback
              const localClients = JSON.parse(localStorage.getItem('clients') || '[]');
              const filteredClients = localClients.filter(c => 
                c.cpf?.includes(cleanDocument) || 
                c.cnpj?.includes(cleanDocument) ||
                c.name?.toLowerCase().includes(formData.name.toLowerCase())
              );
              
              if (filteredClients.length > 0) {
                clients.value = filteredClients;
                console.log('Clientes encontrados no cache local:', clients.value);
              } else {
                clients.value = [];
                console.log('Nenhum cliente encontrado localmente também.');
                clientFound.value = false;
              }
            }
          } catch (apiError) {
            console.error('Erro ao buscar clientes na API:', apiError);
            
            // Fallback para busca local
            const localClients = JSON.parse(localStorage.getItem('clients') || '[]');
            const filteredClients = localClients.filter(c => 
              c.cpf?.includes(cleanDocument) || 
              c.cnpj?.includes(cleanDocument) ||
              c.name?.toLowerCase().includes(formData.name.toLowerCase())
            );
            
            clients.value = filteredClients;
          }
        } catch (error) {
          console.error('Erro geral ao buscar clientes:', error);
          clients.value = [];
        } finally {
          loading.value = false;
        }
      } else {
        clients.value = [];
      }
    };
    
    // Buscar cliente específico
// Buscar cliente específico
const fetchClient = async (id) => {
      try {
        loading.value = true;
        console.log('Buscando cliente por ID:', id);
        
        try {
          // Tentar buscar no backend
          const response = await api.clients.getClient(id);
          
          if (response && response.data) {
            const client = response.data;
            selectClient(client);
          } else {
            throw new Error('Cliente não encontrado na API');
          }
        } catch (apiError) {
          console.error('Erro ao buscar cliente na API:', apiError);
          
          // Tentar buscar localmente
          const localClients = JSON.parse(localStorage.getItem('clients') || '[]');
          const client = localClients.find(c => c.id == id);
          
          if (client) {
            selectClient(client);
          } else {
            throw new Error('Cliente não encontrado');
          }
        }
      } catch (error) {
        console.error('Erro ao buscar cliente:', error);
        alert('Não foi possível encontrar o cliente solicitado.');
      } finally {
        loading.value = false;
      }
    };
    
    // Selecionar cliente
    const selectClient = (client) => {
      console.log('Cliente selecionado:', client);
      
      selectedClient.value = client;
      selectedClientId.value = client.id;
      
      // Preencher automaticamente todos os campos relevantes
      formData.name = client.name;
      formData.document = client.cpf || client.cnpj;
      formData.client_type = client.cpf ? 'PF' : 'PJ';
      formData.contact_phone = client.phone;
      formData.email = client.email;
      formData.marital_status = client.marital_status || '';
      
      // Preencher endereço se disponível
      if (client.address) {
        formData.street = client.address.street;
        formData.number = client.address.number;
        formData.complement = client.address.complement || '';
        formData.neighborhood = client.address.neighborhood;
        formData.city = client.address.city;
        formData.state = client.address.state;
        formData.zipcode = client.address.zip_code;
      }
      
      // Limpar resultados da busca para melhorar a UI
      clients.value = [];
      
      // Mostrar mensagem de confirmação
      clientFound.value = true;
    };
    
    // Buscar endereço pelo CEP
    const searchZipcode = async () => {
      if (formData.zipcode && formData.zipcode.replace(/[^\d]/g, '').length === 8) {
        try {
          loading.value = true;
          const cleanZipcode = formData.zipcode.replace(/[^\d]/g, '');
          
          console.log('Buscando CEP:', cleanZipcode);
          
          // Tentar API ViaCEP (pública e gratuita no Brasil)
          try {
            const response = await fetch(`https://viacep.com.br/ws/${cleanZipcode}/json/`);
            const data = await response.json();
            
            if (!data.erro) {
              console.log('Dados de CEP encontrados:', data);
              formData.street = data.logradouro;
              formData.neighborhood = data.bairro;
              formData.city = data.localidade;
              formData.state = data.uf;
              
              // Focar no campo de número para melhorar a experiência
              setTimeout(() => {
                const numberInput = document.getElementById('number');
                if (numberInput) numberInput.focus();
              }, 100);
            } else {
              console.warn('CEP não encontrado');
              alert('CEP não encontrado. Por favor, verifique o CEP informado.');
            }
          } catch (apiError) {
            console.error('Erro ao buscar CEP na API:', apiError);
            
            // Fallback para dados simulados em caso de erro na API
            alert('Não foi possível consultar o CEP. Preencha os dados manualmente.');
          }
        } catch (error) {
          console.error('Erro geral ao buscar CEP:', error);
        } finally {
          loading.value = false;
        }
      }
    };
    
    // Lidar com upload de arquivos
    const handleFileUpload = (event) => {
      const files = event.target.files;
      formData.files = Array.from(files);
      
      if (files.length > 0) {
        fileUploadInfo.value = `${files.length} ${files.length === 1 ? 'arquivo selecionado' : 'arquivos selecionados'}`;
      } else {
        fileUploadInfo.value = 'Nenhum arquivo selecionado';
      }
    };
    
    // Calcular pagamento
    const calculatePayment = () => {
      if (!formData.amount || !formData.term_months || !formData.interest_rate) return;
      
      const principal = parseFloat(formData.amount);
      const term = parseInt(formData.term_months);
      
      // Converter taxa de juros para mensal se estiver anual
      let rate = parseFloat(formData.interest_rate) / 100;
      if (formData.interest_frequency === 'annually') {
        rate = Math.pow(1 + rate, 1/12) - 1;
      }
      
      // Calcular com base no sistema de amortização
      if (formData.amortization_system === 'price') {
        // Sistema Price (tabela francesa)
        calculatePriceSystem(principal, term, rate);
      } else if (formData.amortization_system === 'sac') {
        // Sistema SAC
        calculateSACSystem(principal, term, rate);
      } else {
        // Sistema PRICEMIX (para MVP, usar PRICE)
        calculatePriceSystem(principal, term, rate);
      }
    };
    
    // Calcular com Sistema Price
    const calculatePriceSystem = (principal, term, rate) => {
      console.log('Calculando sistema Price:', { principal, term, rate });
      
      try {
        // Fórmula Price: PMT = P * [r(1+r)^n / ((1+r)^n)-1)]
        const installment = (principal * rate * Math.pow(1 + rate, term)) / (Math.pow(1 + rate, term) - 1);
        
        firstInstallment.value = formatCurrency(installment);
        totalAmount.value = formatCurrency(installment * term);
        effectiveCost.value = ((Math.pow(1 + rate, 12) - 1) * 100).toFixed(2);
        
        // Gerar plano de pagamento
        paymentPlan.value = [];
        let balance = principal;
        let currentDate = new Date(formData.first_payment_date);
        let totalInterest = 0;
        
        for (let i = 1; i <= term; i++) {
          const interest = balance * rate;
          totalInterest += interest;
          const amortization = installment - interest;
          balance -= amortization;
          
          // Ajustar saldo para evitar -0.00 no final
          const adjustedBalance = i === term ? 0 : Math.max(0, balance);
          
          paymentPlan.value.push({
            installment: i,
            date: new Date(currentDate),
            payment: installment,
            amortization: amortization,
            interest: interest,
            balance: adjustedBalance
          });
          
          // Avançar para o próximo mês
          currentDate.setMonth(currentDate.getMonth() + 1);
        }
        
        console.log('Cálculo Price concluído:', {
          installment: firstInstallment.value,
          total: totalAmount.value,
          effectiveCost: effectiveCost.value,
          totalInterest
        });
        
        return installment;
      } catch (error) {
        console.error('Erro no cálculo Price:', error);
        return 0;
      }
    };
    
    // Calcular com Sistema SAC
    const calculateSACSystem = (principal, term, rate) => {
      console.log('Calculando sistema SAC:', { principal, term, rate });
      
      try {
        // No SAC, a amortização é constante
        const amortization = principal / term;
        
        // Calcular primeira parcela
        const firstInterest = principal * rate;
        const firstPayment = amortization + firstInterest;
        
        firstInstallment.value = formatCurrency(firstPayment);
        
        // Calcular plano de pagamento
        paymentPlan.value = [];
        let balance = principal;
        let total = 0;
        let currentDate = new Date(formData.first_payment_date);
        let totalInterest = 0;
        
        for (let i = 1; i <= term; i++) {
          const interest = balance * rate;
          totalInterest += interest;
          const payment = amortization + interest;
          balance -= amortization;
          total += payment;
          
          // Ajustar saldo para evitar -0.00 no final
          const adjustedBalance = i === term ? 0 : Math.max(0, balance);
          
          paymentPlan.value.push({
            installment: i,
            date: new Date(currentDate),
            payment: payment,
            amortization: amortization,
            interest: interest,
            balance: adjustedBalance
          });
          
          // Avançar para o próximo mês
          currentDate.setMonth(currentDate.getMonth() + 1);
        }
        
        totalAmount.value = formatCurrency(total);
        effectiveCost.value = ((Math.pow(1 + rate, 12) - 1) * 100).toFixed(2);
        
        console.log('Cálculo SAC concluído:', {
          firstInstallment: firstInstallment.value,
          total: totalAmount.value,
          effectiveCost: effectiveCost.value,
          totalInterest
        });
        
        return firstPayment;
      } catch (error) {
        console.error('Erro no cálculo SAC:', error);
        return 0;
      }
    };
    
    // Criar ou buscar cliente
    const createOrUpdateClient = async () => {
      try {
        loading.value = true;
        let client;
        
        // Criar objeto de endereço
        const addressData = {
          street: formData.street,
          number: formData.number,
          complement: formData.complement,
          neighborhood: formData.neighborhood,
          city: formData.city,
          state: formData.state,
          zip_code: formData.zipcode
        };
        
        // Se já encontrou o cliente, só atualiza se necessário
        if (selectedClientId.value) {
          console.log('Atualizando cliente existente:', selectedClientId.value);
          
          const clientData = {
            id: selectedClientId.value,
            name: formData.name,
            phone: formData.contact_phone,
            email: formData.email,
            marital_status: formData.marital_status || null,
            address: addressData
          };
          
          // Adicionar informações específicas do tipo de cliente
          if (formData.client_type === 'PF') {
            clientData.cpf = formData.document;
            clientData.type = 'PF';
          } else {
            clientData.cnpj = formData.document;
            clientData.type = 'PJ';
          }
          
          try {
            await api.clients.updateClient(selectedClientId.value, clientData);
            return selectedClientId.value;
          } catch (apiError) {
            console.error('Erro ao atualizar cliente na API:', apiError);
            
            // Atualizar cache local
            const localClients = JSON.parse(localStorage.getItem('clients') || '[]');
            const clientIndex = localClients.findIndex(c => c.id === selectedClientId.value);
            
            if (clientIndex !== -1) {
              localClients[clientIndex] = { ...clientData };
              localStorage.setItem('clients', JSON.stringify(localClients));
            }
            
            return selectedClientId.value;
          }
        } else {
          // Criar um novo cliente
          console.log('Criando novo cliente');
          
          const clientData = {
            name: formData.name,
            phone: formData.contact_phone,
            email: formData.email,
            marital_status: formData.marital_status || null,
            address: addressData
          };
          
          // Adicionar informações específicas do tipo de cliente
          if (formData.client_type === 'PF') {
            clientData.cpf = formData.document;
            clientData.type = 'PF';
            // Adicionar data de nascimento padrão para o MVP
            clientData.birth_date = new Date().toISOString().split('T')[0];
          } else {
            clientData.cnpj = formData.document;
            clientData.type = 'PJ';
            // Adicionar data de fundação padrão para o MVP
            clientData.founding_date = new Date().toISOString().split('T')[0];
          }
          
          try {
            const response = await api.clients.createClient(clientData);
            return response.data.id;
          } catch (apiError) {
            console.error('Erro ao criar cliente na API:', apiError);
            
            // Salvar no cache local para MVP
            const localClients = JSON.parse(localStorage.getItem('clients') || '[]');
            const newClientId = Date.now();
            const newClient = { 
              ...clientData,
              id: newClientId,
              created_at: new Date().toISOString()
            };
            
            localClients.push(newClient);
            localStorage.setItem('clients', JSON.stringify(localClients));
            
            return newClientId;
          }
        }
      } catch (error) {
        console.error('Erro geral ao salvar cliente:', error);
        throw error;
      } finally {
        loading.value = false;
      }
    };
    
    // Upload de documentos
    const uploadDocuments = async (operationId) => {
      try {
        if (!formData.files || formData.files.length === 0) return;
        
        console.log('Fazendo upload de documentos para a operação:', operationId);
        
        const uploadPromises = formData.files.map(file => {
          const docData = {
            operation: operationId,
            type: 'authorization',
            name: file.name,
            file: file,
          };
          
          try {
            return api.documents.uploadDocument(docData);
          } catch (uploadError) {
            console.error('Erro no upload do documento:', uploadError);
            // Continuar com os próximos uploads mesmo se um falhar
            return Promise.resolve(null);
          }
        });
        
        const results = await Promise.allSettled(uploadPromises);
        const successCount = results.filter(r => r.status === 'fulfilled' && r.value).length;
        
        console.log(`${successCount} de ${formData.files.length} documentos enviados com sucesso`);
        
        return successCount;
      } catch (error) {
        console.error('Erro geral ao fazer upload de documentos:', error);
        
        // Não interromper o fluxo por falha no upload
        return 0;
      }
    };
    
    // Obter título da previsão de pagamento
    const getPaymentTitle = () => {
      if (formData.amortization_system === 'price') {
        return 'Sistema de Amortização PRICE';
      } else if (formData.amortization_system === 'sac') {
        return 'Sistema de Amortização SAC';
      } else {
        return 'Sistema de Amortização PRICEMIX';
      }
    };
    
    // Obter subtítulo da previsão de pagamento
    const getPaymentSubtitle = () => {
      if (formData.amortization_system === 'price') {
        return 'Parcelas fixas do início ao fim';
      } else if (formData.amortization_system === 'sac') {
        return 'Amortização constante e parcelas decrescentes';
      } else {
        return 'Sistema misto com características de PRICE e SAC';
      }
    };
    
    // Obter label da periodicidade da taxa
    const getInterestFrequencyLabel = () => {
      return formData.interest_frequency === 'monthly' ? 'ao mês' : 'ao ano';
    };
    
    // Formatar moeda
    const formatCurrency = (value) => {
      return parseFloat(value).toLocaleString('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    };
    
    // Formatar data
    const formatDate = (date) => {
      return date.toLocaleDateString('pt-BR');
    };
    
    // Validar dados do formulário
    const validateForm = () => {
      if (currentStep.value === 1) {
        // Validar dados do cliente
        if (!formData.document || !formData.name || !formData.contact_phone || !formData.email || !formData.zipcode || !formData.number) {
          alert('Por favor, preencha todos os campos obrigatórios.');
          return false;
        }
        
        // Validar formato do documento
        const cleanDocument = formData.document.replace(/[^\d]/g, '');
        if (formData.client_type === 'PF' && cleanDocument.length !== 11) {
          alert('CPF inválido. Por favor, verifique o número informado.');
          return false;
        } else if (formData.client_type === 'PJ' && cleanDocument.length !== 14) {
          alert('CNPJ inválido. Por favor, verifique o número informado.');
          return false;
        }
        
        // Validar email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(formData.email)) {
          alert('Email inválido. Por favor, verifique o endereço informado.');
          return false;
        }
        
        return true;
      } else if (currentStep.value === 2) {
        // Validar dados do crédito
        if (!formData.amount || !formData.modality || !formData.term_months || !formData.interest_rate || !formData.first_payment_date || !formData.purpose) {
          alert('Por favor, preencha todos os campos obrigatórios.');
          return false;
        }
        
        // Validar finalidade personalizada
        if (formData.purpose === 'Outro' && !formData.purpose_description) {
          alert('Por favor, descreva a finalidade do crédito.');
          return false;
        }
        
        return true;
      }
      
      return true;
    };
    
    // Avançar para próxima etapa
    const nextStep = async () => {
      if (!validateForm()) {
        return;
      }
      
      if (currentStep.value === totalSteps) {
        // Finalizar cadastro
        saveOperation();
      } else {
        currentStep.value += 1;
        
        // Se for a etapa de crédito, calcular pagamento inicial
        if (currentStep.value === 2) {
          calculatePayment();
        }
        
        // Rolar para o topo do formulário
        window.scrollTo(0, 0);
      }
    };
    
    // Voltar para etapa anterior
    const prevStep = () => {
      if (currentStep.value > 1) {
        currentStep.value -= 1;
        
        // Rolar para o topo do formulário
        window.scrollTo(0, 0);
      }
    };
    
    // Salvar operação
    const saveOperation = async () => {
      try {
        loading.value = true;
        console.log('Salvando operação...');
        
        // 1. Criar ou atualizar cliente
        let clientId;
        try {
          clientId = await createOrUpdateClient();
          console.log('Cliente salvo com ID:', clientId);
        } catch (clientError) {
          console.error('Erro ao salvar cliente:', clientError);
          throw new Error('Não foi possível salvar os dados do cliente. Por favor, tente novamente.');
        }
        
        // 2. Preparar dados da operação
        const finalPurpose = formData.purpose === 'Outro' ? formData.purpose_description : formData.purpose;
        
        const operationData = {
          client: clientId,
          amount: parseFloat(formData.amount),
          modality: formData.modality,
          term_months: parseInt(formData.term_months),
          payment_frequency: formData.payment_frequency,
          interest_rate: parseFloat(formData.interest_rate),
          interest_frequency: formData.interest_frequency,
          grace_period: parseInt(formData.grace_period) || 0,
          grace_frequency: formData.grace_frequency,
          amortization_system: formData.amortization_system,
          first_payment_date: formData.first_payment_date,
          indexation: formData.indexation || null,
          index_value: parseFloat(formData.index_value) || 0,
          purpose: finalPurpose,
          observations: formData.observations || null,
          status: 'pending'
        };
        
        console.log('Enviando dados da operação:', operationData);
        
        // 3. Criar operação
        let operationId;
        try {
          const response = await api.operations.createOperation(operationData);
          console.log('Resposta recebida do backend:', response);
          
          if (response && response.data && response.data.id) {
            operationId = response.data.id;
            console.log('Operação criada com ID:', operationId);
          } else {
            throw new Error('ID da operação não retornado pelo backend');
          }
        } catch (apiError) {
          console.error('Erro na API ao criar operação:', apiError);
          
          // Fallback: salvar localmente para MVP
          const localOperations = JSON.parse(localStorage.getItem('operations') || '[]');
          operationData.id = Date.now();
          operationData.created_at = new Date().toISOString();
          operationData.client_name = formData.name;
          operationData.client_document = formData.document;
          
          localOperations.push(operationData);
          localStorage.setItem('operations', JSON.stringify(localOperations));
          operationId = operationData.id;
          
          console.log('Operação salva localmente com ID:', operationId);
        }
        
        // 4. Upload de documentos
        if (formData.files && formData.files.length > 0) {
          try {
            const uploadedCount = await uploadDocuments(operationId);
            console.log(`${uploadedCount} documentos enviados com sucesso`);
          } catch (uploadError) {
            console.warn('Aviso: Documentos não puderam ser enviados:', uploadError);
            // Não interromper o fluxo por falha no upload
          }
        }
        
        // 5. Navegar para a página de detalhes da operação
        alert('Operação cadastrada com sucesso!');
        router.push(`/operations/${operationId}`);
      } catch (error) {
        console.error('Erro ao salvar operação:', error);
        alert(`Erro ao criar operação: ${error.message || 'Verifique o console para mais detalhes'}`);
      } finally {
        loading.value = false;
      }
    };
    
    onMounted(() => {
      // Verificar se há cliente pré-selecionado
      checkQueryParams();
      
      // Definir data atual + 30 dias como data da primeira parcela
      const today = new Date();
      today.setDate(today.getDate() + 30);
      formData.first_payment_date = today.toISOString().split('T')[0];
    });
    
    return {
      currentStep,
      totalSteps,
      formData,
      clients,
      clientFound,
      fileUploadInfo,
      minFirstPaymentDate,
      showPaymentPlan,
      firstInstallment,
      totalAmount,
      effectiveCost,
      paymentPlan,
      loading,
      error,
      searchClient,
      selectClient,
      searchZipcode,
      handleFileUpload,
      calculatePayment,
      getPaymentTitle,
      getPaymentSubtitle,
      getInterestFrequencyLabel,
      formatCurrency,
      formatDate,
      nextStep,
      prevStep
    };
  }
}
</script>

<style scoped>
.operation-form {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 28px;
  color: #00004b;
  font-weight: 700;
  margin: 0;
}

.form-section {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  padding: 30px;
  margin-bottom: 30px;
  animation: fadeIn 0.5s ease-out;
  position: relative;
  overflow: hidden;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}

.form-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
}

.client-section::before {
  background: linear-gradient(180deg, #4673F5, #2556e0);
}

.credit-section::before {
  background: linear-gradient(180deg, #00004b, #000075);
}

.form-section h2 {
  margin-top: 0;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eaedf2;
  font-size: 22px;
  color: #00004b;
  font-weight: 600;
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
  margin-bottom: 8px;
  font-weight: 500;
  color: #444;
  font-size: 15px;
}

input, select, textarea {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 15px;
  transition: all 0.3s ease;
  background-color: #f9f9fc;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #4673F5;
  box-shadow: 0 0 0 3px rgba(70, 115, 245, 0.15);
  background-color: #ffffff;
}

input[readonly] {
  background-color: #f0f0f0;
  cursor: not-allowed;
  border-color: #e0e0e0;
}

small {
  display: block;
  color: #666;
  font-size: 12px;
  margin-top: 5px;
}

.alert {
  padding: 15px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 15px;
  animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
  from { opacity: 0; transform: translateX(-15px); }
  to { opacity: 1; transform: translateX(0); }
}

.alert-success {
  background-color: #E8F5E9;
  color: #388E3C;
  border-left: 4px solid #4CAF50;
}

.client-results {
  margin-bottom: 20px;
  overflow: hidden;
  border-radius: 8px;
  animation: expandDown 0.5s ease-out;
}

@keyframes expandDown {
  from { opacity: 0; max-height: 0; }
  to { opacity: 1; max-height: 500px; }
}

.client-results h3 {
  background-color: #f5f7fa;
  padding: 12px 20px;
  margin: 0;
  font-size: 16px;
  color: #00004b;
  border-bottom: 1px solid #eee;
}

.file-upload {
  position: relative;
  display: flex;
  align-items: center;
  margin-top: 10px;
}

.file-upload input[type="file"] {
  position: absolute;
  width: 0.1px;
  height: 0.1px;
  opacity: 0;
  overflow: hidden;
  z-index: -1;
}

.file-upload-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: #f5f7fa;
  color: #444;
  padding: 12px 20px;
  border-radius: 8px;
  cursor: pointer;
  border: 1px solid #ddd;
  transition: all 0.3s ease;
  font-weight: 500;
}

.file-upload-btn:hover {
  background-color: #e5e7ea;
  color: #00004b;
}

.file-info {
  margin-left: 12px;
  font-size: 14px;
  color: #666;
}

/* Seção de previsão de pagamento */
.payment-preview-section {
  background-color: #F5F7FA;
  padding: 30px;
  border-radius: 12px;
  margin-top: 30px;
  animation: fadeIn 0.5s ease-out;
}

.payment-preview-section h2 {
  border-bottom: none;
  color: #00004b;
  margin-bottom: 20px;
  padding-bottom: 0;
}

.payment-preview {
  background-color: white;
  border-radius: 12px;
  border: 1px solid #E3F2FD;
  padding: 25px;
  margin-bottom: 25px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
}

.payment-header {
  text-align: center;
  margin-bottom: 25px;
}

.payment-title {
  font-size: 20px;
  font-weight: 700;
  color: #00004b;
  margin-bottom: 8px;
}

.payment-subtitle {
  font-size: 15px;
  color: #666;
}

.payment-details {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.payment-info-card {
  background-color: #f9f9fc;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  transition: all 0.3s ease;
}

.payment-info-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.info-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.info-value {
  font-size: 18px;
  font-weight: 700;
  color: #333;
}

.info-value.highlighted {
  color: #4673F5;
  font-size: 22px;
}

.payment-note {
  font-size: 13px;
  color: #666;
  margin-bottom: 20px;
  text-align: center;
  font-style: italic;
}

.payment-actions {
  display: flex;
  justify-content: center;
}

/* Plano de pagamento */
.payment-plan {
  margin-top: 30px;
  animation: fadeIn 0.5s ease-out;
}

.payment-plan h3 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 18px;
  color: #00004b;
  font-weight: 600;
}

.table-container {
  overflow-x: auto;
  max-height: 450px;
  overflow-y: auto;
  border-radius: 10px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
  font-size: 14px;
}

th {
  background-color: #f5f7fa;
  color: #00004b;
  font-weight: 600;
  position: sticky;
  top: 0;
  z-index: 10;
}

tr:hover td {
  background-color: #f9fafc;
}

tr:last-child td {
  border-bottom: none;
}

/* Ações do formulário */
.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 40px;
}

.btn-primary, .btn-secondary, .btn-success {
  padding: 14px 28px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.btn-primary {
  background: linear-gradient(90deg, #4673F5, #2556e0);
  color: white;
  box-shadow: 0 4px 10px rgba(70, 115, 245, 0.2);
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(70, 115, 245, 0.3);
}

.btn-secondary {
  background-color: #f5f5f7;
  color: #444;
  border: 1px solid #ddd;
}

.btn-secondary:hover {
  background-color: #e5e5e7;
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.05);
}

.btn-success {
  background: linear-gradient(90deg, #4CAF50, #388E3C);
  color: white;
  box-shadow: 0 4px 10px rgba(76, 175, 80, 0.2);
}

.btn-success:hover {
  background: linear-gradient(90deg, #388E3C, #2E7D32);
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(76, 175, 80, 0.3);
}

/* Estilos para entrada de seleção */
select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23444' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 15px center;
  padding-right: 40px;
}

/* Responsividade para telas menores */
@media (max-width: 768px) {
  .form-section {
    padding: 20px;
  }
  
  .payment-details {
    grid-template-columns: 1fr 1fr;
  }
  
  .form-actions {
    flex-direction: column-reverse;
    gap: 15px;
  }
  
  .btn-primary, .btn-secondary, .btn-success {
    width: 100%;
    justify-content: center;
  }
}
</style>