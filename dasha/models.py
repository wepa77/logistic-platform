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
from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings


class Vehicle(models.Model):
    # --- Görnüş sanawlary ---
    BODY_TYPES = [
        ('tent', 'Tent (çadyrly)'),
        ('refrigerator', 'Sowadyjy'),
        ('open', 'Açyk platforma'),
        ('isotherm', 'Izotermik'),
        ('tank', 'Sýisternaly'),
        ('container', 'Konteýner daşaýjy'),
        ('car_transporter', 'Awtodaşaýjy'),
        ('other', 'Beýleki görnüş'),
    ]

    LOAD_TYPES = [
        ('top', 'Üstden'),
        ('side', 'Gapdal tarapyndan'),
        ('rear', 'Yzdan'),
        ('full_open', 'Doly açylýan tent'),
        ('crossbar_remove', 'Ştangasy aýrylýan'),
        ('stand_remove', 'Stoýkasy aýrylýan'),
    ]

    TRUCK_CATEGORIES = [
        ('semi_trailer', 'Polupriýep'),
        ('truck', 'Ýük maşyny'),
        ('coupling', 'Skeçka'),
    ]

    RATE_TYPES = [
        ('has_rate', 'Bar stawka'),
        ('request_rate', 'Stawka soralýar'),
    ]

    CURRENCY_TYPES = [
        ('tmt', 'TMT'),
        ('rub', 'RUB'),
        ('usd', 'USD'),
        ('eur', 'EUR'),
    ]

    # --- Baglanyşyk ---
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehicles')

    # --- Esasy maglumatlar ---
    plate_number = models.CharField(max_length=20, unique=True, verbose_name="Nomeri")
    brand = models.CharField(max_length=50, blank=True, null=True, verbose_name="Markasy")
    model = models.CharField(max_length=50, blank=True, null=True, verbose_name="Modeli")
    year = models.PositiveIntegerField(blank=True, null=True, verbose_name="Ýyly")

    body_type = models.CharField(max_length=50, choices=BODY_TYPES, blank=True, null=True, verbose_name="Kuzow görnüşi")
    load_type = models.CharField(max_length=50, choices=LOAD_TYPES, blank=True, null=True, verbose_name="Ýükleme görnüşi")
    truck_category = models.CharField(max_length=20, choices=TRUCK_CATEGORIES, default='truck', verbose_name="Transport görnüşi")

    capacity_kg = models.PositiveIntegerField(verbose_name="Göterim kuwwaty (kg)")
    volume_m3 = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Kuzowyň göwrümi (m³)")
    length_m = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Uzynlygy (m)")
    width_m = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Ini (m)")
    height_m = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Beýikligi (m)")

    # --- Goşmaça aýratynlyklar ---
    has_adr = models.BooleanField(default=False, verbose_name="ADR belgisi")
    has_tir = models.BooleanField(default=False, verbose_name="TIR belgisi")
    has_ekmt = models.BooleanField(default=False, verbose_name="EKMT rugsady")
    has_gps = models.BooleanField(default=False, verbose_name="GPS monitor bar")
    has_lift = models.BooleanField(default=False, verbose_name="Gidrolift bar")
    has_horses = models.BooleanField(default=False, verbose_name="Konik bar")
    partial_load = models.BooleanField(default=False, verbose_name="Dogruz kabul edýär")

    # --- Ýük ugradyş maglumatlary ---
    available_from = models.DateField(blank=True, null=True, verbose_name="Ýüklenmäge taýýar sene")
    available_days = models.PositiveIntegerField(blank=True, null=True, verbose_name="Nähili gün töweregi boş")
    location_from = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ugradyş ýeri")
    location_from_radius_km = models.PositiveIntegerField(blank=True, null=True, verbose_name="Ugradyş radiusy (km)")
    possible_unload = models.CharField(max_length=255, blank=True, null=True, verbose_name="Mümkin düşürme ýerleri")
    unload_radius_km = models.PositiveIntegerField(blank=True, null=True, verbose_name="Düşürme radiusy (km)")

    # --- 💰 Stawka / Rate bölümi ---
    rate_mode = models.CharField(max_length=20, choices=RATE_TYPES, default='has_rate', verbose_name="Stawka görnüşi")
    rate_with_vat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Stawka (NDŞ bilen)")
    rate_without_vat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Stawka (NDŞ-siz)")
    rate_cash = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Nagt töleg")
    rate_currency = models.CharField(max_length=5, choices=CURRENCY_TYPES, default='tmt', verbose_name="Walýuta")
    pay_to_card = models.BooleanField(default=False, verbose_name="Karta geçip bolar")
    without_bargain = models.BooleanField(default=False, verbose_name="Torgsyz (söwda ýok)")

    # --- 🏢 Kompaniýa / Şahsy maglumatlar ---
    is_private = models.BooleanField(default=False, verbose_name="Şahsy adam")
    company_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Kompaniýanyň ady")
    city = models.CharField(max_length=255, blank=True, null=True, verbose_name="Şäher")
    contact_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Kontakt ady (FIO)")
    contact_phone = models.CharField(max_length=30, blank=True, null=True, verbose_name="Telefon belgisi")
    note = models.TextField(blank=True, null=True, max_length=250, verbose_name="Bellik")

    # --- 🚀 Premium / Stealth aýratynlyklar ---
    promote_top = models.BooleanField(default=False, verbose_name="TOP gözlegde görkez")
    stealth_mode = models.BooleanField(default=False, verbose_name="Steýls — belli firmalardan gizle")

    # --- Surat & wagt ---
    photo = models.ImageField(upload_to='vehicles/', blank=True, null=True, verbose_name="Ulag suraty")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        body = self.get_body_type_display() if self.body_type else "Ulag"
        return f"{self.plate_number} - {body}"

    class Meta:
        verbose_name = "Ulag"
        verbose_name_plural = "Ulaglar"

