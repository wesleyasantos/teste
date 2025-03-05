import * as preloadedData from '../data/preloaded-data';

/**
 * Serviço para gerenciar dados no MVP
 * Usa os dados pré-carregados e localStorage para persistência
 */
class DataService {
  constructor() {
    this.initializeData();
  }

  // Inicializa os dados do MVP no localStorage se não existirem
  initializeData() {
    if (!localStorage.getItem('mvp_initialized')) {
      localStorage.setItem('clients', JSON.stringify(preloadedData.clients));
      localStorage.setItem('documents', JSON.stringify(preloadedData.documents));
      localStorage.setItem('creditScores', JSON.stringify(preloadedData.creditScores));
      localStorage.setItem('applications', JSON.stringify(preloadedData.applications));
      localStorage.setItem('analyses', JSON.stringify(preloadedData.analyses));
      localStorage.setItem('aiPredictions', JSON.stringify(preloadedData.aiPredictions));
      localStorage.setItem('users', JSON.stringify(preloadedData.users));
      localStorage.setItem('mvp_initialized', 'true');
    }
  }

  // Reset da base de dados para os valores iniciais
  resetData() {
    localStorage.removeItem('mvp_initialized');
    this.initializeData();
    return { success: true, message: 'Dados reiniciados com sucesso' };
  }

  // OPERAÇÕES DE CLIENTES

  getClients(filters = {}) {
    let clients = JSON.parse(localStorage.getItem('clients')) || [];
    
    // Aplicar filtros
    if (filters.search) {
      const search = filters.search.toLowerCase();
      clients = clients.filter(client => 
        client.name.toLowerCase().includes(search) || 
        (client.cpf && client.cpf.includes(search)) ||
        (client.cnpj && client.cnpj.includes(search))
      );
    }
    
    if (filters.type) {
      clients = clients.filter(client => client.type === filters.type);
    }
    
    return {
      results: clients,
      count: clients.length
    };
  }

  getClientById(id) {
    const clients = JSON.parse(localStorage.getItem('clients')) || [];
    return clients.find(client => client.id === parseInt(id));
  }

  createClient(clientData) {
    const clients = JSON.parse(localStorage.getItem('clients')) || [];
    const newId = clients.length > 0 ? Math.max(...clients.map(c => c.id)) + 1 : 1;
    
    // Criar endereço com novo ID
    const addresses = clients.flatMap(c => c.address ? [c.address] : []);
    const newAddressId = addresses.length > 0 ? Math.max(...addresses.map(a => a.id)) + 1 : 1;
    
    if (clientData.address) {
      clientData.address.id = newAddressId;
    }
    
    const newClient = {
      ...clientData,
      id: newId,
      created_at: new Date().toISOString()
    };
    
    clients.push(newClient);
    localStorage.setItem('clients', JSON.stringify(clients));
    
    return newClient;
  }

  updateClient(id, clientData) {
    const clients = JSON.parse(localStorage.getItem('clients')) || [];
    const index = clients.findIndex(client => client.id === parseInt(id));
    
    if (index !== -1) {
      // Preservar ID e outros campos que não devem ser atualizados
      const updatedClient = {
        ...clients[index],
        ...clientData,
        id: parseInt(id),
        updated_at: new Date().toISOString()
      };
      
      clients[index] = updatedClient;
      localStorage.setItem('clients', JSON.stringify(clients));
      
      return updatedClient;
    }
    
    throw new Error('Cliente não encontrado');
  }

  // OPERAÇÕES DE DOCUMENTOS

  getDocumentsByClientId(clientId) {
    const documents = JSON.parse(localStorage.getItem('documents')) || [];
    return documents.filter(doc => doc.client_id === parseInt(clientId));
  }

  createDocument(documentData) {
    const documents = JSON.parse(localStorage.getItem('documents')) || [];
    const newId = documents.length > 0 ? Math.max(...documents.map(d => d.id)) + 1 : 1;
    
    const newDocument = {
      ...documentData,
      id: newId,
      uploaded_at: new Date().toISOString()
    };
    
    documents.push(newDocument);
    localStorage.setItem('documents', JSON.stringify(documents));
    
    return newDocument;
  }

  // OPERAÇÕES DE SCORES DE CRÉDITO

