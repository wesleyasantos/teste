from rest_framework import serializers
from clients.models import Client, Address, FinancialDocument
from credit_analysis.models import CreditApplication, Analysis, CreditScore
from ai_models.models import AIPrediction

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

class CreditScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditScore
        fields = '__all__'
        read_only_fields = ('last_calculated',)

class CreditApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditApplication
        fields = '__all__'

class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = '__all__'

class AIPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIPrediction
        fields = '__all__'