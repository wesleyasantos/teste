from rest_framework import serializers
from clients.models import Client, Address, FinancialDocument
from credit_analysis.models import (
    CreditOperation, Partner, Guarantee, OperationDocument, CreditAnalysis,
    AIAnalysis, Committee, CommitteeMember, Contract, Signature, Installment
)

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class FinancialDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialDocument
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)
    documents = FinancialDocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Client
        fields = '__all__'
    
    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        client = Client.objects.create(address=address, **validated_data)
        return client
    
    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        if address_data:
            address = instance.address
            for attr, value in address_data.items():
                setattr(address, attr, value)
            address.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'

class GuaranteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guarantee
        fields = '__all__'

class OperationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationDocument
        fields = '__all__'

class InstallmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Installment
        fields = '__all__'

class CreditOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditOperation
        fields = '__all__'  # Isso deve incluir todos os campos do modelo
    
    class Meta:
        model = CreditOperation
        fields = '__all__'
    
    def get_client_name(self, obj):
        return obj.client.name if obj.client else None
    
    def get_client_document(self, obj):
        return obj.client.get_document() if obj.client else None

class CreditAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditAnalysis
        fields = '__all__'

class AIAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIAnalysis
        fields = '__all__'

class CommitteeMemberSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_role = serializers.SerializerMethodField()
    
    class Meta:
        model = CommitteeMember
        fields = '__all__'
    
    def get_user_name(self, obj):
        return obj.user.get_full_name() if obj.user else None
    
    def get_user_role(self, obj):
        return obj.user.get_role_display() if hasattr(obj.user, 'get_role_display') else None

class CommitteeSerializer(serializers.ModelSerializer):
    members = CommitteeMemberSerializer(source='operation.committee_members', many=True, read_only=True)
    
    class Meta:
        model = Committee
        fields = '__all__'

class SignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signature
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    signatures = SignatureSerializer(many=True, read_only=True)
    
    class Meta:
        model = Contract
        fields = '__all__'