  getCreditScoreByClientId(clientId) {
    const creditScores = JSON.parse(localStorage.getItem('creditScores')) || [];
    return creditScores.find(score => score.client_id === parseInt(clientId));
  }

  createOrUpdateCreditScore(scoreData) {
    const creditScores = JSON.parse(localStorage.getItem('creditScores')) || [];
    const index = creditScores.findIndex(score => score.client_id === parseInt(scoreData.client_id));
    
    if (index !== -1) {
      // Atualizar score existente
      creditScores[index] = {
        ...creditScores[index],
        ...scoreData,
        last_calculated: new Date().toISOString()
      };
    } else {
      // Criar novo score
      const newId = creditScores.length > 0 ? Math.max(...creditScores.map(s => s.id)) + 1 : 1;
      const newScore = {
        ...scoreData,
        id: newId,
        last_calculated: new Date().toISOString()
      };
      creditScores.push(newScore);
    }
    
    localStorage.setItem('creditScores', JSON.stringify(creditScores));
    
    return creditScores.find(score => score.client_id === parseInt(scoreData.client_id));
  }

  // OPERAÇÕES DE SOLICITAÇÕES DE CRÉDITO

  getApplications(filters = {}) {
    let applications = JSON.parse(localStorage.getItem('applications')) || [];
    
    // Aplicar filtros
    if (filters.status) {
      applications = applications.filter(app => app.status === filters.status);
    }
    
    if (filters.client_id) {
      applications = applications.filter(app => app.client_id === parseInt(filters.client_id));
    }
    
    // Adicionar informações do cliente
    const clients = JSON.parse(localStorage.getItem('clients')) || [];
    applications = applications.map(app => {
      const client = clients.find(c => c.id === app.client_id);
      return {
        ...app,
        client_name: client ? client.name : 'Cliente Desconhecido'
      };
    });
    
    return {
      results: applications,
      count: applications.length
    };
  }

  getApplicationById(id) {
    const applications = JSON.parse(localStorage.getItem('applications')) || [];
    return applications.find(app => app.id === parseInt(id));
  }

  getApplicationsByClientId(clientId) {
    const applications = JSON.parse(localStorage.getItem('applications')) || [];
    return applications.filter(app => app.client_id === parseInt(clientId));
  }

