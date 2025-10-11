import django_filters
from django.db.models import Q
from .models import User, Vehicle, Cargo, Shipment, WalletTransaction, Offer, Review, TopUpRequest


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name="username", lookup_expr="icontains")
    email = django_filters.CharFilter(field_name="email", lookup_expr="icontains")
    phone = django_filters.CharFilter(field_name="phone", lookup_expr="icontains")
    company_name = django_filters.CharFilter(field_name="company_name", lookup_expr="icontains")
    date_joined_before = django_filters.IsoDateTimeFilter(field_name="date_joined", lookup_expr="lte")
    date_joined_after = django_filters.IsoDateTimeFilter(field_name="date_joined", lookup_expr="gte")

    class Meta:
        model = User
        fields = ["user_type", "verified"]


class VehicleFilter(django_filters.FilterSet):
    # capacity/volume
    capacity_min = django_filters.NumberFilter(field_name="capacity_kg", lookup_expr="gte")
    capacity_max = django_filters.NumberFilter(field_name="capacity_kg", lookup_expr="lte")
    volume_min = django_filters.NumberFilter(field_name="volume_m3", lookup_expr="gte")
    volume_max = django_filters.NumberFilter(field_name="volume_m3", lookup_expr="lte")

    # dimensions
    length_min = django_filters.NumberFilter(field_name="length_m", lookup_expr="gte")
    length_max = django_filters.NumberFilter(field_name="length_m", lookup_expr="lte")
    width_min = django_filters.NumberFilter(field_name="width_m", lookup_expr="gte")
    width_max = django_filters.NumberFilter(field_name="width_m", lookup_expr="lte")
    height_min = django_filters.NumberFilter(field_name="height_m", lookup_expr="gte")
    height_max = django_filters.NumberFilter(field_name="height_m", lookup_expr="lte")

    # availability
    available_from_after = django_filters.DateFilter(field_name="available_from", lookup_expr="gte")
    available_from_before = django_filters.DateFilter(field_name="available_from", lookup_expr="lte")
    available_days_min = django_filters.NumberFilter(field_name="available_days", lookup_expr="gte")
    available_days_max = django_filters.NumberFilter(field_name="available_days", lookup_expr="lte")

    # locations + radius
    location_from = django_filters.CharFilter(field_name="location_from", lookup_expr="icontains")
    location_from_radius_min = django_filters.NumberFilter(field_name="location_from_radius_km", lookup_expr="gte")
    location_from_radius_max = django_filters.NumberFilter(field_name="location_from_radius_km", lookup_expr="lte")
    possible_unload = django_filters.CharFilter(field_name="possible_unload", lookup_expr="icontains")
    unload_radius_min = django_filters.NumberFilter(field_name="unload_radius_km", lookup_expr="gte")
    unload_radius_max = django_filters.NumberFilter(field_name="unload_radius_km", lookup_expr="lte")

    # rate options
    rate_cash_min = django_filters.NumberFilter(field_name="rate_cash", lookup_expr="gte")
    rate_cash_max = django_filters.NumberFilter(field_name="rate_cash", lookup_expr="lte")
    rate_with_vat_min = django_filters.NumberFilter(field_name="rate_with_vat", lookup_expr="gte")
    rate_with_vat_max = django_filters.NumberFilter(field_name="rate_with_vat", lookup_expr="lte")
    rate_without_vat_min = django_filters.NumberFilter(field_name="rate_without_vat", lookup_expr="gte")
    rate_without_vat_max = django_filters.NumberFilter(field_name="rate_without_vat", lookup_expr="lte")

    # created timeframe
    created_after = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="lte")

    # multiple choices to allow selecting many body/load/truck types
    body_types = django_filters.MultipleChoiceFilter(field_name="body_type", choices=Vehicle.BODY_TYPES)
    load_types = django_filters.MultipleChoiceFilter(field_name="load_type", choices=Vehicle.LOAD_TYPES)
    truck_categories = django_filters.MultipleChoiceFilter(field_name="truck_category", choices=Vehicle.TRUCK_CATEGORIES)

    # text search helpers
    city_icontains = django_filters.CharFilter(field_name="city", lookup_expr="icontains")
    company_icontains = django_filters.CharFilter(field_name="company_name", lookup_expr="icontains")
    plate_icontains = django_filters.CharFilter(field_name="plate_number", lookup_expr="icontains")
    brand_icontains = django_filters.CharFilter(field_name="brand", lookup_expr="icontains")
    model_icontains = django_filters.CharFilter(field_name="model", lookup_expr="icontains")

    class Meta:
        model = Vehicle
        fields = [
            "owner", "body_type", "load_type", "truck_category",
            "has_adr", "has_tir", "has_ekmt", "has_gps", "has_lift", "has_horses", "partial_load",
            "rate_mode", "rate_currency", "pay_to_card", "without_bargain",
            "is_private", "promote_top", "stealth_mode", "city",
        ]


