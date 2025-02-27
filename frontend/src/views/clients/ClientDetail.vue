<template>
    <div class="client-detail">
      <div class="page-header">
        <h1>Detalhes do Cliente</h1>
        <div class="header-actions">
          <router-link :to="`/clients/${clientId}/edit`" class="btn-edit">Editar</router-link>
          <router-link :to="`/applications/new?client=${clientId}`" class="btn-primary">Nova Solicitação</router-link>
        </div>
      </div>
      
      <div class="content-grid">
        <!-- Informações pessoais -->
        <div class="info-card">
          <h2>Dados Pessoais</h2>
          <div class="info-row">
            <span class="label">Nome:</span>
            <span class="value">{{ client.name }}</span>
          </div>
          <div class="info-row">
            <span class="label">CPF:</span>
            <span class="value">{{ client.cpf }}</span>
          </div>
          <div class="info-row">
            <span class="label">RG:</span>
            <span class="value">{{ client.rg || '-' }}</span>
          </div>
          <div class="info-row">
            <span class="label">Data de Nascimento:</span>
            <span class="value">{{ formatDate(client.birth_date) }}</span>
          </div>
          <div class="info-row">
            <span class="label">Telefone:</span>
            <span class="value">{{ client.phone }}</span>
          </div>
          <div class="info-row">
            <span class="label">E-mail:</span>
            <span class="value">{{ client.email }}</span>
          </div>
        </div>
        
        <!-- Endereço -->
        <div class="info-card">
          <h2>Endereço</h2>
          <div class="info-row">
            <span class="label">Rua:</span>
            <span class="value">{{ address.street }}, {{ address.number }}</span>
          </div>
          <div class="info-row">
            <span class="label">Complemento:</span>
            <span class="value">{{ address.complement || '-' }}</span>
          </div>
          <div class="info-row">
            <span class="label">Bairro:</span>
            <span class="value">{{ address.neighborhood }}</span>
          </div>
          <div class="info-row">
            <span class="label">Cidade/UF:</span>
            <span class="value">{{ address.city }}/{{ address.state }}</span>
          </div>
          <div class="info-row">
            <span class="label">CEP:</span>
            <span class="value">{{ address.zip_code }}</span>
          </div>
        </div>
        
        <!-- Informações financeiras -->
        <div class="info-card">
          <h2>Informações Financeiras</h2>
          <div class="info-row">
            <span class="label">Profissão:</span>
            <span class="value">{{ client.profession }}</span>
          </div>
          <div class="info-row">
            <span class="label">Renda Mensal:</span>
            <span class="value">R$ {{ formatCurrency(client.monthly_income) }}</span>
          </div>
          <div class="info-row">
            <span class="label">Score de Crédito:</span>
            <span class="value score-value">{{ creditScore.score || '-' }}</span>
          </div>
        </div>
        
        <!-- Documentos -->
        <div class="info-card">
          <h2>Documentos</h2>
          <table v-if="documents.length > 0">
            <thead>
              <tr>
                <th>Tipo</th>
                <th>Data de Upload</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="doc in documents" :key="doc.id">
                <td>{{ getDocumentTypeLabel(doc.document_type) }}</td>
                <td>{{ formatDate(doc.uploaded_at) }}</td>
                <td>
                  <a :href="doc.file" target="_blank" class="btn-view">Visualizar</a>
                </td>
              </tr>
            </tbody>
          </table>
          <div v-else class="empty-state">
            <p>Nenhum documento enviado.</p>
            <button @click="openUploadDialog" class="btn-primary">Enviar Documento</button>
          </div>
        </div>
      </div>
      
      <!-- Histórico de Solicitações -->
      <div class="history-section">
        <h2>Histórico de Solicitações</h2>
        <table v-if="applications.length > 0">
          <thead>
            <tr>
              <th>ID</th>
              <th>Data</th>
              <th>Valor</th>
              <th>Finalidade</th>
              <th>Status</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="app in applications" :key="app.id">
              <td>#{{ app.id }}</td>
              <td>{{ formatDate(app.created_at) }}</td>
              <td>R$ {{ formatCurrency(app.amount_requested) }}</td>
              <td>{{ app.purpose }}</td>
              <td>
                <span :class="'status-badge ' + app.status">
                  {{ getStatusLabel(app.status) }}
                </span>
              </td>
              <td>
                <router-link :to="`/applications/${app.id}`" class="btn-view">Ver</router-link>
              </td>
            </tr>
          </tbody>
        </table>
        <div v-else class="empty-state">
          <p>Nenhuma solicitação de crédito encontrada.</p>
          <router-link :to="`/applications/new?client=${clientId}`" class="btn-primary">
            Nova Solicitação
          </router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  
  export default {
    name: 'ClientDetail',
    setup() {
      const route = useRoute();
      const clientId = ref(parseInt(route.params.id));
      
      const client = ref({});
      const address = ref({});
      const creditScore = ref({});
      const documents = ref([]);
      const applications = ref([]);
      
      // Buscar dados do cliente
      const fetchClientData = async () => {
        try {
          // Dados estáticos para exemplo
          client.value = {
            id: clientId.value,
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
          
          creditScore.value = {
            score: 825,
            payment_history: 85,
            debt_burden: 80,
            length_history: 90
          };
          
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
          
          applications.value = [
            {
              id: 101,
              created_at: '2025-01-15T10:00:00',
              amount_requested: 8000,
              purpose: 'Compra de automóvel',
              status: 'approved'
            },
            {
              id: 102,
              created_at: '2025-02-20T11:30:00',
              amount_requested: 3000,
              purpose: 'Reforma residencial',
              status: 'pending'
            }
          ];
        } catch (error) {
          console.error('Erro ao buscar dados do cliente:', error);
        }
      };
      
      // Função para formatar datas
      const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('pt-BR');
      };
      
      // Função para formatar valores monetários
      const formatCurrency = (value) => {
        return parseFloat(value).toLocaleString('pt-BR', {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2
        });
      };
      
      // Função para obter label do tipo de documento
      const getDocumentTypeLabel = (type) => {
        const labels = {
          'income': 'Comprovante de Renda',
          'bank_statement': 'Extrato Bancário',
          'tax_return': 'Declaração de IR',
          'other': 'Outro'
        };
        return labels[type] || type;
      };
      
      // Função para obter label do status
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
      
      // Função para abrir diálogo de upload
      const openUploadDialog = () => {
        alert('Funcionalidade de upload de documentos será implementada.');
      };
      
      onMounted(() => {
        fetchClientData();
      });
      
      return {
        client,
        clientId,
        address,
        creditScore,
        documents,
        applications,
        formatDate,
        formatCurrency,
        getDocumentTypeLabel,
        getStatusLabel,
        openUploadDialog
      };
    }
  }
  </script>
  
  <style scoped>
  .client-detail {
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
  
  .header-actions {
    display: flex;
    gap: 10px;
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
  }
  
  .info-row {
    display: flex;
    margin-bottom: 10px;
  }
  
  .label {
    flex: 1;
    color: #666;
    font-weight: 500;
  }
  
  .value {
    flex: 2;
  }
  
  .score-value {
    font-weight: 600;
    color: #388E3C;
  }
  
  .history-section {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-top: 20px;
  }
  
  .history-section h2 {
    margin-top: 0;
    margin-bottom: 20px;
    font-size: 18px;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th, td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #eee;
  }
  
  th {
    font-weight: 500;
    color: #666;
  }
  
  .empty-state {
    padding: 20px;
    text-align: center;
    color: #666;
  }
  
  .btn-primary, .btn-edit, .btn-view {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 4px;
    text-decoration: none;
    font-weight: 500;
  }
  
  .btn-primary {
    background-color: #2196F3;
    color: white;
  }
  
  .btn-edit {
    background-color: #FFF8E1;
    color: #FFA000;
  }
  
  .btn-view {
    background-color: #E3F2FD;
    color: #1976D2;
    padding: 6px 12px;
    font-size: 14px;
  }
  
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
  </style>