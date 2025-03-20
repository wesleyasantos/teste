<template>
  <div class="operation-detail">
    <div class="page-header">
      <h1>Operação #{{ operationId }}</h1>
      <div class="status-badge" :class="operation.status">
        {{ getStatusLabel(operation.status) }}
      </div>
    </div>
    
    <!-- Fluxo da operação -->
    <div class="operation-flow">
      <div 
        v-for="(stage, index) in operationStages" 
        :key="stage.id"
        :class="['flow-stage', { 
          active: isStageActive(stage.id), 
          completed: isStageCompleted(stage.id),
          current: currentStage === stage.id
        }]"
      >
        <div class="stage-indicator">
          <div class="stage-number">{{ index + 1 }}</div>
          <div class="stage-icon">
            <i :class="stage.icon"></i>
          </div>
        </div>
        <div class="stage-info">
          <div class="stage-name">{{ stage.name }}</div>
          <div class="stage-date" v-if="stageDates[stage.id]">
            {{ formatDate(stageDates[stage.id]) }}
          </div>
        </div>
        <div class="stage-connector" v-if="index < operationStages.length - 1"></div>
      </div>
    </div>
    
    <!-- Tabs de navegação -->
    <div class="operation-tabs">
      <button 
          v-for="tab in operationTabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="['tab-button', { active: activeTab === tab.id }]"
      >
          {{ tab.name }}
      </button>
      </div>
      
      <!-- Conteúdo da aba selecionada -->
      <div class="tab-content">
      <!-- Informações Básicas -->
      <div v-if="activeTab === 'info'" class="tab-pane">
          <div class="content-grid">
          <!-- Informações da operação -->
          <div class="info-card">
              <h2>Dados da Operação</h2>
              <div class="info-row">
              <span class="label">Valor:</span>
              <span class="value">R$ {{ formatCurrency(operation.amount) }}</span>
              </div>
              <div class="info-row">
              <span class="label">Modalidade:</span>
              <span class="value">{{ operation.modality }}</span>
              </div>
              <div class="info-row">
              <span class="label">Prazo:</span>
              <span class="value">{{ operation.term }} meses</span>
              </div>
              <div class="info-row">
              <span class="label">Taxa de Juros:</span>
              <span class="value">{{ operation.interest_rate }}% ao mês</span>
              </div>
              <div class="info-row">
              <span class="label">Sistema de Amortização:</span>
              <span class="value">{{ getAmortizationSystem(operation.amortization_system) }}</span>
              </div>
              <div class="info-row">
              <span class="label">Data da Solicitação:</span>
              <span class="value">{{ formatDate(operation.created_at) }}</span>
              </div>
              <div class="info-row">
              <span class="label">Status Atual:</span>
              <span class="value">
                  <span :class="'status-badge ' + operation.status">
                  {{ getStatusLabel(operation.status) }}
                  </span>
              </span>
              </div>
          </div>
          
          <!-- Informações do cliente -->
          <div class="info-card">
              <h2>Dados do Cliente</h2>
              <div class="info-row">
              <span class="label">Nome:</span>
              <span class="value">{{ client.name }}</span>
              </div>
              <div class="info-row">
              <span class="label">CPF/CNPJ:</span>
              <span class="value">{{ client.document }}</span>
              </div>
              <div class="info-row">
              <span class="label">Email:</span>
              <span class="value">{{ client.email }}</span>
              </div>
              <div class="info-row">
              <span class="label">Telefone:</span>
              <span class="value">{{ client.phone }}</span>
              </div>
              <div class="info-actions">
              <router-link :to="`/clients/${client.id}`" class="btn-view">
                  Ver Perfil Completo
              </router-link>
              </div>
          </div>
          </div>
      </div>
      
      <!-- Plano de Pagamento -->
      <div v-if="activeTab === 'payment'" class="tab-pane">
          <div class="payment-summary">
          <div class="summary-card">
              <div class="summary-title">Valor da Operação</div>
              <div class="summary-value">R$ {{ formatCurrency(operation.amount) }}</div>
          </div>
          <div class="summary-card">
              <div class="summary-title">Prazo</div>
              <div class="summary-value">{{ operation.term }} meses</div>
          </div>
          <div class="summary-card">
              <div class="summary-title">Taxa de Juros</div>
              <div class="summary-value">{{ operation.interest_rate }}% ao mês</div>
          </div>
          <div class="summary-card">
              <div class="summary-title">Primeira Parcela</div>
              <div class="summary-value">R$ {{ formatCurrency(firstInstallment) }}</div>
          </div>
          <div class="summary-card">
              <div class="summary-title">Valor Total</div>
              <div class="summary-value">R$ {{ formatCurrency(totalAmount) }}</div>
          </div>
          </div>
          
          <div class="table-container">
          <h3>Plano de Pagamento</h3>
          <table>
              <thead>
              <tr>
                  <th>Parcela</th>
                  <th>Data</th>
                  <th>Prestação</th>
                  <th>Amortização</th>
                  <th>Juros</th>
                  <th>Saldo Devedor</th>
                  <th>Status</th>
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
                  <td>
                  <span :class="'payment-status ' + row.status">
                      {{ getPaymentStatusLabel(row.status) }}
                  </span>
                  </td>
              </tr>
              </tbody>
          </table>
          </div>
      </div>
      
      <!-- Sócios -->
      <div v-if="activeTab === 'partners'" class="tab-pane">
          <div class="partners-header">
          <h2>Sócios e Administradores</h2>
          <button @click="showPartnerForm = true" class="btn-add">
              <i class="fas fa-plus"></i> Adicionar Sócio
          </button>
          </div>
          
          <div v-if="partners.length > 0" class="partners-grid">
          <div v-for="partner in partners" :key="partner.id" class="partner-card">
              <div class="partner-header">
              <div class="partner-name">{{ partner.name }}</div>
              <div class="partner-role-badge">{{ partner.role }}</div>
              </div>
              <div class="partner-info">
              <div class="info-item">
                  <span class="info-icon"><i class="fas fa-id-card"></i></span>
                  <span class="info-text">{{ partner.document }}</span>
              </div>
              <div class="info-item">
                  <span class="info-icon"><i class="fas fa-envelope"></i></span>
                  <span class="info-text">{{ partner.email }}</span>
              </div>
              <div class="info-item">
                  <span class="info-icon"><i class="fas fa-phone"></i></span>
                  <span class="info-text">{{ partner.phone }}</span>
              </div>
              <div class="info-item">
                  <span class="info-icon"><i class="fas fa-percentage"></i></span>
                  <span class="info-text">{{ partner.share }}% de participação</span>
              </div>
              </div>
              <div class="partner-actions">
              <button @click="editPartner(partner)" class="btn-edit">Editar</button>
              <button @click="removePartner(partner.id)" class="btn-delete">Remover</button>
              </div>
          </div>
          </div>
          
          <div v-else class="empty-state">
          <p>Nenhum sócio cadastrado para esta operação.</p>
          <button @click="showPartnerForm = true" class="btn-primary">Adicionar Sócio</button>
          </div>
          
          <!-- Modal de formulário de sócio -->
          <div v-if="showPartnerForm" class="modal">
          <div class="modal-content">
              <span @click="showPartnerForm = false" class="close">&times;</span>
              <h3>{{ editingPartner.id ? 'Editar Sócio' : 'Novo Sócio' }}</h3>
              <form @submit.prevent="savePartner">
              <div class="form-row">
                  <div class="form-group">
                  <label for="partner_name">Nome</label>
                  <input type="text" id="partner_name" v-model="editingPartner.name" required>
                  </div>
                  <div class="form-group">
                  <label for="partner_role">Cargo</label>
                  <select id="partner_role" v-model="editingPartner.role" required>
                      <option value="Sócio-Administrador">Sócio-Administrador</option>
                      <option value="Sócio">Sócio</option>
                      <option value="Administrador">Administrador</option>
                      <option value="Diretor">Diretor</option>
                  </select>
                  </div>
              </div>
              <div class="form-row">
                  <div class="form-group">
                  <label for="partner_document">CPF</label>
                  <input type="text" id="partner_document" v-model="editingPartner.document" required>
                  </div>
                  <div class="form-group">
                  <label for="partner_share">Participação (%)</label>
                  <input type="number" id="partner_share" v-model="editingPartner.share" min="0" max="100" required>
                  </div>
              </div>
              <div class="form-row">
                  <div class="form-group">
                  <label for="partner_email">Email</label>
                  <input type="email" id="partner_email" v-model="editingPartner.email" required>
                  </div>
                  <div class="form-group">
                  <label for="partner_phone">Telefone</label>
                  <input type="text" id="partner_phone" v-model="editingPartner.phone" required>
                  </div>
              </div>
              <div class="form-actions">
                  <button type="button" @click="showPartnerForm = false" class="btn-cancel">Cancelar</button>
                  <button type="submit" class="btn-save">Salvar</button>
              </div>
              </form>
          </div>
          </div>
      </div>
      
      <!-- Garantias -->
      <div v-if="activeTab === 'guarantees'" class="tab-pane">
          <div class="guarantees-header">
          <h2>Garantias</h2>
          <button @click="showGuaranteeForm = true" class="btn-add">
              <i class="fas fa-plus"></i> Adicionar Garantia
          </button>
          </div>
          
          <div v-if="guarantees.length > 0" class="guarantees-list">
          <div v-for="guarantee in guarantees" :key="guarantee.id" class="guarantee-card">
              <div class="guarantee-type-badge" :class="getGuaranteeTypeClass(guarantee.type)">
              {{ getGuaranteeTypeLabel(guarantee.type) }}
              </div>
              <div class="guarantee-info">
              <h3 class="guarantee-description">{{ guarantee.description }}</h3>
              <div class="info-grid">
                  <div class="info-item">
                  <span class="label">Valor:</span>
                  <span class="value">R$ {{ formatCurrency(guarantee.value) }}</span>
                  </div>
                  <div class="info-item">
                  <span class="label">Percentual da Operação:</span>
                  <span class="value">{{ calculateGuaranteePercentage(guarantee.value) }}%</span>
                  </div>
                  <div class="info-item" v-if="guarantee.registration_number">
                  <span class="label">Nº de Registro:</span>
                  <span class="value">{{ guarantee.registration_number }}</span>
                  </div>
                  <div class="info-item" v-if="guarantee.location">
                  <span class="label">Localização:</span>
                  <span class="value">{{ guarantee.location }}</span>
                  </div>
              </div>
              <div class="guarantee-notes" v-if="guarantee.notes">
                  <span class="label">Observações:</span>
                  <p>{{ guarantee.notes }}</p>
              </div>
              </div>
              <div class="guarantee-actions">
              <button @click="editGuarantee(guarantee)" class="btn-edit">Editar</button>
              <button @click="removeGuarantee(guarantee.id)" class="btn-delete">Remover</button>
              </div>
          </div>
          </div>
          
          <div v-else class="empty-state">
          <p>Nenhuma garantia cadastrada para esta operação.</p>
          <button @click="showGuaranteeForm = true" class="btn-primary">Adicionar Garantia</button>
          </div>
          
          <!-- Modal de formulário de garantia -->
          <div v-if="showGuaranteeForm" class="modal">
          <div class="modal-content">
              <span @click="showGuaranteeForm = false" class="close">&times;</span>
              <h3>{{ editingGuarantee.id ? 'Editar Garantia' : 'Nova Garantia' }}</h3>
              <form @submit.prevent="saveGuarantee">
              <div class="form-row">
                  <div class="form-group">
                  <label for="guarantee_type">Tipo de Garantia</label>
                  <select id="guarantee_type" v-model="editingGuarantee.type" required>
                      <option value="property">Imóvel</option>
                      <option value="vehicle">Veículo</option>
                      <option value="equipment">Equipamento</option>
                      <option value="financial">Aplicação Financeira</option>
                      <option value="endorsement">Aval/Fiança</option>
                      <option value="other">Outra</option>
                  </select>
                  </div>
                  <div class="form-group">
                  <label for="guarantee_value">Valor (R$)</label>
                  <input type="number" id="guarantee_value" v-model="editingGuarantee.value" min="0" step="0.01" required>
                  </div>
              </div>
              <div class="form-row">
                  <div class="form-group">
                  <label for="guarantee_description">Descrição</label>
                  <input type="text" id="guarantee_description" v-model="editingGuarantee.description" required>
                  </div>
                  <div class="form-group">
                  <label for="guarantee_registration">Nº de Registro (opcional)</label>
                  <input type="text" id="guarantee_registration" v-model="editingGuarantee.registration_number">
                  </div>
              </div>
              <div class="form-row">
                  <div class="form-group">
                  <label for="guarantee_location">Localização (opcional)</label>
                  <input type="text" id="guarantee_location" v-model="editingGuarantee.location">
                  </div>
              </div>
              <div class="form-row">
                  <div class="form-group" style="flex: 100%;">
                  <label for="guarantee_notes">Observações (opcional)</label>
                  <textarea id="guarantee_notes" v-model="editingGuarantee.notes" rows="3"></textarea>
                  </div>
              </div>
              <div class="form-actions">
                  <button type="button" @click="showGuaranteeForm = false" class="btn-cancel">Cancelar</button>
                  <button type="submit" class="btn-save">Salvar</button>
              </div>
              </form>
          </div>
          </div>
      </div>
      
      <!-- Documentos -->
      <div v-if="activeTab === 'documents'" class="tab-pane">
          <div class="documents-header">
          <h2>Documentos</h2>
          <button @click="showDocumentUpload = true" class="btn-add">
              <i class="fas fa-plus"></i> Adicionar Documento
          </button>
          </div>
          
          <div v-if="documents.length > 0" class="documents-grid">
          <div v-for="document in documents" :key="document.id" class="document-card">
              <div class="document-icon">
              <i :class="getDocumentIcon(document.type)"></i>
              </div>
              <div class="document-info">
              <div class="document-name">{{ document.name }}</div>
              <div class="document-meta">
                  <span class="document-type">{{ getDocumentTypeLabel(document.type) }}</span>
                  <span class="document-date">{{ formatDate(document.uploaded_at) }}</span>
              </div>
              </div>
              <div class="document-actions">
              <a :href="document.file" target="_blank" class="btn-view">Visualizar</a>
              <button @click="removeDocument(document.id)" class="btn-delete">Remover</button>
              </div>
          </div>
          </div>
          
          <div v-else class="empty-state">
          <p>Nenhum documento adicionado para esta operação.</p>
          <button @click="showDocumentUpload = true" class="btn-primary">Adicionar Documento</button>
          </div>
          
          <!-- Modal de upload de documento -->
          <div v-if="showDocumentUpload" class="modal">
          <div class="modal-content">
              <span @click="showDocumentUpload = false" class="close">&times;</span>
              <h3>Adicionar Documento</h3>
              <form @submit.prevent="uploadDocument">
              <div class="form-row">
                  <div class="form-group">
                  <label for="document_type">Tipo de Documento</label>
                  <select id="document_type" v-model="uploadingDocument.type" required>
                      <option value="authorization">Termo de Autorização</option>
                      <option value="id">Documento de Identificação</option>
                      <option value="income">Comprovante de Renda</option>
                      <option value="residence">Comprovante de Residência</option>
                      <option value="bank_statement">Extrato Bancário</option>
                      <option value="tax_return">Declaração de IR</option>
                      <option value="business">Documentos Empresariais</option>
                      <option value="other">Outro</option>
                  </select>
                  </div>
                  <div class="form-group">
                  <label for="document_name">Nome do Documento</label>
                  <input type="text" id="document_name" v-model="uploadingDocument.name" required>
                  </div>
              </div>
              <div class="form-row">
                  <div class="form-group" style="flex: 100%;">
                  <label for="document_file">Arquivo</label>
                  <div class="file-upload">
                      <input type="file" id="document_file" @change="handleFileChange" required>
                      <label for="document_file" class="file-upload-btn">
                      <i class="fas fa-upload"></i> Selecionar Arquivo
                      </label>
                      <span class="file-info">{{ fileUploadInfo }}</span>
                  </div>
                  </div>
              </div>
              <div class="form-row">
                  <div class="form-group" style="flex: 100%;">
                  <label for="document_notes">Observações (opcional)</label>
                  <textarea id="document_notes" v-model="uploadingDocument.notes" rows="2"></textarea>
                  </div>
              </div>
              <div class="form-actions">
                  <button type="button" @click="showDocumentUpload = false" class="btn-cancel">Cancelar</button>
                  <button type="submit" class="btn-upload">Enviar Documento</button>
              </div>
              </form>
          </div>
          </div>
      </div>
      
      <!-- Análise de Crédito -->
      <div v-if="activeTab === 'analysis'" class="tab-pane">
          <div class="analysis-section">
          <h2>Análise de Crédito</h2>
          
          <div class="analysis-tabs">
              <button 
              v-for="tab in analysisTabs" 
              :key="tab.id"
              @click="activeAnalysisTab = tab.id"
              :class="['analysis-tab-button', { active: activeAnalysisTab === tab.id }]"
              >
              {{ tab.name }}
              </button>
          </div>
          
          <div class="analysis-content">
              <!-- PGDAS -->
              <div v-if="activeAnalysisTab === 'pgdas'" class="analysis-pane">
              <h3>PGDAS - Faturamento Mensal</h3>
              
              <div class="data-input-section">
                  <div class="form-row">
                  <div class="form-group" style="flex: 100%;">
                      <label>Selecione o Setor</label>
                      <div class="radio-group">
                      <label class="radio-label">
                          <input type="radio" v-model="analysis.sector" value="commerce"> Comércio (75%)
                      </label>
                      <label class="radio-label">
                          <input type="radio" v-model="analysis.sector" value="service"> Serviço (70%)
                      </label>
                      <label class="radio-label">
                          <input type="radio" v-model="analysis.sector" value="transport"> Transporte (85%)
                      </label>
                      <label class="radio-label">
                          <input type="radio" v-model="analysis.sector" value="industry"> Indústria/Posto de Combustível (90%)
                      </label>
                      </div>
                  </div>
                  </div>
                  
                  <table class="input-table">
                  <thead>
                      <tr>
                      <th>Mês</th>
                      <th>Faturamento (R$)</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="(month, index) in months" :key="month">
                      <td>{{ month }}</td>
                      <td>
                          <input 
                          type="number" 
                          v-model="analysis.pgdas[index]" 
                          min="0" 
                          step="0.01"
                          @input="calculateAnalysis"
                          >
                      </td>
                      </tr>
                      <tr class="total-row">
                      <td>Total</td>
                      <td>R$ {{ formatCurrency(analysis.pgdasTotal) }}</td>
                      </tr>
                  </tbody>
                  </table>
              </div>
              </div>
              
              <!-- Despesas Financeiras -->
              <div v-if="activeAnalysisTab === 'expenses'" class="analysis-pane">
              <h3>Despesas Financeiras</h3>
              
              <table class="input-table">
                  <thead>
                  <tr>
                      <th>Tipo de Despesa</th>
                      <th>Valor (R$)</th>
                      <th>Percentual</th>
                      <th>Resultado</th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr v-for="(expense, key) in analysis.financialExpenses" :key="key">
                      <td>{{ expense.name }}</td>
                      <td>
                      <input 
                          type="number" 
                          v-model="expense.value" 
                          min="0" 
                          step="0.01"
                          @input="calculateAnalysis"
                      >
                      </td>
                      <td>{{ expense.percentage }}%</td>
                      <td>R$ {{ formatCurrency(expense.result) }}</td>
                  </tr>
                  <tr class="total-row">
                      <td colspan="3">Total</td>
                      <td>R$ {{ formatCurrency(analysis.financialExpensesTotal) }}</td>
                  </tr>
                  </tbody>
              </table>
              </div>
              
              <!-- Reposição Mensal -->
              <div v-if="activeAnalysisTab === 'repayment'" class="analysis-pane">
              <h3>Reposição Mensal</h3>
              
              <div class="data-input-section">
                  <h4>Valores a Vencer (Curto Prazo)</h4>
                  <table class="input-table">
                  <thead>
                      <tr>
                      <th>Período</th>
                      <th>Valor (R$)</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="(period, key) in analysis.shortTerm" :key="key">
                      <td>{{ period.name }}</td>
                      <td>
                          <input 
                          type="number" 
                          v-model="period.value" 
                          min="0" 
                          step="0.01"
                          @input="calculateAnalysis"
                          >
                      </td>
                      </tr>
                      <tr class="total-row">
                      <td>Total Curto Prazo</td>
                      <td>R$ {{ formatCurrency(analysis.shortTermTotal) }}</td>
                      </tr>
                  </tbody>
                  </table>
                  
                  <h4>Modalidade Futuro</h4>
                  <table class="input-table">
                  <thead>
                      <tr>
                      <th>Tipo</th>
                      <th>Valor (R$)</th>
                      </tr>
                  </thead>
                  <tbody>
                      <tr v-for="(future, key) in analysis.futureModality" :key="key">
                      <td>{{ future.name }}</td>
                      <td>
                          <input 
                          type="number" 
                          v-model="future.value" 
                          min="0" 
                          step="0.01"
                          @input="calculateAnalysis"
                          >
                      </td>
                      </tr>
                      <tr class="total-row">
                      <td>Total Modalidade Futuro</td>
                      <td>R$ {{ formatCurrency(analysis.futureModalityTotal) }}</td>
                      </tr>
                  </tbody>
                  </table>
                  
                  <div class="calculation-result">
                  <div class="result-item">
                      <span class="result-label">Reposição Mensal = (Curto Prazo - Modalidade Futuro) / 12</span>
                      <span class="result-value">R$ {{ formatCurrency(analysis.monthlyRepayment) }}</span>
                  </div>
                  </div>
              </div>
              </div>
              
              <!-- Resultados -->
              <div v-if="activeAnalysisTab === 'results'" class="analysis-pane">
              <h3>Resultados da Análise</h3>
              
              <div class="results-grid">
                  <div class="result-card">
                  <div class="result-title">Receita Operacional Bruta (ROB)</div>
                  <div class="result-value">R$ {{ formatCurrency(analysis.pgdasTotal) }}</div>
                  </div>
                  
                  <div class="result-card">
                  <div class="result-title">Despesa Setorial ({{ getSectorPercentage() }}%)</div>
                  <div class="result-value">R$ {{ formatCurrency(analysis.sectorExpense) }}</div>
                  <div class="calculation-note">{{ getSectorPercentage() }}% do ROB</div>
                  </div>
                  
                  <div class="result-card">
                  <div class="result-title">Lucro Bruto</div>
                  <div class="result-value">R$ {{ formatCurrency(analysis.grossProfit) }}</div>
                  <div class="calculation-note">ROB - Despesa Setorial</div>
                  </div>
                  
                  <div class="result-card">
                  <div class="result-title">Disponibilidade Mensal 1</div>
                  <div class="result-value">R$ {{ formatCurrency(analysis.availability1) }}</div>
                  <div class="calculation-note">(Lucro Bruto - Despesas Financeiras) / 12</div>
                  </div>
                  
                  <div class="result-card">
                  <div class="result-title">Disponibilidade Mensal 2</div>
                  <div class="result-value">R$ {{ formatCurrency(analysis.availability2) }}</div>
                  <div class="calculation-note">Disponibilidade Mensal 1 - Reposição Mensal</div>
                  </div>
                  
                  <div class="result-card highlight">
                  <div class="result-title">Parcela Mensal da Operação</div>
                  <div class="result-value">R$ {{ formatCurrency(firstInstallment) }}</div>
                  </div>
                  
                  <div class="result-card" :class="{'positive': analysis.surplus > 0, 'negative': analysis.surplus < 0}">
                  <div class="result-title">Superávit / Déficit</div>
                  <div class="result-value">R$ {{ formatCurrency(analysis.surplus) }}</div>
                  <div class="calculation-note">Disponibilidade Mensal 2 - Parcela Mensal</div>
                  </div>
                  
                  <div class="result-card decision">
                  <div class="result-title">Resultado da Análise</div>
                  <div class="result-decision" :class="{'approved': analysis.approved, 'rejected': !analysis.approved}">
                      {{ analysis.approved ? 'APROVADO' : 'REPROVADO' }}
                  </div>
                  <div class="decision-note">
                      {{ getAnalysisDecisionNote() }}
                  </div>
                  </div>
              </div>
              
              <div class="analysis-actions">
                  <button @click="saveAnalysis" class="btn-save">Salvar Análise</button>
                  <button @click="generateReport" class="btn-report">Gerar Relatório</button>
              </div>
              </div>

              <!-- IA -->
              <div v-if="activeAnalysisTab === 'ai'" class="analysis-pane">
              <h3>Assistente de Análise de Crédito (IA)</h3>
              
              <div class="ai-section">
                  <div class="ai-header">
                  <div class="ai-badge">Análise automatizada</div>
                  <button @click="generateAIAnalysis" class="btn-ai" :disabled="isGeneratingAI">
                      <i class="fas fa-robot"></i>
                      {{ isGeneratingAI ? 'Gerando análise...' : 'Gerar nova análise' }}
                  </button>
                  </div>
                  
                  <div v-if="aiAnalysis.recommendation" class="ai-result">
                  <div class="recommendation-box" :class="getAIRecommendationClass()">
                      <h4>{{ aiAnalysis.recommendation.split(':')[0] }}</h4>
                      <p>{{ aiAnalysis.recommendation.split(':')[1] }}</p>
                  </div>
                  
                  <div class="risk-indicator">
                      <div class="risk-label">Risco da Operação:</div>
                      <div class="risk-meter">
                      <div class="risk-bar" :style="{ width: `${aiAnalysis.risk_score}%` }"></div>
                      </div>
                      <div class="risk-value">
                      {{ aiAnalysis.risk_score }}% 
                      <span class="risk-note">(menor = melhor)</span>
                      </div>
                  </div>
                  
                  <div class="ai-explanation">
                      <h4>Análise Detalhada</h4>
                      <pre>{{ aiAnalysis.explanation }}</pre>
                  </div>
                  </div>
                  
                  <div v-else class="ai-empty-state">
                  <p>Ainda não há análise de IA para esta operação.</p>
                  <p>Clique no botão "Gerar nova análise" para que a IA avalie os dados disponíveis e forneça uma recomendação.</p>
                  </div>
              </div>
              </div>
          </div>
          </div>
      </div>
      
      <!-- Comitê de Crédito -->
      <div v-if="activeTab === 'committee'" class="tab-pane">
          <div class="committee-section">
          <h2>Comitê de Crédito</h2>
          
          <div class="committee-status">
              <div class="status-indicator" :class="committee.status">
              <i class="fas" :class="getCommitteeStatusIcon()"></i>
              <span>{{ getCommitteeStatusLabel() }}</span>
              </div>
              
              <div class="committee-info">
              <div v-if="committee.status === 'pending'" class="committee-pending">
                  <p>Esta operação está aguardando avaliação do comitê de crédito.</p>
                  <button @click="startCommittee" class="btn-start-committee">Iniciar Comitê</button>
              </div>
              
              <div v-if="committee.status === 'in_progress'" class="committee-in-progress">
                  <p>Comitê iniciado em {{ formatDate(committee.started_at) }}.</p>
                  <p>Aguardando votos dos membros do comitê.</p>
              </div>
              
              <div v-if="committee.status === 'completed'" class="committee-completed">
                  <p>Comitê finalizado em {{ formatDate(committee.completed_at) }}.</p>
                  <p>Decisão: 
                  <span class="decision-badge" :class="committee.decision">
                      {{ committee.decision === 'approved' ? 'Aprovado' : 'Reprovado' }}
                  </span>
                  </p>
              </div>
              </div>
          </div>
          
          <div v-if="committee.status !== 'pending'" class="committee-members">
              <h3>Membros do Comitê</h3>
              
              <table class="committee-table">
              <thead>
                  <tr>
                  <th>Membro</th>
                  <th>Cargo</th>
                  <th>Voto</th>
                  <th>Data</th>
                  <th>Observações</th>
                  </tr>
              </thead>
              <tbody>
                  <tr v-for="member in committee.members" :key="member.id">
                  <td>{{ member.name }}</td>
                  <td>{{ member.role }}</td>
                  <td>
                      <span v-if="member.vote" class="vote-badge" :class="member.vote">
                      {{ member.vote === 'approve' ? 'Aprovado' : 'Reprovado' }}
                      </span>
                      <span v-else class="vote-badge pending">Pendente</span>
                  </td>
                  <td>{{ member.voted_at ? formatDate(member.voted_at) : '-' }}</td>
                  <td>{{ member.notes || '-' }}</td>
                  </tr>
              </tbody>
              </table>
          </div>
          
          <div v-if="canVote" class="committee-voting">
              <h3>Seu Voto</h3>
              
              <form @submit.prevent="submitVote" class="vote-form">
              <div class="vote-options">
                  <label class="vote-option">
                  <input type="radio" v-model="voting.vote" value="approve">
                  <span class="vote-label approve">Aprovar</span>
                  </label>
                  <label class="vote-option">
                  <input type="radio" v-model="voting.vote" value="reject">
                  <span class="vote-label reject">Reprovar</span>
                  </label>
              </div>
              
              <div class="form-row">
                  <div class="form-group" style="flex: 100%;">
                  <label for="vote_notes">Observações</label>
                  <textarea id="vote_notes" v-model="voting.notes" rows="3"></textarea>
                  </div>
              </div>
              
              <div class="form-actions">
                  <button type="submit" class="btn-vote" :disabled="!voting.vote">Registrar Voto</button>
              </div>
              </form>
          </div>
          
          <div v-if="committee.status === 'in_progress' && isCommitteeManager" class="committee-management">
              <h3>Gerenciamento do Comitê</h3>
              <p>Como gerente, você pode finalizar o comitê manualmente.</p>
              <button @click="finishCommittee" class="btn-finish-committee">Finalizar Comitê</button>
          </div>
          </div>
      </div>
      
      <!-- Formalização -->
      <div v-if="activeTab === 'formalization'" class="tab-pane">
          <div class="formalization-section">
          <h2>Formalização da Proposta</h2>
          
          <div class="formalization-status">
              <div class="status-indicator" :class="formalization.status">
              <i class="fas" :class="getFormalizationStatusIcon()"></i>
              <span>{{ getFormalizationStatusLabel() }}</span>
              </div>
          </div>
          
          <div class="contract-info">
              <h3>Contrato</h3>
              
              <div v-if="formalization.status === 'pending'" class="formalization-actions">
              <p>Operação aprovada pelo comitê. Agora é necessário gerar o contrato para formalização.</p>
              <button @click="generateContract" class="btn-generate">Gerar Contrato</button>
              </div>
              
              <div v-if="formalization.contract" class="contract-details">
              <div class="info-row">
                  <span class="label">Número do Contrato:</span>
                  <span class="value">{{ formalization.contract.number }}</span>
              </div>
              <div class="info-row">
                  <span class="label">Gerado em:</span>
                  <span class="value">{{ formatDate(formalization.contract.generated_at) }}</span>
              </div>
              <div class="info-row">
                  <span class="label">Status:</span>
                  <span class="value">
                  <span class="contract-status" :class="formalization.contract.status">
                      {{ getContractStatusLabel(formalization.contract.status) }}
                  </span>
                  </span>
              </div>
              
              <div class="contract-document">
                  <a :href="formalization.contract.file" target="_blank" class="btn-view-contract">
                  <i class="fas fa-file-contract"></i> Visualizar Contrato
                  </a>
              </div>
              </div>
          </div>
          
          <div v-if="formalization.contract" class="signature-section">
              <h3>Assinaturas</h3>
              
              <table class="signatures-table">
              <thead>
                  <tr>
                  <th>Signatário</th>
                  <th>Email</th>
                  <th>Status</th>
                  <th>Data</th>
                  <th>Ações</th>
                  </tr>
              </thead>
              <tbody>
                  <tr v-for="signature in formalization.signatures" :key="signature.id">
                  <td>{{ signature.name }}</td>
                  <td>{{ signature.email }}</td>
                  <td>
                      <span class="signature-status" :class="signature.status">
                      {{ getSignatureStatusLabel(signature.status) }}
                      </span>
                  </td>
                  <td>{{ signature.signed_at ? formatDate(signature.signed_at) : '-' }}</td>
                  <td>
                      <button 
                      v-if="signature.status === 'pending'" 
                      @click="sendSignatureReminder(signature.id)" 
                      class="btn-remind"
                      >
                      Reenviar
                      </button>
                  </td>
                  </tr>
              </tbody>
              </table>
              
              <div class="form-actions">
              <button 
                  v-if="canReleaseCredit" 
                  @click="releaseCredit" 
                  class="btn-release"
              >
                  Liberar Crédito
              </button>
              </div>
          </div>
          </div>
      </div>
      
      <!-- Acompanhamento -->
      <div v-if="activeTab === 'monitoring'" class="tab-pane">
          <div class="monitoring-section">
          <h2>Acompanhamento do Crédito</h2>
          
          <div class="monitoring-summary">
              <div class="summary-card">
              <div class="summary-title">Data de Liberação</div>
              <div class="summary-value">{{ formalization.credit_release_date ? formatDate(formalization.credit_release_date) : 'Não liberado' }}</div>
              </div>
              <div class="summary-card">
              <div class="summary-title">Valor Liberado</div>
              <div class="summary-value">R$ {{ formatCurrency(operation.amount) }}</div>
              </div>
              <div class="summary-card">
              <div class="summary-title">Próxima Parcela</div>
              <div class="summary-value">{{ getNextInstallmentDate() }}</div>
              </div>
              <div class="summary-card">
              <div class="summary-title">Valor da Próxima Parcela</div>
              <div class="summary-value">R$ {{ formatCurrency(getNextInstallmentAmount()) }}</div>
              </div>
              <div class="summary-card">
              <div class="summary-title">Status da Operação</div>
              <div class="summary-value">
                  <span class="monitoring-status" :class="operation.monitoring_status || 'normal'">
                  {{ getMonitoringStatusLabel() }}
                  </span>
              </div>
              </div>
          </div>
          
          <div class="installments-tracking">
              <h3>Parcelas</h3>
              
              <table class="installments-table">
              <thead>
                  <tr>
                  <th>Parcela</th>
                  <th>Vencimento</th>
                  <th>Valor</th>
                  <th>Status</th>
                  <th>Pagamento</th>
                  <th>Dias em Atraso</th>
                  <th>Ações</th>
                  </tr>
              </thead>
              <tbody>
                  <tr v-for="installment in paymentPlan" :key="installment.installment">
                  <td>{{ installment.installment }}</td>
                  <td>{{ formatDate(installment.date) }}</td>
                  <td>R$ {{ formatCurrency(installment.payment) }}</td>
                  <td>
                      <span class="payment-status" :class="installment.status">
                      {{ getPaymentStatusLabel(installment.status) }}
                      </span>
                  </td>
                  <td>{{ installment.payment_date ? formatDate(installment.payment_date) : '-' }}</td>
                  <td>{{ calculateOverdueDays(installment) }}</td>
                  <td>
                      <button 
                      v-if="installment.status === 'pending' || installment.status === 'overdue'"
                      @click="recordPayment(installment)"
                      class="btn-record-payment"
                      >
                      Registrar Pagamento
                      </button>
                  </td>
                  </tr>
              </tbody>
              </table>
          </div>
          
          <!-- Modal de registro de pagamento -->
          <div v-if="showPaymentModal" class="modal">
              <div class="modal-content">
              <span @click="showPaymentModal = false" class="close">&times;</span>
              <h3>Registrar Pagamento</h3>
              <form @submit.prevent="confirmPayment">
                  <div class="form-row">
                  <div class="form-group">
                      <label for="payment_date">Data do Pagamento</label>
                      <input type="date" id="payment_date" v-model="paymentData.date" required>
                  </div>
                  <div class="form-group">
                      <label for="payment_amount">Valor Pago</label>
                      <input type="number" id="payment_amount" v-model="paymentData.amount" min="0" step="0.01" required>
                  </div>
                  </div>
                  <div class="form-row">
                  <div class="form-group">
                      <label for="payment_method">Forma de Pagamento</label>
                      <select id="payment_method" v-model="paymentData.method" required>
                      <option value="bank_transfer">Transferência Bancária</option>
                      <option value="deposit">Depósito</option>
                      <option value="debit">Débito Automático</option>
                      <option value="pix">PIX</option>
                      <option value="other">Outro</option>
                      </select>
                  </div>
                  </div>
                  <div class="form-row">
                  <div class="form-group" style="flex: 100%;">
                      <label for="payment_notes">Observações</label>
                      <textarea id="payment_notes" v-model="paymentData.notes" rows="2"></textarea>
                  </div>
                  </div>
                  <div class="form-actions">
                  <button type="button" @click="showPaymentModal = false" class="btn-cancel">Cancelar</button>
                  <button type="submit" class="btn-confirm">Confirmar Pagamento</button>
                  </div>
              </form>
              </div>
          </div>
          </div>
      </div>
      </div>
      
      <!-- Ações disponíveis baseadas no estágio atual -->
      <div class="stage-actions">
      <div v-if="operation.status === 'pending'">
          <button @click="moveToStage('verification')" class="btn-primary">Enviar para Conferência</button>
      </div>
      
      <div v-if="operation.status === 'verification'">
          <button @click="verifyOperation" class="btn-primary">Confirmar Verificação</button>
      </div>
      
      <div v-if="operation.status === 'analysis' && analysis.approved !== null">
          <button @click="moveToStage('committee')" class="btn-primary">Enviar para Comitê</button>
      </div>
      
      <div v-if="operation.status === 'committee' && committee.status === 'completed' && committee.decision === 'approved'">
          <button @click="moveToStage('formalization')" class="btn-primary">Enviar para Formalização</button>
      </div>
      
      <div v-if="operation.status === 'formalization' && formalization.contract && areAllSignaturesCompleted">
          <button @click="moveToStage('monitoring')" class="btn-success">Iniciar Acompanhamento</button>
      </div>
      </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '../../services/api';
