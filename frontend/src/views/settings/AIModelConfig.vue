<template>
    <div class="ai-model-config">
      <div class="page-header">
        <h1>Configuração do Modelo de IA</h1>
        <div class="header-actions">
          <button @click="saveConfig" class="btn-primary">Salvar Configurações</button>
          <button @click="testModel" class="btn-secondary">Testar Modelo</button>
        </div>
      </div>
      
      <div class="content-grid">
        <!-- Configurações Gerais -->
        <div class="config-card">
          <h2>Configurações Gerais</h2>
          
          <div class="form-group">
            <label for="model_type">Tipo de Modelo</label>
            <select v-model="config.model_type" id="model_type">
              <option value="random_forest">Random Forest</option>
              <option value="gradient_boosting">Gradient Boosting</option>
              <option value="logistic_regression">Regressão Logística</option>
              <option value="neural_network">Rede Neural</option>
              <option value="ensemble">Ensemble (combinação de modelos)</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="threshold">Limite de Aprovação</label>
            <div class="range-input">
              <input 
                type="range" 
                v-model="config.threshold" 
                min="0" 
                max="100" 
                step="1" 
                id="threshold"
              />
              <span class="range-value">{{ config.threshold }}%</span>
            </div>
            <small>Solicitações com score de risco abaixo deste valor serão recomendadas para aprovação</small>
          </div>
          
          <div class="form-group">
            <label for="auto_approve">Aprovação Automática</label>
            <div class="toggle-switch">
              <input 
                type="checkbox" 
                v-model="config.auto_approve" 
                id="auto_approve"
              />
              <span class="toggle-slider"></span>
            </div>
            <small>Se ativado, solicitações com score muito baixo serão aprovadas automaticamente</small>
          </div>
          
          <div v-if="config.auto_approve" class="form-group">
            <label for="auto_approve_threshold">Limite para Aprovação Automática</label>
            <div class="range-input">
              <input 
                type="range" 
                v-model="config.auto_approve_threshold" 
                min="0" 
                max="30" 
                step="1" 
                id="auto_approve_threshold"
              />
              <span class="range-value">{{ config.auto_approve_threshold }}%</span>
            </div>
            <small>Solicitações com score de risco abaixo deste valor serão aprovadas sem análise manual</small>
          </div>
          
          <div class="form-group">
            <label for="auto_reject">Rejeição Automática</label>
            <div class="toggle-switch">
              <input 
                type="checkbox" 
                v-model="config.auto_reject" 
                id="auto_reject"
              />
              <span class="toggle-slider"></span>
            </div>
            <small>Se ativado, solicitações com score muito alto serão rejeitadas automaticamente</small>
          </div>
          
          <div v-if="config.auto_reject" class="form-group">
            <label for="auto_reject_threshold">Limite para Rejeição Automática</label>
            <div class="range-input">
              <input 
                type="range" 
                v-model="config.auto_reject_threshold" 
                min="70" 
                max="100" 
                step="1" 
                id="auto_reject_threshold"
              />
              <span class="range-value">{{ config.auto_reject_threshold }}%</span>
            </div>
            <small>Solicitações com score de risco acima deste valor serão rejeitadas sem análise manual</small>
          </div>
        </div>
        
        <!-- Fatores do Modelo -->
        <div class="config-card">
          <h2>Fatores de Ponderação do Modelo</h2>
          <p class="card-desc">Ajuste a importância de cada fator na análise de risco de crédito.</p>
          
          <div class="factor-list">
            <div v-for="(factor, index) in config.factors" :key="index" class="factor-item">
              <div class="factor-header">
                <h3>{{ factor.name }}</h3>
                <div class="factor-weight">
                  <span class="weight-value">{{ factor.weight }}%</span>
                  <button 
                    type="button" 
                    @click="decrementWeight(index)" 
                    class="weight-button"
                    :disabled="factor.weight <= 5"
                  >-</button>
                  <button 
                    type="button" 
                    @click="incrementWeight(index)" 
                    class="weight-button"
                    :disabled="factor.weight >= 40 || getTotalWeight() >= 100"
                  >+</button>
                </div>
              </div>
              <div class="factor-bar">
                <div 
                  class="factor-bar-fill" 
                  :style="{ width: factor.weight + '%', backgroundColor: factor.color }"
                ></div>
              </div>
              <p class="factor-desc">{{ factor.description }}</p>
            </div>
            
            <div class="total-weight">
              <span>Peso Total:</span>
              <span :class="{ 'error': getTotalWeight() !== 100 }">
                {{ getTotalWeight() }}% 
                <span v-if="getTotalWeight() !== 100" class="weight-warning">
                  (Deve somar 100%)
                </span>
              </span>
            </div>
          </div>
        </div>
        
        <!-- Configurações do Claude IA -->
        <div class="config-card">
          <h2>Configuração do Claude</h2>
          <div class="ai-logo">
            <img src="https://cdn.worldvectorlogo.com/logos/anthropic-1.svg" alt="Claude AI Logo" class="ai-logo-img" />
          </div>
          
          <p class="card-desc">Ajuste as configurações de integração com a IA Claude da Anthropic para análises avançadas.</p>
          
          <div class="form-group">
            <label for="claude_enabled">Habilitar Claude</label>
            <div class="toggle-switch">
              <input 
                type="checkbox" 
                v-model="config.claude_enabled" 
                id="claude_enabled"
              />
              <span class="toggle-slider"></span>
            </div>
            <small>Usar Claude para análises adicionais baseadas em texto e para explicações detalhadas</small>
          </div>
          
          <div v-if="config.claude_enabled">
            <div class="form-group">
              <label for="claude_model">Modelo do Claude</label>
              <select v-model="config.claude_model" id="claude_model">
                <option value="claude-3-opus-20240229">Claude 3 Opus (Mais preciso)</option>
                <option value="claude-3-sonnet-20240229">Claude 3 Sonnet (Balanceado)</option>
                <option value="claude-3-haiku-20240307">Claude 3 Haiku (Mais rápido)</option>
                <option value="claude-3-5-sonnet-20240520">Claude 3.5 Sonnet (Recomendado)</option>
                <option value="claude-3-7-sonnet-20241025">Claude 3.7 Sonnet (Mais recente)</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="claude_temperature">Temperatura</label>
              <div class="range-input">
                <input 
                  type="range" 
                  v-model="config.claude_temperature" 
                  min="0" 
                  max="1" 
                  step="0.1" 
                  id="claude_temperature"
                />
                <span class="range-value">{{ config.claude_temperature }}</span>
              </div>
              <small>Valores mais baixos produzem resultados mais determinísticos, valores mais altos aumentam a criatividade</small>
            </div>
            
            <div class="form-group">
              <label for="claude_prompt">Prompt do Claude</label>
              <textarea 
                v-model="config.claude_prompt" 
                id="claude_prompt" 
                rows="12"
                placeholder="Insira o prompt base para o Claude..."
              ></textarea>
              <small>Prompt que o Claude utilizará como base para a análise. Use {client} para dados do cliente e {application} para dados da solicitação.</small>
            </div>
            
            <button @click="resetPrompt" class="btn-text">Restaurar prompt padrão</button>
          </div>
        </div>
        
        <!-- Histórico de Treinamento -->
        <div class="config-card">
          <h2>Histórico de Treinamento do Modelo</h2>
          
          <div class="stats-row">
            <div class="stat-box">
              <div class="stat-label">Precisão do Modelo</div>
              <div class="stat-value">{{ modelStats.accuracy }}%</div>
            </div>
            <div class="stat-box">
              <div class="stat-label">Última Atualização</div>
              <div class="stat-value">{{ modelStats.last_updated }}</div>
            </div>
            <div class="stat-box">
              <div class="stat-label">Total de Amostras</div>
              <div class="stat-value">{{ modelStats.sample_count }}</div>
            </div>
          </div>
          
          <div class="history-list">
            <table>
              <thead>
                <tr>
                  <th>Data</th>
                  <th>Versão</th>
                  <th>Precisão</th>
                  <th>Amostras</th>
                  <th>Alterações</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in trainingHistory" :key="index">
                  <td>{{ item.date }}</td>
                  <td>v{{ item.version }}</td>
                  <td>{{ item.accuracy }}%</td>
                  <td>{{ item.samples }}</td>
                  <td>{{ item.changes }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div class="action-buttons">
            <button @click="trainModel" class="btn-secondary">Treinar Modelo</button>
            <button @click="downloadHistory" class="btn-outline">Exportar Histórico</button>
          </div>
        </div>
      </div>
      
      <!-- Modal de teste de modelo -->
      <div v-if="showTestModal" class="modal-overlay">
        <div class="modal-content">
          <div class="modal-header">
            <h2>Teste do Modelo de IA</h2>
            <button @click="showTestModal = false" class="btn-close">&times;</button>
          </div>
          
          <div class="modal-body">
            <h3>Dados para teste</h3>
            
            <div class="form-group">
              <label for="test_client_type">Tipo de Cliente</label>
              <select v-model="testData.client_type" id="test_client_type">
                <option value="individual">Pessoa Física</option>
                <option value="business">Pessoa Jurídica</option>
              </select>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="test_income">Renda Mensal</label>
                <input type="number" v-model="testData.income" id="test_income" min="0" step="100">
              </div>
              
              <div class="form-group">
                <label for="test_age">Idade</label>
                <input type="number" v-model="testData.age" id="test_age" min="18" max="100">
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="test_credit_score">Score de Crédito</label>
                <input type="number" v-model="testData.credit_score" id="test_credit_score" min="0" max="1000">
              </div>
              
              <div class="form-group">
                <label for="test_debt_ratio">Relação Dívida/Renda</label>
                <input 
                  type="number" 
                  v-model="testData.debt_ratio" 
                  id="test_debt_ratio" 
                  min="0" 
                  max="100"
                  step="0.1"
                >
                <small>Percentual de comprometimento da renda com dívidas</small>
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="test_amount">Valor do Empréstimo</label>
                <input type="number" v-model="testData.amount" id="test_amount" min="0" step="100">
              </div>
              
              <div class="form-group">
                <label for="test_term">Prazo (meses)</label>
                <input type="number" v-model="testData.term" id="test_term" min="1" max="120">
              </div>
            </div>
            
            <button @click="runModelTest" class="btn-primary btn-full">Executar Teste</button>
            
            <div v-if="testResult" class="test-result">
              <h3>Resultado da Análise</h3>
              
              <div class="risk-score">
                <div class="risk-meter">
                  <div 
                    class="risk-bar" 
                    :style="{ width: testResult.risk_score + '%', backgroundColor: getRiskColor(testResult.risk_score) }"
                  ></div>
                </div>
                <div class="risk-value">
                  Score de Risco: {{ testResult.risk_score }}%
                </div>
              </div>
              
              <div class="recommendation" :class="getRecommendationClass(testResult.recommendation)">
                <h4>Recomendação</h4>
                <p>{{ testResult.recommendation }}</p>
              </div>
              
              <div class="explanation">
                <h4>Explicação</h4>
                <pre>{{ testResult.explanation }}</pre>
              </div>
              
              <div class="factor-breakdown">
                <h4>Contribuição dos Fatores</h4>
                <div v-for="(factor, index) in testResult.factors" :key="index" class="factor-item">
                  <div class="factor-header">
                    <span>{{ factor.name }}</span>
                    <span :class="{'positive': factor.impact < 0, 'negative': factor.impact > 0, 'neutral': factor.impact === 0 }">
                      {{ factor.impact > 0 ? '+' : '' }}{{ factor.impact }}%
                    </span>
                  </div>
                  <div class="factor-impact-bar">
                    <div 
                      class="impact-bar-fill" 
                      :class="{'positive': factor.impact < 0, 'negative': factor.impact > 0, 'neutral': factor.impact === 0 }"
                      :style="{ width: Math.abs(factor.impact) + '%' }"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive, computed } from 'vue';
  
  export default {
    name: 'AIModelConfig',
    setup() {
      // Configurações do modelo
      const config = reactive({
        model_type: 'gradient_boosting',
        threshold: 60,
        auto_approve: true,
        auto_approve_threshold: 20,
        auto_reject: true,
        auto_reject_threshold: 85,
        factors: [
          {
            name: 'Histórico de Crédito',
            weight: 25,
            color: '#4CAF50',
            description: 'Pontuação baseada no histórico de crédito do cliente e pagamentos anteriores.'
          },
          {
            name: 'Capacidade de Pagamento',
            weight: 30,
            color: '#2196F3',
            description: 'Análise da relação entre renda e dívidas existentes.'
          },
          {
            name: 'Valor do Empréstimo',
            weight: 15,
            color: '#FFC107',
            description: 'Análise do valor solicitado em relação à capacidade financeira.'
          },
          {
            name: 'Tempo de Relacionamento',
            weight: 10,
            color: '#9C27B0',
            description: 'Histórico de relacionamento com a instituição.'
          },
          {
            name: 'Perfil Socioeconômico',
            weight: 10,
            color: '#FF5722',
            description: 'Análise de fatores socioeconômicos como emprego e residência.'
          },
          {
            name: 'Garantias Oferecidas',
            weight: 10,
            color: '#607D8B',
            description: 'Avaliação das garantias oferecidas para o empréstimo.'
          }
        ],
        claude_enabled: true,
        claude_model: 'claude-3-5-sonnet-20240520',
        claude_temperature: 0.3,
        claude_prompt: `Você é um assistente especializado em análise de crédito para um sistema financeiro. Por favor, analise cuidadosamente os seguintes dados de cliente e solicitação de crédito:
  
  DADOS DO CLIENTE:
  {client}
  
  DADOS DA SOLICITAÇÃO:
  {application}
  
  Forneça uma análise detalhada dos seguintes aspectos:
  1. Capacidade de pagamento com base na renda e despesas
  2. Histórico de crédito e comportamento financeiro
  3. Compatibilidade do valor solicitado com o perfil do cliente
  4. Qualquer fator de risco identificado
  5. Recomendação final (APROVADO, APROVADO COM CONDIÇÕES, ou REPROVADO)
  
  Para cada fator, identifique pontos POSITIVOS, NEGATIVOS e NEUTROS.
  
  Por fim, forneça uma explicação clara e concisa sobre sua recomendação final e uma pontuação de risco de 0-100 (onde 0 é risco mínimo e 100 é risco máximo).`
      });
      
      // Estatísticas do modelo
      const modelStats = reactive({
        accuracy: 87.5,
        last_updated: '15/02/2025',
        sample_count: 3542
      });
      
      // Histórico de treinamento
      const trainingHistory = ref([
        {
          date: '15/02/2025',
          version: '2.3',
          accuracy: 87.5,
          samples: 3542,
          changes: 'Melhoria na detecção de fraudes'
        },
        {
          date: '10/01/2025',
          version: '2.2',
          accuracy: 85.8,
          samples: 3250,
          changes: 'Calibração para empréstimos de alto valor'
        },
        {
          date: '05/12/2024',
          version: '2.1',
          accuracy: 84.2,
          samples: 3100,
          changes: 'Ajuste para perfis de baixa renda'
        },
        {
          date: '15/11/2024',
          version: '2.0',
          accuracy: 82.7,
          samples: 2840,
          changes: 'Nova versão com mais fatores de análise'
        }
      ]);
      
      // Modal de teste
      const showTestModal = ref(false);
      
      // Dados para teste do modelo
      const testData = reactive({
        client_type: 'individual',
        income: 5000,
        age: 35,
        credit_score: 750,
        debt_ratio: 25,
        amount: 10000,
        term: 36
      });
      
      // Resultado do teste
      const testResult = ref(null);
      
      // Calcular peso total dos fatores
      const getTotalWeight = () => {
        return config.factors.reduce((sum, factor) => sum + factor.weight, 0);
      };
      
      // Incrementar peso de um fator
      const incrementWeight = (index) => {
        if (config.factors[index].weight < 40 && getTotalWeight() < 100) {
          config.factors[index].weight += 5;
        }
      };
      
      // Decrementar peso de um fator
      const decrementWeight = (index) => {
        if (config.factors[index].weight > 5) {
          config.factors[index].weight -= 5;
        }
      };
      
      // Restaurar prompt padrão do Claude
      const resetPrompt = () => {
        config.claude_prompt = `Você é um assistente especializado em análise de crédito para um sistema financeiro. Por favor, analise cuidadosamente os seguintes dados de cliente e solicitação de crédito:
  
  DADOS DO CLIENTE:
  {client}
  
  DADOS DA SOLICITAÇÃO:
  {application}
  
  Forneça uma análise detalhada dos seguintes aspectos:
  1. Capacidade de pagamento com base na renda e despesas
  2. Histórico de crédito e comportamento financeiro
  3. Compatibilidade do valor solicitado com o perfil do cliente
  4. Qualquer fator de risco identificado
  5. Recomendação final (APROVADO, APROVADO COM CONDIÇÕES, ou REPROVADO)
  
  Para cada fator, identifique pontos POSITIVOS, NEGATIVOS e NEUTROS.
  
  Por fim, forneça uma explicação clara e concisa sobre sua recomendação final e uma pontuação de risco de 0-100 (onde 0 é risco mínimo e 100 é risco máximo).`;
      };
      
      // Abrir modal de teste
      const testModel = () => {
        showTestModal.value = true;
      };
      
      // Executar teste do modelo
      const runModelTest = () => {
        // Simulação de resultado de análise da IA
        // Em uma aplicação real, isso seria uma chamada à API
        
        // Calculando score com base nos dados fornecidos
        let baseScore = 50;
        
        // Ajuste pelo score de crédito (melhor score diminui o risco)
        baseScore -= (testData.credit_score / 1000) * 30;
        
        // Ajuste pela relação dívida/renda (maior relação aumenta o risco)
        baseScore += (testData.debt_ratio / 100) * 25;
        
        // Ajuste pela idade (idade muito baixa ou muito alta aumenta o risco)
        const ageRisk = Math.abs(testData.age - 40) / 25 * 10;
        baseScore += ageRisk;
        
        // Ajuste pelo valor do empréstimo em relação à renda
        const loanToIncomeRatio = testData.amount / (testData.income * 12);
        baseScore += loanToIncomeRatio * 20;
        
        // Garantir que o score está entre 0 e 100
        const riskScore = Math.min(Math.max(Math.round(baseScore), 0), 100);
        
        // Determinar recomendação
        let recommendation;
        if (riskScore < config.auto_approve_threshold) {
          recommendation = "APROVADO: Excelente perfil de crédito";
        } else if (riskScore < config.threshold) {
          recommendation = "APROVADO COM CONDIÇÕES: Considerar ajuste na taxa de juros";
        } else if (riskScore >= config.auto_reject_threshold) {
          recommendation = "REPROVADO: Alto risco de inadimplência";
        } else {
          recommendation = "REPROVADO: Capacidade de pagamento insuficiente";
        }
        
        // Gerar explicação de fatores
        const factors = [
          {
            name: 'Histórico de Crédito',
            impact: Math.round((750 - testData.credit_score) / 10),
            details: testData.credit_score > 700 ? 'Bom histórico de crédito' : 'Histórico de crédito limitado'
          },
          {
            name: 'Capacidade de Pagamento',
            impact: Math.round(testData.debt_ratio / 5 - 3),
            details: `Comprometimento de ${testData.debt_ratio}% da renda`
          },
          {
            name: 'Valor do Empréstimo',
            impact: Math.round(loanToIncomeRatio * 15),
            details: `Empréstimo equivale a ${(loanToIncomeRatio * 12).toFixed(1)} meses de renda`
          },
          {
            name: 'Perfil do Cliente',
            impact: Math.round(ageRisk / 2),
            details: `Cliente de ${testData.age} anos de idade`
          }
        ];
        
        // Gerar explicação
        const explanation = `Análise de Crédito - Score de Risco: ${riskScore}/100
  
  Fatores principais analisados:
  - Histórico de crédito: Score de ${testData.credit_score}/1000
  - Capacidade de pagamento: ${testData.debt_ratio}% da renda já comprometida
  - Valor solicitado: R$ ${testData.amount.toLocaleString('pt-BR')} para ${testData.term} meses
  - Renda mensal: R$ ${testData.income.toLocaleString('pt-BR')}
  
  POSITIVO: ${testData.credit_score > 700 ? 'Bom histórico de crédito' : 'Valor do empréstimo compatível com o prazo'}
  ${testData.debt_ratio < 30 ? 'POSITIVO: Baixo comprometimento de renda' : 'NEGATIVO: Alto comprometimento de renda'}
  ${loanToIncomeRatio < 0.5 ? 'POSITIVO: Valor solicitado adequado à renda' : 'NEGATIVO: Valor solicitado elevado em relação à renda'}
  
  Recomendação: ${recommendation}`;
        
        // Retornar resultado do teste
        testResult.value = {
          risk_score: riskScore,
          recommendation,
          explanation,
          factors
        };
      };
      
      // Salvar configurações
      const saveConfig = () => {
        // Em uma aplicação real, aqui enviaríamos as configurações para a API
        // Para o MVP, apenas simulamos uma confirmação
        alert('Configurações salvas com sucesso!');
      };
      
      // Treinar modelo
      const trainModel = () => {
        // Em uma aplicação real, aqui dispararíamos o processo de treinamento na API
        // Para o MVP, apenas simulamos uma confirmação
        alert('O treinamento do modelo foi iniciado. Esse processo pode levar alguns minutos.');
      };
      
      // Exportar histórico
      const downloadHistory = () => {
        // Em uma aplicação real, aqui geramos um arquivo para download
        // Para o MVP, apenas simulamos uma confirmação
        alert('Histórico exportado com sucesso!');
      };
      
      // Obter cor baseada no score de risco
      const getRiskColor = (score) => {
        if (score < 20) return '#4CAF50';
        if (score < 40) return '#8BC34A';
        if (score < 60) return '#FFC107';
        if (score < 80) return '#FF9800';
        return '#F44336';
      };
      
      // Obter classe CSS para a recomendação
      const getRecommendationClass = (recommendation) => {
        if (recommendation.includes('APROVADO') && !recommendation.includes('REPROVADO')) {
          return recommendation.includes('CONDIÇÕES') ? 'warning' : 'success';
        }
        return 'danger';
      };
      
      return {
        config,
        modelStats,
        trainingHistory,
        showTestModal,
        testData,
        testResult,
        getTotalWeight,
        incrementWeight,
        decrementWeight,
        resetPrompt,
        testModel,
        runModelTest,
        saveConfig,
        trainModel,
        downloadHistory,
        getRiskColor,
        getRecommendationClass
      };
    }
  }
  </script>
  
  <style scoped>
  .ai-model-config {
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
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    gap: 20px;
  }
  
  .config-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin-bottom: 20px;
  }
  
  .config-card h2 {
    margin-top: 0;
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #eee;
    font-size: 18px;
  }
  
  .card-desc {
    color: #666;
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  .form-row {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
  }
  
  .form-row .form-group {
    flex: 1;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
    color: #333;
  }
  
  input[type="text"],
  input[type="number"],
  select,
  textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
  }
  
  textarea {
    font-family: inherit;
    line-height: 1.5;
  }
  
  small {
    display: block;
    margin-top: 5px;
    color: #666;
    font-size: 12px;
  }
  
  .range-input {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .range-input input {
    flex: 1;
  }
  
  .range-value {
    font-weight: 500;
    min-width: 40px;
    text-align: right;
  }
  
  .toggle-switch {
    position: relative;
    display: inline-block;
    width: 50px;
    height: 24px;
  }
  
  .toggle-switch input {
    opacity: 0;
    width: 0;
    height: 0;
  }
  
  .toggle-slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    transition: .4s;
    border-radius: 24px;
  }
  
  .toggle-slider:before {
    position: absolute;
    content: "";
    height: 16px;
    width: 16px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
  }
  
  input:checked + .toggle-slider {
    background-color: #2196F3;
  }
  
  input:checked + .toggle-slider:before {
    transform: translateX(26px);
  }
  
  .factor-list {
    margin-top: 20px;
  }
  
  .factor-item {
    margin-bottom: 15px;
  }
  
  .factor-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 5px;
  }
  
  .factor-header h3 {
    margin: 0;
    font-size: 16px;
    font-weight: 500;
  }
  
  .factor-weight {
    display: flex;
    align-items: center;
    gap: 5px;
  }
  
  .weight-value {
    font-weight: 500;
    min-width: 40px;
    text-align: right;
  }
  
  .weight-button {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    border: none;
    background-color: #ddd;
    color: #333;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
  }
  
  .weight-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .factor-bar {
    height: 8px;
    background-color: #eee;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 5px;
  }
  
  .factor-bar-fill {
    height: 100%;
    border-radius: 4px;
  }
  
  .factor-desc {
    margin: 0;
    font-size: 14px;
    color: #666;
  }
  
  .total-weight {
    display: flex;
    justify-content: flex-end;
    gap: 5px;
    margin-top: 20px;
    font-weight: 500;
  }
  
  .error {
    color: #F44336;
  }
  
  .weight-warning {
    color: #F44336;
    font-size: 12px;
    font-weight: normal;
  }
  
  .ai-logo {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
  }
  
  .ai-logo-img {
    height: 40px;
  }
  
  .btn-primary {
    background-color: #2196F3;
    color: white;
    padding: 10px 20px;
    border-radius: 4px;
    border: none;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
  }
  
  .btn-primary:hover {
    background-color: #1976D2;
  }
  
  .btn-secondary {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border-radius: 4px;
    border: none;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
  }
  
  .btn-secondary:hover {
    background-color: #388E3C;
  }
  
  .btn-outline {
    background-color: transparent;
    color: #2196F3;
    padding: 10px 20px;
    border-radius: 4px;
    border: 1px solid #2196F3;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
  }
  
  .btn-outline:hover {
    background-color: rgba(33, 150, 243, 0.1);
  }
  
  .btn-text {
    background-color: transparent;
    color: #2196F3;
    padding: 0;
    border: none;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    text-decoration: underline;
  }
  
  .btn-full {
    width: 100%;
    margin-top: 20px;
  }
  
  .stats-row {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
  }
  
  .stat-box {
    flex: 1;
    background-color: #f5f5f5;
    border-radius: 4px;
    padding: 15px;
    text-align: center;
  }
  
  .stat-label {
    font-size: 14px;
    color: #666;
    margin-bottom: 5px;
  }
  
  .stat-value {
    font-size: 18px;
    font-weight: 600;
    color: #333;
  }
  
  .history-list {
    margin-top: 20px;
    max-height: 300px;
    overflow-y: auto;
  }
  
  .history-list table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .history-list th,
  .history-list td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #eee;
  }
  
  .history-list th {
    font-weight: 500;
    color: #333;
    background-color: #f5f5f5;
    position: sticky;
    top: 0;
  }
  
  .action-buttons {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
    margin-top: 20px;
  }
  
  /* Modal de teste */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }
  
  .modal-content {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    width: 800px;
    max-width: 90%;
    max-height: 90vh;
    overflow-y: auto;
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    border-bottom: 1px solid #eee;
  }
  
  .modal-header h2 {
    margin: 0;
    font-size: 20px;
  }
  
  .btn-close {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #666;
  }
  
  .modal-body {
    padding: 20px;
  }
  
  .modal-body h3 {
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 18px;
  }
  
  .test-result {
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px solid #eee;
  }
  
  .risk-score {
    margin-bottom: 20px;
  }
  
  .risk-meter {
    height: 10px;
    background-color: #eee;
    border-radius: 5px;
    overflow: hidden;
    margin-bottom: 5px;
  }
  
  .risk-bar {
    height: 100%;
    border-radius: 5px;
  }
  
  .risk-value {
    font-weight: 500;
    text-align: right;
  }
  
  .recommendation {
    padding: 15px;
    border-radius: 4px;
    margin-bottom: 20px;
  }
  
  .recommendation h4 {
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 16px;
  }
  
  .recommendation p {
    margin: 0;
  }
  
  .recommendation.success {
    background-color: #E8F5E9;
    border-left: 4px solid #4CAF50;
  }
  
  .recommendation.warning {
    background-color: #FFF8E1;
    border-left: 4px solid #FFC107;
  }
  
  .recommendation.danger {
    background-color: #FFEBEE;
    border-left: 4px solid #F44336;
  }
  
  .explanation {
    margin-bottom: 20px;
  }
  
  .explanation h4 {
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 16px;
  }
  
  .explanation pre {
    background-color: #f5f5f5;
    padding: 15px;
    border-radius: 4px;
    font-family: inherit;
    white-space: pre-wrap;
    font-size: 14px;
    line-height: 1.5;
    margin: 0;
  }
  
  .factor-breakdown {
    margin-bottom: 20px;
  }
  
  .factor-breakdown h4 {
    margin-top: 0;
    margin-bottom: 15px;
    font-size: 16px;
  }
  
  .factor-impact-bar {
    height: 8px;
    background-color: #eee;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 10px;
  }
  
  .impact-bar-fill {
    height: 100%;
    border-radius: 4px;
  }
  
  .impact-bar-fill.positive {
    background-color: #4CAF50;
  }
  
  .impact-bar-fill.negative {
    background-color: #F44336;
  }
  
  .impact-bar-fill.neutral {
    background-color: #9E9E9E;
  }
  
  .positive {
    color: #4CAF50;
  }
  
  .negative {
    color: #F44336;
  }
  
  .neutral {
    color: #9E9E9E;
  }
  </style>