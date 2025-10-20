import pytest
from decimal import Decimal
from django.utils import timezone

from dasha.models import User, Vehicle, Cargo, Offer, Shipment, WalletTransaction, Review, TopUpRequest
from dasha.filters import UserFilter, VehicleFilter, CargoFilter, ShipmentFilter, WalletTransactionFilter, OfferFilter, ReviewFilter, TopUpRequestFilter


@pytest.fixture
def user_carrier(db):
    return User.objects.create_user(username="carrier_f", password="pass", user_type="carrier")


@pytest.fixture
def user_shipper(db):
    return User.objects.create_user(username="shipper_f", password="pass", user_type="shipper")


@pytest.fixture
def vehicle(db, user_carrier):
    return Vehicle.objects.create(owner=user_carrier, plate_number="TM-0001", capacity_kg=12000, city="Ashgabat", body_type="tent", load_type="top")


@pytest.fixture
def cargo(db, user_shipper):
    return Cargo.objects.create(
        shipper=user_shipper,
        title="Metal pipes",
        weight_kg=3000,
        volume_m3=Decimal("12.5"),
        pickup_address="Ashgabat",
        delivery_address="Mary",
        pickup_date=timezone.now().date(),
        rate_cash=Decimal("1500.00"),
        prepayment_percent=30,
        payment_days=7,
        city="Ashgabat",
        body_type="tent",
        load_type="top",
    )


@pytest.fixture
def shipment(db, cargo, user_carrier, vehicle):
    return Shipment.objects.create(cargo=cargo, carrier=user_carrier, vehicle=vehicle, distance_km=Decimal("80"))


@pytest.fixture
def wallet_tx(db, user_shipper):
    return WalletTransaction.objects.create(user=user_shipper, tx_type="top_up", amount=Decimal("100.00"))


@pytest.fixture
def offer(db, cargo, user_carrier, vehicle):
    return Offer.objects.create(cargo=cargo, carrier=user_carrier, vehicle=vehicle, price=Decimal("1200.00"))


@pytest.fixture
def topup(db, user_shipper):
    return TopUpRequest.objects.create(user=user_shipper, amount=Decimal("200.00"))


@pytest.fixture
def review(db, shipment, user_shipper):
    return Review.objects.create(shipment=shipment, reviewer=user_shipper, rating=5, comment="Great service")


# UserFilter tests
@pytest.mark.django_db
def test_user_filter_text_and_booleans(user_shipper, user_carrier):
    user_shipper.verified = True
    user_shipper.company_name = "Turkmen Logistics"
    user_shipper.save()

    qs = User.objects.all()
    f = UserFilter({"username": "shipper", "verified": True}, queryset=qs)
    assert list(f.qs) == [user_shipper]

    f2 = UserFilter({"company_name": "logistic"}, queryset=qs)
    assert user_shipper in list(f2.qs)


# VehicleFilter tests
@pytest.mark.django_db
def test_vehicle_filter_ranges_and_choices(vehicle, user_carrier):
    # add a second record to test upper/lower bounds
    Vehicle.objects.create(owner=user_carrier, plate_number="TM-0002", capacity_kg=8000, city="Mary", body_type="open", load_type="rear")

    f = VehicleFilter({"capacity_min": 10000}, queryset=Vehicle.objects.all())
    assert list(f.qs)[0].plate_number == "TM-0001"

    f2 = VehicleFilter({"body_types": ["tent"], "city_icontains": "ash"}, queryset=Vehicle.objects.all())
    assert len(list(f2.qs)) == 1


# CargoFilter tests
@pytest.mark.django_db
def test_cargo_filter_numbers_dates_and_text(cargo, user_shipper):
    f = CargoFilter({"weight_min": 2000, "rate_min": 1000, "city": "ash"}, queryset=Cargo.objects.all())
    assert list(f.qs) == [cargo]

    f2 = CargoFilter({"prepayment_percent_min": 10, "payment_days_max": 10}, queryset=Cargo.objects.all())
    assert cargo in list(f2.qs)


# ShipmentFilter tests
@pytest.mark.django_db
def test_shipment_filter_price_and_dates(shipment):
    shipment.total_price = Decimal("5000.00")
    shipment.save()

    f = ShipmentFilter({"price_min": 4000}, queryset=Shipment.objects.all())
    assert list(f.qs) == [shipment]


# WalletTransactionFilter tests
@pytest.mark.django_db
def test_wallet_tx_filter_amount_and_user(wallet_tx, user_shipper):
    f = WalletTransactionFilter({"user": user_shipper.id, "amount_min": 50}, queryset=WalletTransaction.objects.all())
    assert list(f.qs) == [wallet_tx]


# OfferFilter tests
@pytest.mark.django_db
def test_offer_filter_basic(offer, cargo):
    f = OfferFilter({"cargo": cargo.id, "price_min": 1000}, queryset=Offer.objects.all())
    assert list(f.qs) == [offer]


# ReviewFilter tests
@pytest.mark.django_db
def test_review_filter_rating_and_user(review, user_shipper):
    f = ReviewFilter({"reviewer": user_shipper.id, "rating_min": 4}, queryset=Review.objects.all())
    assert list(f.qs) == [review]


# TopUpRequestFilter tests
@pytest.mark.django_db
def test_topup_filter_amount_and_paid(topup, user_shipper):
    # unpaid
    f = TopUpRequestFilter({"user": user_shipper.id, "amount_min": 150, "paid": False}, queryset=TopUpRequest.objects.all())
    assert list(f.qs) == [topup]

    # mark paid and filter
    topup.paid = True
    topup.save()
    f2 = TopUpRequestFilter({"paid": True}, queryset=TopUpRequest.objects.all())
    assert list(f2.qs) == [topup]
