from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, CreditApplicationViewSet, AnalysisViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'applications', CreditApplicationViewSet)
router.register(r'analyses', AnalysisViewSet)

urlpatterns = [
    path('', include(router.urls)),
]