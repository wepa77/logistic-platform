from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Vehicle, Cargo, Offer, Shipment, Review, WalletTransaction, TopUpRequest, \
    UserTypeDict, ShipmentPaymentTypeDict, ShipmentPaymentStatusDict, WalletTransactionTypeDict, \
    VehicleBodyTypeDict, VehicleLoadTypeDict, VehicleTruckCategoryDict, VehicleRateTypeDict, \
    CurrencyDict, CargoBodyTypeDict, CargoLoadTypeDict, CargoRateTypeDict, CargoPaymentMethodDict, \
    CompanyTypeDict, CargoStatusDict, CargoTypeDict, ReadyStatusDict, VehicleTruckTypeDict, \
    BodyLoadRequirementDict

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "user_type", "phone"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

# --- WalletTransaction ---
class WalletTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = [
            "id",
            "tx_type",
            "amount",
            "description",
            "created_at",
            "success",
        ]
        read_only_fields = ["id", "created_at", "success"]


# --- TopUpRequest ---
class TopUpRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopUpRequest
        fields = [
            "id",
            "amount",
            "stripe_session_id",
            "created_at",
            "paid",
        ]
        read_only_fields = ["id", "stripe_session_id", "created_at", "paid"]


# --- User ---
class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone', 'company_name', 'address',
            'user_type', 'verified', 'balance', 'deposit_balance', 'avatar'
        ]
        read_only_fields = ['id', 'verified', 'balance', 'deposit_balance']


# --- Vehicle ---
class VehicleSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        source='owner',
        queryset=User.objects.filter(user_type='carrier'),
        write_only=True,
        required=False
    )
    photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Vehicle
        fields = [
            'id', 'plate_number', 'brand', 'model', 'year',
            'body_type', 'load_type', 'truck_category',
            'capacity_kg', 'volume_m3', 'length_m', 'width_m', 'height_m',
            'has_adr', 'has_tir', 'has_ekmt', 'has_gps', 'has_lift', 'has_horses', 'partial_load',
            'available_from', 'available_days', 'location_from', 'location_from_radius_km',
            'possible_unload', 'unload_radius_km',
            'rate_mode', 'rate_with_vat', 'rate_without_vat', 'rate_cash', 'rate_currency', 'pay_to_card', 'without_bargain',
            'is_private', 'company_name', 'city', 'contact_name', 'contact_phone', 'note',
            'promote_top', 'stealth_mode', 'photo',
            'owner', 'owner_id',
        ]
        read_only_fields = ['id', 'owner']


# --- Cargo ---
class CargoSerializer(serializers.ModelSerializer):
    shipper = UserSerializer(read_only=True)
    shipper_id = serializers.PrimaryKeyRelatedField(
        source='shipper',
        queryset=User.objects.filter(user_type='shipper'),
        write_only=True,
        required=False
    )
    photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Cargo
        fields = [
            'id', 'shipper', 'shipper_id',
            'title', 'description', 'weight_kg', 'volume_m3', 'quantity', 'packing_type',
            'ready_status', 'pickup_date', 'pickup_time_from', 'pickup_time_to', 'pickup_address',
            'delivery_date', 'delivery_time_from', 'delivery_time_to', 'delivery_address', 'customs_required', 'route_info',
            'body_type', 'load_type', 'unload_type', 'full_truck', 'partial_load', 'gps_required',
            'has_adr', 'has_tir', 'has_lift', 'has_pneumatic', 'has_straps',
            'rate_mode', 'rate_with_vat', 'rate_without_vat', 'rate_cash', 'rate_currency', 'without_bargain', 'mutual_offers_only', 'prepayment_percent',
            'payment_method', 'payment_days', 'payment_on_unload', 'direct_contract',
            'company_name', 'company_type', 'city', 'contact_name', 'contact_phone', 'note',
            'promote_top', 'stealth_mode', 'photo',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'status', 'shipper']


