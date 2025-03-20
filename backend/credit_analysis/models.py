from django.db import models
from django.conf import settings
from clients.models import Client

# Status das operações
OPERATION_STATUS_CHOICES = [
    ('pending', 'Cadastro Pendente'),
    ('verification', 'Em Conferência'),
    ('analysis', 'Em Análise'),
    ('committee', 'Em Comitê'),
    ('formalization', 'Em Formalização'),
    ('monitoring', 'Em Acompanhamento'),
    ('approved', 'Aprovado'),
    ('rejected', 'Reprovado'),
    ('cancelled', 'Cancelado'),
]

# Sistemas de amortização
AMORTIZATION_SYSTEM_CHOICES = [
    ('price', 'PRICE (Parcelas Fixas)'),
    ('sac', 'SAC (Amortização Constante)'),
    ('pricemix', 'PRICEMIX (Sistema Misto)'),
]

# Periodicidades
FREQUENCY_CHOICES = [
    ('monthly', 'Mensal'),
    ('quarterly', 'Trimestral'),
    ('semiannually', 'Semestral'),
    ('annually', 'Anual'),
]

# Índices de indexação
INDEXATION_CHOICES = [
    ('', 'Sem Indexação'),
    ('cdi', 'CDI'),
    ('selic', 'SELIC'),
    ('fixed', 'Custo Fixo'),
    ('tlp', 'TLP'),
]

