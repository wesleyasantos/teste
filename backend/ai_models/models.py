from django.db import models
from clients.models import Client
from credit_analysis.models import CreditApplication

class AIPrediction(models.Model):
    """
    Modelo para armazenar predições geradas pelo sistema de IA.
    """
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='predictions', verbose_name="Cliente")
    application = models.ForeignKey(CreditApplication, on_delete=models.CASCADE, related_name='predictions', verbose_name="Solicitação")
    risk_score = models.FloatField(verbose_name="Score de Risco")
    default_probability = models.FloatField(verbose_name="Probabilidade de Inadimplência")
    recommendation = models.TextField(verbose_name="Recomendação")
    explanation = models.TextField(verbose_name="Explicação")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Predição de IA"
        verbose_name_plural = "Predições de IA"
        ordering = ['-created_at']

    def __str__(self):
        return f"Predição {self.id} - Score {self.risk_score:.2f} - {self.client.name}"