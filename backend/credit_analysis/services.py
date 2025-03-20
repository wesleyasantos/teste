"""
Serviços para cálculos financeiros e análise de crédito
"""
from decimal import Decimal
import datetime
from django.utils import timezone
from .models import CreditOperation, Installment

def calculate_price_installments(operation):
    """
    Calcula as parcelas usando o sistema Price (parcelas fixas)
    
    Args:
        operation: Instância de CreditOperation
    
    Returns:
        tuple: (valor da parcela fixa, lista de dicionários com detalhes das parcelas)
    """
    principal = Decimal(operation.amount)
    term = int(operation.term_months)
    
    # Converter taxa de juros para decimal mensal
    rate = Decimal(operation.interest_rate) / 100
    if operation.interest_frequency == 'annually':
        rate = (Decimal('1') + rate) ** (Decimal('1') / 12) - Decimal('1')
    
    # Cálculo da parcela fixa (fórmula Price)
    factor = (rate * (1 + rate) ** term) / ((1 + rate) ** term - 1)
    installment_amount = principal * factor
    
    # Gerar plano de pagamento
    installments_data = []
    balance = principal
    current_date = operation.first_payment_date
    
    for i in range(1, term + 1):
        interest = balance * rate
        principal_payment = installment_amount - interest
        balance -= principal_payment
        
        # Ajustar saldo para evitar inconsistências por arredondamento
        if i == term:
            principal_payment += balance
            balance = Decimal('0')
        
        # Determinar status da parcela
        today = timezone.now().date()
        if current_date < today:
            status = 'overdue'
        elif (current_date - today).days <= 30:
            status = 'pending'
        else:
            status = 'future'
        
        installments_data.append({
            'number': i,
            'due_date': current_date,
            'amount': installment_amount,
            'principal': principal_payment,
            'interest': interest,
            'balance': balance,
            'status': status,
        })
        
        # Avançar para o próximo mês
        month = current_date.month + 1
        year = current_date.year
        if month > 12:
            month = 1
            year += 1
        day = min(current_date.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
        current_date = datetime.date(year, month, day)
    
    return installment_amount, installments_data


def calculate_sac_installments(operation):
    """
    Calcula as parcelas usando o sistema SAC (amortização constante)
    
    Args:
        operation: Instância de CreditOperation
    
    Returns:
        tuple: (valor da primeira parcela, lista de dicionários com detalhes das parcelas)
    """
    principal = Decimal(operation.amount)
    term = int(operation.term_months)
    
    # Converter taxa de juros para decimal mensal
    rate = Decimal(operation.interest_rate) / 100
    if operation.interest_frequency == 'annually':
        rate = (Decimal('1') + rate) ** (Decimal('1') / 12) - Decimal('1')
    
    # Cálculo da amortização constante
    amortization = principal / term
    
    # Gerar plano de pagamento
    installments_data = []
    balance = principal
    current_date = operation.first_payment_date
    
    for i in range(1, term + 1):
        interest = balance * rate
        installment_amount = amortization + interest
        balance -= amortization
        
        # Ajustar saldo para evitar inconsistências por arredondamento
        if i == term:
            balance = Decimal('0')
        
        # Determinar status da parcela
        today = timezone.now().date()
        if current_date < today:
            status = 'overdue'
        elif (current_date - today).days <= 30:
            status = 'pending'
        else:
            status = 'future'
        
        installments_data.append({
            'number': i,
            'due_date': current_date,
            'amount': installment_amount,
            'principal': amortization,
            'interest': interest,
            'balance': balance,
            'status': status,
        })
        
        # Avançar para o próximo mês
        month = current_date.month + 1
        year = current_date.year
        if month > 12:
            month = 1
            year += 1
        day = min(current_date.day, [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
        current_date = datetime.date(year, month, day)
    
    # Retornar o valor da primeira parcela e todas as parcelas
    return installments_data[0]['amount'], installments_data


def calculate_installments(operation):
    """
    Calcula as parcelas baseado no sistema de amortização escolhido
    
    Args:
        operation: Instância de CreditOperation
    
    Returns:
        tuple: (valor da primeira parcela, lista de dicionários com detalhes das parcelas)
    """
    if operation.amortization_system == 'sac':
        return calculate_sac_installments(operation)
    else:  # price é o padrão
        return calculate_price_installments(operation)


def create_installments(operation):
    """
    Cria as parcelas para uma operação de crédito
    
    Args:
        operation: Instância de CreditOperation
        
    Returns:
        Decimal: Valor da primeira parcela
    """
    # Excluir parcelas existentes, se houver
    operation.installments.all().delete()
    
    # Calcular parcelas com base no sistema de amortização
    first_installment, installments_data = calculate_installments(operation)
    
    # Criar parcelas no banco
    for data in installments_data:
        Installment.objects.create(
            operation=operation,
            number=data['number'],
            due_date=data['due_date'],
            amount=data['amount'],
            principal=data['principal'],
            interest=data['interest'],
            balance=data['balance'],
            status=data['status']
        )
    
    return first_installment


def create_payment_plan(operation):
    """
    Cria o plano de pagamento para uma operação e
    adiciona um método à operação para calcular o valor da parcela mensal
    
    Args:
        operation: Instância de CreditOperation
    """
    first_installment = create_installments(operation)
    
    # Adicionar método para obter valor mensal da parcela
    operation.calculate_monthly_payment = lambda: first_installment
    
    return first_installment

def calculate_sector_expense(pgdas_total, sector):
    """Calcula a despesa setorial com base no setor"""
    sector_percentages = {
        'commerce': 75,
        'service': 70,
        'transport': 85,
        'industry': 90
    }
    percentage = sector_percentages.get(sector, 75)
    return pgdas_total * percentage / 100

def calculate_analysis_results(analysis_data):
    """Calcula todos os resultados da análise de crédito"""
    results = {}
    
    # Calcula PGDAS total
    pgdas_values = [float(val) for val in analysis_data.get('pgdas_data', {}).values()]
    results['pgdas_total'] = sum(pgdas_values)
    
    # Calcula despesa setorial
    results['sector_expense'] = calculate_sector_expense(
        results['pgdas_total'], 
        analysis_data.get('sector', 'commerce')
    )
    
    # Calcula lucro bruto
    results['gross_profit'] = results['pgdas_total'] - results['sector_expense']
    
    # Calcula despesas financeiras
    financial_expenses_total = 0
    for key, data in analysis_data.get('financial_expenses', {}).items():
        value = float(data.get('value', 0))
        percentage = float(data.get('percentage', 0))
        result = value * percentage / 100
        financial_expenses_total += result
    
    results['financial_expenses_total'] = financial_expenses_total
    
    # Calcula disponibilidade mensal 1
    results['availability1'] = (results['gross_profit'] - results['financial_expenses_total']) / 12
    
    # Calcula reposição mensal
    short_term_values = [float(data.get('value', 0)) for data in analysis_data.get('short_term_data', {}).values()]
    future_modality_values = [float(data.get('value', 0)) for data in analysis_data.get('future_modality_data', {}).values()]
    
    results['short_term_total'] = sum(short_term_values)
    results['future_modality_total'] = sum(future_modality_values)
    results['monthly_repayment'] = max(0, (results['short_term_total'] - results['future_modality_total']) / 12)
    
    # Calcula disponibilidade mensal 2
    results['availability2'] = results['availability1'] - results['monthly_repayment']
    
    # Calcula superávit/déficit
    monthly_payment = analysis_data.get('monthly_payment', 0)
    results['surplus'] = results['availability2'] - monthly_payment
    
    # Determina se está aprovado
    results['approved'] = results['surplus'] >= 0
    
    return results