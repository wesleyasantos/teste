import os
import django
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credito.settings')
django.setup()

# Import management commands to execute migrations programmatically
from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from clients.models import Client, Address
from credit_analysis.models import (
    CreditOperation, CreditAnalysis, Committee, 
    CommitteeMember, Contract, Signature, Installment
)
from credit_analysis.services import create_installments

# Create migrations for all installed apps
print("Creating migrations...")
call_command('makemigrations', 'accounts')
call_command('makemigrations', 'clients')
call_command('makemigrations', 'credit_analysis')
call_command('makemigrations', 'api')
call_command('makemigrations', 'ai_models')
call_command('makemigrations', 'reports')

# Execute migrations
print("Applying migrations...")
call_command('migrate')

User = get_user_model()

def create_superuser():
    """Cria um superuser para acesso administrativo"""
    if not User.objects.filter(username='wesley.sobreira').exists():
        User.objects.create_superuser(
            username='wesley.sobreira',
            email='admin@w2msolucoes.com',
            password='admin123',
            first_name='Wesley ',
            last_name='Sobreira',
            is_analyst=True,
            is_manager=True
        )
        print("Superuser 'wesley.sobreira' criado com senha 'admin123'")
    else:
        print("Superuser 'wesley.sobreira' já existe")

def create_sample_data():
    """Cria dados de exemplo para demonstração"""
    
    # Verificar os campos disponíveis no modelo Client
    client_fields = [field.name for field in Client._meta.get_fields()]
    
    # Criar um cliente pessoa física com os campos disponíveis
    pf_exists = Client.objects.filter(cpf='123.456.789-00').exists() if 'cpf' in client_fields else False
    
    if not pf_exists:
        address = Address.objects.create(
            street='Rua das Flores',
            number='123',
            complement='Apto 45',
            neighborhood='Jardim Primavera',
            city='São Paulo',
            state='SP',
            zip_code='01234-567'
        )
        
        # Dicionário base com os campos que são mais prováveis de existir
        client_data = {
            'name': 'João Silva',
            'email': 'joao.silva@email.com',
            'phone': '(11) 98765-4321',
            'address': address,
        }
        
        # Adicionar campos opcionais apenas se existirem no modelo
        if 'cpf' in client_fields:
            client_data['cpf'] = '123.456.789-00'
        if 'rg' in client_fields:
            client_data['rg'] = '12.345.678-9'
        if 'birth_date' in client_fields:
            client_data['birth_date'] = '1985-05-15'
        if 'type' in client_fields:
            client_data['type'] = 'PF'  # Pessoa Física
        if 'marital_status' in client_fields:
            client_data['marital_status'] = 'married'
        if 'profession' in client_fields:
            client_data['profession'] = 'Engenheiro'
        if 'monthly_income' in client_fields:
            client_data['monthly_income'] = 5000
        
        # Criar o cliente com os campos disponíveis
        Client.objects.create(**client_data)
        print("Cliente PF de exemplo criado")
    
    # Criar um cliente pessoa jurídica se o campo 'cnpj' existir
    pj_exists = Client.objects.filter(cnpj='12.345.678/0001-90').exists() if 'cnpj' in client_fields else False
    
    if not pj_exists and 'cnpj' in client_fields:
        address = Address.objects.create(
            street='Rua Tecnológica',
            number='500',
            complement='10º Andar',
            neighborhood='Vila Olímpia',
            city='São Paulo',
            state='SP',
            zip_code='04551-000'
        )
        
        # Dicionário base com os campos que são mais prováveis de existir
        client_data = {
            'name': 'Tech Solutions Ltda',
            'cnpj': '12.345.678/0001-90',
            'email': 'contato@techsolutions.com',
            'phone': '(11) 3456-7890',
            'address': address,
        }
        
        # Adicionar campos opcionais apenas se existirem no modelo
        if 'type' in client_fields:
            client_data['type'] = 'PJ'  # Pessoa Jurídica
        if 'founding_date' in client_fields:
            client_data['founding_date'] = '2010-08-10'
        if 'business_area' in client_fields:
            client_data['business_area'] = 'Tecnologia'
        if 'annual_revenue' in client_fields:
            client_data['annual_revenue'] = 1500000
        
        # Criar o cliente com os campos disponíveis
        Client.objects.create(**client_data)
        print("Cliente PJ de exemplo criado")
        
    # Chamar a função para criar operações de exemplo
    create_sample_operations()

