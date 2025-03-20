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
    
    const saveCreditPolicy = async () => {
      try {
        // Em uma aplicação real, salvaria no backend
        // await api.settings.saveCreditPolicy(creditPolicy);
        
        // Para o MVP, simular sucesso
        alert('Configurações de política de crédito salvas com sucesso!');
      } catch (error) {
        console.error('Erro ao salvar configurações:', error);
        alert('Erro ao salvar configurações');
      }
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
    
    const saveWorkflow = async () => {
      try {
        // Em uma aplicação real, salvaria no backend
        // await api.settings.saveWorkflow(workflow);
        
        // Para o MVP, simular sucesso
        alert('Configurações de fluxo de aprovação salvas com sucesso!');
      } catch (error) {
        console.error('Erro ao salvar configurações:', error);
        alert('Erro ao salvar configurações');
      }
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

.tabs {
  display: flex;
  margin-bottom: 30px;
  border-bottom: 1px solid #ddd;
  overflow-x: auto;
  padding-bottom: 1px;
}

.tab-button {
  padding: 12px 24px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  color: #666;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.tab-button.active {
  color: #4673F5;
  border-bottom-color: #4673F5;
  font-weight: 600;
}

.tab-button:hover {
  color: #4673F5;
}

.tab-content {
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}

.settings-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  padding: 30px;
  margin-bottom: 25px;
}

.settings-card h2 {
  margin-top: 0;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eaedf2;
  font-size: 20px;
  color: #00004b;
  font-weight: 600;
}

/* Tabela de usuários */
.users-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 25px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.users-table th, 
.users-table td {
  padding: 14px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.users-table th {
  background-color: #f5f7fa;
  color: #00004b;
  font-weight: 600;
}

.users-table tr:hover td {
  background-color: #f9fafc;
}

.status-active {
  display: inline-flex;
  padding: 5px 10px;
  background-color: #E8F5E9;
  color: #388E3C;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  align-items: center;
}

.status-active::before {
  content: '●';
  margin-right: 5px;
  font-size: 10px;
}

.status-inactive {
  display: inline-flex;
  padding: 5px 10px;
  background-color: #FFEBEE;
  color: #D32F2F;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  align-items: center;
}

.status-inactive::before {
  content: '●';
  margin-right: 5px;
  font-size: 10px;
}

.actions {
  display: flex;
  gap: 10px;
}

.btn-edit, .btn-activate, .btn-deactivate {
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 13px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.btn-edit {
  background-color: #E3F2FD;
  color: #1976D2;
}

.btn-edit:hover {
  background-color: #BBDEFB;
  color: #0D47A1;
  transform: translateY(-2px);
}

.btn-activate {
  background-color: #E8F5E9;
  color: #388E3C;
}

.btn-activate:hover {
  background-color: #C8E6C9;
  color: #2E7D32;
  transform: translateY(-2px);
}

.btn-deactivate {
  background-color: #FFEBEE;
  color: #D32F2F;
}

.btn-deactivate:hover {
  background-color: #FFCDD2;
  color: #B71C1C;
  transform: translateY(-2px);
}

.add-button-container {
  display: flex;
  justify-content: flex-end;
}

.btn-add {
  background: linear-gradient(90deg, #4673F5, #2556e0);
  color: white;
  padding: 10px 20px;
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

.btn-add:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(70, 115, 245, 0.3);
}

.btn-add::before {
  content: '+';
  font-size: 18px;
  font-weight: 700;
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
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  width: 500px;
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

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 25px;
  font-size: 20px;
  color: #00004b;
  font-weight: 600;
}

/* Formulários */
.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #444;
  font-size: 14px;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.3s ease;
  background-color: #f9f9fc;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #4673F5;
  box-shadow: 0 0 0 3px rgba(70, 115, 245, 0.15);
  background-color: #ffffff;
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 25px;
}

.btn-save, .btn-cancel, .btn-reset {
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-save {
  background: linear-gradient(90deg, #4673F5, #2556e0);
  color: white;
  border: none;
  box-shadow: 0 4px 10px rgba(70, 115, 245, 0.2);
}

.btn-save:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(70, 115, 245, 0.3);
}

.btn-cancel {
  background-color: #f5f5f7;
  color: #444;
  border: 1px solid #ddd;
}

.btn-cancel:hover {
  background-color: #e5e5e7;
  transform: translateY(-3px);
}

.btn-reset {
  background-color: #f5f5f7;
  color: #D32F2F;
  border: 1px solid #FFCDD2;
}

.btn-reset:hover {
  background-color: #FFEBEE;
  transform: translateY(-3px);
}

/* Políticas de crédito */
.policy-section {
  margin-bottom: 35px;
}

.policy-section h3 {
  font-size: 18px;
  color: #00004b;
  margin-bottom: 20px;
  font-weight: 600;
}

small {
  display: block;
  color: #666;
  font-size: 12px;
  margin-top: 5px;
}

/* Workflow */
.workflow-description {
  margin-bottom: 25px;
  color: #666;
  line-height: 1.6;
}

.workflow-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 25px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.workflow-table th,
.workflow-table td {
  padding: 14px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.workflow-table th {
  background-color: #f5f7fa;
  color: #00004b;
  font-weight: 600;
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
  cursor: pointer;
  background-color: #f5f7fa;
  padding: 6px 10px;
  border-radius: 6px;
  transition: all 0.3s ease;
}

.checkbox-group label:hover {
  background-color: #e3f2fd;
}

.checkbox-group label input {
  margin-right: 8px;
  width: auto;
}

.workflow-section {
  margin-bottom: 35px;
}

.workflow-section h3 {
  font-size: 18px;
  color: #00004b;
  margin-bottom: 20px;
  font-weight: 600;
}

/* Ajustes adicionais para o componente de workflow */
.workflow-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 25px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

.workflow-table th, 
.workflow-table td {
  padding: 14px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.workflow-table th {
  background-color: #f5f7fa;
  color: #00004b;
  font-weight: 600;
}

/* Ajustes para responsividade */
@media (max-width: 768px) {
  .form-section {
    padding: 20px;
  }
  
  .form-row {
    flex-direction: column;
  }
  
  .form-group {
    flex: none;
    width: 100%;
  }
  
  .checkbox-group {
    flex-direction: column;
    gap: 10px;
  }
  
  .workflow-table {
    display: block;
    overflow-x: auto;
  }
}
</style>