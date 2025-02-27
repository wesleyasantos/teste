from django.contrib import admin
from .models import AIPrediction

@admin.register(AIPrediction)
class AIPredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'application', 'risk_score', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('client__name', 'client__cpf')
    readonly_fields = ('risk_score', 'default_probability', 'recommendation', 'explanation', 'created_at')