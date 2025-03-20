from django.contrib import admin
from .models import Client, Address, FinancialDocument

class FinancialDocumentInline(admin.TabularInline):
    model = FinancialDocument
    extra = 1

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('street', 'number', 'neighborhood', 'city', 'state', 'zip_code')
    search_fields = ('street', 'city', 'zip_code')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'email', 'phone', 'monthly_income', 'created_at')
    search_fields = ('name', 'cpf', 'email')
    list_filter = ('created_at',)
    inlines = [FinancialDocumentInline]

@admin.register(FinancialDocument)
class FinancialDocumentAdmin(admin.ModelAdmin):
    list_display = ('client', 'document_type', 'description', 'uploaded_at')
    list_filter = ('document_type', 'uploaded_at')
    search_fields = ('client__name', 'description')