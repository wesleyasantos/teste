import dataService from './data-service';

/**
 * Serviço de API simulada para o MVP
 * Usa dataService para manipular os dados locais
 */
const apiClient = {
  // Auth
  login(credentials) {
    try {
      const result = dataService.login(credentials.username, credentials.password);
      return Promise.resolve({ data: result });
    } catch (error) {
      return Promise.reject({ response: { data: { detail: error.message } } });
    }
  },
  
  logout() {
    const result = dataService.logout();
    return Promise.resolve({ data: result });
  },
  
  // Clientes
  getClients(params = {}) {
    const result = dataService.getClients(params);
    return Promise.resolve({ data: result });
  },
  
  getClient(id) {
    const client = dataService.getClientById(id);
    if (client) {
      return Promise.resolve({ data: client });
    } else {
      return Promise.reject({ response: { status: 404, data: { detail: "Cliente não encontrado" } } });
    }
  },
  
  createClient(client) {
    const result = dataService.createClient(client);
    return Promise.resolve({ data: result });
  },
  
  updateClient(id, client) {
    try {
      const result = dataService.updateClient(id, client);
      return Promise.resolve({ data: result });
    } catch (error) {
      return Promise.reject({ response: { data: { detail: error.message } } });
    }
  },
  
  getClientCreditHistory(id) {
    const applications = dataService.getApplicationsByClientId(id);
    return Promise.resolve({ data: applications });
  },
  
  getDocuments(clientId) {
    const documents = dataService.getDocumentsByClientId(clientId);
    return Promise.resolve({ data: { results: documents, count: documents.length } });
  },
  
  getCreditScore(clientId) {
    const score = dataService.getCreditScoreByClientId(clientId);
    if (score) {
      return Promise.resolve({ data: score });
    } else {
      // Gerar score para demo se não existir
      const generatedScore = dataService.generateCreditScore(clientId);
      return Promise.resolve({ data: generatedScore });
    }
  },
  
  // Aplicações de crédito
  getApplications(params = {}) {
    const result = dataService.getApplications(params);
    return Promise.resolve({ data: result });
  },
  
  getApplication(id) {
    const application = dataService.getApplicationById(id);
    if (application) {
      return Promise.resolve({ data: application });
    } else {
      return Promise.reject({ response: { status: 404, data: { detail: "Aplicação não encontrada" } } });
    }
  },
  
  createApplication(application) {
    const result = dataService.createApplication(application);
    return Promise.resolve({ data: result });
  },
  
  updateApplication(id, application) {
    try {
      const result = dataService.updateApplication(id, application);
      return Promise.resolve({ data: result });
    } catch (error) {
      return Promise.reject({ response: { data: { detail: error.message } } });
    }
  },
  
  analyzeApplication(id) {
    try {
      // Verificar se já existe uma análise
      let analysis = dataService.getAnalysisByApplicationId(id);
      
      if (!analysis) {
        // Criar nova análise
        const currentUser = dataService.getCurrentUser();
        analysis = dataService.createAnalysis({
          application_id: id,
          analyst_name: currentUser ? currentUser.name : 'Analista Demo',
          decision: 'pending',
          notes: ''
        });
      }
      
      // Gerar predição de IA para demonstração
      const aiPrediction = dataService.generateAIPrediction(id);
      
      return Promise.resolve({
        data: {
          analysis: analysis,
          ai_prediction: aiPrediction
        }
      });
    } catch (error) {
      return Promise.reject({ response: { data: { detail: error.message } } });
    }
  },
  
  // Análises
  getAnalyses(params = {}) {
    const result = dataService.getAnalyses(params);
    return Promise.resolve({ data: result });
  },
  
  getAnalysis(id) {
    const analysis = dataService.getAnalysisById(id);
    if (analysis) {
      return Promise.resolve({ data: analysis });
    } else {
      return Promise.reject({ response: { status: 404, data: { detail: "Análise não encontrada" } } });
    }
  },
  
  updateAnalysis(id, analysis) {
    try {
      const result = dataService.updateAnalysis(id, analysis);
      return Promise.resolve({ data: result });
    } catch (error) {
      return Promise.reject({ response: { data: { detail: error.message } } });
    }
  },
  
  // Predições de IA
  getAIPrediction(applicationId) {
    const prediction = dataService.getAIPredictionByApplicationId(applicationId);
    if (prediction) {
      return Promise.resolve({ data: prediction });
    } else {
      // Gerar predição para demo se não existir
      const generatedPrediction = dataService.generateAIPrediction(applicationId);
      return Promise.resolve({ data: generatedPrediction });
    }
  },
  
  // Utilitários para o MVP
  resetMVPData() {
    const result = dataService.resetData();
    return Promise.resolve({ data: result });
  }
};

export default apiClient;