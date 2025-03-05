<template>
    <div class="settings-container">
      <div class="page-header">
        <h1>Configurações do Sistema</h1>
      </div>
      
      <div class="tabs">
        <button 
          @click="activeTab = 'users'" 
          :class="{ active: activeTab === 'users' }"
          class="tab-button"
        >
          Gestão de Usuários
        </button>
        <button 
          @click="activeTab = 'creditPolicy'" 
          :class="{ active: activeTab === 'creditPolicy' }"
          class="tab-button"
        >
          Políticas de Crédito
        </button>
        <button 
          @click="activeTab = 'workflow'" 
          :class="{ active: activeTab === 'workflow' }"
          class="tab-button"
        >
          Fluxo de Aprovação
        </button>
      </div>
      
      <div class="tab-content">
        <!-- Gestão de Usuários -->
        <div v-if="activeTab === 'users'" class="users-tab">
          <div class="settings-card">
            <h2>Usuários do Sistema</h2>
            <table class="users-table">
              <thead>
                <tr>
                  <th>Nome</th>
                  <th>Usuário</th>
                  <th>Perfil</th>
                  <th>Email</th>
                  <th>Status</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in users" :key="user.id">
                  <td>{{ user.name }}</td>
                  <td>{{ user.username }}</td>
                  <td>{{ getRoleLabel(user.role) }}</td>
                  <td>{{ user.email }}</td>
                  <td>
                    <span :class="user.is_active ? 'status-active' : 'status-inactive'">
                      {{ user.is_active ? 'Ativo' : 'Inativo' }}
                    </span>
                  </td>
                  <td class="actions">
                    <button @click="editUser(user)" class="btn-edit">Editar</button>
                    <button 
                      @click="toggleUserStatus(user)" 
                      :class="user.is_active ? 'btn-deactivate' : 'btn-activate'"
                    >
                      {{ user.is_active ? 'Desativar' : 'Ativar' }}
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
            <div class="add-button-container">
              <button @click="showUserForm = true" class="btn-add">Adicionar Usuário</button>
            </div>
          </div>
          
          <!-- Modal de formulário de usuário -->
          <div v-if="showUserForm" class="modal">
            <div class="modal-content">
              <span @click="showUserForm = false" class="close">&times;</span>
              <h3>{{ editingUser.id ? 'Editar Usuário' : 'Novo Usuário' }}</h3>
              <form @submit.prevent="saveUser">
                <div class="form-group">
                  <label for="name">Nome Completo</label>
                  <input type="text" id="name" v-model="editingUser.name" required>
                </div>
                <div class="form-group">
                  <label for="username">Nome de Usuário</label>
                  <input type="text" id="username" v-model="editingUser.username" required>
                </div>
                <div class="form-group">
                  <label for="email">Email</label>
                  <input type="email" id="email" v-model="editingUser.email" required>
                </div>
                <div class="form-group">
                  <label for="role">Perfil</label>
                  <select id="role" v-model="editingUser.role" required>
                    <option value="admin">Administrador</option>
                    <option value="analyst">Analista</option>
                    <option value="manager">Gerente</option>
                    <option value="committee">Membro de Comitê</option>
                    <option value="formalization">Formalização</option>
                  </select>
                </div>
                <div class="form-group" v-if="!editingUser.id">
                  <label for="password">Senha</label>
                  <input type="password" id="password" v-model="editingUser.password" required>
                </div>
                <div class="form-actions">
                  <button type="button" @click="showUserForm = false" class="btn-cancel">Cancelar</button>
                  <button type="submit" class="btn-save">Salvar</button>
                </div>
              </form>
            </div>
          </div>
        </div>
        
        <!-- Políticas de Crédito -->
        <div v-if="activeTab === 'creditPolicy'" class="credit-policy-tab">
          <div class="settings-card">
            <h2>Configurações de Política de Crédito</h2>
            
            <div class="policy-section">
              <h3>Percentuais Setoriais</h3>
              <div class="form-row">
                <div class="form-group">
                  <label for="commercePercent">Comércio (%)</label>
                  <input type="number" id="commercePercent" v-model="creditPolicy.sectorPercentages.commerce" min="1" max="100">
                </div>
                <div class="form-group">
                  <label for="servicePercent">Serviço (%)</label>
                  <input type="number" id="servicePercent" v-model="creditPolicy.sectorPercentages.service" min="1" max="100">
                </div>
                <div class="form-group">
                  <label for="transportPercent">Transporte (%)</label>
                  <input type="number" id="transportPercent" v-model="creditPolicy.sectorPercentages.transport" min="1" max="100">
                </div>
                <div class="form-group">
                  <label for="industryPercent">Indústria e Posto de Combustível (%)</label>
                  <input type="number" id="industryPercent" v-model="creditPolicy.sectorPercentages.industry" min="1" max="100">
                </div>
              </div>
            </div>
            
            <div class="policy-section">
              <h3>Percentuais de Despesas Financeiras</h3>
              <div class="form-row">
                <div class="form-group">
                  <label for="overdraftPercent">Cheque Especial (%)</label>
                  <input type="number" id="overdraftPercent" v-model="creditPolicy.financialExpenses.overdraft" step="0.01">
                </div>
                <div class="form-group">
                  <label for="advancePercent">Adiantamento ao Depositante (%)</label>
                  <input type="number" id="advancePercent" v-model="creditPolicy.financialExpenses.advance" step="0.01">
                </div>
                <div class="form-group">
                  <label for="guaranteedPercent">Conta Garantida (%)</label>
                  <input type="number" id="guaranteedPercent" v-model="creditPolicy.financialExpenses.guaranteed" step="0.01">
                </div>
                <div class="form-group">
                  <label for="workingCapitalPercent">Capital de Giro com Teto Rotativo (%)</label>
                  <input type="number" id="workingCapitalPercent" v-model="creditPolicy.financialExpenses.workingCapital" step="0.01">
                </div>
                <div class="form-group">
                  <label for="checkDiscountPercent">Desconto de Cheques (%)</label>
                  <input type="number" id="checkDiscountPercent" v-model="creditPolicy.financialExpenses.checkDiscount" step="0.01">
                </div>
                <div class="form-group">
                  <label for="duplicateDiscountPercent">Desconto de Duplicatas (%)</label>
                  <input type="number" id="duplicateDiscountPercent" v-model="creditPolicy.financialExpenses.duplicateDiscount" step="0.01">
                </div>
                <div class="form-group">
                  <label for="creditCardPercent">Desconto Antecipação de Cartão de Crédito (%)</label>
                  <input type="number" id="creditCardPercent" v-model="creditPolicy.financialExpenses.creditCard" step="0.01">
                </div>
                <div class="form-group">
                  <label for="receivablesPercent">Recebíveis Adquiridos (%)</label>
                  <input type="number" id="receivablesPercent" v-model="creditPolicy.financialExpenses.receivables" step="0.01">
                </div>
              </div>
            </div>
            
            <div class="policy-section">
              <h3>Limites de Aprovação</h3>
              <div class="form-row">
                <div class="form-group">
                  <label for="minApprovalRate">Percentual Mínimo para Aprovação (%)</label>
                  <input type="number" id="minApprovalRate" v-model="creditPolicy.approvalLimits.minRate" min="1" max="100">
                  <small>Percentual mínimo de disponibilidade em relação à parcela</small>
                </div>
                <div class="form-group">
                  <label for="maxCommitmentRate">Comprometimento Máximo da Renda (%)</label>
                  <input type="number" id="maxCommitmentRate" v-model="creditPolicy.approvalLimits.maxCommitment" min="1" max="100">
                  <small>Percentual máximo da parcela em relação à disponibilidade</small>
                </div>
              </div>
            </div>
            
            <div class="form-actions">
              <button @click="saveCreditPolicy" class="btn-save">Salvar Configurações</button>
              <button @click="resetCreditPolicy" class="btn-reset">Restaurar Padrões</button>
            </div>
          </div>
        </div>
        
        <!-- Fluxo de Aprovação -->
        <div v-if="activeTab === 'workflow'" class="workflow-tab">
          <div class="settings-card">
            <h2>Configuração do Fluxo de Aprovação</h2>
            
            <div class="workflow-section">
              <h3>Etapas do Fluxo</h3>
              <p class="workflow-description">
                Configure as etapas obrigatórias e opcionais do fluxo de aprovação de crédito.
              </p>
              
              <table class="workflow-table">
                <thead>
                  <tr>
                    <th>Etapa</th>
                    <th>Obrigatória</th>
                    <th>Perfis que podem aprovar</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Cadastro</td>
                    <td><input type="checkbox" v-model="workflow.stages.register.required" disabled checked></td>
                    <td>
                      <div class="checkbox-group">
                        <label><input type="checkbox" v-model="workflow.stages.register.roles" value="analyst"> Analista</label>
                        <label><input type="checkbox" v-model="workflow.stages.register.roles" value="manager"> Gerente</label>
                        <label><input type="checkbox" v-model="workflow.stages.register.roles" value="admin"> Administrador</label>
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td>Conferência</td>
                    <td><input type="checkbox" v-model="workflow.stages.verification.required"></td>
                    <td>
                      <div class="checkbox-group">
                        <label><input type="checkbox" v-model="workflow.stages.verification.roles" value="analyst"> Analista</label>
                        <label><input type="checkbox" v-model="workflow.stages.verification.roles" value="manager"> Gerente</label>
                        <label><input type="checkbox" v-model="workflow.stages.verification.roles" value="admin"> Administrador</label>
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td>Análise de Crédito</td>
                    <td><input type="checkbox" v-model="workflow.stages.analysis.required" disabled checked></td>
                    <td>
                      <div class="checkbox-group">
                        <label><input type="checkbox" v-model="workflow.stages.analysis.roles" value="analyst"> Analista</label>
                        <label><input type="checkbox" v-model="workflow.stages.analysis.roles" value="manager"> Gerente</label>
                        <label><input type="checkbox" v-model="workflow.stages.analysis.roles" value="admin"> Administrador</label>
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td>Comitê de Crédito</td>
                    <td><input type="checkbox" v-model="workflow.stages.committee.required"></td>
                    <td>
                      <div class="checkbox-group">
                        <label><input type="checkbox" v-model="workflow.stages.committee.roles" value="committee"> Membro de Comitê</label>
                        <label><input type="checkbox" v-model="workflow.stages.committee.roles" value="manager"> Gerente</label>
                        <label><input type="checkbox" v-model="workflow.stages.committee.roles" value="admin"> Administrador</label>
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td>Formalização</td>
                    <td><input type="checkbox" v-model="workflow.stages.formalization.required"></td>
                    <td>
                      <div class="checkbox-group">
                        <label><input type="checkbox" v-model="workflow.stages.formalization.roles" value="formalization"> Formalização</label>
                        <label><input type="checkbox" v-model="workflow.stages.formalization.roles" value="manager"> Gerente</label>
                        <label><input type="checkbox" v-model="workflow.stages.formalization.roles" value="admin"> Administrador</label>
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td>Acompanhamento</td>
                    <td><input type="checkbox" v-model="workflow.stages.monitoring.required"></td>
                    <td>
                      <div class="checkbox-group">
                        <label><input type="checkbox" v-model="workflow.stages.monitoring.roles" value="analyst"> Analista</label>
                        <label><input type="checkbox" v-model="workflow.stages.monitoring.roles" value="manager"> Gerente</label>
                        <label><input type="checkbox" v-model="workflow.stages.monitoring.roles" value="admin"> Administrador</label>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <div class="workflow-section">
              <h3>Configurações do Comitê</h3>
              <div class="form-row">
                <div class="form-group">
                  <label for="minCommitteeMembers">Número Mínimo de Membros para Aprovação</label>
                  <input type="number" id="minCommitteeMembers" v-model="workflow.committee.minMembers" min="1" max="10">
                </div>
                <div class="form-group">
                  <label for="approvalType">Tipo de Aprovação</label>
                  <select id="approvalType" v-model="workflow.committee.approvalType">
                    <option value="unanimous">Unânime</option>
                    <option value="majority">Maioria Simples</option>
                    <option value="weighted">Ponderada por Cargo</option>
                  </select>
                </div>
              </div>
            </div>
            
            <div class="form-actions">
              <button @click="saveWorkflow" class="btn-save">Salvar Configurações</button>
              <button @click="resetWorkflow" class="btn-reset">Restaurar Padrões</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, onMounted } from 'vue';
  
  export default {
    name: 'Settings',
    setup() {
      const activeTab = ref('users');
      const users = ref([]);
      const showUserForm = ref(false);
      const editingUser = reactive({
        id: null,
        name: '',
        username: '',
        email: '',
        role: 'analyst',
        password: '',
        is_active: true
      });
      
      const creditPolicy = reactive({
        sectorPercentages: {
          commerce: 75,
          service: 70,
          transport: 85,
          industry: 90
        },
        financialExpenses: {
          overdraft: 7,
          advance: 15,
          guaranteed: 3.90,
          workingCapital: 2.70,
          checkDiscount: 2.67,
          duplicateDiscount: 2.08,
          creditCard: 1.21,
          receivables: 2.08
        },
        approvalLimits: {
          minRate: 110,
          maxCommitment: 30
        }
      });
      
      const workflow = reactive({
        stages: {
          register: {
            required: true,
            roles: ['analyst', 'manager', 'admin']
          },
          verification: {
            required: true,
            roles: ['analyst', 'manager', 'admin']
          },
          analysis: {
            required: true,
            roles: ['analyst', 'manager', 'admin']
          },
          committee: {
            required: true,
            roles: ['committee', 'manager', 'admin']
          },
          formalization: {
            required: true,
            roles: ['formalization', 'manager', 'admin']
          },
          monitoring: {
            required: true,
            roles: ['analyst', 'manager', 'admin']
          }
        },
        committee: {
          minMembers: 1,
          approvalType: 'unanimous'
        }
      });
      
      const fetchUsers = () => {
        // No MVP, vamos usar dados simulados
        users.value = [
          {
            id: 1,
            name: 'Administrador',
            username: 'admin',
            email: 'admin@w2mfinance.com',
            role: 'admin',
            is_active: true
          },
          {
            id: 2,
            name: 'Ana Ferreira',
            username: 'analista',
            email: 'ana.ferreira@w2mfinance.com',
            role: 'analyst',
            is_active: true
          },
          {
            id: 3,
            name: 'Carlos Gomes',
            username: 'gerente',
            email: 'carlos.gomes@w2mfinance.com',
            role: 'manager',
            is_active: true
          }
        ];
      };
      
      const editUser = (user) => {
        // Copia os dados do usuário para o formulário
        Object.assign(editingUser, user);
        editingUser.password = ''; // Limpa a senha por segurança
        showUserForm.value = true;
      };
      
      const toggleUserStatus = (user) => {
        // Toggle o status do usuário
        const newStatus = !user.is_active;
        // Em uma aplicação real, chamaríamos a API
        user.is_active = newStatus;
      };
      
      const saveUser = () => {
        // Em uma aplicação real, chamaríamos a API
        if (editingUser.id) {
          // Atualizar usuário existente
          const index = users.value.findIndex(u => u.id === editingUser.id);
          if (index !== -1) {
            users.value[index] = { ...editingUser };
          }
        } else {
          // Adicionar novo usuário
          const newId = Math.max(...users.value.map(u => u.id)) + 1;
          users.value.push({
            ...editingUser,
            id: newId
          });
        }
        
        // Limpar formulário e fechar modal
        resetUserForm();
        showUserForm.value = false;
      };
      
      const resetUserForm = () => {
        Object.assign(editingUser, {
          id: null,
          name: '',
          username: '',
          email: '',
          role: 'analyst',
          password: '',
          is_active: true
        });
      };
      
      const getRoleLabel = (role) => {
        const labels = {
          'admin': 'Administrador',
          'analyst': 'Analista',
          'manager': 'Gerente',
          'committee': 'Membro de Comitê',
          'formalization': 'Formalização'
        };
        return labels[role] || role;
      };
      
      const saveCreditPolicy = () => {
        // Em uma aplicação real, chamaríamos a API
        alert('Configurações de política de crédito salvas com sucesso!');
      };
      
      const resetCreditPolicy = () => {
        // Restaurar valores padrão
        Object.assign(creditPolicy.sectorPercentages, {
          commerce: 75,
          service: 70,
          transport: 85,
          industry: 90
        });
        
        Object.assign(creditPolicy.financialExpenses, {
          overdraft: 7,
          advance: 15,
          guaranteed: 3.90,
          workingCapital: 2.70,
          checkDiscount: 2.67,
          duplicateDiscount: 2.08,
          creditCard: 1.21,
          receivables: 2.08
        });
        
        Object.assign(creditPolicy.approvalLimits, {
          minRate: 110,
          maxCommitment: 30
        });
      };
      
      const saveWorkflow = () => {
        // Em uma aplicação real, chamaríamos a API
        alert('Configurações de fluxo de aprovação salvas com sucesso!');
      };
      
      const resetWorkflow = () => {
        // Restaurar valores padrão
        Object.assign(workflow.stages, {
          register: {
            required: true,
            roles: ['analyst', 'manager', 'admin']
          },
          verification: {
            required: true,
            roles: ['analyst', 'manager', 'admin']
          },
          analysis: {
            required: true,
            roles: ['analyst', 'manager', 'admin']
          },
          committee: {
            required: true,
            roles: ['committee', 'manager', 'admin']
          },
          formalization: {
            required: true,
            roles: ['formalization', 'manager', 'admin']
          },
          monitoring: {
            required: true,
            roles: ['analyst', 'manager', 'admin']
          }
        });
        
        Object.assign(workflow.committee, {
          minMembers: 1,
          approvalType: 'unanimous'
        });
      };
      
      onMounted(() => {
        fetchUsers();
      });
      
      return {
        activeTab,
        users,
        showUserForm,
        editingUser,
        creditPolicy,
        workflow,
        editUser,
        toggleUserStatus,
        saveUser,
        resetUserForm,
        getRoleLabel,
        saveCreditPolicy,
        resetCreditPolicy,
        saveWorkflow,
        resetWorkflow
      };
    }
  }
  </script>
  
  <style scoped>
  .settings-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .page-header {
    margin-bottom: 20px;
  }
  
  .tabs {
    display: flex;
    margin-bottom: 20px;
    border-bottom: 1px solid #ddd;
  }
  
  .tab-button {
    padding: 10px 20px;
    background: none;
    border: none;
    cursor: pointer;
    font-size: 16px;
    font-weight: 500;
    color: #666;
    border-bottom: 3px solid transparent;
    transition: all 0.3s ease;
  }
  
  .tab-button.active {
    color: var(--primary-color);
    border-bottom-color: var(--primary-color);
  }

    .tab-button:hover {
    color: var(--primary-color);
  }

    .settings-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-bottom: 20px;
    }

    .settings-card h2 {
    margin-top: 0;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
    font-size: 18px;
    }

    /* Tabela de usuários */
    .users-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    }

    .users-table th, 
    .users-table td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #eee;
    }

    .users-table th {
    background-color: #f5f5f5;
    font-weight: 500;
    }

    .status-active {
    display: inline-block;
    padding: 4px 8px;
    background-color: #E8F5E9;
    color: #388E3C;
    border-radius: 4px;
    font-size: 12px;
    }

    .status-inactive {
    display: inline-block;
    padding: 4px 8px;
    background-color: #FFEBEE;
    color: #D32F2F;
    border-radius: 4px;
    font-size: 12px;
    }

    .actions {
    display: flex;
    gap: 8px;
    }

    .btn-edit, .btn-activate, .btn-deactivate {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    border: none;
    cursor: pointer;
    }

    .btn-edit {
    background-color: #E3F2FD;
    color: #1976D2;
    }

    .btn-activate {
    background-color: #E8F5E9;
    color: #388E3C;
    }

    .btn-deactivate {
    background-color: #FFEBEE;
    color: #D32F2F;
    }

    .add-button-container {
    display: flex;
    justify-content: flex-end;
    }

    .btn-add {
    background-color: var(--primary-color);
    color: white;
    padding: 8px 16px;
    border-radius: 4px;
    border: none;
    font-weight: 500;
    cursor: pointer;
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
    width: 500px;
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
    .form-group {
    margin-bottom: 15px;
    }

    .form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
    }

    .form-group input,
    .form-group select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
    }

    .form-row {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin-bottom: 20px;
    }

    .form-actions {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
    }

    .btn-save, .btn-cancel, .btn-reset {
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: 500;
    cursor: pointer;
    border: none;
    }

    .btn-save {
    background-color: var(--primary-color);
    color: white;
    }

    .btn-cancel {
    background-color: #f5f5f5;
    color: #333;
    }

    .btn-reset {
    background-color: #f5f5f5;
    color: #D32F2F;
    border: 1px solid #FFCDD2;
    }

    /* Políticas de crédito */
    .policy-section {
    margin-bottom: 30px;
    }

    .policy-section h3 {
    font-size: 16px;
    color: #444;
    margin-bottom: 15px;
    }

    small {
    display: block;
    color: #666;
    font-size: 12px;
    margin-top: 4px;
    }

    /* Workflow */
    .workflow-description {
    margin-bottom: 20px;
    color: #666;
    }

    .workflow-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
    }

    .workflow-table th,
    .workflow-table td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #eee;
    }

    .workflow-table th {
    background-color: #f5f5f5;
    font-weight: 500;
    }

    .checkbox-group {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    }

    .checkbox-group label {
    margin-right: 15px;
    display: flex;
    align-items: center;
    font-weight: normal;
    }

    .checkbox-group label input {
    margin-right: 5px;
    }

    .workflow-section {
    margin-bottom: 30px;
    }

    .workflow-section h3 {
    font-size: 16px;
    color: #444;
    margin-bottom: 15px;
    }
    </style>