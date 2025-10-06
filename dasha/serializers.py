from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Vehicle, Cargo, Offer, Shipment, Review, WalletTransaction, TopUpRequest


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
            'id', 'plate_number', 'brand', 'model', 'year', 'capacity_kg',
            'volume_m3', 'truck_type', 'gps_enabled', 'owner', 'owner_id', 'photo'
        ]


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
            'id', 'title', 'description', 'weight_kg', 'volume_m3',
            'pickup_address', 'delivery_address',
            'pickup_date', 'delivery_date', 'price_offer',
            'status', 'created_at', 'shipper', 'shipper_id', 'photo'
        ]
        read_only_fields = ['created_at', 'status']


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


# --- Register ---
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "phone", "company_name",
            "address", "user_type", "password"
        ]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


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