import reportService from '../../services/report.js';

export default {
  name: 'OperationDetail',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const operationId = ref(parseInt(route.params.id));
    
    // Dados da operação e cliente
    const operation = ref({});
    const client = ref({});
    
    // Estágio atual e datas dos estágios
    const currentStage = ref('');
    const stageDates = ref({});
    
    // Abas
    const activeTab = ref('info');
    const activeAnalysisTab = ref('pgdas');
    
    // Dados do plano de pagamento
    const firstInstallment = ref(0);
    const totalAmount = ref(0);
    const paymentPlan = ref([]);
    
    // Sócios e garantias
    const partners = ref([]);
    const guarantees = ref([]);
    const documents = ref([]);
    
    // Modais
    const showPartnerForm = ref(false);
    const showGuaranteeForm = ref(false);
    const showDocumentUpload = ref(false);
    const showPaymentModal = ref(false);
    
    // Formulários
    const editingPartner = reactive({
      id: null,
      operation: null,
      name: '',
      role: '',
      document: '',
      email: '',
      phone: '',
      share: 0
    });
    
    const editingGuarantee = reactive({
      id: null,
      operation: null,
      type: '',
      value: 0,
      description: '',
      registration_number: '',
      location: '',
      notes: ''
    });
    
    const uploadingDocument = reactive({
      operation: null,
      type: '',
      name: '',
      file: null,
      notes: ''
    });
    
    const fileUploadInfo = ref('Nenhum arquivo selecionado');
    
    // Análise de crédito
    const months = [
      'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
      'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ];
    
    const analysis = reactive({
      id: null,
      operation: null,
      sector: 'commerce',
      pgdas_data: {},
      financial_expenses: {},
      short_term_data: {},
      future_modality_data: {},
      pgdas_total: 0,
      financial_expenses_total: 0,
      short_term_total: 0,
      future_modality_total: 0,
      monthly_repayment: 0,
      sector_expense: 0,
      gross_profit: 0,
      availability1: 0,
      availability2: 0,
      surplus: 0,
      approved: null,
      analyst: null,
      notes: ''
    });
    
    // Inicializar dados da análise
    const initAnalysisData = () => {
      // Inicializar PGDAS
      for (let i = 0; i < months.length; i++) {
        analysis.pgdas_data[i] = 0;
      }
      
      // Inicializar despesas financeiras
      analysis.financial_expenses = {
        overdraft: { name: 'Cheque Especial', value: 0, percentage: 7, result: 0 },
        advance: { name: 'Adiantamento ao Depositante', value: 0, percentage: 15, result: 0 },
        guaranteed: { name: 'Conta Garantida', value: 0, percentage: 3.90, result: 0 },
        workingCapital: { name: 'Capital de Giro com Teto Rotativo', value: 0, percentage: 2.70, result: 0 },
        checkDiscount: { name: 'Desconto de Cheques', value: 0, percentage: 2.67, result: 0 },
        duplicateDiscount: { name: 'Desconto de Duplicatas', value: 0, percentage: 2.08, result: 0 },
        creditCard: { name: 'Desconto Antecipação de Cartão de Crédito', value: 0, percentage: 1.21, result: 0 },
        receivables: { name: 'Recebíveis Adquiridos', value: 0, percentage: 2.08, result: 0 }
      };
      
      // Inicializar curto prazo
      analysis.short_term_data = {
        days30: { name: 'a Vencer até 30 dias', value: 0 },
        days60: { name: 'a Vencer de 31 a 60 dias', value: 0 },
        days90: { name: 'a Vencer de 61 a 90 dias', value: 0 },
        days180: { name: 'a Vencer de 91 a 180 dias', value: 0 },
        days360: { name: 'a Vencer de 181 a 360 dias', value: 0 }
      };
      
      // Inicializar modalidade futuro
      analysis.future_modality_data = {
        overdraft: { name: 'Cheque Especial', value: 0 },
        advance: { name: 'Adiantamento ao Depositante', value: 0 },
        guaranteed: { name: 'Conta Garantida', value: 0 },
        checkDiscount: { name: 'Desconto de Cheques', value: 0 },
        duplicateDiscount: { name: 'Desconto de Duplicatas', value: 0 },
        creditCard: { name: 'Antecipação de Fatura de Cartão', value: 0 }
      };
    };
    
    // Análise de IA
    const aiAnalysis = reactive({
      risk_score: 0,
      default_probability: 0,
      recommendation: '',
      explanation: ''
    });
    
    const isGeneratingAI = ref(false);
    
    // Comitê de crédito
    const committee = reactive({
      id: null,
      operation: null,
      status: 'pending',
      started_at: null,
      completed_at: null,
      decision: null,
      members: []
    });
    
    const voting = reactive({
      vote: '',
      notes: ''
    });
    
    // Formalização
    const formalization = reactive({
      status: 'pending',
      contract: null,
      signatures: [],
      credit_release_date: null
    });
    
    // Pagamento
    const paymentData = reactive({
      installment: null,
      date: new Date().toISOString().split('T')[0],
      amount: 0,
      method: 'bank_transfer',
      notes: ''
    });
    
    // Estágios da operação
    const operationStages = [
      { id: 'pending', name: 'Cadastro', icon: 'fas fa-file-alt' },
      { id: 'verification', name: 'Conferência', icon: 'fas fa-check-double' },
      { id: 'analysis', name: 'Análise de Crédito', icon: 'fas fa-chart-line' },
      { id: 'committee', name: 'Comitê de Crédito', icon: 'fas fa-users' },
      { id: 'formalization', name: 'Formalização', icon: 'fas fa-file-signature' },
      { id: 'monitoring', name: 'Acompanhamento', icon: 'fas fa-chart-bar' }
    ];
    
    // Abas da operação
    const operationTabs = [
      { id: 'info', name: 'Informações Básicas' },
      { id: 'payment', name: 'Plano de Pagamento' },
      { id: 'partners', name: 'Sócios' },
      { id: 'guarantees', name: 'Garantias' },
      { id: 'documents', name: 'Documentos' },
      { id: 'analysis', name: 'Análise de Crédito' },
      { id: 'committee', name: 'Comitê de Crédito' },
      { id: 'formalization', name: 'Formalização' },
      { id: 'monitoring', name: 'Acompanhamento' }
    ];
    
    // Abas da análise
    const analysisTabs = [
      { id: 'pgdas', name: 'PGDAS' },
      { id: 'expenses', name: 'Despesas Financeiras' },
      { id: 'repayment', name: 'Reposição Mensal' },
      { id: 'results', name: 'Resultados' },
      { id: 'ai', name: 'IA' }
    ];
    
    // Buscar dados da operação
    const fetchOperation = async () => {
      try {
        loading.value = true;
        
        console.log(`Buscando operação com ID: ${operationId.value}`);
        const response = await api.operations.getOperation(operationId.value);
        
        console.log('Resposta da API de detalhes da operação:', response.data);
        
        if (response.data) {
          operation.value = response.data;
          
          // Definir estágio atual
          currentStage.value = operation.value.status;
          
          // Definir datas dos estágios
          stageDates.value = {
            pending: operation.value.pending_date,
            verification: operation.value.verification_date,
            analysis: operation.value.analysis_date,
            committee: operation.value.committee_date,
            formalization: operation.value.formalization_date,
            monitoring: operation.value.monitoring_date
          };
          
          // Buscar dados relacionados
          await fetchClient(operation.value.client);
          await fetchInstallments();
          await fetchPartners();
          await fetchGuarantees();
          await fetchDocuments();
          await fetchAnalysis();
          await fetchCommittee();
          await fetchFormalization();
        }
      } catch (error) {
        console.error('Erro ao buscar operação:', error);
        
        // Tentativa de recuperação com dados locais
        const localOperations = JSON.parse(localStorage.getItem('operations') || '[]');
        const localOperation = localOperations.find(op => op.id === parseInt(operationId.value));
        
        if (localOperation) {
          console.log('Usando dados locais para operação:', localOperation);
          operation.value = localOperation;
          currentStage.value = operation.value.status || 'pending';
        } else {
          alert('Erro ao carregar operação. Tente novamente ou crie uma nova operação.');
        }
      } finally {
        loading.value = false;
      }
    };
    
    // Buscar cliente
    const fetchClient = async (clientId) => {
      try {
        const response = await api.clients.getClient(clientId);
        client.value = response.data;
      } catch (error) {
        console.error('Erro ao buscar cliente:', error);
      }
    };
    
    // Buscar parcelas
    const fetchInstallments = async () => {
      try {
        const response = await api.operations.getInstallments(operationId.value);
        paymentPlan.value = response.data;
        
        if (paymentPlan.value.length > 0) {
          firstInstallment.value = paymentPlan.value[0].amount;
          totalAmount.value = paymentPlan.value.reduce((total, item) => total + parseFloat(item.amount), 0);
        }
      } catch (error) {
        console.error('Erro ao buscar parcelas:', error);
      }
    };
    
    // Buscar sócios
    const fetchPartners = async () => {
      try {
        const response = await api.partners.getPartners({ operation: operationId.value });
        partners.value = response.data.results;
      } catch (error) {
        console.error('Erro ao buscar sócios:', error);
      }
    };
    
    // Buscar garantias
    const fetchGuarantees = async () => {
      try {
        const response = await api.guarantees.getGuarantees({ operation: operationId.value });
        guarantees.value = response.data.results;
      } catch (error) {
        console.error('Erro ao buscar garantias:', error);
      }
    };
    
    // Buscar documentos
    const fetchDocuments = async () => {
      try {
        const response = await api.documents.getDocuments({ operation: operationId.value });
        documents.value = response.data.results;
      } catch (error) {
        console.error('Erro ao buscar documentos:', error);
      }
    };
    
    // Buscar análise
    const fetchAnalysis = async () => {
      try {
        const response = await api.analyses.getAnalyses({ operation: operationId.value });
        
        if (response.data.results && response.data.results.length > 0) {
          // Usar os dados da análise existente
          const analysisData = response.data.results[0];
          Object.assign(analysis, analysisData);
        } else {
          // Inicializar dados para nova análise
          initAnalysisData();
          analysis.operation = operationId.value;
        }
        
        // Buscar análise de IA se existir
        fetchAIAnalysis();
      } catch (error) {
        console.error('Erro ao buscar análise:', error);
      }
    };
    
    // Buscar análise de IA
    const fetchAIAnalysis = async () => {
      try {
        // No MVP, apenas simulamos uma análise de IA
        aiAnalysis.risk_score = 35.8;
        aiAnalysis.default_probability = 0.358;
        aiAnalysis.recommendation = "APROVADO COM CONDIÇÕES: Bom candidato, mas considerar redução do valor ou aumento do prazo.";
        aiAnalysis.explanation = 
          "Score de risco: 35.80/100 (quanto menor, melhor)\n\n" +
          "Análise de capacidade de pagamento:\n" +
          "- Valor da parcela: R$ " + formatCurrency(firstInstallment.value) + "\n" +
          "- Comprometimento: 72.22% da disponibilidade mensal\n\n" +
          "Principais fatores para a decisão:\n" +
          "- POSITIVO: Score de crédito adequado (825)\n" +
          "- POSITIVO: Histórico de operações anteriores sem atrasos\n" +
          "- NEUTRO: Valor solicitado dentro da capacidade financeira do cliente\n" +
          "- ALERTA: Alto comprometimento da disponibilidade mensal\n\n" +
          "Recomendações:\n" +
          "- Considerar aumento do prazo para reduzir o valor da parcela\n" +
          "- Analisar possibilidade de redução do valor do empréstimo\n" +
          "- Reforçar garantias para mitigar riscos";
      } catch (error) {
        console.error('Erro ao buscar análise de IA:', error);
      }
    };
    
    // Buscar comitê
    const fetchCommittee = async () => {
      try {
        const response = await api.committees.getCommittees({ operation: operationId.value });
        
        if (response.data.results && response.data.results.length > 0) {
          // Usar os dados do comitê existente
          const committeeData = response.data.results[0];
          committee.id = committeeData.id;
          committee.operation = committeeData.operation;
          committee.status = committeeData.status;
          committee.started_at = committeeData.started_at;
          committee.completed_at = committeeData.completed_at;
          committee.decision = committeeData.decision;
          committee.members = committeeData.members || [];
        } else {
          // Preparar dados para novo comitê
          committee.operation = operationId.value;
        }
      } catch (error) {
        console.error('Erro ao buscar comitê:', error);
      }
    };
    
    // Buscar formalização
    const fetchFormalization = async () => {
      try {
        // Buscar contrato
        const contractResponse = await api.contracts.getContracts({ operation: operationId.value });
        
        if (contractResponse.data.results && contractResponse.data.results.length > 0) {
          formalization.contract = contractResponse.data.results[0];
          formalization.status = 'contract_generated';
          
          // Se contrato estiver assinado
          if (formalization.contract.status === 'signed') {
            formalization.status = 'completed';
            formalization.credit_release_date = operation.value.monitoring_date;
          } else {
            formalization.status = 'signatures_pending';
          }
        }
      } catch (error) {
        console.error('Erro ao buscar formalização:', error);
      }
    };
    
    // Funções para o gerenciamento de sócios
    const editPartner = (partner) => {
      Object.assign(editingPartner, { ...partner });
      showPartnerForm.value = true;
    };
    
    const savePartner = async () => {
      try {
        if (!editingPartner.operation) {
          editingPartner.operation = operationId.value;
        }
        
        if (editingPartner.id) {
          // Atualizar sócio existente
          await api.partners.updatePartner(editingPartner.id, editingPartner);
        } else {
          // Adicionar novo sócio
          await api.partners.createPartner(editingPartner);
        }
        
        // Atualizar lista de sócios
        fetchPartners();
        
        // Limpar formulário e fechar modal
        resetPartnerForm();
        showPartnerForm.value = false;
      } catch (error) {
        console.error('Erro ao salvar sócio:', error);
      }
    };
    
    const removePartner = async (partnerId) => {
      if (confirm('Tem certeza que deseja remover este sócio?')) {
        try {
          await api.partners.deletePartner(partnerId);
          fetchPartners();
        } catch (error) {
          console.error('Erro ao remover sócio:', error);
        }
      }
    };
    
    const resetPartnerForm = () => {
      Object.assign(editingPartner, {
        id: null,
        operation: operationId.value,
        name: '',
        role: '',
        document: '',
        email: '',
        phone: '',
        share: 0
      });
    };
    
    // Funções para o gerenciamento de garantias
    const editGuarantee = (guarantee) => {
      Object.assign(editingGuarantee, { ...guarantee });
      showGuaranteeForm.value = true;
    };
    
    const saveGuarantee = async () => {
      try {
        if (!editingGuarantee.operation) {
          editingGuarantee.operation = operationId.value;
        }
        
        if (editingGuarantee.id) {
          // Atualizar garantia existente
          await api.guarantees.updateGuarantee(editingGuarantee.id, editingGuarantee);
        } else {
          // Adicionar nova garantia
          await api.guarantees.createGuarantee(editingGuarantee);
        }
        
        // Atualizar lista de garantias
        fetchGuarantees();
        
        // Limpar formulário e fechar modal
        resetGuaranteeForm();
        showGuaranteeForm.value = false;
      } catch (error) {
        console.error('Erro ao salvar garantia:', error);
      }
    };
    
    const removeGuarantee = async (guaranteeId) => {
      if (confirm('Tem certeza que deseja remover esta garantia?')) {
        try {
          await api.guarantees.deleteGuarantee(guaranteeId);
          fetchGuarantees();
        } catch (error) {
          console.error('Erro ao remover garantia:', error);
        }
      }
    };
    
    const resetGuaranteeForm = () => {
      Object.assign(editingGuarantee, {
        id: null,
        operation: operationId.value,
        type: '',
        value: 0,
        description: '',
        registration_number: '',
        location: '',
        notes: ''
      });
    };
    
    // Função para calcular o percentual da garantia em relação ao valor da operação
    const calculateGuaranteePercentage = (guaranteeValue) => {
      if (!operation.value.amount || !guaranteeValue) return 0;
      return ((guaranteeValue / operation.value.amount) * 100).toFixed(2);
    };
    
    // Funções para o gerenciamento de documentos
    const handleFileChange = (event) => {
      const file = event.target.files[0];
      if (file) {
        uploadingDocument.file = file;
        fileUploadInfo.value = file.name;
      } else {
        uploadingDocument.file = null;
        fileUploadInfo.value = 'Nenhum arquivo selecionado';
      }
    };
    
    const uploadDocument = async () => {
      try {
        if (!uploadingDocument.operation) {
          uploadingDocument.operation = operationId.value;
        }
        
        await api.documents.uploadDocument(uploadingDocument);
        
        // Atualizar lista de documentos
        fetchDocuments();
        
        // Limpar formulário e fechar modal
        uploadingDocument.type = '';
        uploadingDocument.name = '';
        uploadingDocument.file = null;
        uploadingDocument.notes = '';
        fileUploadInfo.value = 'Nenhum arquivo selecionado';
        showDocumentUpload.value = false;
      } catch (error) {
        console.error('Erro ao fazer upload de documento:', error);
      }
    };
    
    const removeDocument = async (documentId) => {
      if (confirm('Tem certeza que deseja remover este documento?')) {
        try {
          await api.documents.deleteDocument(documentId);
          fetchDocuments();
        } catch (error) {
          console.error('Erro ao remover documento:', error);
        }
      }
    };
    
    // Funções para a análise de crédito
    const calculateAnalysis = async () => {
      try {
        // Validar dados de entrada
        if (!analysis.sector) {
          alert('Por favor, selecione um setor');
          return;
        }
        
        // Verificar se há dados PGDAS
        const pgdasValues = Object.values(analysis.pgdas_data).filter(v => v > 0);
        if (pgdasValues.length === 0) {
          alert('Por favor, insira pelo menos um valor de faturamento mensal');
          return;
        }
        
        loading.value = true;
        
        // Preparar dados da análise
        const analysisData = {
          operation: operationId.value,
          sector: analysis.sector,
          pgdas_data: analysis.pgdas_data,
          financial_expenses: analysis.financial_expenses,
          short_term_data: analysis.short_term_data,
          future_modality_data: analysis.future_modality_data,
          monthly_payment: firstInstallment.value,
          analyst: api.auth.getCurrentUser()?.id || 1 // Usar ID 1 como fallback
        };
        
        let response;
        
        if (analysis.id) {
          // Atualizar análise existente
          response = await api.analyses.updateAnalysis(analysis.id, analysisData);
        } else {
          // Criar nova análise
          response = await api.analyses.createAnalysis(analysisData);
          if (response.data && response.data.id) {
            analysis.id = response.data.id;
          }
        }
        
        // Calcular resultados
        if (analysis.id) {
          await api.analyses.calculateAnalysis(analysis.id);
        }
        
        // Recarregar dados da análise
        await fetchAnalysis();
        
        alert('Análise calculada com sucesso!');
      } catch (error) {
        console.error('Erro ao calcular análise:', error);
        
        // Fallback: calcular localmente se a API falhar
        try {
          // Cálculos locais como fallback
          calculateAnalysisLocally();
          alert('Análise calculada localmente (modo de testes)');
        } catch (localError) {
          alert('Erro ao calcular análise. Verifique os dados e tente novamente.');
        }
      } finally {
        loading.value = false;
      }
    };

    // Função de fallback para cálculo local
    const calculateAnalysisLocally = () => {
      // PGDAS total
      analysis.pgdas_total = Object.values(analysis.pgdas_data).reduce((sum, val) => sum + parseFloat(val || 0), 0);
      
      // Despesa setorial
      const sectorPercentages = {
        'commerce': 75,
        'service': 70,
        'transport': 85,
        'industry': 90
      };
      const percentage = sectorPercentages[analysis.sector] || 75;
      analysis.sector_expense = analysis.pgdas_total * percentage / 100;
      
      // Lucro bruto
      analysis.gross_profit = analysis.pgdas_total - analysis.sector_expense;
      
      // Despesas financeiras
      analysis.financial_expenses_total = 0;
      for (const key in analysis.financial_expenses) {
        const item = analysis.financial_expenses[key];
        const value = parseFloat(item.value || 0);
        const percentage = parseFloat(item.percentage || 0);
        item.result = value * percentage / 100;
        analysis.financial_expenses_total += item.result;
      }
      
      // Disponibilidade mensal 1
      analysis.availability1 = (analysis.gross_profit - analysis.financial_expenses_total) / 12;
      
      // Somar curto prazo
      analysis.short_term_total = 0;
      for (const key in analysis.short_term_data) {
        analysis.short_term_total += parseFloat(analysis.short_term_data[key].value || 0);
      }
      
      // Somar modalidade futuro
      analysis.future_modality_total = 0;
      for (const key in analysis.future_modality_data) {
        analysis.future_modality_total += parseFloat(analysis.future_modality_data[key].value || 0);
      }
      
      // Reposição mensal
      analysis.monthly_repayment = Math.max(0, (analysis.short_term_total - analysis.future_modality_total) / 12);
      
      // Disponibilidade mensal 2
      analysis.availability2 = analysis.availability1 - analysis.monthly_repayment;
      
      // Superávit / Déficit
      analysis.surplus = analysis.availability2 - firstInstallment.value;
      
      // Decisão
      analysis.approved = analysis.surplus >= 0;
    };
    
    // Gerar análise de IA
    const generateAIAnalysis = () => {
      isGeneratingAI.value = true;
      
      // Simular tempo de processamento
      setTimeout(() => {
        // No MVP, apenas simulamos uma análise de IA
        aiAnalysis.risk_score = 35.8;
        aiAnalysis.default_probability = 0.358;
        aiAnalysis.recommendation = "APROVADO COM CONDIÇÕES: Bom candidato, mas considerar redução do valor ou aumento do prazo.";
        aiAnalysis.explanation = 
          "Score de risco: 35.80/100 (quanto menor, melhor)\n\n" +
          "Análise de capacidade de pagamento:\n" +
          "- Valor da parcela: R$ " + formatCurrency(firstInstallment.value) + "\n" +
          "- Comprometimento: 72.22% da disponibilidade mensal\n\n" +
          "Principais fatores para a decisão:\n" +
          "- POSITIVO: Score de crédito adequado (825)\n" +
          "- POSITIVO: Histórico de operações anteriores sem atrasos\n" +
          "- NEUTRO: Valor solicitado dentro da capacidade financeira do cliente\n" +
          "- ALERTA: Alto comprometimento da disponibilidade mensal\n\n" +
          "Recomendações:\n" +
          "- Considerar aumento do prazo para reduzir o valor da parcela\n" +
          "- Analisar possibilidade de redução do valor do empréstimo\n" +
          "- Reforçar garantias para mitigar riscos";
        
        isGeneratingAI.value = false;
      }, 2000);
    };
    
    // Obter classe da recomendação de IA
    const getAIRecommendationClass = () => {
      if (!aiAnalysis.recommendation) return '';
      
      const rec = aiAnalysis.recommendation.toLowerCase();
      if (rec.includes('aprovado com condições')) return 'warning';
      if (rec.includes('aprovado')) return 'success';
      if (rec.includes('reprovado')) return 'danger';
      if (rec.includes('análise manual')) return 'info';
      
      return '';
    };
    
    // Funções para o comitê de crédito
    const startCommittee = async () => {
      try {
        if (committee.id) {
          await api.committees.startCommittee(committee.id);
        } else {
          // Criar comitê se não existir
          const response = await api.committees.getCommittees({ operation: operationId.value });
          if (response.data.results && response.data.results.length > 0) {
            committee.id = response.data.results[0].id;
            await api.committees.startCommittee(committee.id);
          }
        }
        
        // Atualizar dados do comitê
        fetchCommittee();
      } catch (error) {
        console.error('Erro ao iniciar comitê:', error);
      }
    };
    
    const submitVote = async () => {
      try {
        if (!voting.vote) {
          alert('Selecione um voto');
          return;
        }
        
        // Encontrar membro do comitê atual
        const currentUser = api.auth.getCurrentUser();
        const member = committee.members.find(m => m.user === currentUser.id);
        
        if (!member) {
          alert('Você não é membro deste comitê');
          return;
        }
        
        // Registrar voto
        await api.committeeMembers.vote(member.id, {
          vote: voting.vote,
          notes: voting.notes
        });
        
        // Atualizar comitê
        fetchCommittee();
        
        // Para o MVP, um voto é suficiente para concluir automaticamente o comitê
        if (committee.status === 'in_progress') {
          finishCommittee();
        }
        
        alert('Voto registrado com sucesso!');
      } catch (error) {
        console.error('Erro ao registrar voto:', error);
        alert('Erro ao registrar voto');
      }
    };

    const finishCommittee = async () => {
      try {
        await api.committees.finishCommittee(committee.id);
        
        // Atualizar dados
        fetchCommittee();
        fetchOperation();
        
        alert('Comitê finalizado com sucesso!');
      } catch (error) {
        console.error('Erro ao finalizar comitê:', error);
        alert('Erro ao finalizar comitê');
      }
    };
    
    // Funções para a formalização
    const generateContract = async () => {
      try {
        await api.contracts.generateContract(operationId.value);
        
        // Atualizar dados de formalização
        fetchFormalization();
        
        alert('Contrato gerado com sucesso!');
      } catch (error) {
        console.error('Erro ao gerar contrato:', error);
        alert('Erro ao gerar contrato');
      }
    };

    const sendSignatureReminder = async (signatureId) => {
      try {
        // Para o MVP, apenas simulamos o envio
        alert('Lembrete de assinatura enviado com sucesso!');
        
        // Em produção, chamaria uma API para enviar o lembrete
        // await api.signatures.sendReminder(signatureId);
      } catch (error) {
        console.error('Erro ao enviar lembrete:', error);
        alert('Erro ao enviar lembrete');
      }
    };

    const releaseCredit = async () => {
      if (!areAllSignaturesCompleted.value) {
        alert('Todas as assinaturas precisam ser coletadas antes de liberar o crédito');
        return;
      }
      
      try {
        await api.contracts.finalizeContract(formalization.contract.id);
        
        // Atualizar operação para o estágio de monitoramento
        await api.operations.updateOperationStatus(operationId.value, 'monitoring');
        
        // Atualizar dados
        fetchFormalization();
        fetchOperation();
        
        alert('Crédito liberado com sucesso!');
      } catch (error) {
        console.error('Erro ao liberar crédito:', error);
        alert('Erro ao liberar crédito');
      }
    };
    
    // Funções para pagamento
    const recordPayment = (installment) => {
      paymentData.installment = installment.id;
      paymentData.amount = installment.amount;
      showPaymentModal.value = true;
    };

    const confirmPayment = async () => {
      try {
        await api.installments.recordPayment(paymentData.installment, {
          payment_date: paymentData.date,
          payment_amount: paymentData.amount,
          payment_method: paymentData.method,
          notes: paymentData.notes
        });
        
        // Atualizar parcelas
        fetchInstallments();
        
        showPaymentModal.value = false;
        alert('Pagamento registrado com sucesso!');
      } catch (error) {
        console.error('Erro ao registrar pagamento:', error);
        alert('Erro ao registrar pagamento');
      }
    };
    
    const calculateOverdueDays = (installment) => {
      if (installment.status !== 'overdue') return '-';
      
      const today = new Date();
      const dueDate = new Date(installment.due_date);
      const diffTime = Math.abs(today - dueDate);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      
      return diffDays;
    };
    
    // Funções para acompanhamento
    const getNextInstallmentDate = () => {
      const pendingInstallment = paymentPlan.value.find(i => i.status === 'pending');
      return pendingInstallment ? formatDate(new Date(pendingInstallment.due_date)) : '-';
    };
    
    const getNextInstallmentAmount = () => {
      const pendingInstallment = paymentPlan.value.find(i => i.status === 'pending');
      return pendingInstallment ? pendingInstallment.amount : 0;
    };
    
    const validateData = () => {
      // Verificar se a operação está carregada
      if (!operation.value || !operation.value.id) {
        console.warn('Operação não carregada completamente');
        return false;
      }
      
      // Verificar cliente
      if (!client.value || !client.value.id) {
        console.warn('Cliente não carregado completamente');
        return false;
      }
      
      return true;
    };

    // Transições de estágio
    const moveToStage = async (stageId) => {
      try {
        if (!validateData()) {
          alert('Dados da operação não estão completamente carregados. Tente novamente em alguns instantes.');
          return;
        }

        // Validar se pode avançar para o próximo estágio
        if (stageId === 'committee' && !analysis.approved) {
          alert('A análise deve ser aprovada antes de enviar para o comitê');
          return;
        }
        
        // Atualizar status da operação
        await api.operations.updateOperationStatus(operationId.value, stageId);
        
        // Executar ações específicas para cada etapa
        if (stageId === 'analysis') {
          // Inicializar análise se não existir
          if (!analysis.id) {
            await initializeAnalysis();
          }
        } else if (stageId === 'committee') {
          // Inicializar comitê se não existir
          if (!committee.id) {
            await api.committees.getCommittees({ operation: operationId.value });
          }
        }
        
        // Atualizar dados da operação
        fetchOperation();
      } catch (error) {
        console.error('Erro ao atualizar status da operação:', error);
        alert('Erro ao atualizar status da operação');
      }
    };
    
    // Função para verificação
    const verifyOperation = async () => {
      try {
        await api.operations.updateOperationStatus(operationId.value, 'analysis');
        
        // Atualizar dados da operação
        fetchOperation();
      } catch (error) {
        console.error('Erro ao verificar operação:', error);
      }
    };
    
    // Funções auxiliares
    const isStageActive = (stageId) => {
      const stageIndex = operationStages.findIndex(s => s.id === stageId);
      const currentIndex = operationStages.findIndex(s => s.id === currentStage.value);
      
      return stageIndex <= currentIndex;
    };
    
    const isStageCompleted = (stageId) => {
      const stageIndex = operationStages.findIndex(s => s.id === stageId);
      const currentIndex = operationStages.findIndex(s => s.id === currentStage.value);
      
      return stageIndex < currentIndex;
    };
    
    // Formatação e labels
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
    
    const getStatusLabel = (status) => {
      const labels = {
        'pending': 'Cadastro Pendente',
        'verification': 'Em Conferência',
        'analysis': 'Em Análise',
        'committee': 'Em Comitê',
        'formalization': 'Em Formalização',
        'monitoring': 'Em Acompanhamento',
        'approved': 'Aprovado',
        'rejected': 'Reprovado',
        'cancelled': 'Cancelado'
      };
      return labels[status] || status;
    };
    
    const getAmortizationSystem = (system) => {
      const systems = {
        'price': 'PRICE (Parcelas Fixas)',
        'sac': 'SAC (Amortização Constante)',
        'pricemix': 'PRICEMIX (Sistema Misto)'
      };
      return systems[system] || system;
    };
    
    const getPaymentStatusLabel = (status) => {
      const labels = {
        'paid': 'Pago',
        'pending': 'Pendente',
        'overdue': 'Em Atraso',
        'future': 'A Vencer'
      };
      return labels[status] || status;
    };
    
    const getDocumentIcon = (type) => {
      const icons = {
        'authorization': 'fas fa-file-contract',
        'id': 'fas fa-id-card',
        'income': 'fas fa-file-invoice-dollar',
        'residence': 'fas fa-home',
        'bank_statement': 'fas fa-money-check-alt',
        'tax_return': 'fas fa-file-alt',
        'business': 'fas fa-building',
        'other': 'fas fa-file'
      };
      return icons[type] || 'fas fa-file';
    };
    
    const getDocumentTypeLabel = (type) => {
      const labels = {
        'authorization': 'Termo de Autorização',
        'id': 'Documento de Identificação',
        'income': 'Comprovante de Renda',
        'residence': 'Comprovante de Residência',
        'bank_statement': 'Extrato Bancário',
        'tax_return': 'Declaração de IR',
        'business': 'Documentos Empresariais',
        'other': 'Outro'
      };
      return labels[type] || type;
    };
    
    const getGuaranteeTypeClass = (type) => {
      return `guarantee-${type}`;
    };
    
    const getGuaranteeTypeLabel = (type) => {
      const labels = {
        'property': 'Imóvel',
        'vehicle': 'Veículo',
        'equipment': 'Equipamento',
        'financial': 'Aplicação Financeira',
        'endorsement': 'Aval/Fiança',
        'other': 'Outra'
      };
      return labels[type] || type;
    };
    
    const getSectorPercentage = () => {
      const percentages = {
        'commerce': 75,
        'service': 70,
        'transport': 85,
        'industry': 90
      };
      return percentages[analysis.sector] || 0;
    };
    
    const getAnalysisDecisionNote = () => {
      if (analysis.approved === null) return '';
      
      if (analysis.approved) {
        return 'A operação atende aos critérios de aprovação. A disponibilidade mensal é suficiente para cobrir a parcela.';
      } else {
        return 'A operação não atende aos critérios de aprovação. A disponibilidade mensal é insuficiente para cobrir a parcela.';
      }
    };
    
    const getCommitteeStatusIcon = () => {
      const icons = {
        'pending': 'fa-clock',
        'in_progress': 'fa-spinner fa-spin',
        'completed': 'fa-check-circle'
      };
      return icons[committee.status] || 'fa-circle';
    };
    
    const getCommitteeStatusLabel = () => {
      const labels = {
        'pending': 'Aguardando Início do Comitê',
        'in_progress': 'Comitê em Andamento',
        'completed': 'Comitê Finalizado'
      };
      return labels[committee.status] || committee.status;
    };
    
    const getFormalizationStatusIcon = () => {
      const icons = {
        'pending': 'fa-clock',
        'contract_generated': 'fa-file-contract',
        'signatures_pending': 'fa-signature',
        'completed': 'fa-check-circle'
      };
      return icons[formalization.status] || 'fa-circle';
    };
    
    const getFormalizationStatusLabel = () => {
      const labels = {
        'pending': 'Aguardando Geração do Contrato',
        'contract_generated': 'Contrato Gerado',
        'signatures_pending': 'Aguardando Assinaturas',
        'completed': 'Formalização Concluída'
      };
      return labels[formalization.status] || formalization.status;
    };
    
    const getContractStatusLabel = (status) => {
      const labels = {
        'pending_signature': 'Aguardando Assinaturas',
        'signed': 'Assinado',
        'cancelled': 'Cancelado'
      };
      return labels[status] || status;
    };
    
    const getSignatureStatusLabel = (status) => {
      const labels = {
        'pending': 'Pendente',
        'signed': 'Assinado',
        'refused': 'Recusado'
      };
      return labels[status] || status;
    };
    
    const getMonitoringStatusLabel = () => {
      const labels = {
        'normal': 'Normal',
        'attention': 'Atenção',
        'risk': 'Em Risco',
        'default': 'Inadimplente',
        'completed': 'Concluído'
      };
      return labels[operation.value.monitoring_status] || 'Normal';
    };
    
    // Propriedades computadas
    const canVote = computed(() => {
      // Verificar se o usuário atual é membro do comitê e ainda não votou
      if (committee.status !== 'in_progress') return false;
      
      const currentUser = api.auth.getCurrentUser();
      if (!currentUser) return false;
          
      const member = committee.members.find(m => m.user === currentUser.id);
      
      return member && member.vote === null;
    });
    
    const isCommitteeManager = computed(() => {
      // No MVP, vamos simular que o usuário é gerente
      return true;
    });
    
    const areAllSignaturesCompleted = computed(() => {
      if (!formalization.contract || !formalization.contract.signatures || !formalization.contract.signatures.length) return false;
      return formalization.contract.signatures.every(s => s.status === 'signed');
    });
    
    const canReleaseCredit = computed(() => {
      if (!formalization.contract) return false;
      return areAllSignaturesCompleted.value;
    });
    
    // Funções para salvar análise e gerar relatório
    const saveAnalysis = async () => {
      try {
        await calculateAnalysis();
        alert('Análise salva com sucesso!');
      } catch (error) {
        console.error('Erro ao salvar análise:', error);
        alert('Erro ao salvar análise');
      }
    };
    
    const generateReport = () => {
      reportService.generateOperationReport(
        operation.value,
        client.value,
        analysis,
        committee
      );
    };
    
    // Observar mudanças na rota para atualizar os dados
    watch(() => route.params.id, (newId) => {
      if (newId && parseInt(newId) !== operationId.value) {
        operationId.value = parseInt(newId);
        fetchOperation();
      }
    });
    
    onMounted(() => {
      fetchOperation();
      initAnalysisData();
    });
    
    return {
      operationId,
      operation,
      client,
      currentStage,
      stageDates,
      activeTab,
      activeAnalysisTab,
      firstInstallment,
      totalAmount,
      paymentPlan,
      partners,
      guarantees,
      documents,
      operationStages,
      operationTabs,
      analysisTabs,
      months,
      analysis,
      aiAnalysis,
      committee,
      formalization,
      showPartnerForm,
      showGuaranteeForm,
      showDocumentUpload,
      showPaymentModal,
      editingPartner,
      editingGuarantee,
      uploadingDocument,
      fileUploadInfo,
      isGeneratingAI,
      voting,
      paymentData,
      canVote,
      isCommitteeManager,
      areAllSignaturesCompleted,
      canReleaseCredit,
      isStageActive,
      isStageCompleted,
      formatDate,
      formatCurrency,
      getStatusLabel,
      getAmortizationSystem,
      getPaymentStatusLabel,
      getDocumentIcon,
      getDocumentTypeLabel,
      getGuaranteeTypeClass,
      getGuaranteeTypeLabel,
      getSectorPercentage,
      getAnalysisDecisionNote,
      getAIRecommendationClass,
      getCommitteeStatusIcon,
      getCommitteeStatusLabel,
      getFormalizationStatusIcon,
      getFormalizationStatusLabel,
      getContractStatusLabel,
      getSignatureStatusLabel,
      getMonitoringStatusLabel,
      getNextInstallmentDate,
      getNextInstallmentAmount,
      calculateGuaranteePercentage,
      calculateAnalysis,
      calculateOverdueDays,
      generateAIAnalysis,
      saveAnalysis,
      generateReport,
      editPartner,
      savePartner,
      removePartner,
      editGuarantee,
      saveGuarantee,
      removeGuarantee,
      handleFileChange,
      uploadDocument,
      removeDocument,
      startCommittee,
      submitVote,
      finishCommittee,
      generateContract,
      sendSignatureReminder,
      releaseCredit,
      recordPayment,
      confirmPayment,
      moveToStage,
      verifyOperation
    };
  }
}
</script>

