<template>
  <div class="client-detail">
    <div class="page-header">
      <h1>Detalhes do Cliente</h1>
      <div class="header-actions">
        <router-link :to="`/clients/${clientId}/edit`" class="btn-edit">Editar</router-link>
        <router-link :to="`/operations/new?client=${clientId}`" class="btn-primary">Nova Solicitação</router-link>
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
              <router-link :to="`/operations/${app.id}`" class="btn-view">Ver</router-link>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else class="empty-state">
        <p>Nenhuma solicitação de crédito encontrada.</p>
        <router-link :to="`/operations/new?client=${clientId}`" class="btn-primary">
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
  padding: 30px 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eaedf2;
}

.page-header h1 {
  font-size: 28px;
  color: #00004b;
  font-weight: 700;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.btn-edit {
  background-color: #FFF8E1;
  color: #FFA000;
  padding: 10px 18px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-edit:hover {
  background-color: #FFECB3;
  color: #FF6F00;
  transform: translateY(-2px);
  text-decoration: none;
}

.btn-primary {
  background: linear-gradient(90deg, #4673F5, #2556e0);
  color: white;
  padding: 10px 18px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 10px rgba(70, 115, 245, 0.2);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 15px rgba(70, 115, 245, 0.3);
  text-decoration: none;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 25px;
  margin-bottom: 30px;
}

.info-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  padding: 25px;
  transition: all 0.3s ease;
  animation: slideIn 0.5s ease-out forwards;
  animation-delay: calc(var(--animation-order, 0) * 0.1s);
  opacity: 0;
  transform: translateY(20px);
}

@keyframes slideIn {
  to { opacity: 1; transform: translateY(0); }
}

.info-card:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  transform: translateY(-5px);
}

.info-card h2 {
  margin-top: 0;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #eee;
  font-size: 18px;
  color: #00004b;
  font-weight: 600;
}

.info-row {
  display: flex;
  margin-bottom: 12px;
  align-items: center;
}

.label {
  flex: 1;
  color: #666;
  font-weight: 500;
  font-size: 14px;
}

.value {
  flex: 2;
  color: #333;
  font-weight: 500;
}

.score-value {
  font-weight: 700;
  color: #4CAF50;
  font-size: 18px;
}

.history-section {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  padding: 25px;
  margin-top: 25px;
  animation: slideIn 0.5s ease-out forwards;
  animation-delay: 0.3s;
  opacity: 0;
  transform: translateY(20px);
}

.history-section h2 {
  margin-top: 0;
  margin-bottom: 25px;
  font-size: 20px;
  color: #00004b;
  font-weight: 600;
}

table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 8px;
  overflow: hidden;
}

th, td {
  padding: 14px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  font-weight: 600;
  color: #444;
  background-color: #f9f9fc;
}

tr:hover td {
  background-color: #f5f7fa;
}

tr:last-child td {
  border-bottom: none;
}

.empty-state {
  padding: 40px 20px;
  text-align: center;
  color: #666;
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

.status-badge {
  display: inline-flex;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  align-items: center;
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

.info-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>