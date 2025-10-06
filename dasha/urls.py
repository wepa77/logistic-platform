from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from .views import (
    UserViewSet, VehicleViewSet, CargoViewSet, OfferViewSet,
    ShipmentViewSet, ReviewViewSet,
    RegisterView, MeView,
    WalletTransactionViewSet, TopUpRequestViewSet,
    stripe_webhook, SetUserTypeView
)

# DRF Router
router = DefaultRouter()
router.register('users', UserViewSet)
router.register('vehicles', VehicleViewSet)
router.register('cargos', CargoViewSet)
router.register('offers', OfferViewSet)
router.register('shipments', ShipmentViewSet)
router.register('reviews', ReviewViewSet)
router.register('wallet', WalletTransactionViewSet, basename='wallet')
router.register('topups', TopUpRequestViewSet, basename='topups')

urlpatterns = [
    # API routers
    path("", include(router.urls)),

    # --- Auth ---
    path("auth/register/", RegisterView.as_view(), name="auth-register"),
    path("auth/me/", MeView.as_view(), name="auth-me"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # --- API Schema & Docs ---
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # --- Stripe webhook ---
    path('stripe/webhook/', stripe_webhook, name='stripe-webhook'),
    path("auth/set-type/", SetUserTypeView.as_view(), name="auth-set-type"),

]

# Media URL
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
