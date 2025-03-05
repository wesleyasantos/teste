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
    import { ref, reactive, computed, onMounted } from 'vue';
    import { useRoute, useRouter } from 'vue-router';

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
        name: '',
        role: '',
        document: '',
        email: '',
        phone: '',
        share: 0
        });
        
        const editingGuarantee = reactive({
        id: null,
        type: '',
        value: 0,
        description: '',
        registration_number: '',
        location: '',
        notes: ''
        });
        
        const uploadingDocument = reactive({
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
        sector: 'commerce',
        pgdas: Array(12).fill(0),
        pgdasTotal: 0,
        financialExpenses: {
            overdraft: { name: 'Cheque Especial', value: 0, percentage: 7, result: 0 },
            advance: { name: 'Adiantamento ao Depositante', value: 0, percentage: 15, result: 0 },
            guaranteed: { name: 'Conta Garantida', value: 0, percentage: 3.90, result: 0 },
            workingCapital: { name: 'Capital de Giro com Teto Rotativo', value: 0, percentage: 2.70, result: 0 },
            checkDiscount: { name: 'Desconto de Cheques', value: 0, percentage: 2.67, result: 0 },
            duplicateDiscount: { name: 'Desconto de Duplicatas', value: 0, percentage: 2.08, result: 0 },
            creditCard: { name: 'Desconto Antecipação de Cartão de Crédito', value: 0, percentage: 1.21, result: 0 },
            receivables: { name: 'Recebíveis Adquiridos', value: 0, percentage: 2.08, result: 0 }
        },
        financialExpensesTotal: 0,
        shortTerm: {
            days30: { name: 'a Vencer até 30 dias', value: 0 },
            days60: { name: 'a Vencer de 31 a 60 dias', value: 0 },
            days90: { name: 'a Vencer de 61 a 90 dias', value: 0 },
            days180: { name: 'a Vencer de 91 a 180 dias', value: 0 },
            days360: { name: 'a Vencer de 181 a 360 dias', value: 0 }
        },
        shortTermTotal: 0,
        futureModality: {
            overdraft: { name: 'Cheque Especial', value: 0 },
            advance: { name: 'Adiantamento ao Depositante', value: 0 },
            guaranteed: { name: 'Conta Garantida', value: 0 },
            checkDiscount: { name: 'Desconto de Cheques', value: 0 },
            duplicateDiscount: { name: 'Desconto de Duplicatas', value: 0 },
            creditCard: { name: 'Antecipação de Fatura de Cartão', value: 0 }
        },
        futureModalityTotal: 0,
        monthlyRepayment: 0,
        sectorExpense: 0,
        grossProfit: 0,
        availability1: 0,
        availability2: 0,
        surplus: 0,
        approved: null
        });
        
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
            // No MVP, usaremos dados simulados
            operation.value = {
            id: operationId.value,
            client_id: 1,
            amount: 150000,
            modality: 'Capital de Giro',
            term: 36,
            interest_rate: 1.5,
            amortization_system: 'price',
            created_at: '2025-02-15T10:30:00',
            status: 'analysis',
            monitoring_status: 'normal'
            };
            
            // Definir estágio atual
            currentStage.value = operation.value.status;
            
            // Definir datas dos estágios
            stageDates.value = {
            pending: operation.value.created_at,
            verification: '2025-02-16T11:45:00',
            analysis: '2025-02-17T09:30:00'
            };
            
            // Buscar cliente
            fetchClient(operation.value.client_id);
            
            // Gerar plano de pagamento
            generatePaymentPlan();
            
            // Buscar sócios
            fetchPartners();
            
            // Buscar garantias
            fetchGuarantees();
            
            // Buscar documentos
            fetchDocuments();
            
            // Buscar dados do comitê
            fetchCommittee();
            
            // Buscar dados de formalização
            fetchFormalization();
        } catch (error) {
            console.error('Erro ao buscar operação:', error);
        }
        };
        
        // Buscar cliente
        const fetchClient = async (clientId) => {
        try {
            // No MVP, usaremos dados simulados
            client.value = {
            id: clientId,
            name: 'Tech Solutions Ltda',
            document: '12.345.678/0001-90',
            email: 'contato@techsolutions.com',
            phone: '(11) 98765-4321'
            };
        } catch (error) {
            console.error('Erro ao buscar cliente:', error);
        }
        };
        
        // Gerar plano de pagamento
        const generatePaymentPlan = () => {
        try {
            const principal = operation.value.amount;
            const term = operation.value.term;
            const rate = operation.value.interest_rate / 100;
            
            // Usar o sistema de amortização correto
            if (operation.value.amortization_system === 'price') {
            calculatePriceSystem(principal, term, rate);
            } else if (operation.value.amortization_system === 'sac') {
            calculateSACSystem(principal, term, rate);
            } else {
            // Caso default: Price
            calculatePriceSystem(principal, term, rate);
            }
        } catch (error) {
            console.error('Erro ao gerar plano de pagamento:', error);
        }
        };
        
        // Calcular com Sistema Price
        const calculatePriceSystem = (principal, term, rate) => {
        const installment = (principal * rate * Math.pow(1 + rate, term)) / (Math.pow(1 + rate, term) - 1);
        
        firstInstallment.value = installment;
        totalAmount.value = installment * term;
        
        // Gerar plano de pagamento
        paymentPlan.value = [];
        let balance = principal;
        let currentDate = new Date('2025-03-15');
        
        for (let i = 1; i <= term; i++) {
            const interest = balance * rate;
            const amortization = installment - interest;
            balance -= amortization;
            
            // Definir status baseado na data atual
            let status = 'future';
            const today = new Date();
            
            if (currentDate < today) {
            if (i <= 2) {
                status = 'paid';
            } else {
                status = 'overdue';
            }
            } else if (i === 3) {
            status = 'pending';
            }
            
            paymentPlan.value.push({
            installment: i,
            date: new Date(currentDate),
            payment: installment,
            amortization: amortization,
            interest: interest,
            balance: balance < 0.01 ? 0 : balance,
            status: status,
            payment_date: status === 'paid' ? new Date(currentDate.getTime() - Math.random() * 5 * 24 * 60 * 60 * 1000) : null
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
        const firstPaymentValue = amortization + firstInterest;
        
        firstInstallment.value = firstPaymentValue;
        
        // Gerar plano de pagamento
        paymentPlan.value = [];
        let balance = principal;
        let total = 0;
        let currentDate = new Date('2025-03-15');
        
        for (let i = 1; i <= term; i++) {
            const interest = balance * rate;
            const payment = amortization + interest;
            balance -= amortization;
            total += payment;
            
            // Definir status baseado na data atual
            let status = 'future';
            const today = new Date();
            
            if (currentDate < today) {
            if (i <= 2) {
                status = 'paid';
            } else {
                status = 'overdue';
            }
            } else if (i === 3) {
            status = 'pending';
            }
            
            paymentPlan.value.push({
            installment: i,
            date: new Date(currentDate),
            payment: payment,
            amortization: amortization,
            interest: interest,
            balance: balance < 0.01 ? 0 : balance,
            status: status,
            payment_date: status === 'paid' ? new Date(currentDate.getTime() - Math.random() * 5 * 24 * 60 * 60 * 1000) : null
            });
            
            // Avançar para o próximo mês
            currentDate.setMonth(currentDate.getMonth() + 1);
        }
        
        totalAmount.value = total;
        };
        
        // Buscar sócios
        const fetchPartners = async () => {
        try {
            // No MVP, usaremos dados simulados
            partners.value = [
            {
                id: 1,
                name: 'João Silva',
                role: 'Sócio-Administrador',
                document: '123.456.789-00',
                email: 'joao.silva@example.com',
                phone: '(11) 98765-4321',
                share: 70
            },
            {
                id: 2,
                name: 'Maria Souza',
                role: 'Sócia',
                document: '987.654.321-00',
                email: 'maria.souza@example.com',
                phone: '(11) 91234-5678',
                share: 30
            }
            ];
        } catch (error) {
            console.error('Erro ao buscar sócios:', error);
        }
        };
        
        // Buscar garantias
        const fetchGuarantees = async () => {
        try {
            // No MVP, usaremos dados simulados
            guarantees.value = [
            {
                id: 1,
                type: 'property',
                value: 300000,
                description: 'Imóvel Comercial - Centro',
                registration_number: '123456',
                location: 'Av. Paulista, 1000 - São Paulo/SP',
                notes: 'Imóvel livre de ônus.'
            }
            ];
        } catch (error) {
            console.error('Erro ao buscar garantias:', error);
        }
        };
        
        // Buscar documentos
        const fetchDocuments = async () => {
        try {
            // No MVP, usaremos dados simulados
            documents.value = [
            {
                id: 1,
                type: 'authorization',
                name: 'Termo de Autorização',
                file: '#',
                uploaded_at: '2025-02-15T10:30:00'
            },
            {
                id: 2,
                type: 'business',
                name: 'Contrato Social',
                file: '#',
                uploaded_at: '2025-02-15T10:35:00'
            },
            {
                id: 3,
                type: 'income',
                name: 'Balanço Patrimonial',
                file: '#',
                uploaded_at: '2025-02-15T10:40:00'
            }
            ];
        } catch (error) {
            console.error('Erro ao buscar documentos:', error);
        }
        };
        
        // Buscar dados do comitê
        const fetchCommittee = async () => {
        try {
            // No MVP, usaremos dados simulados
            committee.members = [
            {
                id: 1,
                name: 'Carlos Gomes',
                role: 'Gerente',
                vote: null,
                voted_at: null,
                notes: ''
            },
            {
                id: 2,
                name: 'Ana Ferreira',
                role: 'Analista Sênior',
                vote: null,
                voted_at: null,
                notes: ''
            }
            ];
        } catch (error) {
            console.error('Erro ao buscar dados do comitê:', error);
        }
        };
        
        // Buscar dados de formalização
        const fetchFormalization = async () => {
        try {
            // No MVP, usaremos dados simulados
            // Dados vazios, pois a operação ainda não chegou nessa etapa
        } catch (error) {
            console.error('Erro ao buscar dados de formalização:', error);
        }
        };
        
        // Funções para o gerenciamento de sócios
        const editPartner = (partner) => {
        Object.assign(editingPartner, { ...partner });
        showPartnerForm.value = true;
        };
        
        const savePartner = () => {
        if (editingPartner.id) {
            // Atualizar sócio existente
            const index = partners.value.findIndex(p => p.id === editingPartner.id);
            if (index !== -1) {
            partners.value[index] = { ...editingPartner };
            }
        } else {
            // Adicionar novo sócio
            const newId = partners.value.length > 0 
            ? Math.max(...partners.value.map(p => p.id)) + 1 
            : 1;
            
            partners.value.push({
            ...editingPartner,
            id: newId
            });
        }
        
        // Limpar formulário e fechar modal
        resetPartnerForm();
        showPartnerForm.value = false;
        };
        
        const removePartner = (partnerId) => {
        if (confirm('Tem certeza que deseja remover este sócio?')) {
            partners.value = partners.value.filter(p => p.id !== partnerId);
        }
        };
        
        const resetPartnerForm = () => {
        Object.assign(editingPartner, {
            id: null,
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
        
        const saveGuarantee = () => {
        if (editingGuarantee.id) {
            // Atualizar garantia existente
            const index = guarantees.value.findIndex(g => g.id === editingGuarantee.id);
            if (index !== -1) {
            guarantees.value[index] = { ...editingGuarantee };
            }
        } else {
            // Adicionar nova garantia
            const newId = guarantees.value.length > 0 
            ? Math.max(...guarantees.value.map(g => g.id)) + 1 
            : 1;
            
            guarantees.value.push({
            ...editingGuarantee,
            id: newId
            });
        }
        
        // Limpar formulário e fechar modal
        resetGuaranteeForm();
        showGuaranteeForm.value = false;
        };
        
        const removeGuarantee = (guaranteeId) => {
        if (confirm('Tem certeza que deseja remover esta garantia?')) {
            guarantees.value = guarantees.value.filter(g => g.id !== guaranteeId);
        }
        };
        
        const resetGuaranteeForm = () => {
        Object.assign(editingGuarantee, {
            id: null,
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
        
        const uploadDocument = () => {
        // Em uma aplicação real, enviaria o arquivo para o servidor
        const newId = documents.value.length > 0 
            ? Math.max(...documents.value.map(d => d.id)) + 1 
            : 1;
        
        documents.value.push({
            id: newId,
            type: uploadingDocument.type,
            name: uploadingDocument.name,
            file: '#', // URL simulada
            notes: uploadingDocument.notes,
            uploaded_at: new Date().toISOString()
        });
        
        // Limpar formulário e fechar modal
        uploadingDocument.type = '';
        uploadingDocument.name = '';
        uploadingDocument.file = null;
        uploadingDocument.notes = '';
        fileUploadInfo.value = 'Nenhum arquivo selecionado';
        showDocumentUpload.value = false;
        };
        
        const removeDocument = (documentId) => {
        if (confirm('Tem certeza que deseja remover este documento?')) {
            documents.value = documents.value.filter(d => d.id !== documentId);
        }
        };
        
        // Funções para a análise de crédito
        const calculateAnalysis = () => {
        // Calcular total do PGDAS
        analysis.pgdasTotal = analysis.pgdas.reduce((sum, value) => sum + parseFloat(value || 0), 0);
        
        // Calcular resultados das despesas financeiras
        for (const key in analysis.financialExpenses) {
            const expense = analysis.financialExpenses[key];
            expense.result = (parseFloat(expense.value || 0) * expense.percentage / 100);
        }
        
        // Calcular total das despesas financeiras
        analysis.financialExpensesTotal = Object.values(analysis.financialExpenses)
            .reduce((sum, expense) => sum + expense.result, 0);
        
        // Calcular total do curto prazo
        analysis.shortTermTotal = Object.values(analysis.shortTerm)
            .reduce((sum, period) => sum + parseFloat(period.value || 0), 0);
        
        // Calcular total da modalidade futuro
        analysis.futureModalityTotal = Object.values(analysis.futureModality)
            .reduce((sum, future) => sum + parseFloat(future.value || 0), 0);
        
        // Calcular reposição mensal
        analysis.monthlyRepayment = (analysis.shortTermTotal - analysis.futureModalityTotal) / 12;
        if (analysis.monthlyRepayment < 0) analysis.monthlyRepayment = 0;
        
        // Calcular equações finais
        const sectorPercentages = {
            commerce: 75,
            service: 70,
            transport: 85,
            industry: 90
        };
        
        // Despesa setorial
        analysis.sectorExpense = analysis.pgdasTotal * (sectorPercentages[analysis.sector] / 100);
        
        // Lucro bruto
        analysis.grossProfit = analysis.pgdasTotal - analysis.sectorExpense;
        
        // Disponibilidade mensal 1
        analysis.availability1 = (analysis.grossProfit - analysis.financialExpensesTotal) / 12;
        
        // Disponibilidade mensal 2
        analysis.availability2 = analysis.availability1 - analysis.monthlyRepayment;
        
        // Superávit ou déficit
        analysis.surplus = analysis.availability2 - firstInstallment.value;
        
        // Decisão
        analysis.approved = analysis.surplus >= 0;
        };
        
        // Gerar análise de IA
        const generateAIAnalysis = () => {
        isGeneratingAI.value = true;
        
        // Simular tempo de processamento
        setTimeout(() => {
            // Em uma aplicação real, chamaríamos uma API de IA
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
        const startCommittee = () => {
        committee.status = 'in_progress';
        committee.started_at = new Date().toISOString();
        };
        
        const submitVote = () => {
        // Em uma aplicação real, chamaríamos a API
        const currentUser = {
            id: 1,
            name: 'Carlos Gomes'
        };
        
        // Encontrar o membro correspondente ao usuário atual
        const memberIndex = committee.members.findIndex(m => m.name === currentUser.name);
        if (memberIndex !== -1) {
            committee.members[memberIndex].vote = voting.vote;
            committee.members[memberIndex].voted_at = new Date().toISOString();
            committee.members[memberIndex].notes = voting.notes;
            
            // Verificar se todos os membros votaram
            const allVoted = committee.members.every(m => m.vote !== null);
            
            if (allVoted) {
            finishCommittee();
            }
        }
        
        // Limpar formulário de votação
        voting.vote = '';
        voting.notes = '';
        };
        
        const finishCommittee = () => {
        committee.status = 'completed';
        committee.completed_at = new Date().toISOString();
        
        // Determinar decisão final
        // No MVP, vamos considerar a decisão como aprovada se pelo menos um membro aprovou
        const hasApprovals = committee.members.some(m => m.vote === 'approve');
        committee.decision = hasApprovals ? 'approved' : 'rejected';
        };
        
        // Funções para a formalização
        const generateContract = () => {
        // Em uma aplicação real, chamaríamos a API
        formalization.contract = {
            number: '2025/' + operationId.value,
            generated_at: new Date().toISOString(),
            status: 'pending_signature',
            file: '#' // URL simulada
        };
        
        // Adicionar signatários
        formalization.signatures = [
            {
            id: 1,
            name: client.value.name,
            email: client.value.email,
            status: 'pending',
            signed_at: null
            },
            {
            id: 2,
            name: 'Representante da Instituição',
            email: 'representante@instituicao.com',
            status: 'pending',
            signed_at: null
            }
        ];
        };
        
        const sendSignatureReminder = (signatureId) => {
        // Em uma aplicação real, chamaríamos a API
        alert('Lembrete de assinatura enviado com sucesso!');
        };
        
        const releaseCredit = () => {
        // Em uma aplicação real, chamaríamos a API
        formalization.credit_release_date = new Date().toISOString();
        
        // Atualizar status para monitoramento
        moveToStage('monitoring');
        };
        
        // Funções para pagamento
        const recordPayment = (installment) => {
        paymentData.installment = installment.installment;
        paymentData.amount = installment.payment;
        showPaymentModal.value = true;
        };
        
        const confirmPayment = () => {
        // Em uma aplicação real, chamaríamos a API
        
        // Atualizar status da parcela
        const index = paymentPlan.value.findIndex(i => i.installment === paymentData.installment);
        if (index !== -1) {
            paymentPlan.value[index].status = 'paid';
            paymentPlan.value[index].payment_date = new Date(paymentData.date);
        }
        
        showPaymentModal.value = false;
        };
        
        const calculateOverdueDays = (installment) => {
        if (installment.status !== 'overdue') return '-';
        
        const today = new Date();
        const dueDate = new Date(installment.date);
        const diffTime = Math.abs(today - dueDate);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        
        return diffDays;
        };
        
        // Funções para acompanhamento
        const getNextInstallmentDate = () => {
        const pendingInstallment = paymentPlan.value.find(i => i.status === 'pending');
        return pendingInstallment ? formatDate(pendingInstallment.date) : '-';
        };
        
        const getNextInstallmentAmount = () => {
        const pendingInstallment = paymentPlan.value.find(i => i.status === 'pending');
        return pendingInstallment ? pendingInstallment.payment : 0;
        };
        
        // Transições de estágio
        const moveToStage = (stageId) => {
        // Em uma aplicação real, chamaríamos a API
        operation.value.status = stageId;
        currentStage.value = stageId;
        
        // Registrar data da transição
        stageDates.value[stageId] = new Date().toISOString();
        };
        
        // Função para verificação
        const verifyOperation = () => {
        // Em uma aplicação real, chamaríamos a API
        moveToStage('analysis');
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
        // No MVP, vamos simular que o usuário é Carlos Gomes
        if (committee.status !== 'in_progress') return false;
        
        const currentUser = { name: 'Carlos Gomes' };
        const member = committee.members.find(m => m.name === currentUser.name);
        
        return member && member.vote === null;
        });
        
        const isCommitteeManager = computed(() => {
        // No MVP, vamos simular que o usuário é gerente
        return true;
        });
        
        const areAllSignaturesCompleted = computed(() => {
        if (!formalization.signatures.length) return false;
        return formalization.signatures.every(s => s.status === 'signed');
        });
        
        const canReleaseCredit = computed(() => {
        if (!formalization.contract) return false;
        return areAllSignaturesCompleted.value;
        });
        
        // Funções para salvar análise e gerar relatório
        const saveAnalysis = () => {
        // Em uma aplicação real, chamaríamos a API
        alert('Análise salva com sucesso!');
        };
        
        const generateReport = () => {
        // Em uma aplicação real, chamaríamos a API
        alert('Relatório gerado com sucesso!');
        };
        
        onMounted(() => {
        fetchOperation();
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
      padding: 20px;
    }
    
    .page-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 30px;
    }
    
    /* Fluxo da operação */
    .operation-flow {
      display: flex;
      align-items: center;
      margin-bottom: 30px;
      padding: 20px;
      background-color: white;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      overflow-x: auto;
    }
    
    .flow-stage {
      display: flex;
      flex-direction: column;
      align-items: center;
      position: relative;
      flex: 1;
      min-width: 120px;
      opacity: 0.5;
    }
    
    .flow-stage.active {
      opacity: 1;
    }
    
    .flow-stage.completed .stage-indicator {
      background-color: #4CAF50;
      color: white;
    }
    
    .flow-stage.current .stage-indicator {
      background-color: var(--primary-color);
      color: white;
      transform: scale(1.1);
      box-shadow: 0 4px 10px rgba(0, 0, 75, 0.2);
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
      margin-bottom: 10px;
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
      background-color: #4CAF50;
    }
    
    /* Tabs de navegação */
    .operation-tabs {
      display: flex;
      overflow-x: auto;
      margin-bottom: 20px;
      border-bottom: 1px solid #ddd;
      padding-bottom: 1px;
    }
    
    .tab-button {
      padding: 10px 20px;
      background: none;
      border: none;
      cursor: pointer;
      font-size: 14px;
      color: #666;
      border-bottom: 3px solid transparent;
      white-space: nowrap;
    }
    
    .tab-button.active {
      color: var(--primary-color);
      border-bottom-color: var(--primary-color);
      font-weight: 500;
    }
    
    .tab-button:hover {
      color: var(--primary-color);
    }
    
    /* Conteúdo das abas */
    .tab-pane {
      background-color: white;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      padding: 20px;
      margin-bottom: 20px;
    }
    
    .content-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
      gap: 20px;
    }
    
    .info-card {
      background-color: #f9f9f9;
      border-radius: 8px;
      padding: 20px;
    }
    
    .info-card h2 {
      margin-top: 0;
      margin-bottom: 20px;
      padding-bottom: 10px;
      border-bottom: 1px solid #eee;
      font-size: 18px;
      color: var(--primary-color);
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
    
    .info-actions {
      display: flex;
      justify-content: flex-end;
      margin-top: 20px;
    }
    
    /* Badges e status */
    .status-badge {
      display: inline-block;
      padding: 6px 12px;
      border-radius: 4px;
      font-size: 14px;
      font-weight: 500;
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
      grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
      gap: 15px;
      margin-bottom: 20px;
    }
    
    .summary-card {
      background-color: #f9f9f9;
      border-radius: 6px;
      padding: 15px;
      text-align: center;
    }
    
    .summary-title {
      font-size: 14px;
      color: #666;
      margin-bottom: 8px;
    }
    
    .summary-value {
      font-size: 18px;
      font-weight: 600;
      color: #333;
    }
    
    .table-container {
      margin-top: 20px;
      overflow-x: auto;
    }
    
    .table-container h3 {
      margin-top: 0;
      margin-bottom: 15px;
      font-size: 16px;
    }
    
    table {
      width: 100%;
      border-collapse: collapse;
    }
    
    th, td {
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid #eee;
      font-size: 14px;
    }
    
    th {
      background-color: #f5f5f5;
      font-weight: 500;
      position: sticky;
      top: 0;
      z-index: 10;
    }
    
    .payment-status {
      display: inline-block;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 500;
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
      margin-bottom: 20px;
    }
    
    .partners-header h2 {
      margin: 0;
      font-size: 18px;
    }
    
    .partners-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 20px;
    }
    
    .partner-card {
      background-color: #f9f9f9;
      border-radius: 8px;
      overflow: hidden;
    }
    
    .partner-header {
      padding: 15px;
      background-color: #f0f0f0;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .partner-name {
      font-size: 16px;
      font-weight: 600;
    }
    
    .partner-role-badge {
      background-color: #E1F5FE;
      color: #0288D1;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 500;
    }
    
    .partner-info {
      padding: 15px;
    }
    
    .info-item {
      margin-bottom: 10px;
      display: flex;
      align-items: center;
    }
    
    .info-icon {
      margin-right: 10px;
      color: #666;
      width: 20px;
      text-align: center;
    }
    
    .partner-actions {
      display: flex;
      padding: 15px;
      background-color: #f0f0f0;
      gap: 10px;
    }
    
    .btn-edit, .btn-delete, .btn-view, .btn-add {
      padding: 6px 12px;
      border-radius: 4px;
      font-size: 14px;
      border: none;
      cursor: pointer;
      transition: all 0.3s ease;
    }
    
    .btn-edit {
      background-color: #FFF8E1;
      color: #FFA000;
    }
    
    .btn-delete {
      background-color: #FFEBEE;
      color: #D32F2F;
    }
    
    .btn-view {
      background-color: #E3F2FD;
      color: #1976D2;
      text-decoration: none;
    }
    
    .btn-add {
      background-color: #E8F5E9;
      color: #388E3C;
      display: flex;
      align-items: center;
      gap: 5px;
    }
    
    .btn-edit:hover, .btn-delete:hover, .btn-view:hover, .btn-add:hover {
      opacity: 0.8;
    }
    
    /* Garantias */
    .guarantees-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }
    
    .guarantees-header h2 {
      margin: 0;
      font-size: 18px;
    }
    
    .guarantees-list {
      display: flex;
      flex-direction: column;
      gap: 15px;
    }
    
    .guarantee-card {
      background-color: #f9f9f9;
      border-radius: 8px;
      padding: 15px;
      display: flex;
      align-items: flex-start;
      gap: 15px;
    }
    
    .guarantee-type-badge {
      padding: 6px 12px;
      border-radius: 4px;
      font-size: 14px;
      font-weight: 500;
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
    }
    
    .info-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 10px;
      margin-bottom: 15px;
    }
    
    .guarantee-notes {
      border-top: 1px solid #eee;
      padding-top: 10px;
    }
    
    .guarantee-notes .label {
      display: block;
      margin-bottom: 5px;
    }
    
    .guarantee-notes p {
      margin: 0;
      color: #666;
    }
    
    .guarantee-actions {
      display: flex;
      flex-direction: column;
      gap: 5px;
    }
    
    /* Documentos */
    .documents-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }
    
    .documents-header h2 {
      margin: 0;
      font-size: 18px;
    }
    
    .documents-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 15px;
    }
    
    .document-card {
      background-color: #f9f9f9;
      border-radius: 8px;
      padding: 15px;
      display: flex;
      align-items: center;
      gap: 15px;
    }
    
    .document-icon {
      font-size: 24px;
      color: #1976D2;
      width: 40px;
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #E3F2FD;
      border-radius: 8px;
    }
    
    .document-info {
      flex: 1;
    }
    
    .document-name {
      font-weight: 500;
      margin-bottom: 5px;
    }
    
    .document-meta {
      font-size: 12px;
      color: #666;
      display: flex;
      gap: 15px;
    }
    
    .document-type {
      background-color: #f0f0f0;
      padding: 2px 6px;
      border-radius: 4px;
    }
    
    .document-actions {
      display: flex;
      gap: 5px;
    }
    
    /* Upload de arquivo */
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
      display: inline-flex;
      align-items: center;
      gap: 5px;
      background-color: #F5F5F5;
      color: #333;
      padding: 8px 15px;
      border-radius: 4px;
      cursor: pointer;
      border: 1px solid #ddd;
    }
    
    .file-info {
      margin-left: 10px;
      font-size: 14px;
      color: #666;
    }
    
    /* Estado vazio */
    .empty-state {
      padding: 40px 20px;
      text-align: center;
      background-color: #f9f9f9;
      border-radius: 8px;
      margin-bottom: 20px;
    }
    
    .empty-state p {
      color: #666;
      margin-bottom: 20px;
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
    }
    
    .modal-content {
      background-color: white;
      padding: 20px;
      border-radius: 8px;
      width: 600px;
      max-width: 90%;
      max-height: 90vh;
      overflow-y: auto;
      position: relative;
    }
    
    .close {
      position: absolute;
      top: 10px;
      right: 15px;
      font-size: 24px;
      cursor: pointer;
      color: #666;
    }
    
    /* Formulários */
    .form-row {
      display: flex;
      flex-wrap: wrap;
      gap: 15px;
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
      padding: 8px;
      border: 1px solid #ddd;
      border-radius: 4px;
      font-size: 14px;
    }
    
    .form-actions {
      display: flex;
      justify-content: flex-end;
      gap: 10px;
      margin-top: 20px;
    }
    
    .btn-cancel, .btn-save, .btn-upload, .btn-confirm {
      padding: 8px 16px;
      border-radius: 4px;
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;
      border: none;
    }
    
    .btn-cancel {
      background-color: #f5f5f5;
      color: #333;
    }
    
    .btn-save, .btn-confirm {
      background-color: var(--primary-color);
      color: white;
    }
    
    .btn-upload {
      background-color: #2196F3;
      color: white;
    }
    
    /* Análise de crédito */
    .analysis-tabs {
      display: flex;
      overflow-x: auto;
      margin-bottom: 15px;
      border-bottom: 1px solid #ddd;
    }
    
    .analysis-tab-button {
      padding: 8px 16px;
      background: none;
      border: none;
      cursor: pointer;
      font-size: 14px;
      color: #666;
      border-bottom: 2px solid transparent;
      white-space: nowrap;
    }
    
    .analysis-tab-button.active {
      color: var(--primary-color);
      border-bottom-color: var(--primary-color);
      font-weight: 500;
    }
    
    .analysis-pane {
      margin-top: 20px;
    }
    
    .analysis-pane h3 {
      margin-top: 0;
      margin-bottom: 15px;
      font-size: 16px;
      color: var(--primary-color);
    }
    
    .data-input-section {
      margin-bottom: 20px;
    }
    
    .data-input-section h4 {
      margin-top: 20px;
      margin-bottom: 10px;
      font-size: 14px;
      color: #333;
    }
    
    .radio-group {
      display: flex;
      flex-wrap: wrap;
      gap: 15px;
      margin-bottom: 15px;
    }
    
    .radio-label {
      display: flex;
      align-items: center;
      cursor: pointer;
    }
    
    .radio-label input {
      margin-right: 5px;
      width: auto;
    }
    
    .input-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 20px;
    }
    
    .input-table th, .input-table td {
      padding: 10px;
      text-align: left;
      border-bottom: 1px solid #eee;
    }
    
    .input-table th {
      background-color: #f5f5f5;
      font-weight: 500;
    }
    
    .input-table input {
      width: 100%;
      padding: 8px;
      border: 1px solid #ddd;
      border-radius: 4px;
    }
    
    .total-row {
      font-weight: 600;
      background-color: #f9f9f9;
    }
    
    .calculation-result {
      background-color: #f5f5f5;
      padding: 15px;
      border-radius: 8px;
      margin-top: 20px;
    }
    
    .result-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .result-label {
      font-weight: 500;
    }
    
    .result-value {
      font-weight: 600;
      color: var(--primary-color);
    }
    
    .results-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 15px;
      margin-bottom: 20px;
    }
    
    .result-card {
      background-color: #f9f9f9;
      border-radius: 8px;
      padding: 15px;
    }
    
    .result-title {
      font-weight: 500;
      margin-bottom: 10px;
      color: #555;
    }
    
    .result-value {
      font-size: 18px;
      font-weight: 600;
      color: #333;
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
      padding: 20px;
    }
    
    .result-decision {
      font-size: 24px;
      font-weight: 700;
      margin: 10px 0;
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
    }
    
    .analysis-actions {
      display: flex;
      justify-content: center;
      gap: 15px;
      margin-top: 20px;
    }
    
    .btn-report {
      background-color: #FFA000;
      color: white;
      padding: 8px 16px;
      border-radius: 4px;
      border: none;
      font-weight: 500;
      cursor: pointer;
    }
    
    /* Análise IA */
    .ai-section {
      background-color: #f9f9f9;
      border-radius: 8px;
      padding: 20px;
    }
    
    .ai-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }
    
    .ai-badge {
      background-color: #E1F5FE;
      color: #0288D1;
      padding: 6px 12px;
      border-radius: 20px;
      font-size: 14px;
      font-weight: 500;
    }
    
    .btn-ai {
      background-color: #0288D1;
      color: white;
      padding: 8px 16px;
      border-radius: 4px;
      border: none;
      font-weight: 500;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
    }
    
    .btn-ai:disabled {
      opacity: 0.7;
      cursor: not-allowed;
    }
    
    .ai-result {
      border: 1px solid #E1F5FE;
      border-radius: 8px;
      padding: 20px;
      background-color: white;
    }
    
    .recommendation-box {
      padding: 15px;
      border-radius: 6px;
      margin-bottom: 20px;
    }
    
    .recommendation-box h4 {
      margin-top: 0;
      margin-bottom: 10px;
      font-size: 16px;
      font-weight: 600;
    }
    
    .recommendation-box p {
      margin: 0;
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
    
    .risk-indicator {
      margin-bottom: 20px;
    }
    
    .risk-label {
      font-weight: 500;
      margin-bottom: 5px;
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
    
    .risk-value {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 500;
    }
    
    .risk-note {
      font-size: 12px;
      color: #666;
      font-weight: normal;
    }
    
    .ai-explanation {
      background-color: #F5F5F5;
      border-radius: 6px;
      padding: 15px;
    }
    
    .ai-explanation h4 {
      margin-top: 0;
      margin-bottom: 10px;
      font-size: 16px;
    }
    
    .ai-explanation pre {
      white-space: pre-wrap;
      font-family: inherit;
      font-size: 14px;
      margin: 0;
      color: #555;
    }
    
    .ai-empty-state {
      text-align: center;
      padding: 30px;
      color: #666;
    }
    
    /* Comitê de Crédito */
    .committee-section {
      padding: 15px 0;
    }
    
    .committee-status {
      background-color: #f9f9f9;
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 20px;
      display: flex;
      gap: 20px;
    }
    
    .status-indicator {
      background-color: #f0f0f0;
      color: #666;
      padding: 10px 20px;
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      align-items: center;
      min-width: 160px;
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
      margin: 0 0 10px;
    }
    
    .btn-start-committee, .btn-finish-committee {
      background-color: var(--primary-color);
      color: white;
      padding: 8px 16px;
      border-radius: 4px;
      border: none;
      font-weight: 500;
      cursor: pointer;
    }
    
    .committee-table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: 20px;
    }
    
    .committee-voting {
      background-color: #f9f9f9;
      border-radius: 8px;
      padding: 20px;
      margin-top: 20px;
    }
    
    .committee-voting h3 {
      margin-top: 0;
      margin-bottom: 15px;
      font-size: 16px;
    }
    
    .vote-form {
      padding: 15px;
      background-color: white;
      border-radius: 8px;
    }
    
    .vote-options {
      display: flex;
      gap: 15px;
      margin-bottom: 15px;
    }
    
    .vote-option {
      display: flex;
      align-items: center;
      cursor: pointer;
    }
    
    .vote-option input {
      margin-right: 5px;
      width: auto;
    }
    
    .vote-label {
      padding: 4px 10px;
      border-radius: 4px;
      font-size: 14px;
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
      display: inline-block;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 500;
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
    background-color: var(--primary-color);
    color: white;
    padding: 8px 16px;
    border-radius: 4px;
    border: none;
    font-weight: 500;
    cursor: pointer;
    }

    .btn-vote:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    }

    .committee-management {
    margin-top: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 20px;
    }

    .committee-management h3 {
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 16px;
    }

    .committee-management p {
    margin-bottom: 15px;
    color: #666;
    }

    .decision-badge {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
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
    background-color: #f9f9f9;
    border-radius: 8px;
    padding: 20px;
    margin-top: 20px;
    }

    .contract-info h3 {
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 16px;
    }

    .formalization-actions {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    }

    .formalization-actions p {
    margin-bottom: 10px;
    }

    .btn-generate {
    background-color: var(--primary-color);
    color: white;
    padding: 8px 16px;
    border-radius: 4px;
    border: none;
    font-weight: 500;
    cursor: pointer;
    }

    .contract-details {
    margin-top: 20px;
    }

    .contract-document {
    margin-top: 20px;
    display: flex;
    justify-content: center;
    }

    .btn-view-contract {
    background-color: #E3F2FD;
    color: #1976D2;
    padding: 10px 20px;
    border-radius: 4px;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-weight: 500;
    }

    .btn-view-contract i {
    font-size: 18px;
    }

    .contract-status {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
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
    margin-bottom: 15px;
    font-size: 16px;
    }

    .signatures-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    }

    .signature-status {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
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
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    background-color: #f0f0f0;
    color: #666;
    border: none;
    cursor: pointer;
    }

    .btn-release {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border-radius: 4px;
    border: none;
    font-weight: 500;
    cursor: pointer;
    }

    /* Acompanhamento */
    .monitoring-section {
    padding: 15px 0;
    }

    .monitoring-summary {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 15px;
    margin-bottom: 20px;
    }

    .monitoring-status {
    display: inline-block;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
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
    margin-top: 30px;
    }

    .installments-tracking h3 {
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 16px;
    }

    .installments-table {
    width: 100%;
    border-collapse: collapse;
    }

    .btn-record-payment {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    background-color: #E8F5E9;
    color: #388E3C;
    border: none;
    cursor: pointer;
    }

    /* Ações de estágio */
    .stage-actions {
    display: flex;
    justify-content: flex-end;
    margin-top: 30px;
    }

    .btn-primary, .btn-success {
    padding: 10px 20px;
    border-radius: 4px;
    font-weight: 500;
    cursor: pointer;
    border: none;
    margin-left: 10px;
    }

    .btn-primary {
    background-color: var(--primary-color);
    color: white;
    }

    .btn-success {
    background-color: #4CAF50;
    color: white;
    }

    .btn-primary:hover, .btn-success:hover {
    opacity: 0.9;
    }
    </style>