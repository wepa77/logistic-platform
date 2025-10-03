from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, generics, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import stripe

from .models import (
    User, Vehicle, Cargo, Offer, Shipment, Review,
    WalletTransaction, TopUpRequest
)
from .serializers import (
    UserSerializer, VehicleSerializer, CargoSerializer,
    OfferSerializer, ShipmentSerializer, ReviewSerializer,
    RegisterSerializer, MeSerializer,
    WalletTransactionSerializer, TopUpRequestSerializer
)
from .permissions import IsOwnerOrReadOnly

stripe.api_key = settings.STRIPE_SECRET_KEY


# --- Stripe webhook ---
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        topup = TopUpRequest.objects.filter(stripe_session_id=session["id"]).first()
        if topup and not topup.paid:
            topup.paid = True
            topup.save()
            user = topup.user
            user.balance += topup.amount
            user.save()
            WalletTransaction.objects.create(
                user=user,
                tx_type="top_up",
                amount=topup.amount,
                description="Balans doldurmak"
            )
    return HttpResponse(status=200)


# --- WalletTransaction ---
class WalletTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WalletTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WalletTransaction.objects.filter(user=self.request.user).order_by("-created_at")


# --- TopUpRequest ---

class TopUpRequestViewSet(viewsets.ModelViewSet):
    serializer_class = TopUpRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TopUpRequest.objects.filter(user=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        # Stripe ulanmaýarys — diňe offline balans goşmak
        topup = serializer.save(user=self.request.user, paid=True)
        user = self.request.user
        user.balance += topup.amount
        user.save()

        WalletTransaction.objects.create(
            user=user,
            tx_type="top_up",
            amount=topup.amount,
            description="Manual offline top-up"
        )

    # ✅ balance endpoint
    @action(detail=False, methods=["get"])
    def balance(self, request):
        return Response({"balance": request.user.balance})

# --- Auth: Register ---
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# --- Auth: Me ---
class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = MeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# --- User list ---
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["user_type", "verified"]
    search_fields = ["username", "email", "phone", "company_name", "address"]
    ordering_fields = ["date_joined", "last_login"]
    ordering = ["-date_joined"]


# --- Vehicle ---
class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["truck_type", "gps_enabled", "capacity_kg", "volume_m3"]
    search_fields = ["plate_number", "brand", "model"]
    ordering_fields = ["year", "capacity_kg", "volume_m3", "id"]
    ordering = ["-id"]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# --- Cargo ---
class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "pickup_date"]
    search_fields = ["title", "pickup_address", "delivery_address"]
    ordering_fields = ["pickup_date", "created_at", "price_offer"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        serializer.save(shipper=self.request.user)


# --- Offer ---
class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "cargo", "carrier", "vehicle"]
    search_fields = ["note", "cargo__title", "carrier__username"]
    ordering_fields = ["price", "created_at"]
    ordering = ["-created_at"]

    def perform_create(self, serializer):
        serializer.save(carrier=self.request.user)


# --- Shipment ---
# views.py
class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["cargo", "carrier", "vehicle", "payment_status", "payment_type"]
    search_fields = ["cargo__title", "carrier__username"]
    ordering_fields = ["start_time", "end_time", "total_price", "created_at"]
    ordering = ["-start_time"]

    def perform_create(self, serializer):
        # Carrier awtomatik goýmak islän bolsaňyz:
        if not serializer.validated_data.get('carrier'):
            serializer.save(carrier=self.request.user)
        else:
            serializer.save()



# --- Review ---
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["rating", "created_at"]
    search_fields = ["comment", "shipment__cargo__title", "reviewer__username"]
    ordering_fields = ["rating", "created_at"]
    ordering = ["-created_at"]
