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
  padding: 30px 20px;
}

.page-header {
  margin-bottom: 35px;
}

.page-header h1 {
  color: #00004b;
  font-size: 28px;
  font-weight: 700;
  margin: 0;
}

.form-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 25px;
}

.form-section {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  padding: 25px;
  margin-bottom: 25px;
  transition: all 0.3s ease;
}

.form-section:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.form-section h2 {
  margin-top: 0;
  margin-bottom: 25px;
  padding-bottom: 12px;
  border-bottom: 1px solid #eef0f5;
  font-size: 20px;
  color: #00004b;
  font-weight: 600;
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  gap: 22px;
  margin-bottom: 20px;
}

.form-group {
  flex: 1;
  min-width: 200px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #444;
  font-size: 14px;
}

input, select {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 15px;
  transition: all 0.3s ease;
  background-color: #f9f9fc;
}

input:focus, select:focus {
  outline: none;
  border-color: #4673F5;
  box-shadow: 0 0 0 3px rgba(70, 115, 245, 0.15);
  background-color: #ffffff;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 30px;
}

.btn-cancel, .btn-save {
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 15px;
  cursor: pointer;
  border: none;
  font-weight: 600;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-cancel {
  background-color: #f5f5f7;
  color: #444;
}

.btn-cancel:hover {
  background-color: #e5e5e7;
}

.btn-save {
  background: linear-gradient(90deg, #2196F3, #1565C0);
  color: white;
  box-shadow: 0 4px 10px rgba(33, 150, 243, 0.3);
}

.btn-save:hover {
  background: linear-gradient(90deg, #1976D2, #0D47A1);
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(33, 150, 243, 0.4);
}

select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23444' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 15px center;
  padding-right: 40px;
}

/* Adiciona efeito quando os dados são salvos */
@keyframes savedAnimation {
  0% { transform: scale(1); }
  50% { transform: scale(1.02); }
  100% { transform: scale(1); }
}

.form-section.saved {
  animation: savedAnimation 0.5s ease-in-out;
  border: 1px solid #4CAF50;
}
</style>