# --- Ýükler ---
from django.db import models
from django.conf import settings


class Cargo(models.Model):
    # --- Sanaw görnüşleri ---
    BODY_TYPES = [
        ('tent', 'Tent (çadyrly)'),
        ('refrigerator', 'Sowadyjy'),
        ('open', 'Açyk platforma'),
        ('isotherm', 'Izotermik'),
        ('tank', 'Sýisternaly'),
        ('container', 'Konteýner daşaýjy'),
        ('car_transporter', 'Awtodaşaýjy'),
        ('other', 'Beýleki görnüş'),
    ]

    LOAD_TYPES = [
        ('top', 'Üstden'),
        ('side', 'Gapdal tarapyndan'),
        ('rear', 'Yzdan'),
        ('full_open', 'Doly açylýan tent'),
        ('crossbar_remove', 'Ştangasy aýrylýan'),
        ('stand_remove', 'Stoýkasy aýrylýan'),
    ]

    RATE_TYPES = [
        ('has_rate', 'Bar stawka'),
        ('request_rate', 'Stawka soralýar'),
    ]

    CURRENCY_TYPES = [
        ('tmt', 'TMT'),
        ('rub', 'RUB'),
        ('usd', 'USD'),
        ('eur', 'EUR'),
    ]

    PAYMENT_METHODS = [
        ('cash', 'Nagt'),
        ('bank', 'Bank geçirim'),
        ('stripe', 'Onlaýn töleg'),
    ]

    # --- Esasy baglanyşyk ---
    shipper = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cargos')

    # --- Esasy maglumatlar ---
    title = models.CharField(max_length=255, verbose_name="Ýük ady")
    description = models.TextField(blank=True, null=True, verbose_name="Beýany")
    weight_kg = models.PositiveIntegerField(verbose_name="Agramy (kg)")
    volume_m3 = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Göwrümi (m³)")
    quantity = models.PositiveIntegerField(blank=True, null=True, verbose_name="Ýük sany")
    packing_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Gaplaýyş görnüşi")

    # --- Ugradyş / düşürme maglumatlary ---
    ready_status = models.CharField(max_length=50, default='ready', verbose_name="Ýüklenmäge taýýarlyk")
    pickup_date = models.DateField(verbose_name="Ýüklenme senesi")
    pickup_time_from = models.TimeField(blank=True, null=True, verbose_name="Ýüklenme başlangyç wagty")
    pickup_time_to = models.TimeField(blank=True, null=True, verbose_name="Ýüklenme tamamlanýan wagty")
    pickup_address = models.CharField(max_length=255, verbose_name="Ýüklenýän ýer (adres)")
    delivery_date = models.DateField(blank=True, null=True, verbose_name="Düşürme senesi")
    delivery_time_from = models.TimeField(blank=True, null=True, verbose_name="Düşürme başlangyç wagty")
    delivery_time_to = models.TimeField(blank=True, null=True, verbose_name="Düşürme tamamlanýan wagty")
    delivery_address = models.CharField(max_length=255, verbose_name="Düşürme ýeri (adres)")
    customs_required = models.BooleanField(default=False, verbose_name="Gümrük arkaly geçýärmi")
    route_info = models.TextField(blank=True, null=True, verbose_name="Marşrut barada maglumat")

    # --- Kuzow / ýükleme görnüşleri ---
    body_type = models.CharField(max_length=50, choices=BODY_TYPES, blank=True, null=True, verbose_name="Kuzow görnüşi")
    load_type = models.CharField(max_length=50, choices=LOAD_TYPES, blank=True, null=True, verbose_name="Ýükleme görnüşi")
    unload_type = models.CharField(max_length=50, choices=LOAD_TYPES, blank=True, null=True, verbose_name="Düşürme görnüşi")
    full_truck = models.BooleanField(default=True, verbose_name="Aýry maşyn bilen daşalýar (FTL)")
    partial_load = models.BooleanField(default=False, verbose_name="Dogruz kabul edýär (LTL)")
    gps_required = models.BooleanField(default=False, verbose_name="GPS monitor talap edilýär")

    # --- Goşmaça aýratynlyklar ---
    has_adr = models.BooleanField(default=False, verbose_name="ADR gerek")
    has_tir = models.BooleanField(default=False, verbose_name="TIR dokument gerek")
    has_lift = models.BooleanField(default=False, verbose_name="Gidrolift gerek")
    has_pneumatic = models.BooleanField(default=False, verbose_name="Pnewmohod gerek")
    has_straps = models.BooleanField(default=False, verbose_name="Remen gerek")

    # --- 💰 Stawka maglumatlary ---
    rate_mode = models.CharField(max_length=20, choices=RATE_TYPES, default='has_rate', verbose_name="Stawka görnüşi")
    rate_with_vat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Stawka (NDŞ bilen)")
    rate_without_vat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Stawka (NDŞ-siz)")
    rate_cash = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Nagt stawka")
    rate_currency = models.CharField(max_length=5, choices=CURRENCY_TYPES, default='tmt', verbose_name="Walýuta")
    without_bargain = models.BooleanField(default=False, verbose_name="Torgsyz")
    mutual_offers_only = models.BooleanField(default=False, verbose_name="Diňe garşy teklipler")
    prepayment_percent = models.PositiveIntegerField(blank=True, null=True, verbose_name="Öňünden töleg (%)")

    # --- Töleg şertleri ---
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash', verbose_name="Töleg usuly")
    payment_days = models.PositiveIntegerField(blank=True, null=True, verbose_name="Töleg gijikmesi (b.gün)")
    payment_on_unload = models.BooleanField(default=False, verbose_name="Düşürilenden soň tölenýärmi")
    direct_contract = models.BooleanField(default=False, verbose_name="Göni şertnama boýunça")

    # --- Firma we kontakt maglumatlary ---
    company_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Kompaniýanyň ady")
    company_type = models.CharField(
        max_length=20,
        choices=[('ooo', 'ООО'), ('ip', 'IP'), ('fl', 'Fiziki şahs'), ('self', 'Özbaşdak')],
        default='ooo',
        verbose_name="Firma görnüşi",
    )
    city = models.CharField(max_length=255, blank=True, null=True, verbose_name="Şäher")
    contact_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Kontakt ady")
    contact_phone = models.CharField(max_length=30, blank=True, null=True, verbose_name="Telefon belgisi")
    note = models.TextField(blank=True, null=True, max_length=1000, verbose_name="Bellik")

    # --- Premium görkezme ---
    promote_top = models.BooleanField(default=False, verbose_name="TOP gözlegde görkez")
    stealth_mode = models.BooleanField(default=False, verbose_name="Steýls — belli firmalardan gizle")

    # --- Surat & wagt ---
    photo = models.ImageField(upload_to='cargos/', blank=True, null=True, verbose_name="Ýük suraty")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # --- Ýük ýagdaýy ---
    status = models.CharField(max_length=30, choices=[
        ('open', 'Açyk'),
        ('in_progress', 'Ýolda'),
        ('delivered', 'Gowşuryldy'),
        ('cancelled', 'Ýatyryldy')
    ], default='open', verbose_name="Ýük ýagdaýy")

    def __str__(self):
        return f"{self.title} ({self.weight_kg} kg)"

    class Meta:
        verbose_name = "Ýük"
        verbose_name_plural = "Ýükler"


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
