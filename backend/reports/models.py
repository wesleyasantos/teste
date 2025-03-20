from django.db import models
from django.conf import settings

class Report(models.Model):
    """
    Modelo para relatórios gerados no sistema.
    """
    REPORT_TYPES = [
        ('monthly', 'Relatório Mensal'),
        ('client', 'Relatório de Cliente'),
        ('performance', 'Desempenho de Analistas'),
        ('risk', 'Análise de Risco'),
        ('custom', 'Relatório Personalizado'),
    ]
    
    title = models.CharField(max_length=255, verbose_name="Título")
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES, verbose_name="Tipo de Relatório")
    parameters = models.JSONField(blank=True, null=True, verbose_name="Parâmetros")
    file = models.FileField(upload_to='reports/', blank=True, null=True, verbose_name="Arquivo")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports', verbose_name="Criado por")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    class Meta:
        verbose_name = "Relatório"
        verbose_name_plural = "Relatórios"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.get_report_type_display()}"