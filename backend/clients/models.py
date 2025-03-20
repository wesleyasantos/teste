from django.db import models

class Address(models.Model):
    """
    Modelo para endereços de clientes.
    """
    street = models.CharField(max_length=255, verbose_name="Rua")
    number = models.CharField(max_length=20, verbose_name="Número")
    complement = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    neighborhood = models.CharField(max_length=100, verbose_name="Bairro")
    city = models.CharField(max_length=100, verbose_name="Cidade")
    state = models.CharField(max_length=2, verbose_name="Estado")
    zip_code = models.CharField(max_length=10, verbose_name="CEP")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.street}, {self.number} - {self.city}/{self.state}"


class Client(models.Model):
    """
    Modelo para clientes do sistema de crédito.
    """
    name = models.CharField(max_length=255, verbose_name="Nome")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    rg = models.CharField(max_length=20, blank=True, null=True, verbose_name="RG")
    birth_date = models.DateField(verbose_name="Data de Nascimento")
    phone = models.CharField(max_length=20, verbose_name="Telefone")
    email = models.EmailField(verbose_name="E-mail")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name="Endereço")
    profession = models.CharField(max_length=100, verbose_name="Profissão")
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Renda Mensal")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.cpf}"


class FinancialDocument(models.Model):
    """
    Modelo para documentos financeiros dos clientes.
    """
    DOCUMENT_TYPES = [
        ('income', 'Comprovante de Renda'),
        ('bank_statement', 'Extrato Bancário'),
        ('tax_return', 'Declaração de Imposto de Renda'),
        ('other', 'Outro'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='documents', verbose_name="Cliente")
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, verbose_name="Tipo de Documento")
    file = models.FileField(upload_to='documents/', verbose_name="Arquivo")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Enviado em")

    class Meta:
        verbose_name = "Documento Financeiro"
        verbose_name_plural = "Documentos Financeiros"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.client.name}"