from django.contrib import admin
from .models import CreditApplication, CreditScore, Analysis

@admin.register(CreditApplication)
class CreditApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'amount_requested', 'term_months', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('client__name', 'client__cpf')

@admin.register(CreditScore)
class CreditScoreAdmin(admin.ModelAdmin):
    list_display = ('client', 'score', 'payment_history', 'debt_burden', 'last_calculated')
    search_fields = ('client__name', 'client__cpf')

@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ('id', 'application', 'analyst', 'decision', 'created_at')
    list_filter = ('decision', 'created_at')
    search_fields = ('application__client__name', 'analyst__username')