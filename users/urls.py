from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