  createApplication(applicationData) {
    const applications = JSON.parse(localStorage.getItem('applications')) || [];
    const newId = applications.length > 0 ? Math.max(...applications.map(a => a.id)) + 1 : 1;
    
    const newApplication = {
      ...applicationData,
      id: newId,
      status: 'pending',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
    
    applications.push(newApplication);
    localStorage.setItem('applications', JSON.stringify(applications));
    
    return newApplication;
  }

  updateApplication(id, applicationData) {
    const applications = JSON.parse(localStorage.getItem('applications')) || [];
    const index = applications.findIndex(app => app.id === parseInt(id));
    
    if (index !== -1) {
      // Preservar ID e outros campos que não devem ser atualizados
      const updatedApplication = {
        ...applications[index],
        ...applicationData,
        id: parseInt(id),
        updated_at: new Date().toISOString()
      };
      
      applications[index] = updatedApplication;
      localStorage.setItem('applications', JSON.stringify(applications));
      
      return updatedApplication;
    }
    
    throw new Error('Solicitação não encontrada');
  }

  // OPERAÇÕES DE ANÁLISES

  getAnalyses(filters = {}) {
    let analyses = JSON.parse(localStorage.getItem('analyses')) || [];
    
    // Aplicar filtros
    if (filters.decision) {
      analyses = analyses.filter(analysis => analysis.decision === filters.decision);
    }
    
    if (filters.application_id) {
      analyses = analyses.filter(analysis => analysis.application_id === parseInt(filters.application_id));
    }
    
    // Adicionar informações complementares
    const applications = JSON.parse(localStorage.getItem('applications')) || [];
    const clients = JSON.parse(localStorage.getItem('clients')) || [];
    
    analyses = analyses.map(analysis => {
      const application = applications.find(app => app.id === analysis.application_id);
      const client = application ? clients.find(c => c.id === application.client_id) : null;
      
      return {
        ...analysis,
        client_id: client ? client.id : null,
        client_name: client ? client.name : 'Cliente Desconhecido',
      };
    });
    
    return {
      results: analyses,
      count: analyses.length
    };
  }

  getAnalysisById(id) {
    const analyses = JSON.parse(localStorage.getItem('analyses')) || [];
    return analyses.find(analysis => analysis.id === parseInt(id));
  }

  getAnalysisByApplicationId(applicationId) {
    const analyses = JSON.parse(localStorage.getItem('analyses')) || [];
    return analyses.find(analysis => analysis.application_id === parseInt(applicationId));
  }

  createAnalysis(analysisData) {
    const analyses = JSON.parse(localStorage.getItem('analyses')) || [];
    const newId = analyses.length > 0 ? Math.max(...analyses.map(a => a.id)) + 1 : 1;
    
    const newAnalysis = {
      ...analysisData,
      id: newId,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };
    
    analyses.push(newAnalysis);
    localStorage.setItem('analyses', JSON.stringify(analyses));
    
    // Atualizar status da aplicação para "in_analysis"
    if (analysisData.application_id) {
      const applications = JSON.parse(localStorage.getItem('applications')) || [];
      const appIndex = applications.findIndex(app => app.id === parseInt(analysisData.application_id));
      
      if (appIndex !== -1) {
        applications[appIndex].status = 'in_analysis';
        applications[appIndex].updated_at = new Date().toISOString();
        localStorage.setItem('applications', JSON.stringify(applications));
      }
    }
    
    return newAnalysis;
  }

  updateAnalysis(id, analysisData) {
    const analyses = JSON.parse(localStorage.getItem('analyses')) || [];
    const index = analyses.findIndex(analysis => analysis.id === parseInt(id));
    
    if (index !== -1) {
      // Preservar ID e outros campos que não devem ser atualizados
      const updatedAnalysis = {
        ...analyses[index],
        ...analysisData,
        id: parseInt(id),
        updated_at: new Date().toISOString()
      };
      
      analyses[index] = updatedAnalysis;
      localStorage.setItem('analyses', JSON.stringify(analyses));
      
      // Atualizar status da aplicação se decisão for conclusiva
      if (analysisData.decision && (analysisData.decision === 'approved' || analysisData.decision === 'rejected')) {
        const applications = JSON.parse(localStorage.getItem('applications')) || [];
        const appIndex = applications.findIndex(app => app.id === parseInt(updatedAnalysis.application_id));
        
        if (appIndex !== -1) {
          applications[appIndex].status = analysisData.decision;
          applications[appIndex].updated_at = new Date().toISOString();
          localStorage.setItem('applications', JSON.stringify(applications));
        }
      }
      
      return updatedAnalysis;
    }
    
    throw new Error('Análise não encontrada');
  }

  // OPERAÇÕES DE PREDIÇÕES DE IA

  getAIPredictionByApplicationId(applicationId) {
    const predictions = JSON.parse(localStorage.getItem('aiPredictions')) || [];
    return predictions.find(prediction => prediction.application_id === parseInt(applicationId));
  }

  createAIPrediction(predictionData) {
    const predictions = JSON.parse(localStorage.getItem('aiPredictions')) || [];
    const newId = predictions.length > 0 ? Math.max(...predictions.map(p => p.id)) + 1 : 1;
    
    const newPrediction = {
      ...predictionData,
      id: newId,
      created_at: new Date().toISOString()
    };
    
    predictions.push(newPrediction);
    localStorage.setItem('aiPredictions', JSON.stringify(predictions));
    
    return newPrediction;
  }

  // OPERAÇÕES DE AUTENTICAÇÃO

  login(username, password) {
    const users = JSON.parse(localStorage.getItem('users')) || [];
    const user = users.find(u => u.username === username && u.password === password);
    
    if (user) {
      // Gerar token simulado
      const token = btoa(JSON.stringify({
        user_id: user.id,
        username: user.username,
        role: user.role,
        exp: Date.now() + 24 * 60 * 60 * 1000 // 24 horas
      }));
      
      // Salvar informações de autenticação
      localStorage.setItem('auth_token', token);
      localStorage.setItem('auth_user', JSON.stringify({
        id: user.id,
        username: user.username,
        name: user.name,
        role: user.role,
        email: user.email
      }));
      
      return {
        token,
        user: {
          id: user.id,
          username: user.username,
          name: user.name,
          role: user.role,
          email: user.email
        }
      };
    }
    
    throw new Error('Credenciais inválidas');
  }

  logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('auth_user');
    return { success: true };
  }

