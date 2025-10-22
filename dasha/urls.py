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
    stripe_webhook, SetUserTypeView,
    UserTypeDictViewSet, ShipmentPaymentTypeDictViewSet, ShipmentPaymentStatusDictViewSet,
    WalletTransactionTypeDictViewSet, VehicleBodyTypeDictViewSet, VehicleLoadTypeDictViewSet,
    VehicleTruckCategoryDictViewSet, VehicleRateTypeDictViewSet, CurrencyDictViewSet,
    CargoBodyTypeDictViewSet, CargoLoadTypeDictViewSet, CargoRateTypeDictViewSet,
    CargoPaymentMethodDictViewSet, CompanyTypeDictViewSet, CargoStatusDictViewSet
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

# Dictionary routes (read-only)
router.register('dicts/user-types', UserTypeDictViewSet, basename='dict-user-types')
router.register('dicts/shipment-payment-types', ShipmentPaymentTypeDictViewSet, basename='dict-shipment-payment-types')
router.register('dicts/shipment-payment-statuses', ShipmentPaymentStatusDictViewSet, basename='dict-shipment-payment-statuses')
router.register('dicts/wallet-transaction-types', WalletTransactionTypeDictViewSet, basename='dict-wallet-transaction-types')
router.register('dicts/vehicle-body-types', VehicleBodyTypeDictViewSet, basename='dict-vehicle-body-types')
router.register('dicts/vehicle-load-types', VehicleLoadTypeDictViewSet, basename='dict-vehicle-load-types')
router.register('dicts/vehicle-truck-categories', VehicleTruckCategoryDictViewSet, basename='dict-vehicle-truck-categories')
router.register('dicts/vehicle-rate-types', VehicleRateTypeDictViewSet, basename='dict-vehicle-rate-types')
router.register('dicts/currencies', CurrencyDictViewSet, basename='dict-currencies')
router.register('dicts/cargo-body-types', CargoBodyTypeDictViewSet, basename='dict-cargo-body-types')
router.register('dicts/cargo-load-types', CargoLoadTypeDictViewSet, basename='dict-cargo-load-types')
router.register('dicts/cargo-rate-types', CargoRateTypeDictViewSet, basename='dict-cargo-rate-types')
router.register('dicts/cargo-payment-methods', CargoPaymentMethodDictViewSet, basename='dict-cargo-payment-methods')
router.register('dicts/company-types', CompanyTypeDictViewSet, basename='dict-company-types')
router.register('dicts/cargo-statuses', CargoStatusDictViewSet, basename='dict-cargo-statuses')

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
    path('auth/register/', RegisterView.as_view(), name='register'),

]

# Media URL
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
