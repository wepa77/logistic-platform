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
    # --- Görkezilýän kolonkalary ---
    list_display = (
        "plate_number",
        "owner",
        "brand",
        "truck_category",
        "body_type",
        "capacity_kg",
        "rate_mode",
        "rate_currency",
        "has_gps",
        "created_at",
    )

    # --- Filtrler (sagdaky panelde) ---
    list_filter = (
        "truck_category",
        "body_type",
        "load_type",
        "has_adr",
        "has_tir",
        "has_ekmt",
        "has_gps",
        "promote_top",
        "stealth_mode",
        "rate_currency",
        "rate_mode",
        "created_at",
    )

    # --- Gözleg meýdanlary ---
    search_fields = (
        "plate_number",
        "brand",
        "model",
        "owner__username",
        "company_name",
        "city",
    )

    # --- Sütün boýunça tertipleme ---
    ordering = ("-created_at",)

    # --- Her bir kategoriýany admin formda toparlaýar ---
    fieldsets = (
        ("Esasy maglumatlar", {
            "fields": (
                "owner",
                "plate_number",
                "brand",
                "model",
                "year",
                "truck_category",
                "body_type",
                "load_type",
                "capacity_kg",
                "volume_m3",
                ("length_m", "width_m", "height_m"),
                "photo",
            )
        }),
        ("Goşmaça aýratynlyklar", {
            "classes": ("collapse",),
            "fields": (
                "has_adr",
                "has_tir",
                "has_ekmt",
                "has_gps",
                "has_lift",
                "has_horses",
                "partial_load",
            )
        }),
        ("Ýük ugradyş maglumatlary", {
            "classes": ("collapse",),
            "fields": (
                "available_from",
                "available_days",
                "location_from",
                "location_from_radius_km",
                "possible_unload",
                "unload_radius_km",
            )
        }),
        ("Stawka maglumatlary", {
            "classes": ("collapse",),
            "fields": (
                "rate_mode",
                ("rate_with_vat", "rate_without_vat", "rate_cash"),
                "rate_currency",
                "pay_to_card",
                "without_bargain",
            )
        }),
        ("Kompaniýa / Kontakt maglumatlary", {
            "classes": ("collapse",),
            "fields": (
                "is_private",
                "company_name",
                "city",
                "contact_name",
                "contact_phone",
                "note",
            )
        }),
        ("Premium görkezme", {
            "classes": ("collapse",),
            "fields": (
                "promote_top",
                "stealth_mode",
            )
        }),
        ("Wagt bellikleri", {
            "classes": ("collapse",),
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    readonly_fields = ("created_at", "updated_at")

    # --- Dürli görnüşde has gowy görünüş üçin ---
    list_per_page = 25
    date_hierarchy = "created_at"
    save_on_top = True


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
