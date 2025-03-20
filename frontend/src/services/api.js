import axios from 'axios';

// Criar instância do axios com configurações base
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api', // Garanta que a URL aponta para o backend Django
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptador para adicionar token de autenticação
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Token ${token}`;
    }
    console.log(`API Request: ${config.method.toUpperCase()} ${config.url}`, config.data);
    return config;
  },
  error => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  response => {
    console.log(`API Response: ${response.status}`, response.data);
    return response;
  },
  error => {
    console.error('API Response Error:', error.response || error);
    return Promise.reject(error);
  }
);

// Serviço de autenticação
const authService = {
  login(credentials) {
    return apiClient.post('/auth/login/', credentials);
  },
  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    return Promise.resolve({ success: true });
  },
  getCurrentUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },
  isAuthenticated() {
    return !!localStorage.getItem('token');
  }
};

// Serviço de clientes
const clientService = {
  getClients(params = {}) {
    return apiClient.get('/clients/', { params });
  },
  getClient(id) {
    return apiClient.get(`/clients/${id}/`);
  },
  createClient(client) {
    return apiClient.post('/clients/', client);
  },
  updateClient(id, client) {
    return apiClient.put(`/clients/${id}/`, client);
  },
  deleteClient(id) {
    return apiClient.delete(`/clients/${id}/`);
  },
  getClientOperations(id) {
    return apiClient.get(`/clients/${id}/operations/`);
  },
  getClientDocuments(id) {
    return apiClient.get(`/clients/${id}/documents/`);
  }
};

// Serviço de operações
const operationService = {
  getOperations(params = {}) {
    return apiClient.get('/operations/', { params });
  },
  getOperation(id) {
    return apiClient.get(`/operations/${id}/`);
  },
  createOperation(operation) {
    console.log('API - Enviando operação para backend:', operation);
    return apiClient.post('/operations/', operation);
  },
  updateOperation(id, operation) {
    return apiClient.put(`/operations/${id}/`, operation);
  },
  deleteOperation(id) {
    return apiClient.delete(`/operations/${id}/`);
  },
  updateOperationStatus(id, status) {
    return apiClient.post(`/operations/${id}/update_status/`, { status });
  },
  getInstallments(id) {
    return apiClient.get(`/operations/${id}/installments/`);
  }
};

// Serviço de análise de crédito
const analysisService = {
  getAnalyses(params = {}) {
    return apiClient.get('/analyses/', { params });
  },
  getAnalysis(id) {
    return apiClient.get(`/analyses/${id}/`);
  },
  createAnalysis(analysis) {
    return apiClient.post('/analyses/', analysis);
  },
  updateAnalysis(id, analysis) {
    return apiClient.put(`/analyses/${id}/`, analysis);
  },
  calculateAnalysis(id) {
    return apiClient.post(`/analyses/${id}/calculate/`);
  }
};

// Serviço de parceiros
const partnerService = {
  getPartners(params = {}) {
    return apiClient.get('/partners/', { params });
  },
  getPartner(id) {
    return apiClient.get(`/partners/${id}/`);
  },
  createPartner(partner) {
    return apiClient.post('/partners/', partner);
  },
  updatePartner(id, partner) {
    return apiClient.put(`/partners/${id}/`, partner);
  },
  deletePartner(id) {
    return apiClient.delete(`/partners/${id}/`);
  }
};

// Serviço de garantias
const guaranteeService = {
  getGuarantees(params = {}) {
    return apiClient.get('/guarantees/', { params });
  },
  getGuarantee(id) {
    return apiClient.get(`/guarantees/${id}/`);
  },
  createGuarantee(guarantee) {
    return apiClient.post('/guarantees/', guarantee);
  },
  updateGuarantee(id, guarantee) {
    return apiClient.put(`/guarantees/${id}/`, guarantee);
  },
  deleteGuarantee(id) {
    return apiClient.delete(`/guarantees/${id}/`);
  }
};

// Serviço de documentos
const documentService = {
  getDocuments(params = {}) {
    return apiClient.get('/documents/', { params });
  },
  getDocument(id) {
    return apiClient.get(`/documents/${id}/`);
  },
  uploadDocument(document) {
    const formData = new FormData();
    Object.keys(document).forEach(key => {
      formData.append(key, document[key]);
    });
    return apiClient.post('/documents/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },
  deleteDocument(id) {
    return apiClient.delete(`/documents/${id}/`);
  }
};

// Serviço de comitê
const committeeService = {
  getCommittees(params = {}) {
    return apiClient.get('/committees/', { params });
  },
  getCommittee(id) {
    return apiClient.get(`/committees/${id}/`);
  },
  startCommittee(id) {
    return apiClient.post(`/committees/${id}/start/`);
  },
  finishCommittee(id) {
    return apiClient.post(`/committees/${id}/finish/`);
  }
};

// Serviço de membro de comitê
const committeeMemberService = {
  getCommitteeMembers(params = {}) {
    return apiClient.get('/committee-members/', { params });
  },
  getCommitteeMember(id) {
    return apiClient.get(`/committee-members/${id}/`);
  },
  vote(id, voteData) {
    return apiClient.post(`/committee-members/${id}/vote/`, voteData);
  }
};

// Serviço de contratos
const contractService = {
  getContracts(params = {}) {
    return apiClient.get('/contracts/', { params });
  },
  getContract(id) {
    return apiClient.get(`/contracts/${id}/`);
  },
  generateContract(operationId) {
    return apiClient.post(`/contracts/generate/`, { operation: operationId });
  },
  finalizeContract(id) {
    return apiClient.post(`/contracts/${id}/finalize/`);
  }
};

// Serviço de assinaturas
const signatureService = {
  getSignatures(params = {}) {
    return apiClient.get('/signatures/', { params });
  },
  getSignature(id) {
    return apiClient.get(`/signatures/${id}/`);
  },
  signDocument(id) {
    return apiClient.post(`/signatures/${id}/sign/`);
  }
};

// Serviço de parcelas
const installmentService = {
  getInstallments(params = {}) {
    return apiClient.get('/installments/', { params });
  },
  getInstallment(id) {
    return apiClient.get(`/installments/${id}/`);
  },
  recordPayment(id, paymentData) {
    return apiClient.post(`/installments/${id}/record_payment/`, paymentData);
  }
};

export default {
  auth: authService,
  clients: clientService,
  operations: operationService,
  analyses: analysisService,
  partners: partnerService,
  guarantees: guaranteeService,
  documents: documentService,
  committees: committeeService,
  committeeMembers: committeeMemberService,
  contracts: contractService,
  signatures: signatureService,
  installments: installmentService
};