# --- Offer ---
class OfferSerializer(serializers.ModelSerializer):
    carrier = UserSerializer(read_only=True)
    carrier_id = serializers.PrimaryKeyRelatedField(
        source='carrier',
        queryset=User.objects.filter(user_type='carrier'),
        write_only=True,
        required=False
    )
    vehicle = VehicleSerializer(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(
        source='vehicle',
        queryset=Vehicle.objects.all(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Offer
        fields = [
            'id', 'price', 'note', 'status', 'created_at',
            'cargo', 'carrier', 'carrier_id', 'vehicle', 'vehicle_id'
        ]
        read_only_fields = ['status', 'created_at']



# --- Shipment ---
class ShipmentSerializer(serializers.ModelSerializer):
    carrier = UserSerializer(read_only=True)
    carrier_id = serializers.PrimaryKeyRelatedField(
        source='carrier',
        queryset=User.objects.filter(user_type='carrier'),
        write_only=True,
        required=False
    )
    vehicle = VehicleSerializer(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(
        source='vehicle',
        queryset=Vehicle.objects.all(),
        write_only=True,
        required=False   # <<< ŞU ÝERE GOWULMALYDY
    )

    class Meta:
        model = Shipment
        fields = [
            'id', 'cargo', 'carrier', 'carrier_id', 'vehicle', 'vehicle_id',
            'start_time', 'end_time', 'total_price',
            'commission_amount', 'payment_type', 'payment_status',
            'cash_received_by', 'received_date', 'distance_km'
        ]
        read_only_fields = [
            'start_time', 'end_time', 'commission_amount',
            'payment_type', 'payment_status', 'cash_received_by', 'received_date'
        ]

# --- Review ---
class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserSerializer(read_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source='reviewer',
        queryset=User.objects.all(),
        write_only=True
    )

    class Meta:
        model = Review
        fields = ['id', 'shipment', 'reviewer', 'reviewer_id', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']


# --- Me (profile) ---
class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "username", "email", "phone", "company_name",
            "address", "user_type", "verified", "balance", "deposit_balance"
        ]
        read_only_fields = ["username", "verified", "balance", "deposit_balance"]

class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_type']


# --- Dictionary serializers (read-only) ---
class DictionaryBaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "code", "name_tk", "name_ru", "name_en", "is_active", "ordering"]
        read_only_fields = fields
        extra_kwargs = {f: {"read_only": True} for f in fields}


class UserTypeDictSerializer(DictionaryBaseSerializer):
    class Meta(DictionaryBaseSerializer.Meta):
        model = UserTypeDict


class ShipmentPaymentTypeDictSerializer(DictionaryBaseSerializer):
    class Meta(DictionaryBaseSerializer.Meta):
        model = ShipmentPaymentTypeDict


class ShipmentPaymentStatusDictSerializer(DictionaryBaseSerializer):
    class Meta(DictionaryBaseSerializer.Meta):
        model = ShipmentPaymentStatusDict


class WalletTransactionTypeDictSerializer(DictionaryBaseSerializer):
    class Meta(DictionaryBaseSerializer.Meta):
        model = WalletTransactionTypeDict


class VehicleBodyTypeDictSerializer(DictionaryBaseSerializer):
    class Meta(DictionaryBaseSerializer.Meta):
        model = VehicleBodyTypeDict


class VehicleLoadTypeDictSerializer(DictionaryBaseSerializer):
    class Meta(DictionaryBaseSerializer.Meta):
        model = VehicleLoadTypeDict


class VehicleTruckCategoryDictSerializer(DictionaryBaseSerializer):
    class Meta(DictionaryBaseSerializer.Meta):
        model = VehicleTruckCategoryDict


class VehicleRateTypeDictSerializer(DictionaryBaseSerializer):
    class Meta(DictionaryBaseSerializer.Meta):
        model = VehicleRateTypeDict


class CurrencyDictSerializer(DictionaryBaseSerializer):
    class Meta(DictionaryBaseSerializer.Meta):
        model = CurrencyDict


class CargoBodyTypeDictSerializer(DictionaryBaseSerializer):
    class Meta(DictionaryBaseSerializer.Meta):
        model = CargoBodyTypeDict


class CargoLoadTypeDictSerializer(DictionaryBaseSerializer):
    class Meta(DictionaryBaseSerializer.Meta):
        model = CargoLoadTypeDict


class CargoRateTypeDictSerializer(DictionaryBaseSerializer):
    class Meta(DictionaryBaseSerializer.Meta):
        model = CargoRateTypeDict


class CargoPaymentMethodDictSerializer(DictionaryBaseSerializer):
    class Meta(DictionaryBaseSerializer.Meta):
        model = CargoPaymentMethodDict


class CompanyTypeDictSerializer(DictionaryBaseSerializer):
    class Meta(DictionaryBaseSerializer.Meta):
        model = CompanyTypeDict


class CargoStatusDictSerializer(DictionaryBaseSerializer):
    class Meta(DictionaryBaseSerializer.Meta):
        model = CargoStatusDict


class CargoTypeDictSerializer(DictionaryBaseSerializer):
    class Meta(DictionaryBaseSerializer.Meta):
        model = CargoTypeDict


class ReadyStatusDictSerializer(DictionaryBaseSerializer):
    class Meta(DictionaryBaseSerializer.Meta):
        model = ReadyStatusDict


class VehicleTruckTypeDictSerializer(DictionaryBaseSerializer):
    class Meta(DictionaryBaseSerializer.Meta):
        model = VehicleTruckTypeDict


class BodyLoadRequirementDictSerializer(DictionaryBaseSerializer):
    class Meta(DictionaryBaseSerializer.Meta):
        model = BodyLoadRequirementDict