from django.db import models
from credit_analysis.models import CreditOperation

class AIPrediction(models.Model):
    """
    Modelo para predições de IA para solicitações de crédito.
    """
    operation = models.ForeignKey(CreditOperation, on_delete=models.CASCADE, related_name='ai_predictions', verbose_name="Operação")
    risk_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Score de Risco")
    default_probability = models.DecimalField(max_digits=5, decimal_places=3, verbose_name="Probabilidade de Default")
    recommendation = models.CharField(max_length=255, verbose_name="Recomendação")
    explanation = models.TextField(verbose_name="Explicação")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Predição de IA"
        verbose_name_plural = "Predições de IA"
    
    def __str__(self):
        return f"Predição de IA para Operação {self.operation.id}"