<style scoped>
.operation-detail {
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

/* Fluxo da operação */
.operation-flow {
  display: flex;
  align-items: center;
  margin-bottom: 35px;
  padding: 25px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  overflow-x: auto;
  position: relative;
}

.flow-stage {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  flex: 1;
  min-width: 120px;
  opacity: 0.5;
  transition: all 0.3s ease;
}

.flow-stage.active {
  opacity: 1;
}

.flow-stage.completed .stage-indicator {
  background: linear-gradient(135deg, #4CAF50, #2E7D32);
  color: white;
  box-shadow: 0 5px 15px rgba(76, 175, 80, 0.3);
}

.flow-stage.current .stage-indicator {
  background: linear-gradient(135deg, #4673F5, #2556e0);
  color: white;
  transform: scale(1.1);
  box-shadow: 0 8px 20px rgba(70, 115, 245, 0.3);
}

.stage-indicator {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #f0f0f0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-bottom: 12px;
  transition: all 0.3s ease;
  position: relative;
  z-index: 2;
}

.stage-number {
  font-size: 18px;
  font-weight: 600;
  line-height: 1;
  margin-bottom: 2px;
}

.stage-icon {
  font-size: 16px;
}

.stage-info {
  text-align: center;
  max-width: 120px;
}

.stage-name {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 5px;
  color: #444;
}

.stage-date {
  font-size: 12px;
  color: #666;
}

.stage-connector {
  position: absolute;
  top: 30px;
  right: -50%;
  width: 100%;
  height: 2px;
  background-color: #ddd;
  z-index: 1;
}

.flow-stage.active .stage-connector,
.flow-stage.completed .stage-connector {
  background: linear-gradient(90deg, #4CAF50, #4673F5);
}

/* Tabs de navegação */
.operation-tabs {
  display: flex;
  overflow-x: auto;
  margin-bottom: 25px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 1px;
  position: sticky;
  top: 80px;
  background-color: #f5f7fa;
  z-index: 3;
  padding-top: 10px;
  border-radius: 8px 8px 0 0;
}

.tab-button {
  padding: 12px 20px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  border-bottom: 3px solid transparent;
  white-space: nowrap;
  transition: all 0.3s ease;
  font-weight: 500;
}

.tab-button.active {
  color: #4673F5;
  border-bottom-color: #4673F5;
  font-weight: 600;
}

.tab-button:hover {
  color: #4673F5;
}

/* Conteúdo das abas */
.tab-pane {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  padding: 25px;
  margin-bottom: 25px;
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 25px;
}

.info-card {
  background-color: #f9f9fc;
  border-radius: 10px;
  padding: 20px;
  transition: all 0.3s ease;
}

.info-card:hover {
  background-color: #f5f7fa;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.info-card h2 {
  margin-top: 0;
  margin-bottom: 20px;
  padding-bottom: 10px;
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

.info-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

/* Badges e status */
.status-badge {
  display: inline-flex;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  align-items: center;
}

.status-badge.pending {
  background-color: #E3F2FD;
  color: #1976D2;
}

.status-badge.verification {
  background-color: #EDE7F6;
  color: #7E57C2;
}

.status-badge.analysis {
  background-color: #FFF8E1;
  color: #FFA000;
}

.status-badge.committee {
  background-color: #E8F5E9;
  color: #388E3C;
}

.status-badge.formalization {
  background-color: #E1F5FE;
  color: #0288D1;
}

.status-badge.monitoring {
  background-color: #F3E5F5;
  color: #AB47BC;
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

/* Plano de pagamento */
.payment-summary {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.summary-card {
  background-color: #f9f9fc;
  border-radius: 10px;
  padding: 18px;
  text-align: center;
  transition: all 0.3s ease;
}

.summary-card:hover {
  background-color: #f5f7fa;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
  transform: translateY(-3px);
}

.summary-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.summary-value {
  font-size: 20px;
  font-weight: 700;
  color: #00004b;
}

.table-container {
  margin-top: 25px;
  overflow-x: auto;
  border-radius: 8px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 14px;
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
  z-index: 2;
}

tr:hover td {
  background-color: #f9fafc;
}

.payment-status {
  display: inline-flex;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  align-items: center;
}

.payment-status.paid {
  background-color: #E8F5E9;
  color: #388E3C;
}

.payment-status.pending {
  background-color: #FFF8E1;
  color: #FFA000;
}

.payment-status.overdue {
  background-color: #FFEBEE;
  color: #D32F2F;
}

.payment-status.future {
  background-color: #E3F2FD;
  color: #1976D2;
}

/* Sócios */
.partners-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.partners-header h2 {
  margin: 0;
  font-size: 20px;
  color: #00004b;
  font-weight: 600;
}

.partners-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 25px;
}

.partner-card {
  background-color: #f9f9fc;
  border-radius: 10px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.03);
}

.partner-card:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  transform: translateY(-5px);
}

.partner-header {
  padding: 18px;
  background-color: #f0f0f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.partner-name {
  font-size: 16px;
  font-weight: 600;
  color: #00004b;
}

.partner-role-badge {
  background-color: #E1F5FE;
  color: #0288D1;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.partner-info {
  padding: 18px;
}

.info-item {
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}

.info-icon {
  margin-right: 12px;
  color: #666;
  width: 20px;
  text-align: center;
  font-size: 14px;
}

.partner-actions {
  display: flex;
  padding: 15px;
  background-color: #f0f0f0;
  gap: 10px;
}

.btn-edit, .btn-delete, .btn-view, .btn-add {
  padding: 8px 14px;
  border-radius: 6px;
  font-size: 13px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-edit {
  background-color: #FFF8E1;
  color: #FFA000;
}

.btn-edit:hover {
  background-color: #FFECB3;
  color: #FF6F00;
  transform: translateY(-2px);
}

.btn-delete {
  background-color: #FFEBEE;
  color: #D32F2F;
}

.btn-delete:hover {
  background-color: #FFCDD2;
  color: #B71C1C;
  transform: translateY(-2px);
}

.btn-view {
  background-color: #E3F2FD;
  color: #1976D2;
  text-decoration: none;
}

.btn-view:hover {
  background-color: #BBDEFB;
  color: #0D47A1;
  transform: translateY(-2px);
  text-decoration: none;
}

.btn-add {
  background-color: #E8F5E9;
  color: #388E3C;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-add:hover {
  background-color: #C8E6C9;
  color: #2E7D32;
  transform: translateY(-2px);
}

/* Garantias */
.guarantees-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.guarantees-header h2 {
  margin: 0;
  font-size: 20px;
  color: #00004b;
  font-weight: 600;
}

.guarantees-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.guarantee-card {
  background-color: #f9f9fc;
  border-radius: 10px;
  padding: 20px;
  display: flex;
  align-items: flex-start;
  gap: 20px;
  transition: all 0.3s ease;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.03);
}

.guarantee-card:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  transform: translateY(-5px);
}

.guarantee-type-badge {
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  margin-top: 5px;
}

.guarantee-property {
  background-color: #E8EAF6;
  color: #3F51B5;
}

.guarantee-vehicle {
  background-color: #E0F7FA;
  color: #00BCD4;
}

.guarantee-equipment {
  background-color: #F3E5F5;
  color: #9C27B0;
}

.guarantee-financial {
  background-color: #E8F5E9;
  color: #4CAF50;
}

.guarantee-endorsement {
  background-color: #FFF8E1;
  color: #FFC107;
}

.guarantee-other {
  background-color: #ECEFF1;
  color: #607D8B;
}

.guarantee-info {
  flex: 1;
}

.guarantee-description {
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 16px;
  color: #333;
  font-weight: 600;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 15px;
}

.guarantee-notes {
  border-top: 1px solid #eee;
  padding-top: 12px;
}

.guarantee-notes .label {
  display: block;
  margin-bottom: 5px;
  color: #666;
  font-weight: 500;
}

.guarantee-notes p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.guarantee-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* Análise de crédito */
.analysis-tabs {
  display: flex;
  overflow-x: auto;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
}

.analysis-tab-button {
  padding: 10px 16px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  border-bottom: 2px solid transparent;
  white-space: nowrap;
  transition: all 0.3s ease;
  font-weight: 500;
}

.analysis-tab-button.active {
  color: #4673F5;
  border-bottom-color: #4673F5;
  font-weight: 600;
}

.analysis-tab-button:hover {
  color: #4673F5;
}

.analysis-pane {
  margin-top: 25px;
  animation: fadeIn 0.4s ease-out;
}

.analysis-pane h3 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 18px;
  color: #00004b;
  font-weight: 600;
}

.data-input-section {
  margin-bottom: 25px;
}

.data-input-section h4 {
  margin-top: 25px;
  margin-bottom: 12px;
  font-size: 16px;
  color: #444;
  font-weight: 600;
}

.radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
}

.radio-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 16px;
  background-color: #f5f7fa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.radio-label:hover {
  background-color: #e3f2fd;
}

