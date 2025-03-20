from django.contrib import admin
from .models import (
    CreditOperation, Partner, Guarantee, OperationDocument, 
    CreditAnalysis, Committee, CommitteeMember, Contract, 
    Signature, Installment
)

@admin.register(CreditOperation)
class CreditOperationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'amount', 'modality', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('client__name', 'client__cpf', 'client__cnpj')

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'operation', 'role', 'share')
    list_filter = ('role',)
    search_fields = ('name', 'document', 'email')

@admin.register(Guarantee)
class GuaranteeAdmin(admin.ModelAdmin):
    list_display = ('description', 'operation', 'type', 'value')
    list_filter = ('type',)
    search_fields = ('description', 'operation__client__name')

@admin.register(OperationDocument)
class OperationDocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'operation', 'type', 'uploaded_at')
    list_filter = ('type', 'uploaded_at')
    search_fields = ('name', 'operation__client__name')

@admin.register(CreditAnalysis)
class CreditAnalysisAdmin(admin.ModelAdmin):
    list_display = ('operation', 'sector', 'approved', 'created_at')
    list_filter = ('sector', 'approved', 'created_at')
    search_fields = ('operation__client__name',)

@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ('operation', 'status', 'decision', 'started_at', 'completed_at')
    list_filter = ('status', 'decision')
    search_fields = ('operation__client__name',)

@admin.register(CommitteeMember)
class CommitteeMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'operation', 'vote', 'voted_at')
    list_filter = ('vote', 'voted_at')
    search_fields = ('user__username', 'operation__client__name')

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('number', 'operation', 'status', 'generated_at')
    list_filter = ('status', 'generated_at')
    search_fields = ('number', 'operation__client__name')

@admin.register(Signature)
class SignatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'contract', 'status', 'signed_at')
    list_filter = ('status', 'signed_at')
    search_fields = ('name', 'email', 'contract__number')

@admin.register(Installment)
class InstallmentAdmin(admin.ModelAdmin):
    list_display = ('operation', 'number', 'due_date', 'amount', 'status')
    list_filter = ('status', 'due_date')
    search_fields = ('operation__client__name',)