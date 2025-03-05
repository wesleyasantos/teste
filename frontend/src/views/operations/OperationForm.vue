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
              v-model="formData.term" 
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
      </div>
      
      <!-- Previsão da Parcela -->
      <div v-if="currentStep === 2" class="form-section payment-preview-section">
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
              <div class="info-value">{{ formData.term }} meses</div>
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
import { useRouter } from 'vue-router';

export default {
  name: 'OperationForm',
  setup() {
    const router = useRouter();
    
    const currentStep = ref(1);
    const totalSteps = 2;
    const clientFound = ref(false);
    const fileUploadInfo = ref('Nenhum arquivo selecionado');
    const showPaymentPlan = ref(false);
    
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
      term: 24,
      payment_frequency: 'monthly',
      interest_rate: 1.5,
      interest_frequency: 'monthly',
      grace_period: 0,
      grace_frequency: 'monthly',
      amortization_system: 'price',
      first_payment_date: new Date().toISOString().split('T')[0],
      indexation: '',
      index_value: 0,
      observations: '',
      files: []
    });
    
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
    
    // Buscar cliente pelo documento
    const searchClient = async () => {
      if (formData.document && formData.document.length >= 11) {
        try {
          // Simular busca de cliente
          // Em uma aplicação real, chamaríamos a API
          setTimeout(() => {
            if (formData.document === '12345678900' || formData.document === '12345678901234') {
              formData.name = formData.document.length > 11 ? 'Tech Solutions Ltda' : 'João Silva';
              formData.email = formData.document.length > 11 ? 'contato@techsolutions.com' : 'joao.silva@email.com';
              formData.contact_phone = '(11) 98765-4321';
              clientFound.value = true;
            }
          }, 500);
        } catch (error) {
          console.error('Erro ao buscar cliente:', error);
        }
      }
    };
    
    // Buscar endereço pelo CEP
    const searchZipcode = async () => {
      if (formData.zipcode && formData.zipcode.length === 8) {
        try {
          // Simular busca de CEP
          // Em uma aplicação real, chamaríamos a API
          setTimeout(() => {
            formData.street = 'Rua das Flores';
            formData.neighborhood = 'Jardim Primavera';
            formData.city = 'São Paulo';
            formData.state = 'SP';
          }, 500);
        } catch (error) {
          console.error('Erro ao buscar CEP:', error);
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
      if (!formData.amount || !formData.term || !formData.interest_rate) return;
      
      const principal = parseFloat(formData.amount);
      const term = parseInt(formData.term);
      
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
      const installment = (principal * rate * Math.pow(1 + rate, term)) / (Math.pow(1 + rate, term) - 1);
      
      firstInstallment.value = formatCurrency(installment);
      totalAmount.value = formatCurrency(installment * term);
      effectiveCost.value = ((Math.pow(1 + rate, 12) - 1) * 100).toFixed(2);
      
      // Gerar plano de pagamento
      paymentPlan.value = [];
      let balance = principal;
      let currentDate = new Date(formData.first_payment_date);
      
      for (let i = 1; i <= term; i++) {
        const interest = balance * rate;
        const amortization = installment - interest;
        balance -= amortization;
        
        paymentPlan.value.push({
          installment: i,
          date: new Date(currentDate),
          payment: installment,
          amortization: amortization,
          interest: interest,
          balance: balance < 0.01 ? 0 : balance
        });
        
        // Avançar para o próximo mês
        currentDate.setMonth(currentDate.getMonth() + 1);
      }
    };
    
    // Calcular com Sistema SAC
    const calculateSACSystem = (principal, term, rate) => {
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
      
      for (let i = 1; i <= term; i++) {
        const interest = balance * rate;
        const payment = amortization + interest;
        balance -= amortization;
        total += payment;
        
        paymentPlan.value.push({
          installment: i,
          date: new Date(currentDate),
          payment: payment,
          amortization: amortization,
          interest: interest,
          balance: balance < 0.01 ? 0 : balance
        });
        
        // Avançar para o próximo mês
        currentDate.setMonth(currentDate.getMonth() + 1);
      }
      
      totalAmount.value = formatCurrency(total);
      effectiveCost.value = ((Math.pow(1 + rate, 12) - 1) * 100).toFixed(2);
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
    
    // Avançar para próxima etapa
    const nextStep = () => {
      if (currentStep.value === totalSteps) {
        // Finalizar cadastro
        saveOperation();
      } else {
        currentStep.value += 1;
        
        // Se for a etapa de crédito, calcular pagamento inicial
        if (currentStep.value === 2) {
          calculatePayment();
        }
      }
    };
    
    // Voltar para etapa anterior
    const prevStep = () => {
      if (currentStep.value > 1) {
        currentStep.value -= 1;
      }
    };
    
    // Salvar operação
    const saveOperation = () => {
      // Em uma aplicação real, chamaríamos a API
      console.log('Salvando operação:', formData);
      
      // Redirecionar para detalhes da operação (simulação)
      const newOperationId = Math.floor(Math.random() * 1000) + 100;
      router.push(`/operations/${newOperationId}`);
    };
    
    onMounted(() => {
      // Definir data atual + 30 dias como data da primeira parcela
      const today = new Date();
      today.setDate(today.getDate() + 30);
      formData.first_payment_date = today.toISOString().split('T')[0];
    });
    
    return {
      currentStep,
      totalSteps,
      formData,
      clientFound,
      fileUploadInfo,
      minFirstPaymentDate,
      showPaymentPlan,
      firstInstallment,
      totalAmount,
      effectiveCost,
      paymentPlan,
      searchClient,
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
  padding: 20px;
}

.page-header {
  margin-bottom: 20px;
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
  color: var(--primary-color);
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
  font-size: 14px;
}

input:focus, select:focus, textarea:focus {
  border-color: var(--primary-color);
  outline: none;
  box-shadow: 0 0 0 2px rgba(0, 0, 75, 0.1);
}

input[readonly] {
  background-color: #f9f9f9;
  cursor: not-allowed;
}

small {
  display: block;
  color: #666;
  font-size: 12px;
  margin-top: 4px;
}

.alert {
  padding: 12px 15px;
  border-radius: 4px;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
}

.alert-success {
  background-color: #E8F5E9;
  color: #388E3C;
  border-left: 4px solid #388E3C;
}

.file-upload {
  position: relative;
  display: flex;
  align-items: center;
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
  display: inline-block;
  background-color: #F5F5F5;
  color: #333;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  border: 1px solid #ddd;
  transition: all 0.3s ease;
}

.file-upload-btn:hover {
  background-color: #E0E0E0;
}

.file-info {
  margin-left: 10px;
  font-size: 14px;
  color: #666;
}

/* Seção de previsão de pagamento */
.payment-preview-section {
  background-color: #F9FBFF;
}

.payment-preview {
  background-color: white;
  border-radius: 8px;
  border: 1px solid #E3F2FD;
  padding: 20px;
  margin-bottom: 20px;
}

.payment-header {
  text-align: center;
  margin-bottom: 20px;
}

.payment-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 5px;
}

.payment-subtitle {
  font-size: 14px;
  color: #666;
}

.payment-details {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.payment-info-card {
  background-color: #F5F7FA;
  border-radius: 6px;
  padding: 15px;
  text-align: center;
}

.info-label {
  font-size: 12px;
  color: #666;
  margin-bottom: 5px;
}

.info-value {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.info-value.highlighted {
  color: var(--primary-color);
  font-size: 18px;
}

.payment-note {
  font-size: 12px;
  color: #666;
  margin-bottom: 15px;
  text-align: center;
}

.payment-actions {
  display: flex;
  justify-content: center;
}

/* Plano de pagamento */
.payment-plan {
  margin-top: 20px;
}

.payment-plan h3 {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 16px;
  color: #333;
}

.table-container {
  overflow-x: auto;
  max-height: 400px;
  overflow-y: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
  font-size: 14px;
}

th {
  background-color: #f0f0f0;
  position: sticky;
  top: 0;
  z-index: 10;
  font-weight: 500;
}

/* Ações do formulário */
.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}

.btn-primary, .btn-secondary, .btn-success {
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
}

.btn-primary:hover {
  background-color: #000075;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
}

.btn-secondary:hover {
  background-color: #e0e0e0;
}

.btn-success {
  background-color: #4CAF50;
  color: white;
}

.btn-success:hover {
  background-color: #388E3C;
}
</style>