.radio-label input {
  margin-right: 8px;
  width: auto;
}

.input-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 25px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.input-table th, .input-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.input-table th {
  background-color: #f5f7fa;
  color: #00004b;
  font-weight: 600;
}

.input-table input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.input-table input:focus {
  border-color: #4673F5;
  box-shadow: 0 0 0 3px rgba(70, 115, 245, 0.15);
  outline: none;
}

.total-row {
  font-weight: 700;
  background-color: #f9f9fc;
}

.calculation-result {
  background-color: #f5f7fa;
  padding: 20px;
  border-radius: 10px;
  margin-top: 25px;
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 15px;
}

.result-label {
  font-weight: 600;
  color: #444;
}

.result-value {
  font-weight: 700;
  color: #4673F5;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}

.result-card {
  background-color: #f9f9fc;
  border-radius: 10px;
  padding: 20px;
  transition: all 0.3s ease;
}

.result-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.result-title {
  font-weight: 600;
  margin-bottom: 12px;
  color: #444;
}

.result-value {
  font-size: 22px;
  font-weight: 700;
  color: #00004b;
  margin-bottom: 5px;
}

.calculation-note {
  font-size: 12px;
  color: #666;
}

.result-card.highlight {
  background-color: #E3F2FD;
  border-left: 4px solid #1976D2;
}

.result-card.positive {
  background-color: #E8F5E9;
  border-left: 4px solid #4CAF50;
}

.result-card.negative {
  background-color: #FFEBEE;
  border-left: 4px solid #F44336;
}

.result-card.positive .result-value {
  color: #4CAF50;
}

.result-card.negative .result-value {
  color: #F44336;
}

.result-card.decision {
  grid-column: 1 / -1;
  background-color: #ECEFF1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 25px;
}

.result-decision {
  font-size: 26px;
  font-weight: 700;
  margin: 12px 0;
}

.result-decision.approved {
  color: #4CAF50;
}

.result-decision.rejected {
  color: #F44336;
}

.decision-note {
  text-align: center;
  max-width: 600px;
  color: #666;
  font-size: 15px;
}

.analysis-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 25px;
}