class CargoFilter(django_filters.FilterSet):
    # numeric ranges
    weight_min = django_filters.NumberFilter(field_name="weight_kg", lookup_expr="gte")
    weight_max = django_filters.NumberFilter(field_name="weight_kg", lookup_expr="lte")
    volume_min = django_filters.NumberFilter(field_name="volume_m3", lookup_expr="gte")
    volume_max = django_filters.NumberFilter(field_name="volume_m3", lookup_expr="lte")
    quantity_min = django_filters.NumberFilter(field_name="quantity", lookup_expr="gte")
    quantity_max = django_filters.NumberFilter(field_name="quantity", lookup_expr="lte")

    # date ranges
    pickup_date_after = django_filters.DateFilter(field_name="pickup_date", lookup_expr="gte")
    pickup_date_before = django_filters.DateFilter(field_name="pickup_date", lookup_expr="lte")
    delivery_date_after = django_filters.DateFilter(field_name="delivery_date", lookup_expr="gte")
    delivery_date_before = django_filters.DateFilter(field_name="delivery_date", lookup_expr="lte")
    created_after = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="lte")

    # rate ranges
    rate_min = django_filters.NumberFilter(field_name="rate_cash", lookup_expr="gte")
    rate_max = django_filters.NumberFilter(field_name="rate_cash", lookup_expr="lte")
    rate_with_vat_min = django_filters.NumberFilter(field_name="rate_with_vat", lookup_expr="gte")
    rate_with_vat_max = django_filters.NumberFilter(field_name="rate_with_vat", lookup_expr="lte")
    rate_without_vat_min = django_filters.NumberFilter(field_name="rate_without_vat", lookup_expr="gte")
    rate_without_vat_max = django_filters.NumberFilter(field_name="rate_without_vat", lookup_expr="lte")

    # payment related ranges
    prepayment_percent_min = django_filters.NumberFilter(field_name="prepayment_percent", lookup_expr="gte")
    prepayment_percent_max = django_filters.NumberFilter(field_name="prepayment_percent", lookup_expr="lte")
    payment_days_min = django_filters.NumberFilter(field_name="payment_days", lookup_expr="gte")
    payment_days_max = django_filters.NumberFilter(field_name="payment_days", lookup_expr="lte")

    # text contains
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    pickup_address = django_filters.CharFilter(field_name="pickup_address", lookup_expr="icontains")
    delivery_address = django_filters.CharFilter(field_name="delivery_address", lookup_expr="icontains")
    city = django_filters.CharFilter(field_name="city", lookup_expr="icontains")
    route_info = django_filters.CharFilter(field_name="route_info", lookup_expr="icontains")

    class Meta:
        model = Cargo
        fields = [
            "shipper", "body_type", "load_type", "unload_type",
            "full_truck", "partial_load", "gps_required",
            "has_adr", "has_tir", "has_lift", "has_pneumatic", "has_straps",
            "rate_mode", "rate_currency", "without_bargain", "mutual_offers_only",
            "payment_method", "payment_on_unload", "direct_contract",
            "company_type", "promote_top", "stealth_mode", "status",
            "ready_status",
        ]


class ShipmentFilter(django_filters.FilterSet):
    start_after = django_filters.IsoDateTimeFilter(field_name="start_time", lookup_expr="gte")
    start_before = django_filters.IsoDateTimeFilter(field_name="start_time", lookup_expr="lte")
    end_after = django_filters.IsoDateTimeFilter(field_name="end_time", lookup_expr="gte")
    end_before = django_filters.IsoDateTimeFilter(field_name="end_time", lookup_expr="lte")
    price_min = django_filters.NumberFilter(field_name="total_price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="total_price", lookup_expr="lte")
    commission_min = django_filters.NumberFilter(field_name="commission_amount", lookup_expr="gte")
    commission_max = django_filters.NumberFilter(field_name="commission_amount", lookup_expr="lte")

    class Meta:
        model = Shipment
        fields = ["cargo", "carrier", "vehicle", "payment_type", "payment_status"]


class WalletTransactionFilter(django_filters.FilterSet):
    amount_min = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")
    amount_max = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")
    created_after = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = WalletTransaction
        fields = ["user", "tx_type", "success"]


class OfferFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    created_after = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Offer
        fields = ["cargo", "carrier", "vehicle", "status"]


class ReviewFilter(django_filters.FilterSet):
    rating_min = django_filters.NumberFilter(field_name="rating", lookup_expr="gte")
    rating_max = django_filters.NumberFilter(field_name="rating", lookup_expr="lte")
    created_after = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Review
        fields = ["reviewer", "shipment"]


class TopUpRequestFilter(django_filters.FilterSet):
    amount_min = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")
    amount_max = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")
    created_after = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.IsoDateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = TopUpRequest
        fields = ["user", "paid"]