def create_sample_operations():
    """Cria operações de crédito de exemplo em diferentes estágios"""
    # Verificar se existem clientes
    if Client.objects.count() == 0:
        print("Nenhum cliente encontrado. Não é possível criar operações de exemplo.")
        return
    
    # Obter um cliente para pessoa física
    client_pf = None
    if hasattr(Client, 'cpf'):
        client_pf = Client.objects.filter(cpf='123.456.789-00').first()
    if not client_pf:
        client_pf = Client.objects.first()
    
    # Obter um cliente para pessoa jurídica (ou usar o mesmo cliente se não existir PJ)
    client_pj = None
    if hasattr(Client, 'cnpj'):
        client_pj = Client.objects.filter(cnpj='12.345.678/0001-90').first()
    if not client_pj:
        client_pj = client_pf
    
    # Obter usuário administrador
    admin_user = User.objects.get(username='wesley.sobreira')
    
    # Criar operações em diferentes estágios
    
    # 1. Operação em estágio de verificação
    if not CreditOperation.objects.filter(status='verification').exists():
        op1 = CreditOperation.objects.create(
            client=client_pf,
            amount=8000,
            modality='Capital de Giro',
            term_months=24,
            payment_frequency='monthly',
            interest_rate=1.5,
            interest_frequency='monthly',
            amortization_system='price',
            first_payment_date=timezone.now().date() + timezone.timedelta(days=30),
            purpose='Compra de automóvel',
            status='verification',
            verification_date=timezone.now()
        )
        print(f"Operação de exemplo em verificação criada: #{op1.id}")
    
    # 2. Operação em estágio de análise
    if not CreditOperation.objects.filter(status='analysis').exists():
        op2 = CreditOperation.objects.create(
            client=client_pj,
            amount=150000,
            modality='Financiamento',
            term_months=36,
            payment_frequency='monthly',
            interest_rate=1.2,
            interest_frequency='monthly',
            amortization_system='sac',
            first_payment_date=timezone.now().date() + timezone.timedelta(days=45),
            purpose='Expansão do negócio',
            status='analysis',
            verification_date=timezone.now() - timezone.timedelta(days=2),
            analysis_date=timezone.now()
        )
        
        # Criar parcelas para esta operação
        create_installments(op2)
        
        # Criar análise para esta operação
        try:
            CreditAnalysis.objects.create(
                operation=op2,
                sector='service',
                pgdas_data={str(i): 50000 for i in range(12)},
                financial_expenses={
                    'overdraft': {'name': 'Cheque Especial', 'value': 10000, 'percentage': 7, 'result': 700},
                    'advance': {'name': 'Adiantamento ao Depositante', 'value': 0, 'percentage': 15, 'result': 0}
                },
                short_term_data={
                    'days30': {'name': 'a Vencer até 30 dias', 'value': 20000},
                    'days60': {'name': 'a Vencer de 31 a 60 dias', 'value': 15000}
                },
                future_modality_data={
                    'overdraft': {'name': 'Cheque Especial', 'value': 0},
                    'advance': {'name': 'Adiantamento ao Depositante', 'value': 0}
                },
                pgdas_total=600000,
                sector_expense=420000,
                gross_profit=180000,
                financial_expenses_total=700,
                availability1=14941.67,
                availability2=12108.33,
                surplus=3525.00,
                approved=True,
                analyst=admin_user
            )
        except Exception as e:
            print(f"Erro ao criar análise: {e}")
        
        print(f"Operação de exemplo em análise criada: #{op2.id}")
    
    # 3. Operação em estágio de comitê
    if not CreditOperation.objects.filter(status='committee').exists():
        op3 = CreditOperation.objects.create(
            client=client_pf,
            amount=25000,
            modality='Crédito Pessoal',
            term_months=18,
            payment_frequency='monthly',
            interest_rate=1.8,
            interest_frequency='monthly',
            amortization_system='price',
            first_payment_date=timezone.now().date() + timezone.timedelta(days=30),
            purpose='Pagamento de dívidas',
            status='committee',
            verification_date=timezone.now() - timezone.timedelta(days=5),
            analysis_date=timezone.now() - timezone.timedelta(days=3),
            committee_date=timezone.now()
        )
        
        # Criar parcelas para esta operação
        create_installments(op3)
        
        # Criar comitê para esta operação
        try:
            committee = Committee.objects.create(
                operation=op3,
                status='in_progress',
                started_at=timezone.now()
            )
            
            # Adicionar membro ao comitê
            CommitteeMember.objects.create(
                operation=op3,
                user=admin_user
            )
        except Exception as e:
            print(f"Erro ao criar comitê: {e}")
        
        print(f"Operação de exemplo em comitê criada: #{op3.id}")
    
    # 4. Operação em estágio de formalização
    if not CreditOperation.objects.filter(status='formalization').exists():
        op4 = CreditOperation.objects.create(
            client=client_pj,
            amount=200000,
            modality='Capital de Giro',
            term_months=48,
            payment_frequency='monthly',
            interest_rate=1.3,
            interest_frequency='monthly',
            amortization_system='price',
            first_payment_date=timezone.now().date() + timezone.timedelta(days=30),
            purpose='Compra de equipamentos',
            status='formalization',
            verification_date=timezone.now() - timezone.timedelta(days=10),
            analysis_date=timezone.now() - timezone.timedelta(days=8),
            committee_date=timezone.now() - timezone.timedelta(days=3),
            formalization_date=timezone.now()
        )
        
        # Criar parcelas para esta operação
        create_installments(op4)
        
        # Criar contrato para esta operação
        try:
            contract = Contract.objects.create(
                operation=op4,
                number=f"{timezone.now().year}/{op4.id}",
                status='pending_signature'
            )
            
            # Adicionar assinaturas pendentes
            Signature.objects.create(
                contract=contract,
                name=op4.client.name,
                email=op4.client.email
            )
            
            Signature.objects.create(
                contract=contract,
                name="Representante da Instituição",
                email="representante@instituicao.com"
            )
        except Exception as e:
            print(f"Erro ao criar contrato: {e}")
        
        print(f"Operação de exemplo em formalização criada: #{op4.id}")
    
    # 5. Operação em estágio de monitoramento
    if not CreditOperation.objects.filter(status='monitoring').exists():
        op5 = CreditOperation.objects.create(
            client=client_pf,
            amount=10000,
            modality='Crédito Pessoal',
            term_months=12,
            payment_frequency='monthly',
            interest_rate=1.5,
            interest_frequency='monthly',
            amortization_system='price',
            first_payment_date=timezone.now().date() - timezone.timedelta(days=60),
            purpose='Reforma residencial',
            status='monitoring',
            verification_date=timezone.now() - timezone.timedelta(days=90),
            analysis_date=timezone.now() - timezone.timedelta(days=85),
            committee_date=timezone.now() - timezone.timedelta(days=80),
            formalization_date=timezone.now() - timezone.timedelta(days=70),
            monitoring_date=timezone.now() - timezone.timedelta(days=65)
        )
        
        # Criar parcelas para esta operação
        create_installments(op5)
        
        # Marcar primeiras parcelas como pagas
        try:
            installments = Installment.objects.filter(operation=op5).order_by('number')[:2]
            for installment in installments:
                installment.status = 'paid'
                installment.payment_date = installment.due_date
                installment.payment_amount = installment.amount
                installment.save()
        except Exception as e:
            print(f"Erro ao marcar parcelas como pagas: {e}")
        
        print(f"Operação de exemplo em monitoramento criada: #{op5.id}")

if __name__ == "__main__":
    with transaction.atomic():
        create_superuser()
        create_sample_data()
    
    print("Inicialização concluída com sucesso!")