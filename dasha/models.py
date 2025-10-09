from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPES = [
        ('shipper', 'Ýük ugradýan'),              # Shipper / Sender
        ('carrier', 'Ýük gatnadýan'),             # Carrier / Driver
        ('both', 'Ýük ugradýan-gatnadýan'),       # Both (dual role)
        ('expeditor', 'Ekspeditor'),              # Dispatcher / Forwarder
        ('guest', 'Myhman'),                      # Guest user
        ('admin', 'Administrator'),               # System administrator
        ('operator', 'Operator'),                 # Operator / Support
        ('merchant', 'Söwdagar'),                 # Business / Seller
    ]

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPES,
        default='guest',
        verbose_name="Ulanyjy görnüşi"
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Telefon belgisi"
    )

    company_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Kompaniýanyň ady"
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Salgysy"
    )

    verified = models.BooleanField(
        default=False,
        verbose_name="Tassyklananmy"
    )

    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Balans"
    )

    deposit_balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Carrier tarapyndan goýlan öňki depozit",
        verbose_name="Depozit balansy"
    )

    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name="Profil suraty"
    )

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    class Meta:
        verbose_name = "Ulanyjy"
        verbose_name_plural = "Ulanyjylar"

class Shipment(models.Model):
    PAYMENT_TYPES = [
        ('stripe', 'Stripe onlaýn'),
        ('cash', 'Nagt / offline'),
        ('bank', 'Bank geçirim'),
    ]
    PAYMENT_STATUS = [
        ('pending', 'Garaşylýar'),
        ('paid', 'Tölenildi'),
        ('failed', 'Şowsuz boldy'),
    ]

    cargo = models.OneToOneField('Cargo', on_delete=models.CASCADE, related_name='shipment')
    carrier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shipments')
    vehicle = models.ForeignKey('Vehicle', on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    distance_km = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES, default='stripe')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    cash_received_by = models.CharField(max_length=100, blank=True, null=True)
    received_date = models.DateTimeField(blank=True, null=True)

    commission_amount = models.DecimalField(  # ✅ täze meýdan
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Şu sargyt üçin komissiýa"
    )

    def __str__(self):
        return f"Shipment for {self.cargo}"


class WalletTransaction(models.Model):
    TRANSACTION_TYPES = [
        ("top_up", "Balans doldurmak"),
        ("commission", "Komissiýa tutuldy"),
        ("refund", "Pul yzyna gaýtaryldy"),
        ("deposit_top_up", "Depozit goýmak"),      # ✅ täze görnüş
        ("deposit_commission", "Depozitden tutuldy"),  # ✅ täze görnüş
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wallet_transactions")
    tx_type = models.CharField(max_length=30, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} {self.tx_type} {self.amount} TMT"



# --- Ulaglar ---
class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    plate_number = models.CharField(max_length=20, unique=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    capacity_kg = models.PositiveIntegerField()
    volume_m3 = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    truck_type = models.CharField(max_length=50, blank=True, null=True)
    gps_enabled = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='vehicles/', blank=True, null=True)

    def __str__(self):
        return f"{self.plate_number} ({self.capacity_kg} kg)"


# --- Ýükler ---
class Cargo(models.Model):
    shipper = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cargos')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    weight_kg = models.PositiveIntegerField()
    volume_m3 = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    pickup_address = models.CharField(max_length=255)
    delivery_address = models.CharField(max_length=255)
    pickup_date = models.DateField()
    delivery_date = models.DateField(blank=True, null=True)
    price_offer = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=30, choices=[
        ('open', 'Açyk'),
        ('in_progress', 'Ýolda'),
        ('delivered', 'Gowşuryldy'),
        ('cancelled', 'Ýatyryldy')
    ], default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='cargos/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.weight_kg} kg)"


# --- Teklipler ---
class Offer(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, related_name='offers')
    carrier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Garaşylýar'),
        ('accepted', 'Kabul edildi'),
        ('rejected', 'Ret edildi'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offer {self.id} - {self.price} TMT"



# --- Reýting & teswirler ---
class Review(models.Model):
    shipment = models.OneToOneField(Shipment, on_delete=models.CASCADE, related_name='review')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # 1-5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.rating}★ by {self.reviewer}"


# --- Balans doldurma haýyşlary (Stripe ýa-da beýleki gateway üçin) ---
class TopUpRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="topups")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_session_id = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Top-up {self.amount} TMT for {self.user}"
