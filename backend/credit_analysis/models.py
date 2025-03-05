from django.db import models
from django.conf import settings
from clients.models import Client

class CreditApplication(models.Model):
    """
    Modelo para solicitações de crédito.
    """
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('in_analysis', 'Em Análise'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
        ('cancelled', 'Cancelado'),
    ]
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='credit_applications', verbose_name="Cliente")
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Solicitado")
    purpose = models.CharField(max_length=255, verbose_name="Finalidade")
    term_months = models.IntegerField(verbose_name="Prazo em Meses")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Taxa de Juros (%)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Solicitação de Crédito"
        verbose_name_plural = "Solicitações de Crédito"
        ordering = ['-created_at']

    def __str__(self):
        return f"Solicitação {self.id} - {self.client.name} - R$ {self.amount_requested}"


class CreditScore(models.Model):
    """
    Modelo para pontuação de crédito dos clientes.
    """
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='credit_score', verbose_name="Cliente")
    score = models.IntegerField(verbose_name="Pontuação")
    payment_history = models.IntegerField(verbose_name="Histórico de Pagamento")  # Pontuação componente
    debt_burden = models.IntegerField(verbose_name="Carga de Dívida")  # Pontuação componente
    length_history = models.IntegerField(verbose_name="Tempo de Histórico")  # Pontuação componente
    last_calculated = models.DateTimeField(auto_now=True, verbose_name="Último Cálculo")

    class Meta:
        verbose_name = "Score de Crédito"
        verbose_name_plural = "Scores de Crédito"
        ordering = ['-last_calculated']

    def __str__(self):
        return f"Score {self.score} - {self.client.name}"


class Analysis(models.Model):
    """
    Modelo para análises de crédito realizadas por analistas.
    """
    DECISION_CHOICES = [
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
        ('need_info', 'Necessita Informações Adicionais'),
    ]
    
    application = models.ForeignKey(CreditApplication, on_delete=models.CASCADE, related_name='analyses', verbose_name="Solicitação")
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='analyses', verbose_name="Analista")
    decision = models.CharField(max_length=20, choices=DECISION_CHOICES, default='pending', verbose_name="Decisão")
    notes = models.TextField(blank=True, null=True, verbose_name="Observações")
    ai_recommendation = models.TextField(blank=True, null=True, verbose_name="Recomendação da IA")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        verbose_name = "Análise"
        verbose_name_plural = "Análises"
        ordering = ['-created_at']

    def __str__(self):
        return f"Análise {self.id} - {self.get_decision_display()} - {self.application.client.name}"