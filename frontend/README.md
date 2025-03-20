# Sistema de Análise de Crédito

Sistema completo para análise de crédito com cadastro de clientes, gerenciamento de análises e recomendações utilizando IA.

## Funcionalidades

- Cadastro e gerenciamento de clientes
- Upload e visualização de documentos
- Cadastro e acompanhamento de solicitações de crédito
- Análise de crédito com recomendações baseadas em IA
- Dashboards e relatórios
- Diferentes níveis de acesso (analistas e gerentes)

## Tecnologias Utilizadas

### Backend
- Django (Python)
- Django REST Framework (API REST)
- SQLite3 (Banco de dados para desenvolvimento)
- Scikit-learn (Modelos de IA)

### Frontend
- Vue.js
- Vite
- Chart.js (para gráficos e visualizações)
- Axios (comunicação com a API)

## Estrutura do Projeto

```
credito/                       # Pasta raiz do projeto
│
├── backend/                   # Aplicação Django
│   ├── credito/               # Configurações do projeto Django
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── api/                   # App para API REST
│   ├── accounts/              # App para gerenciamento de usuários
│   ├── clients/               # App para cadastro de clientes
│   ├── credit_analysis/       # App para análise de crédito
│   ├── reports/               # App para relatórios
│   └── ai_models/             # App para modelos de IA
│
└── frontend/                  # Aplicação Vue.js
    ├── src/
    │   ├── assets/
    │   ├── components/
    │   ├── views/
    │   ├── router/
    │   ├── store/
    │   └── services/          # Serviços para comunicação com a API
    └── public/
```

## Instalação e Configuração

### Requisitos
- Python 3.8+ 
- Node.js 16+ e npm
- Git

### Configuração do Backend

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/sistema-credito.git
cd sistema-credito
```

2. Crie e ative um ambiente virtual Python:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências do backend:
```bash
pip install -r requirements.txt
```

4. Configure o banco de dados:
```bash
cd backend
python manage.py migrate
```

5. Crie um superusuário:
```bash
python manage.py createsuperuser
```

6. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

O backend estará rodando em `http://localhost:8000/`.

### Configuração do Frontend

1. Em um novo terminal, navegue até a pasta do frontend:
```bash
cd frontend
```

2. Instale as dependências:
```bash
npm install
```

3. Inicie o servidor de desenvolvimento:
```bash
npm run dev
```

O frontend estará rodando em `http://localhost:5173/`.

## Fluxo de Uso

1. **Cadastro de Cliente**:
   - Adicione um novo cliente com seus dados pessoais
   - Faça upload dos documentos necessários (comprovantes de renda, etc.)

2. **Solicitação de Crédito**:
   - Crie uma nova solicitação para o cliente
   - Defina o valor, prazo e finalidade

3. **Análise de Crédito**:
   - O sistema de IA gera automaticamente uma recomendação
   - O analista de crédito revisa os dados e toma a decisão final

4. **Conclusão do Processo**:
   - Aprovação ou rejeição da solicitação
   - Geração de documentação necessária

## Desenvolvimento

### Backend
Para adicionar um novo modelo ao Django:
1. Adicione a classe no arquivo `models.py` da app correspondente
2. Gere as migrações: `python manage.py makemigrations`
3. Aplique as migrações: `python manage.py migrate`

### Frontend
Para adicionar uma nova tela:
1. Crie o componente Vue no diretório `views/`
2. Adicione a rota no arquivo `router/index.js`
3. Atualize o menu de navegação se necessário

## Implantação em Produção

Para implantar em produção, algumas modificações são necessárias:

1. Configurar um banco de dados mais robusto (PostgreSQL ou MySQL)
2. Configurar ambiente seguro (variáveis de ambiente para credenciais)
3. Configurar servidor web (Nginx ou Apache)
4. Configurar WSGI para Django (Gunicorn ou uWSGI)
5. Construir os arquivos estáticos do frontend e servir através do servidor web

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.








Passo a passo:
python manage.py makemigrations accounts clients credit_analysis api ai_models reports

python manage.py migrate

python initialize_db.py

