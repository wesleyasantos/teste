/**
 * Dados pré-carregados para o MVP
 * Esse arquivo contém dados simulados para demonstração
 */

// Dados de clientes pessoa física e jurídica
export const clients = [
    {
      id: 1,
      name: 'João Silva',
      cpf: '123.456.789-00',
      rg: '12.345.678-9',
      birth_date: '1985-05-15',
      phone: '(11) 98765-4321',
      email: 'joao.silva@email.com',
      profession: 'Engenheiro',
      monthly_income: 5000,
      type: 'PF', // Pessoa Física
      address: {
        id: 1,
        street: 'Rua das Flores',
        number: '123',
        complement: 'Apto 45',
        neighborhood: 'Jardim Primavera',
        city: 'São Paulo',
        state: 'SP',
        zip_code: '01234-567'
      }
    },
    {
      id: 2,
      name: 'Maria Souza',
      cpf: '987.654.321-00',
      rg: '98.765.432-1',
      birth_date: '1990-03-22',
      phone: '(11) 91234-5678',
      email: 'maria.souza@email.com',
      profession: 'Médica',
      monthly_income: 12000,
      type: 'PF',
      address: {
        id: 2,
        street: 'Avenida Paulista',
        number: '1500',
        complement: 'Sala 304',
        neighborhood: 'Bela Vista',
        city: 'São Paulo',
        state: 'SP',
        zip_code: '01310-200'
      }
    },
    {
      id: 3,
      name: 'Tech Solutions Ltda',
      cnpj: '12.345.678/0001-90',
      registration: '987654321',
      founding_date: '2010-08-10',
      phone: '(11) 3456-7890',
      email: 'contato@techsolutions.com',
      business_area: 'Tecnologia',
      annual_revenue: 1500000,
      type: 'PJ', // Pessoa Jurídica
      address: {
        id: 3,
        street: 'Rua Tecnológica',
        number: '500',
        complement: '10º Andar',
        neighborhood: 'Vila Olímpia',
        city: 'São Paulo',
        state: 'SP',
        zip_code: '04551-000'
      }
    },
    {
      id: 4,
      name: 'Comércio Verde Ltda',
      cnpj: '98.765.432/0001-10',
      registration: '123456789',
      founding_date: '2015-03-25',
      phone: '(11) 2345-6789',
      email: 'contato@comercioverde.com',
      business_area: 'Comércio Varejista',
      annual_revenue: 800000,
      type: 'PJ',
      address: {
        id: 4,
        street: 'Avenida Comercial',
        number: '1250',
        complement: 'Loja 22',
        neighborhood: 'Centro',
        city: 'Campinas',
        state: 'SP',
        zip_code: '13015-000'
      }
    }
  ];
  
  // Dados de documentos para clientes
  export const documents = [
    {
      id: 1,
      client_id: 1,
      document_type: 'income',
      uploaded_at: '2025-01-10T14:30:00',
      file: '#',
      file_name: 'comprovante_renda_joao.pdf'
    },
    {
      id: 2,
      client_id: 1,
      document_type: 'bank_statement',
      uploaded_at: '2025-01-10T14:35:00',
      file: '#',
      file_name: 'extrato_bancario_joao.pdf'
    },
    {
      id: 3,
      client_id: 2,
      document_type: 'income',
      uploaded_at: '2025-01-12T10:15:00',
      file: '#',
      file_name: 'comprovante_renda_maria.pdf'
    },
    {
      id: 4,
      client_id: 3,
      document_type: 'tax_return',
      uploaded_at: '2025-01-15T09:30:00',
      file: '#',
      file_name: 'balanco_techsolutions.pdf'
    },
    {
      id: 5,
      client_id: 3,
      document_type: 'bank_statement',
      uploaded_at: '2025-01-15T09:32:00',
      file: '#',
      file_name: 'extrato_bancario_techsolutions.pdf'
    },
    {
      id: 6,
      client_id: 4,
      document_type: 'tax_return',
      uploaded_at: '2025-01-18T14:20:00',
      file: '#',
      file_name: 'balanco_comercioverde.pdf'
    }
  ];
  
  // Dados de scores de crédito
  export const creditScores = [
    {
      id: 1,
      client_id: 1,
      score: 825,
      payment_history: 85,
      debt_burden: 80,
      length_history: 90,
      last_calculated: '2025-02-01T10:00:00'
    },
    {
      id: 2,
      client_id: 2,
      score: 765,
      payment_history: 75,
      debt_burden: 70,
      length_history: 65,
      last_calculated: '2025-02-03T11:30:00'
    },
    {
      id: 3,
      client_id: 3,
      score: 850,
      payment_history: 90,
      debt_burden: 85,
      length_history: 95,
      last_calculated: '2025-02-05T15:45:00'
    },
    {
      id: 4,
      client_id: 4,
      score: 720,
      payment_history: 70,
      debt_burden: 75,
      length_history: 60,
      last_calculated: '2025-02-08T13:15:00'
    }
  ];
  
  // Dados de solicitações de crédito
  export const applications = [
    {
      id: 101,
      client_id: 1,
      amount_requested: 8000,
      term_months: 12,
      interest_rate: 1.5,
      purpose: 'Compra de automóvel',
      status: 'approved',
      created_at: '2025-01-15T10:00:00',
      updated_at: '2025-01-18T14:30:00'
    },
    {
      id: 102,
      client_id: 1,
      amount_requested: 3000,
      term_months: 6,
      interest_rate: 1.8,
      purpose: 'Reforma residencial',
      status: 'pending',
      created_at: '2025-02-20T11:30:00',
      updated_at: '2025-02-20T11:30:00'
    },
    {
      id: 103,
      client_id: 2,
      amount_requested: 15000,
      term_months: 24,
      interest_rate: 1.6,
      purpose: 'Viagem internacional',
      status: 'in_analysis',
      created_at: '2025-02-18T09:15:00',
      updated_at: '2025-02-19T14:20:00'
    },
    {
      id: 104,
      client_id: 3,
      amount_requested: 120000,
      term_months: 36,
      interest_rate: 1.2,
      purpose: 'Expansão de negócio',
      status: 'approved',
      created_at: '2025-01-25T16:45:00',
      updated_at: '2025-01-30T10:30:00'
    },
    {
      id: 105,
      client_id: 4,
      amount_requested: 75000,
      term_months: 24,
      interest_rate: 1.4,
      purpose: 'Compra de estoque',
      status: 'in_analysis',
      created_at: '2025-02-22T13:40:00',
      updated_at: '2025-02-23T09:10:00'
    }
  ];
  
  // Dados de análises
  export const analyses = [
    {
      id: 1,
      application_id: 101,
      analyst_name: 'Ana Ferreira',
      decision: 'approved',
      notes: 'Cliente com bom histórico e capacidade de pagamento adequada',
      created_at: '2025-01-16T14:20:00',
      updated_at: '2025-01-18T14:30:00'
    },
    {
      id: 2,
      application_id: 103,
      analyst_name: 'Carlos Gomes',
      decision: 'pending',
      notes: 'Aguardando comprovantes adicionais de renda',
      created_at: '2025-02-19T10:15:00',
      updated_at: '2025-02-19T14:20:00'
    },
    {
      id: 3,
      application_id: 104,
      analyst_name: 'Ana Ferreira',
      decision: 'approved',
      notes: 'Empresa com bom fluxo de caixa e crescimento sustentável. Aprovado conforme política de crédito PJ.',
      created_at: '2025-01-28T16:30:00',
      updated_at: '2025-01-30T10:30:00'
    },
    {
      id: 4,
      application_id: 105,
      analyst_name: 'Pedro Santos',
      decision: 'pending',
      notes: 'Solicitando balanço do último trimestre para completar análise',
      created_at: '2025-02-23T09:10:00',
      updated_at: '2025-02-23T09:10:00'
    }
  ];
  
  // Dados de predições de IA
  export const aiPredictions = [
    {
      id: 1,
      application_id: 101,
      risk_score: 22.5,
      default_probability: 0.225,
      recommendation: "APROVADO: Risco baixo, excelente candidato para aprovação.",
      explanation: "Score de risco: 22.50/100 (quanto menor, melhor)\n\n" +
        "Análise de capacidade de pagamento:\n" +
        "- Valor da parcela: R$ 686.44\n" +
        "- Comprometimento da renda: 13.73% da renda mensal\n\n" +
        "Principais fatores para a decisão:\n" +
        "- POSITIVO: Excelente histórico de crédito (score 825)\n" +
        "- POSITIVO: Baixo comprometimento da renda (abaixo de 30%)\n" +
        "- POSITIVO: Estabilidade profissional\n"
    },
    {
      id: 2,
      application_id: 103,
      risk_score: 35.8,
      default_probability: 0.358,
      recommendation: "APROVADO COM CONDIÇÕES: Bom candidato, mas considerar redução do valor ou aumento do prazo.",
      explanation: "Score de risco: 35.80/100 (quanto menor, melhor)\n\n" +
        "Análise de capacidade de pagamento:\n" +
        "- Valor da parcela: R$ 712.69\n" +
        "- Comprometimento da renda: 5.94% da renda mensal\n\n" +
        "Principais fatores para a decisão:\n" +
        "- POSITIVO: Bom comprometimento da renda (abaixo de 30%)\n" +
        "- POSITIVO: Score de crédito adequado (765)\n" +
        "- NEUTRO: Valor solicitado relativamente alto para o perfil\n"
    },
    {
      id: 3,
      application_id: 104,
      risk_score: 18.2,
      default_probability: 0.182,
      recommendation: "APROVADO: Risco baixo, excelente candidato para aprovação.",
      explanation: "Score de risco: 18.20/100 (quanto menor, melhor)\n\n" +
        "Análise de capacidade de pagamento:\n" +
        "- Valor da parcela: R$ 3,775.43\n" +
        "- Faturamento anual: R$ 1,500,000.00\n" +
        "- Comprometimento do faturamento: 3.02% ao ano\n\n" +
        "Principais fatores para a decisão:\n" +
        "- POSITIVO: Excelente histórico de crédito empresarial (score 850)\n" +
        "- POSITIVO: Empresa com mais de 10 anos de mercado\n" +
        "- POSITIVO: Baixo comprometimento do faturamento\n"
    },
    {
      id: 4,
      application_id: 105,
      risk_score: 42.3,
      default_probability: 0.423,
      recommendation: "ANÁLISE MANUAL: Risco moderado, recomendada revisão manual do histórico e documentos.",
      explanation: "Score de risco: 42.30/100 (quanto menor, melhor)\n\n" +
        "Análise de capacidade de pagamento:\n" +
        "- Valor da parcela: R$ 3,575.55\n" +
        "- Faturamento anual: R$ 800,000.00\n" +
        "- Comprometimento do faturamento: 5.36% ao ano\n\n" +
        "Principais fatores para a decisão:\n" +
        "- POSITIVO: Score de crédito aceitável (720)\n" +
        "- NEGATIVO: Empresa com menos de 10 anos de mercado\n" +
        "- NEUTRO: Comprometimento do faturamento moderado\n" +
        "- RECOMENDAÇÃO: Avaliar sazonalidade do negócio e fluxo de caixa\n"
    }
  ];
  
  // Usuários do sistema
  export const users = [
    {
      id: 1,
      username: 'admin',
      password: 'admin123', // Apenas para demonstração!
      name: 'Administrador',
      role: 'admin',
      email: 'admin@sistemaanalise.com',
      is_active: true
    },
    {
      id: 2,
      username: 'analista',
      password: 'analista123', // Apenas para demonstração!
      name: 'Ana Ferreira',
      role: 'analyst',
      email: 'ana.ferreira@sistemaanalise.com',
      is_active: true
    },
    {
      id: 3,
      username: 'gerente',
      password: 'gerente123', // Apenas para demonstração!
      name: 'Carlos Gomes',
      role: 'manager',
      email: 'carlos.gomes@sistemaanalise.com',
      is_active: true
    }
  ];
  
  // Função para buscar cliente pelo ID
  export function getClientById(id) {
    return clients.find(client => client.id === id);
  }
  
  // Função para buscar aplicação pelo ID
  export function getApplicationById(id) {
    return applications.find(application => application.id === id);
  }
  
  // Função para buscar análise pelo ID
  export function getAnalysisById(id) {
    return analyses.find(analysis => analysis.id === id);
  }
  
  // Função para buscar documentos de um cliente
  export function getDocumentsByClientId(clientId) {
    return documents.filter(doc => doc.client_id === clientId);
  }
  
  // Função para buscar score de crédito de um cliente
  export function getCreditScoreByClientId(clientId) {
    return creditScores.find(score => score.client_id === clientId);
  }
  
  // Função para buscar aplicações de um cliente
  export function getApplicationsByClientId(clientId) {
    return applications.filter(app => app.client_id === clientId);
  }
  
  // Função para buscar predição de IA para uma aplicação
  export function getAIPredictionByApplicationId(applicationId) {
    return aiPredictions.find(prediction => prediction.application_id === applicationId);
  }
  
  // Função para buscar análise por ID de aplicação
  export function getAnalysisByApplicationId(applicationId) {
    return analyses.find(analysis => analysis.application_id === applicationId);
  }