.btn-save {
  background: linear-gradient(90deg, #4673F5, #2556e0);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 10px rgba(70, 115, 245, 0.2);
}

.btn-save:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(70, 115, 245, 0.3);
}

.btn-report {
  background: linear-gradient(90deg, #FFA000, #FF6F00);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 10px rgba(255, 160, 0, 0.2);
}

.btn-report:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(255, 160, 0, 0.3);
}

/* Análise IA */
.ai-section {
  background-color: #f9f9fc;
  border-radius: 12px;
  padding: 25px;
  position: relative;
  transition: all 0.3s ease;
}

.ai-section:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.ai-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.ai-badge {
  background-color: #E1F5FE;
  color: #0288D1;
  padding: 8px 15px;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.ai-badge::before {
  content: '🤖';
  font-size: 16px;
}

.btn-ai {
  background: linear-gradient(90deg, #0288D1, #01579B);
  color: white;
  padding: 10px 18px;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 10px rgba(2, 136, 209, 0.2);
}

.btn-ai:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(2, 136, 209, 0.3);
}

.btn-ai:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.ai-result {
  border: 1px solid #E1F5FE;
  border-radius: 12px;
  padding: 25px;
  background-color: white;
  animation: fadeIn 0.5s ease-out;
}

.recommendation-box {
  padding: 20px;
  border-radius: 10px;
  margin-bottom: 25px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.recommendation-box h4 {
  margin-top: 0;
  margin-bottom: 12px;
  font-size: 18px;
  font-weight: 600;
}

.recommendation-box p {
  margin: 0;
  font-size: 15px;
  color: #444;
}

.recommendation-box.success {
  background-color: #E8F5E9;
  border-left: 5px solid #4CAF50;
}

.recommendation-box.warning {
  background-color: #FFF8E1;
  border-left: 5px solid #FFC107;
}

.recommendation-box.danger {
  background-color: #FFEBEE;
  border-left: 5px solid #F44336;
}

.recommendation-box.info {
  background-color: #E3F2FD;
  border-left: 5px solid #2196F3;
}

.risk-indicator {
  margin-bottom: 25px;
}

.risk-label {
  font-weight: 600;
  margin-bottom: 8px;
  color: #444;
  font-size: 15px;
}

.risk-meter {
  height: 12px;
  background-color: #ECEFF1;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 10px;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
}

.risk-bar {
  height: 100%;
  background: linear-gradient(to right, #4CAF50, #FFC107, #F44336);
  border-radius: 6px;
  transition: width 1s ease-in-out;
}

.risk-value {
  display: flex;
  justify-content: space-between;
  font-weight: 500;
  font-size: 14px;
}

.risk-note {
  color: #777;
  font-size: 12px;
  font-weight: normal;
}

.ai-explanation {
  background-color: #F5F7FA;
  border-radius: 10px;
  padding: 20px;
}

.ai-explanation h4 {
  margin-top: 0;
  margin-bottom: 12px;
  font-size: 16px;
  color: #444;
  font-weight: 600;
}

.ai-explanation pre {
  white-space: pre-wrap;
  font-family: 'Segoe UI', system-ui, sans-serif;
  font-size: 14px;
  margin: 0;
  color: #555;
  background: #ffffff;
  padding: 15px;
  border-radius: 8px;
  border: 1px dashed #e0e0e0;
  line-height: 1.6;
}

.ai-empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

/* Documentos */
.documents-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.documents-header h2 {
  margin: 0;
  font-size: 20px;
  color: #00004b;
  font-weight: 600;
}

.documents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.document-card {
  background-color: #f9f9fc;
  border-radius: 10px;
  padding: 18px;
  display: flex;
  align-items: center;
  gap: 15px;
  transition: all 0.3s ease;
}

.document-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.document-icon {
  font-size: 24px;
  color: #4673F5;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #E3F2FD;
  border-radius: 12px;
}

.document-info {
  flex: 1;
}

.document-name {
  font-weight: 600;
  margin-bottom: 5px;
  color: #333;
  font-size: 15px;
}

.document-meta {
  font-size: 12px;
  color: #666;
  display: flex;
  gap: 15px;
}

.document-type {
  background-color: #f0f0f0;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 500;
}

.document-actions {
  display: flex;
  gap: 8px;
}

/* Upload de arquivo */
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
  padding: 10px 18px;
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

/* Comitê de Crédito */
.committee-section {
  padding: 15px 0;
}

.committee-status {
  background-color: #f9f9fc;
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 25px;
  display: flex;
  gap: 25px;
  transition: all 0.3s ease;
}

.committee-status:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.status-indicator {
  background-color: #f0f0f0;
  color: #666;
  padding: 15px 25px;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 160px;
  transition: all 0.3s ease;
}

.status-indicator i {
  font-size: 24px;
  margin-bottom: 10px;
}

.status-indicator.pending {
  background-color: #E3F2FD;
  color: #1976D2;
}

.status-indicator.in_progress {
  background-color: #FFF8E1;
  color: #FFA000;
}

.status-indicator.completed {
  background-color: #E8F5E9;
  color: #4CAF50;
}

.committee-info {
  flex: 1;
}

.committee-pending, .committee-in-progress, .committee-completed {
  padding: 10px 0;
}

.committee-pending p, .committee-in-progress p, .committee-completed p {
  margin: 0 0 15px;
  font-size: 15px;
  color: #444;
}

.btn-start-committee, .btn-finish-committee {
  background: linear-gradient(90deg, #4673F5, #2556e0);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 10px rgba(70, 115, 245, 0.2);
}

.btn-start-committee:hover, .btn-finish-committee:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(70, 115, 245, 0.3);
}

.committee-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 25px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.committee-voting {
  background-color: #f9f9fc;
  border-radius: 12px;
  padding: 25px;
  margin-top: 25px;
  transition: all 0.3s ease;
}

.committee-voting:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.committee-voting h3 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 18px;
  color: #00004b;
  font-weight: 600;
}

.vote-form {
  padding: 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.03);
}

.vote-options {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.vote-option {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0;
}

.vote-option input {
  margin-right: 8px;
  width: auto;
}

.vote-label {
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.vote-label.approve {
  background-color: #E8F5E9;
  color: #388E3C;
}

.vote-label.reject {
  background-color: #FFEBEE;
  color: #D32F2F;
}

.vote-badge {
  display: inline-flex;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  align-items: center;
}

.vote-badge.approve {
  background-color: #E8F5E9;
  color: #388E3C;
}

.vote-badge.reject {
  background-color: #FFEBEE;
  color: #D32F2F;
}

.vote-badge.pending {
  background-color: #ECEFF1;
  color: #607D8B;
}

.btn-vote {
  background: linear-gradient(90deg, #4673F5, #2556e0);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 10px rgba(70, 115, 245, 0.2);
}

.btn-vote:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(70, 115, 245, 0.3);
}

.btn-vote:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.committee-management {
  margin-top: 25px;
  background-color: #f9f9fc;
  border-radius: 12px;
  padding: 25px;
}

.committee-management h3 {
  margin-top: 0;
  margin-bottom: 12px;
  font-size: 18px;
  color: #00004b;
  font-weight: 600;
}

.committee-management p {
  margin-bottom: 20px;
  color: #666;
}

.decision-badge {
  display: inline-flex;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  align-items: center;
}

.decision-badge.approved {
  background-color: #E8F5E9;
  color: #388E3C;
}

.decision-badge.rejected {
  background-color: #FFEBEE;
  color: #D32F2F;
}

/* Formalização */
.formalization-section {
  padding: 15px 0;
}

.contract-info {
  background-color: #f9f9fc;
  border-radius: 12px;
  padding: 25px;
  margin-top: 25px;
  transition: all 0.3s ease;
}

.contract-info:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.contract-info h3 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 18px;
  color: #00004b;
  font-weight: 600;
}

.formalization-actions {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 12px;
}

.formalization-actions p {
  margin-bottom: 15px;
  color: #444;
  font-size: 15px;
}

.btn-generate {
  background: linear-gradient(90deg, #4673F5, #2556e0);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 10px rgba(70, 115, 245, 0.2);
}

.btn-generate:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(70, 115, 245, 0.3);
}

.contract-details {
  margin-top: 25px;
}

.contract-document {
  margin-top: 25px;
  display: flex;
  justify-content: center;
}

.btn-view-contract {
  background-color: #E3F2FD;
  color: #1976D2;
  padding: 12px 24px;
  border-radius: 8px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 10px rgba(25, 118, 210, 0.1);
}

.btn-view-contract:hover {
  background-color: #BBDEFB;
  color: #0D47A1;
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(25, 118, 210, 0.2);
  text-decoration: none;
}

.btn-view-contract i {
  font-size: 20px;
}

.contract-status {
  display: inline-flex;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  align-items: center;
}

.contract-status.pending_signature {
  background-color: #FFF8E1;
  color: #FFA000;
}

.contract-status.signed {
  background-color: #E8F5E9;
  color: #388E3C;
}

.contract-status.cancelled {
  background-color: #FFEBEE;
  color: #D32F2F;
}

.signature-section {
  margin-top: 30px;
}

.signature-section h3 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 18px;
  color: #00004b;
  font-weight: 600;
}

.signatures-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 25px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.signature-status {
  display: inline-flex;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  align-items: center;
}

.signature-status.pending {
  background-color: #FFF8E1;
  color: #FFA000;
}

.signature-status.signed {
  background-color: #E8F5E9;
  color: #388E3C;
}

.signature-status.refused {
  background-color: #FFEBEE;
  color: #D32F2F;
}

.btn-remind {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  background-color: #f0f0f0;
  color: #666;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.btn-remind:hover {
  background-color: #e0e0e0;
  color: #444;
}

.btn-release {
  background: linear-gradient(90deg, #4CAF50, #388E3C);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 10px rgba(76, 175, 80, 0.2);
}

.btn-release:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(76, 175, 80, 0.3);
}

/* Acompanhamento */
.monitoring-section {
  padding: 15px 0;
}

.monitoring-summary {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.monitoring-status {
  display: inline-flex;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  align-items: center;
}

.monitoring-status.normal {
  background-color: #E8F5E9;
  color: #388E3C;
}

.monitoring-status.attention {
  background-color: #FFF8E1;
  color: #FFA000;
}

.monitoring-status.risk {
  background-color: #FFEBEE;
  color: #F44336;
}

.monitoring-status.default {
  background-color: #FFEBEE;
  color: #D32F2F;
  font-weight: 700;
}

.monitoring-status.completed {
  background-color: #E8F5E9;
  color: #388E3C;
  font-weight: 700;
}

.installments-tracking {
  margin-top: 35px;
}

.installments-tracking h3 {
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 18px;
  color: #00004b;
  font-weight: 600;
}

.installments-table {
  width: 100%;
  border-collapse: collapse;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.btn-record-payment {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  background-color: #E8F5E9;
  color: #388E3C;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-weight: 500;
}

.btn-record-payment:hover {
  background-color: #C8E6C9;
  color: #2E7D32;
  transform: translateY(-2px);
}

/* Modal */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

.modal-content {
  background-color: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  width: 600px;
  max-width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  animation: zoomIn 0.3s ease-out;
}

@keyframes zoomIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

.close {
  position: absolute;
  top: 15px;
  right: 20px;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  transition: all 0.3s ease;
  width: 30px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
}

.close:hover {
  color: #D32F2F;
  background-color: #FFEBEE;
}

/* Ações de estágio */
.stage-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 35px;
}

.btn-primary, .btn-success {
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-left: 15px;
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

.btn-success {
  background: linear-gradient(90deg, #4CAF50, #388E3C);
  color: white;
  box-shadow: 0 4px 10px rgba(76, 175, 80, 0.2);
}

.btn-success:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(76, 175, 80, 0.3);
}

/* Responsividade para telas menores */
@media (max-width: 768px) {
  .operation-flow {
    overflow-x: auto;
    padding: 15px;
  }
  
  .stage-indicator {
    width: 50px;
    height: 50px;
  }
  
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .partners-grid, .documents-grid {
    grid-template-columns: 1fr;
  }
  
  .results-grid {
    grid-template-columns: 1fr;
  }
  
  .monitoring-summary {
    grid-template-columns: 1fr 1fr;
  }
  
  .btn-primary, .btn-success {
    padding: 10px 16px;
    font-size: 14px;
  }
}
</style>