from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from clients.models import Client, Address, FinancialDocument
from credit_analysis.models import CreditApplication, Analysis, CreditScore
from ai_models.models import AIPrediction
from .serializers import (
    ClientSerializer, AddressSerializer, FinancialDocumentSerializer,
    CreditApplicationSerializer, AnalysisSerializer, CreditScoreSerializer,
    AIPredictionSerializer
)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['cpf', 'name']
    search_fields = ['name', 'cpf', 'email']
    
    @action(detail=True, methods=['get'])
    def credit_history(self, request, pk=None):
        client = self.get_object()
        applications = client.credit_applications.all()
        serializer = CreditApplicationSerializer(applications, many=True)
        return Response(serializer.data)

class CreditApplicationViewSet(viewsets.ModelViewSet):
    queryset = CreditApplication.objects.all()
    serializer_class = CreditApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'client']
    
    @action(detail=True, methods=['post'])
    def analyze(self, request, pk=None):
        application = self.get_object()
        application.status = 'in_analysis'
        application.save()
        
        # Aqui pode incluir chamada ao modelo de IA para gerar recomendação
        # ai_prediction = run_ai_model(application)
        
        analysis = Analysis.objects.create(
            application=application,
            analyst=request.user,
            decision='pending',
            # ai_recommendation=ai_prediction.recommendation if ai_prediction else None
        )
        
        serializer = AnalysisSerializer(analysis)
        return Response(serializer.data)

class AnalysisViewSet(viewsets.ModelViewSet):
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['decision', 'analyst', 'application']