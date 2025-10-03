from django.contrib import admin
from django.utils import timezone
from .models import User, Vehicle, Cargo, Offer, Shipment, Review, WalletTransaction, TopUpRequest


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "user_type", "email", "phone", "company_name", "verified", "balance", "deposit_balance")
    list_filter = ("user_type", "verified")
    search_fields = ("username", "email", "phone", "company_name")


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("plate_number", "owner", "capacity_kg", "truck_type", "gps_enabled")
    search_fields = ("plate_number",)
    list_filter = ("truck_type",)


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ("title", "shipper", "status", "pickup_address", "delivery_address", "created_at")
    list_filter = ("status", "pickup_date")
    search_fields = ("title", "pickup_address", "delivery_address")


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("cargo", "carrier", "price", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("cargo__title",)


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = (
        "cargo",
        "carrier",
        "start_time",
        "end_time",
        "total_price",
        "commission_amount",
        "payment_type",
        "payment_status",
        "cash_received_by",
        "received_date",
    )
    list_filter = ("payment_type", "payment_status", "start_time")
    search_fields = ("cargo__title", "carrier__username")
    actions = ["mark_as_cash_paid"]

    @admin.action(description="✅ Nagt tölegi PAID diýip belläň")
    def mark_as_cash_paid(self, request, queryset):
        updated = queryset.update(
            payment_status='paid',
            payment_type='cash',
            cash_received_by=request.user.username,
            received_date=timezone.now()
        )
        self.message_user(request, f"{updated} sargyt nagt PAID hökmünde bellendi ✅")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("shipment", "reviewer", "rating", "created_at")
    list_filter = ("rating",)


@admin.register(WalletTransaction)
class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "tx_type", "amount", "description", "success", "created_at")
    list_filter = ("tx_type", "success")
    search_fields = ("user__username", "description")


@admin.register(TopUpRequest)
class TopUpRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "stripe_session_id", "paid", "created_at")
    list_filter = ("paid",)
    search_fields = ("user__username", "stripe_session_id")