  getCurrentUser() {
    const userJson = localStorage.getItem('auth_user');
    return userJson ? JSON.parse(userJson) : null;
  }

  isAuthenticated() {
    const token = localStorage.getItem('auth_token');
    if (!token) return false;
    
    try {
      const payload = JSON.parse(atob(token));
      return payload.exp > Date.now();
    } catch (e) {
      return false;
    }
  }

  // UTILITÁRIOS PARA O MVP

  // Gerar um score de crédito simulado
  generateCreditScore(clientId) {
    const client = this.getClientById(clientId);
    if (!client) throw new Error('Cliente não encontrado');
    
    // Gerar valores simulados baseados no tipo de cliente
    let score, payment_history, debt_burden, length_history;
    
    if (client.type === 'PJ') { // Pessoa Jurídica
      // Uma pontuação um pouco melhor para empresas com maior faturamento
      const baseScore = 650 + Math.floor(Math.random() * 200);
      const revenueBonus = Math.floor((client.annual_revenue / 1000000) * 50); // Até 50 pontos extras por milhão
      score = Math.min(baseScore + revenueBonus, 900);
      
      // Componentes do score
      payment_history = 60 + Math.floor(Math.random() * 30);
      debt_burden = 60 + Math.floor(Math.random() * 30);
      length_history = 60 + Math.floor(Math.random() * 30);
    } else { // Pessoa Física
      // Uma pontuação um pouco melhor para pessoas com maior renda
      const baseScore = 600 + Math.floor(Math.random() * 250);
      const incomeBonus = Math.floor((client.monthly_income / 1000) * 20); // Até 20 pontos extras por mil
      score = Math.min(baseScore + incomeBonus, 900);
      
      // Componentes do score
      payment_history = 60 + Math.floor(Math.random() * 35);
      debt_burden = 60 + Math.floor(Math.random() * 35);
      length_history = 60 + Math.floor(Math.random() * 35);
    }
    
    return this.createOrUpdateCreditScore({
      client_id: clientId,
      score,
      payment_history,
      debt_burden,
      length_history
    });
  }

