from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from clients.models import Client, Address, FinancialDocument
from credit_analysis.models import (
    CreditOperation, Partner, Guarantee, OperationDocument, CreditAnalysis,
    AIAnalysis, Committee, CommitteeMember, Contract, Signature, Installment
)
from credit_analysis.services import create_payment_plan

from .serializers import (
    ClientSerializer, AddressSerializer, FinancialDocumentSerializer,
    CreditOperationSerializer, PartnerSerializer, GuaranteeSerializer, 
    OperationDocumentSerializer, CreditAnalysisSerializer, AIAnalysisSerializer,
    CommitteeSerializer, CommitteeMemberSerializer, ContractSerializer, 
    SignatureSerializer, InstallmentSerializer
)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['cpf', 'cnpj', 'name', 'type']
    search_fields = ['name', 'cpf', 'cnpj', 'email']
    
    @action(detail=True, methods=['get'])
    def operations(self, request, pk=None):
        client = self.get_object()
        operations = client.operations.all()
        serializer = CreditOperationSerializer(operations, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        client = self.get_object()
        documents = client.documents.all()
        serializer = FinancialDocumentSerializer(documents, many=True)
        return Response(serializer.data)

class CreditOperationViewSet(viewsets.ModelViewSet):
    queryset = CreditOperation.objects.all()
    serializer_class = CreditOperationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        print("Backend - Recebendo dados da operação:", request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print("Backend - Operação criada com ID:", serializer.data.get('id'))
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        operation = serializer.save()
        create_payment_plan(operation)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        operation = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response({'detail': 'Status não fornecido.'}, status=status.HTTP_400_BAD_REQUEST)
            
        if new_status not in dict(OPERATION_STATUS_CHOICES).keys():
            return Response({'detail': 'Status inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Atualizar status e registrar data
        operation.update_status(new_status)
        
        # Ações específicas para cada status
        if new_status == 'committee':
            # Criar comitê para a operação se ainda não existir
            Committee.objects.get_or_create(operation=operation)
        
        return Response({'status': 'Status atualizado com sucesso.'})
    
    @action(detail=True, methods=['get'])
    def installments(self, request, pk=None):
        operation = self.get_object()
        installments = operation.installments.all()
        serializer = InstallmentSerializer(installments, many=True)
        return Response(serializer.data)

class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['operation']

class GuaranteeViewSet(viewsets.ModelViewSet):
    queryset = Guarantee.objects.all()
    serializer_class = GuaranteeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['operation', 'type']

class OperationDocumentViewSet(viewsets.ModelViewSet):
    queryset = OperationDocument.objects.all()
    serializer_class = OperationDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['operation', 'type']

class CreditAnalysisViewSet(viewsets.ModelViewSet):
    queryset = CreditAnalysis.objects.all()
    serializer_class = CreditAnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['operation', 'approved']
    
    @action(detail=True, methods=['post'])
    def calculate(self, request, pk=None):
        analysis = self.get_object()
        analysis.calculate_results()
        serializer = self.get_serializer(analysis)
        return Response(serializer.data)

class CommitteeViewSet(viewsets.ModelViewSet):
    queryset = Committee.objects.all()
    serializer_class = CommitteeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['operation', 'status']
    
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        committee = self.get_object()
        
        if committee.status != 'pending':
            return Response({'detail': 'Este comitê já foi iniciado.'}, status=status.HTTP_400_BAD_REQUEST)
        
        committee.status = 'in_progress'
        committee.started_at = timezone.now()
        committee.save()
        
        # Criar membros do comitê (para o MVP, apenas o usuário atual)
        CommitteeMember.objects.create(
            operation=committee.operation,
            user=request.user
        )
        
        return Response({'detail': 'Comitê iniciado com sucesso.'})
    
    @action(detail=True, methods=['post'])
    def finish(self, request, pk=None):
        committee = self.get_object()
        
        if committee.status != 'in_progress':
            return Response({'detail': 'Este comitê não está em andamento.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar votos (para o MVP, basta um voto)
        members = committee.operation.committee_members.all()
        if not members.filter(vote__isnull=False).exists():
            return Response({'detail': 'Nenhum membro votou ainda.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Para o MVP, qualquer aprovação significa decisão aprovada
        has_approval = members.filter(vote='approve').exists()
        
        committee.status = 'completed'
        committee.decision = 'approved' if has_approval else 'rejected'
        committee.completed_at = timezone.now()
        committee.save()
        
        # Atualizar status da operação
        if has_approval:
            committee.operation.update_status('formalization')
        else:
            committee.operation.update_status('rejected')
        
        return Response({'detail': 'Comitê finalizado com sucesso.'})

class CommitteeMemberViewSet(viewsets.ModelViewSet):
    queryset = CommitteeMember.objects.all()
    serializer_class = CommitteeMemberSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['operation', 'user', 'vote']
    
    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        member = self.get_object()
        
        if member.vote is not None:
            return Response({'detail': 'Este membro já votou.'}, status=status.HTTP_400_BAD_REQUEST)
        
        vote = request.data.get('vote')
        if vote not in ['approve', 'reject']:
            return Response({'detail': 'Voto inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        
        notes = request.data.get('notes', '')
        
        member.vote = vote
        member.notes = notes
        member.voted_at = timezone.now()
        member.save()
        
        # Verificar se todos membros votaram
        operation_members = member.operation.committee_members.all()
        all_voted = not operation_members.filter(vote__isnull=True).exists()
        
        if all_voted:
            # Finalizar comitê automaticamente
            committee = Committee.objects.get(operation=member.operation)
            committee.status = 'completed'
            
            # Para o MVP, qualquer aprovação significa decisão aprovada
            has_approval = operation_members.filter(vote='approve').exists()
            committee.decision = 'approved' if has_approval else 'rejected'
            
            committee.completed_at = timezone.now()
            committee.save()
            
            # Atualizar status da operação
            if has_approval:
                member.operation.update_status('formalization')
            else:
                member.operation.update_status('rejected')
        
        return Response({'detail': 'Voto registrado com sucesso.'})

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['operation', 'status']
    
    @action(detail=True, methods=['post'])
    def generate(self, request, pk=None):
        operation = CreditOperation.objects.get(pk=pk)
        
        if hasattr(operation, 'contract'):
            return Response({'detail': 'Esta operação já possui um contrato.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Gerar número do contrato
        contract_number = f"{timezone.now().year}/{operation.id}"
        
        # No MVP, apenas criamos o contrato sem gerar arquivo real
        contract = Contract.objects.create(
            operation=operation,
            number=contract_number,
            file=None  # No MVP não teremos arquivo real
        )
        
        # Criar assinaturas necessárias
        Signature.objects.create(
            contract=contract,
            name=operation.client.name,
            email=operation.client.email
        )
        
        Signature.objects.create(
            contract=contract,
            name="Representante da Instituição",
            email="representante@instituicao.com"
        )
        
        serializer = self.get_serializer(contract)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def finalize(self, request, pk=None):
        contract = self.get_object()
        
        # Verificar se todas as assinaturas foram coletadas
        all_signed = not contract.signatures.filter(status='pending').exists()
        
        if not all_signed:
            return Response({'detail': 'Há assinaturas pendentes.'}, status=status.HTTP_400_BAD_REQUEST)
        
        contract.status = 'signed'
        contract.save()
        
        # Atualizar status da operação para monitoramento
        contract.operation.update_status('monitoring')
        
        return Response({'detail': 'Contrato finalizado com sucesso.'})

class SignatureViewSet(viewsets.ModelViewSet):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contract', 'status']
    
    @action(detail=True, methods=['post'])
    def sign(self, request, pk=None):
        signature = self.get_object()
        
        if signature.status != 'pending':
            return Response({'detail': 'Esta assinatura já foi processada.'}, status=status.HTTP_400_BAD_REQUEST)
        
        signature.status = 'signed'
        signature.signed_at = timezone.now()
        signature.save()
        
        # Verificar se todas as assinaturas foram coletadas
        contract = signature.contract
        all_signed = not contract.signatures.filter(status='pending').exists()
        
        if all_signed:
            # Finalizar contrato automaticamente
            contract.status = 'signed'
            contract.save()
            
            # Atualizar status da operação
            contract.operation.update_status('monitoring')
        
        return Response({'detail': 'Assinatura registrada com sucesso.'})

class InstallmentViewSet(viewsets.ModelViewSet):
    queryset = Installment.objects.all()
    serializer_class = InstallmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['operation', 'status']
    
    @action(detail=True, methods=['post'])
    def record_payment(self, request, pk=None):
        installment = self.get_object()
        
        if installment.status not in ['pending', 'overdue']:
            return Response({'detail': 'Esta parcela não está pendente ou em atraso.'}, status=status.HTTP_400_BAD_REQUEST)
        
        payment_date = request.data.get('payment_date')
        payment_amount = request.data.get('payment_amount')
        
        if not payment_date or not payment_amount:
            return Response({'detail': 'Data e valor do pagamento são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)
        
        installment.status = 'paid'
        installment.payment_date = payment_date
        installment.payment_amount = payment_amount
        installment.save()
        
        return Response({'detail': 'Pagamento registrado com sucesso.'})