class CreditOperation(models.Model):
    """
    Modelo para operações de crédito que passam pelo fluxo completo.
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='operations', verbose_name="Cliente")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor do Crédito")
    modality = models.CharField(max_length=100, verbose_name="Modalidade do Crédito")
    term_months = models.IntegerField(verbose_name="Prazo em Meses")
    payment_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='monthly', verbose_name="Periodicidade das Parcelas")
    interest_rate = models.DecimalField(max_digits=6, decimal_places=3, verbose_name="Taxa de Juros")
    interest_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='monthly', verbose_name="Periodicidade da Taxa")
    grace_period = models.IntegerField(default=0, verbose_name="Carência em Meses")
    grace_frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='monthly', verbose_name="Periodicidade da Carência")
    amortization_system = models.CharField(max_length=20, choices=AMORTIZATION_SYSTEM_CHOICES, default='price', verbose_name="Sistema de Amortização")
    first_payment_date = models.DateField(verbose_name="Data da Primeira Parcela")
    indexation = models.CharField(max_length=20, choices=INDEXATION_CHOICES, blank=True, null=True, verbose_name="Índice de Indexação")
    index_value = models.DecimalField(max_digits=6, decimal_places=3, default=0, verbose_name="Valor do Índice (%)")
    purpose = models.TextField(blank=True, null=True, verbose_name="Finalidade")
    observations = models.TextField(blank=True, null=True, verbose_name="Observações")
    status = models.CharField(max_length=20, choices=OPERATION_STATUS_CHOICES, default='pending', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    # Campos de datas para cada etapa (auditoria)
    pending_date = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    verification_date = models.DateTimeField(null=True, blank=True, verbose_name="Data de Conferência")
    analysis_date = models.DateTimeField(null=True, blank=True, verbose_name="Data de Análise")
    committee_date = models.DateTimeField(null=True, blank=True, verbose_name="Data de Comitê")
    formalization_date = models.DateTimeField(null=True, blank=True, verbose_name="Data de Formalização")
    monitoring_date = models.DateTimeField(null=True, blank=True, verbose_name="Data de Acompanhamento")
    
    class Meta:
        verbose_name = "Operação de Crédito"
        verbose_name_plural = "Operações de Crédito"
        ordering = ['-created_at']

    def __str__(self):
        return f"Operação {self.id} - {self.client.name} - R$ {self.amount}"

    def update_status(self, new_status):
        """Atualiza o status da operação e registra a data"""
        self.status = new_status
        
        # Atualizar a data correspondente ao novo status
        if new_status == 'verification':
            self.verification_date = timezone.now()
        elif new_status == 'analysis':
            self.analysis_date = timezone.now()
        elif new_status == 'committee':
            self.committee_date = timezone.now()
        elif new_status == 'formalization':
            self.formalization_date = timezone.now()
        elif new_status == 'monitoring':
            self.monitoring_date = timezone.now()
            
        self.save()


class Partner(models.Model):
    """
    Modelo para sócios de uma operação de crédito.
    """
    operation = models.ForeignKey(CreditOperation, on_delete=models.CASCADE, related_name='partners', verbose_name="Operação")
    name = models.CharField(max_length=255, verbose_name="Nome")
    role = models.CharField(max_length=100, verbose_name="Cargo")
    document = models.CharField(max_length=20, verbose_name="CPF")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Telefone")
    share = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Participação (%)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Sócio"
        verbose_name_plural = "Sócios"
        
    def __str__(self):
        return f"{self.name} - {self.operation.id}"


class Guarantee(models.Model):
    """
    Modelo para garantias de uma operação de crédito.
    """
    GUARANTEE_TYPE_CHOICES = [
        ('property', 'Imóvel'),
        ('vehicle', 'Veículo'),
        ('equipment', 'Equipamento'),
        ('financial', 'Aplicação Financeira'),
        ('endorsement', 'Aval/Fiança'),
        ('other', 'Outra'),
    ]
    
    operation = models.ForeignKey(CreditOperation, on_delete=models.CASCADE, related_name='guarantees', verbose_name="Operação")
    type = models.CharField(max_length=20, choices=GUARANTEE_TYPE_CHOICES, verbose_name="Tipo de Garantia")
    value = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor")
    description = models.CharField(max_length=255, verbose_name="Descrição")
    registration_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Número de Registro")
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Localização")
    notes = models.TextField(blank=True, null=True, verbose_name="Observações")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Garantia"
        verbose_name_plural = "Garantias"
        
    def __str__(self):
        return f"{self.get_type_display()} - {self.description}"


class OperationDocument(models.Model):
    """
    Modelo para documentos de uma operação de crédito.
    """
    DOCUMENT_TYPE_CHOICES = [
        ('authorization', 'Termo de Autorização'),
        ('id', 'Documento de Identificação'),
        ('income', 'Comprovante de Renda'),
        ('residence', 'Comprovante de Residência'),
        ('bank_statement', 'Extrato Bancário'),
        ('tax_return', 'Declaração de IR'),
        ('business', 'Documentos Empresariais'),
        ('contract', 'Contrato'),
        ('other', 'Outro'),
    ]
    
    operation = models.ForeignKey(CreditOperation, on_delete=models.CASCADE, related_name='documents', verbose_name="Operação")
    type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES, verbose_name="Tipo de Documento")
    name = models.CharField(max_length=255, verbose_name="Nome do Documento")
    file = models.FileField(upload_to='operation_documents/', verbose_name="Arquivo")
    notes = models.TextField(blank=True, null=True, verbose_name="Observações")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Enviado em")
    
    class Meta:
        verbose_name = "Documento da Operação"
        verbose_name_plural = "Documentos da Operação"
        
    def __str__(self):
        return f"{self.name} - {self.operation.id}"


class CreditAnalysis(models.Model):
    """
    Modelo para análise de crédito de uma operação.
    """
    SECTOR_CHOICES = [
        ('commerce', 'Comércio (75%)'),
        ('service', 'Serviço (70%)'),
        ('transport', 'Transporte (85%)'),
        ('industry', 'Indústria/Posto de Combustível (90%)'),
    ]
    
    operation = models.OneToOneField(CreditOperation, on_delete=models.CASCADE, related_name='analysis', verbose_name="Operação")
    sector = models.CharField(max_length=20, choices=SECTOR_CHOICES, default='commerce', verbose_name="Setor")
    pgdas_data = models.JSONField(default=dict, verbose_name="Dados do PGDAS")
    financial_expenses = models.JSONField(default=dict, verbose_name="Despesas Financeiras")
    short_term_data = models.JSONField(default=dict, verbose_name="Curto Prazo")
    future_modality_data = models.JSONField(default=dict, verbose_name="Modalidade Futuro")
    
    # Resultados calculados
    pgdas_total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total PGDAS")
    financial_expenses_total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total Despesas Financeiras")
    short_term_total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total Curto Prazo")
    future_modality_total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Total Modalidade Futuro")
    monthly_repayment = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Reposição Mensal")
    sector_expense = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Despesa Setorial")
    gross_profit = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Lucro Bruto")
    availability1 = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Disponibilidade Mensal 1")
    availability2 = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Disponibilidade Mensal 2")
    surplus = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Superávit/Déficit")
    
    approved = models.BooleanField(null=True, blank=True, verbose_name="Aprovado")
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='analyses', verbose_name="Analista")
    notes = models.TextField(blank=True, null=True, verbose_name="Observações")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    class Meta:
        verbose_name = "Análise de Crédito"
        verbose_name_plural = "Análises de Crédito"
        
    def __str__(self):
        return f"Análise da Operação {self.operation.id}"
    
    def calculate_results(self):
        """Executa todos os cálculos da análise"""
        # Calcular totais
        self.calculate_pgdas_total()
        self.calculate_financial_expenses()
        self.calculate_short_term_total()
        self.calculate_future_modality_total()
        self.calculate_monthly_repayment()
        
        # Calcular resultados finais
        self.calculate_sector_expense()
        self.calculate_gross_profit()
        self.calculate_availability1()
        self.calculate_availability2()
        self.calculate_surplus()
        
        # Determinar aprovação
        self.approved = self.surplus >= 0
        
        self.save()
    
    def calculate_pgdas_total(self):
        """Calcula o total do PGDAS"""
        pgdas_values = [float(value) for value in self.pgdas_data.values()]
        self.pgdas_total = sum(pgdas_values)
        
    def calculate_financial_expenses(self):
        """Calcula o total das despesas financeiras"""
        total = 0
        for key, data in self.financial_expenses.items():
            value = float(data.get('value', 0))
            percentage = float(data.get('percentage', 0))
            result = value * percentage / 100
            self.financial_expenses[key]['result'] = result
            total += result
        
        self.financial_expenses_total = total
        
    def calculate_short_term_total(self):
        """Calcula o total do curto prazo"""
        values = [float(data.get('value', 0)) for data in self.short_term_data.values()]
        self.short_term_total = sum(values)
        
    def calculate_future_modality_total(self):
        """Calcula o total da modalidade futuro"""
        values = [float(data.get('value', 0)) for data in self.future_modality_data.values()]
        self.future_modality_total = sum(values)
        
    def calculate_monthly_repayment(self):
        """Calcula a reposição mensal"""
        self.monthly_repayment = max(0, (self.short_term_total - self.future_modality_total) / 12)
        
    def calculate_sector_expense(self):
        """Calcula a despesa setorial"""
        sector_percentages = {
            'commerce': 75,
            'service': 70,
            'transport': 85,
            'industry': 90
        }
        percentage = sector_percentages.get(self.sector, 75)
        self.sector_expense = self.pgdas_total * percentage / 100
        
    def calculate_gross_profit(self):
        """Calcula o lucro bruto"""
        self.gross_profit = self.pgdas_total - self.sector_expense
        
    def calculate_availability1(self):
        """Calcula a disponibilidade mensal 1"""
        self.availability1 = (self.gross_profit - self.financial_expenses_total) / 12
        
    def calculate_availability2(self):
        """Calcula a disponibilidade mensal 2"""
        self.availability2 = self.availability1 - self.monthly_repayment
        
    def calculate_surplus(self):
        """Calcula o superávit ou déficit"""
        # Obter a parcela mensal da operação
        # Isso depende de como você está calculando o valor da parcela,
        # aqui estamos usando um método que você precisa implementar na operação
        monthly_payment = self.operation.calculate_monthly_payment()
        self.surplus = self.availability2 - monthly_payment


class AIAnalysis(models.Model):
    """
    Modelo para análise de IA de uma operação.
    """
    operation = models.OneToOneField(CreditOperation, on_delete=models.CASCADE, related_name='ai_analysis', verbose_name="Operação")
    risk_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Score de Risco")
    default_probability = models.DecimalField(max_digits=5, decimal_places=3, verbose_name="Probabilidade de Default")
    recommendation = models.CharField(max_length=255, verbose_name="Recomendação")
    explanation = models.TextField(verbose_name="Explicação")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Análise de IA"
        verbose_name_plural = "Análises de IA"
        
    def __str__(self):
        return f"Análise de IA da Operação {self.operation.id}"


class CommitteeMember(models.Model):
    """
    Modelo para membros de comitê de uma operação.
    """
    operation = models.ForeignKey(CreditOperation, on_delete=models.CASCADE, related_name='committee_members', verbose_name="Operação")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='committee_participations', verbose_name="Usuário")
    vote = models.CharField(max_length=10, choices=[('approve', 'Aprovar'), ('reject', 'Reprovar')], null=True, blank=True, verbose_name="Voto")
    notes = models.TextField(blank=True, null=True, verbose_name="Observações")
    voted_at = models.DateTimeField(null=True, blank=True, verbose_name="Data do Voto")
    
    class Meta:
        verbose_name = "Membro de Comitê"
        verbose_name_plural = "Membros de Comitê"
        
    def __str__(self):
        return f"{self.user.get_full_name()} - Operação {self.operation.id}"


class Committee(models.Model):
    """
    Modelo para comitê de uma operação.
    """
    operation = models.OneToOneField(CreditOperation, on_delete=models.CASCADE, related_name='committee', verbose_name="Operação")
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pendente'), 
        ('in_progress', 'Em Andamento'), 
        ('completed', 'Concluído')
    ], default='pending', verbose_name="Status")
    decision = models.CharField(max_length=10, choices=[
        ('approved', 'Aprovado'), 
        ('rejected', 'Reprovado')
    ], null=True, blank=True, verbose_name="Decisão")
    started_at = models.DateTimeField(null=True, blank=True, verbose_name="Iniciado em")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Concluído em")
    
    class Meta:
        verbose_name = "Comitê"
        verbose_name_plural = "Comitês"
        
    def __str__(self):
        return f"Comitê da Operação {self.operation.id}"


class Contract(models.Model):
    """
    Modelo para contrato de uma operação.
    """
    operation = models.OneToOneField(CreditOperation, on_delete=models.CASCADE, related_name='contract', verbose_name="Operação")
    number = models.CharField(max_length=50, verbose_name="Número do Contrato")
    status = models.CharField(max_length=20, choices=[
        ('pending_signature', 'Aguardando Assinaturas'), 
        ('signed', 'Assinado'), 
        ('cancelled', 'Cancelado')
    ], default='pending_signature', verbose_name="Status")
    file = models.FileField(upload_to='contracts/', verbose_name="Arquivo do Contrato")
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name="Gerado em")
    
    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
        
    def __str__(self):
        return f"Contrato {self.number} - Operação {self.operation.id}"


class Signature(models.Model):
    """
    Modelo para assinaturas de um contrato.
    """
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='signatures', verbose_name="Contrato")
    name = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField(verbose_name="Email")
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pendente'), 
        ('signed', 'Assinado'), 
        ('refused', 'Recusado')
    ], default='pending', verbose_name="Status")
    signed_at = models.DateTimeField(null=True, blank=True, verbose_name="Assinado em")
    
    class Meta:
        verbose_name = "Assinatura"
        verbose_name_plural = "Assinaturas"
        
    def __str__(self):
        return f"Assinatura de {self.name} - Contrato {self.contract.number}"


class Installment(models.Model):
    """
    Modelo para parcelas de uma operação.
    """
    operation = models.ForeignKey(CreditOperation, on_delete=models.CASCADE, related_name='installments', verbose_name="Operação")
    number = models.IntegerField(verbose_name="Número da Parcela")
    due_date = models.DateField(verbose_name="Data de Vencimento")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor da Parcela")
    principal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor Principal")
    interest = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Juros")
    balance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Saldo Devedor")
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pendente'), 
        ('paid', 'Pago'), 
        ('overdue', 'Em Atraso'), 
        ('future', 'A Vencer')
    ], default='future', verbose_name="Status")
    payment_date = models.DateField(null=True, blank=True, verbose_name="Data do Pagamento")
    payment_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Valor Pago")
    
    class Meta:
        verbose_name = "Parcela"
        verbose_name_plural = "Parcelas"
        ordering = ['number']
        
    def __str__(self):
        return f"Parcela {self.number} - Operação {self.operation.id}"