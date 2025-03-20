from django.contrib import admin
from .models import AIPrediction

@admin.register(AIPrediction)
class AIPredictionAdmin(admin.ModelAdmin):
    list_display = ('operation', 'risk_score', 'recommendation', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('operation__client__name', 'recommendation')