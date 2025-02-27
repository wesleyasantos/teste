<template>
    <div class="client-form">
      <div class="page-header">
        <h1>{{ isEditMode ? 'Editar Cliente' : 'Novo Cliente' }}</h1>
      </div>
      
      <form @submit.prevent="saveClient">
        <div class="form-container">
          <!-- Informações Pessoais -->
          <div class="form-section">
            <h2>Dados Pessoais</h2>
            
            <div class="form-row">
              <div class="form-group">
                <label for="name">Nome Completo *</label>
                <input 
                  type="text" 
                  id="name" 
                  v-model="client.name" 
                  required
                />
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="cpf">CPF *</label>
                <input 
                  type="text" 
                  id="cpf" 
                  v-model="client.cpf" 
                  required
                />
              </div>
              
              <div class="form-group">
                <label for="rg">RG</label>
                <input 
                  type="text" 
                  id="rg" 
                  v-model="client.rg"
                />
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="birth_date">Data de Nascimento *</label>
                <input 
                  type="date" 
                  id="birth_date" 
                  v-model="client.birth_date" 
                  required
                />
              </div>
              
              <div class="form-group">
                <label for="phone">Telefone *</label>
                <input 
                  type="tel" 
                  id="phone" 
                  v-model="client.phone" 
                  required
                />
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="email">E-mail *</label>
                <input 
                  type="email" 
                  id="email" 
                  v-model="client.email" 
                  required
                />
              </div>
            </div>
          </div>
          
          <!-- Endereço -->
          <div class="form-section">
            <h2>Endereço</h2>
            
            <div class="form-row">
              <div class="form-group">
                <label for="street">Rua *</label>
                <input 
                  type="text" 
                  id="street" 
                  v-model="address.street" 
                  required
                />
              </div>
              
              <div class="form-group">
                <label for="number">Número *</label>
                <input 
                  type="text" 
                  id="number" 
                  v-model="address.number" 
                  required
                />
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="complement">Complemento</label>
                <input 
                  type="text" 
                  id="complement" 
                  v-model="address.complement"
                />
              </div>
              
              <div class="form-group">
                <label for="neighborhood">Bairro *</label>
                <input 
                  type="text" 
                  id="neighborhood" 
                  v-model="address.neighborhood" 
                  required
                />
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="city">Cidade *</label>
                <input 
                  type="text" 
                  id="city" 
                  v-model="address.city" 
                  required
                />
              </div>
              
              <div class="form-group">
                <label for="state">Estado *</label>
                <select 
                  id="state" 
                  v-model="address.state" 
                  required
                >
                  <option value="">Selecione...</option>
                  <option value="AC">Acre</option>
                  <option value="AL">Alagoas</option>
                  <option value="AP">Amapá</option>
                  <option value="AM">Amazonas</option>
                  <option value="BA">Bahia</option>
                  <option value="CE">Ceará</option>
                  <option value="DF">Distrito Federal</option>
                  <option value="ES">Espírito Santo</option>
                  <option value="GO">Goiás</option>
                  <option value="MA">Maranhão</option>
                  <option value="MT">Mato Grosso</option>
                  <option value="MS">Mato Grosso do Sul</option>
                  <option value="MG">Minas Gerais</option>
                  <option value="PA">Pará</option>
                  <option value="PB">Paraíba</option>
                  <option value="PR">Paraná</option>
                  <option value="PE">Pernambuco</option>
                  <option value="PI">Piauí</option>
                  <option value="RJ">Rio de Janeiro</option>
                  <option value="RN">Rio Grande do Norte</option>
                  <option value="RS">Rio Grande do Sul</option>
                  <option value="RO">Rondônia</option>
                  <option value="RR">Roraima</option>
                  <option value="SC">Santa Catarina</option>
                  <option value="SP">São Paulo</option>
                  <option value="SE">Sergipe</option>
                  <option value="TO">Tocantins</option>
                </select>
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="zip_code">CEP *</label>
                <input 
                  type="text" 
                  id="zip_code" 
                  v-model="address.zip_code" 
                  required
                />
              </div>
            </div>
          </div>
          
          <!-- Informações Financeiras -->
          <div class="form-section">
            <h2>Informações Financeiras</h2>
            
            <div class="form-row">
              <div class="form-group">
                <label for="profession">Profissão *</label>
                <input 
                  type="text" 
                  id="profession" 
                  v-model="client.profession" 
                  required
                />
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="monthly_income">Renda Mensal *</label>
                <input 
                  type="number" 
                  id="monthly_income" 
                  v-model="client.monthly_income" 
                  step="0.01" 
                  min="0" 
                  required
                />
              </div>
            </div>
          </div>
        </div>
        
        <div class="form-actions">
          <button type="button" @click="cancel" class="btn-cancel">Cancelar</button>
          <button type="submit" class="btn-save">Salvar</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, computed } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  
  export default {
    name: 'ClientForm',
    setup() {
      const route = useRoute();
      const router = useRouter();
      
      const clientId = computed(() => route.params.id);
      const isEditMode = computed(() => !!clientId.value);
      
      const client = ref({
        name: '',
        cpf: '',
        rg: '',
        birth_date: '',
        phone: '',
        email: '',
        profession: '',
        monthly_income: 0
      });
      
      const address = ref({
        street: '',
        number: '',
        complement: '',
        neighborhood: '',
        city: '',
        state: '',
        zip_code: ''
      });
      
      // Buscar dados do cliente se estiver em modo de edição
      const fetchClient = async () => {
        if (isEditMode.value) {
          try {
            // Em uma aplicação real, você buscaria do backend aqui
            // Dados estáticos para exemplo
            client.value = {
              name: 'João Silva',
              cpf: '123.456.789-00',
              rg: '12.345.678-9',
              birth_date: '1985-05-15',
              phone: '(11) 98765-4321',
              email: 'joao.silva@email.com',
              profession: 'Engenheiro',
              monthly_income: 5000
            };
            
            address.value = {
              street: 'Rua das Flores',
              number: '123',
              complement: 'Apto 45',
              neighborhood: 'Jardim Primavera',
              city: 'São Paulo',
              state: 'SP',
              zip_code: '01234-567'
            };
          } catch (error) {
            console.error('Erro ao buscar dados do cliente:', error);
          }
        }
      };
      
      // Salvar cliente
      const saveClient = async () => {
        try {
          // Em uma aplicação real, você enviaria para o backend aqui
          console.log('Salvando cliente:', { ...client.value, address: address.value });
          
          // Navegar de volta para a lista de clientes
          router.push('/clients');
          
        } catch (error) {
          console.error('Erro ao salvar cliente:', error);
        }
      };
      
      // Cancelar e voltar para a lista
      const cancel = () => {
        router.push('/clients');
      };
      
      onMounted(() => {
        fetchClient();
      });
      
      return {
        client,
        address,
        isEditMode,
        saveClient,
        cancel
      };
    }
  }
  </script>
  
  <style scoped>
  .client-form {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .page-header {
    margin-bottom: 30px;
  }
  
  .form-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 20px;
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
  
  input, select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
  }
  
  input:focus, select:focus {
    outline: none;
    border-color: #2196F3;
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
  </style>