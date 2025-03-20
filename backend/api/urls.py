from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClientViewSet, CreditOperationViewSet, PartnerViewSet, GuaranteeViewSet,
    OperationDocumentViewSet, CreditAnalysisViewSet, CommitteeViewSet,
    CommitteeMemberViewSet, ContractViewSet, SignatureViewSet, InstallmentViewSet
)

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'operations', CreditOperationViewSet)
router.register(r'partners', PartnerViewSet)
router.register(r'guarantees', GuaranteeViewSet)
router.register(r'documents', OperationDocumentViewSet)
router.register(r'analyses', CreditAnalysisViewSet)
router.register(r'committees', CommitteeViewSet)
router.register(r'committee-members', CommitteeMemberViewSet)
router.register(r'contracts', ContractViewSet)
router.register(r'signatures', SignatureViewSet)
router.register(r'installments', InstallmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]