  // Gerar uma predição de IA simulada
  generateAIPrediction(applicationId) {
    const application = this.getApplicationById(applicationId);
    if (!application) throw new Error('Aplicação não encontrada');
    
    const client = this.getClientById(application.client_id);
    if (!client) throw new Error('Cliente não encontrado');
    
    // Buscar ou gerar score de crédito
    let creditScore = this.getCreditScoreByClientId(client.id);
    if (!creditScore) {
      creditScore = this.generateCreditScore(client.id);
    }
    
    // Calcular valor da parcela
    const monthlyCost = this.calculateInstallment(application.amount_requested, application.term_months, application.interest_rate || 1.5);
    
    // Calcular comprometimento de renda
    let incomeRatio, incomeRatioLabel;
    if (client.type === 'PJ') {
      // Para PJ - comprometimento anual do faturamento
      incomeRatio = (monthlyCost * 12 / client.annual_revenue) * 100;
      incomeRatioLabel = `${incomeRatio.toFixed(2)}% ao ano`;
    } else {
      // Para PF - comprometimento mensal da renda
      incomeRatio = (monthlyCost / client.monthly_income) * 100;
      incomeRatioLabel = `${incomeRatio.toFixed(2)}% da renda mensal`;
    }
    
    // Calcular score de risco (escala de 0-100, menor é melhor)
    // Base no score de crédito, comprometimento de renda e valor/prazo
    const maxScore = 900; // Score máximo de crédito
    const creditFactor = (maxScore - creditScore.score) / maxScore; // Inverso da pontuação (pior score = maior risco)
    const incomeFactor = Math.min(incomeRatio / 100, 1); // Quanto maior o comprometimento, maior o risco
    
    // Valor e prazo também influenciam
    const amountFactor = Math.min(application.amount_requested / 1000000, 1); // Até 1 milhão
    const termFactor = application.term_months / 60; // Até 60 meses
    
    // Calcular score final (0-100)
    let riskScore = (creditFactor * 0.5 + incomeFactor * 0.3 + amountFactor * 0.1 + termFactor * 0.1) * 100;
    riskScore = Math.min(Math.max(riskScore, 5), 95); // Garantir entre 5 e 95
    
    // Determinar recomendação baseada no score de risco
    let recommendation, explanation;
    
    if (riskScore < 20) {
      recommendation = "APROVADO: Risco baixo, excelente candidato para aprovação.";
    } else if (riskScore < 40) {
      recommendation = "APROVADO COM CONDIÇÕES: Bom candidato, mas considerar redução do valor ou aumento do prazo.";
    } else if (riskScore < 60) {
      recommendation = "ANÁLISE MANUAL: Risco moderado, recomendada revisão manual do histórico e documentos.";
    } else if (riskScore < 80) {
      recommendation = "REPROVADO COM CONDIÇÕES: Alto risco, considerar apenas com garantias adicionais ou fiador.";
    } else {
      recommendation = "REPROVADO: Risco muito alto, não recomendada aprovação.";
    }
    
    // Gerar explicação personalizada
    if (client.type === 'PJ') {
      explanation = `Score de risco: ${riskScore.toFixed(2)}/100 (quanto menor, melhor)\n\n` +
        `Análise de capacidade de pagamento:\n` +
        `- Valor da parcela: R$ ${monthlyCost.toFixed(2)}\n` +
        `- Faturamento anual: R$ ${client.annual_revenue.toLocaleString('pt-BR')}\n` +
        `- Comprometimento do faturamento: ${incomeRatio.toFixed(2)}% ao ano\n\n` +
        `Principais fatores para a decisão:\n`;
    } else {
      explanation = `Score de risco: ${riskScore.toFixed(2)}/100 (quanto menor, melhor)\n\n` +
        `Análise de capacidade de pagamento:\n` +
        `- Valor da parcela: R$ ${monthlyCost.toFixed(2)}\n` +
        `- Comprometimento da renda: ${incomeRatio.toFixed(2)}% da renda mensal\n\n` +
        `Principais fatores para a decisão:\n`;
    }
    
    // Adicionar fatores específicos
    if (creditScore.score > 800) {
      explanation += `- POSITIVO: Excelente histórico de crédito (score ${creditScore.score})\n`;
    } else if (creditScore.score > 700) {
      explanation += `- POSITIVO: Bom histórico de crédito (score ${creditScore.score})\n`;
    } else if (creditScore.score > 600) {
      explanation += `- NEUTRO: Score de crédito aceitável (${creditScore.score})\n`;
    } else {
      explanation += `- NEGATIVO: Score de crédito baixo (${creditScore.score})\n`;
    }
    
    if (incomeRatio < 20) {
      explanation += `- POSITIVO: Excelente comprometimento da renda (abaixo de 20%)\n`;
    } else if (incomeRatio < 30) {
      explanation += `- POSITIVO: Bom comprometimento da renda (abaixo de 30%)\n`;
    } else if (incomeRatio < 40) {
      explanation += `- NEUTRO: Comprometimento da renda moderado\n`;
    } else {
      explanation += `- NEGATIVO: Alto comprometimento da renda (acima de 40%)\n`;
    }
    
    if (client.type === 'PJ' && client.founding_date) {
      const foundingDate = new Date(client.founding_date);
      const years = new Date().getFullYear() - foundingDate.getFullYear();
      
      if (years > 10) {
        explanation += `- POSITIVO: Empresa com mais de 10 anos de mercado\n`;
      } else if (years > 5) {
        explanation += `- NEUTRO: Empresa com ${years} anos de mercado\n`;
      } else {
        explanation += `- NEGATIVO: Empresa com menos de 5 anos de mercado\n`;
      }
    }
    
    // Criar e retornar a predição
    return this.createAIPrediction({
      application_id: applicationId,
      risk_score: riskScore,
      default_probability: riskScore / 100,
      recommendation,
      explanation
    });
  }

  // Calcular valor da parcela
  calculateInstallment(principal, months, rate) {
    const monthlyRate = rate / 100;
    return (principal * monthlyRate * Math.pow(1 + monthlyRate, months)) / (Math.pow(1 + monthlyRate, months) - 1);
  }
}

export default new DataService();