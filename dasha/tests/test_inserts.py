import pytest
from decimal import Decimal
from django.utils import timezone

from dasha.models import User, Vehicle, Cargo, Offer, Shipment, WalletTransaction, Review, TopUpRequest


@pytest.mark.django_db
def test_insert_user_minimal():
    u = User.objects.create_user(username="u1", password="pass")
    assert u.id is not None
    assert u.user_type == "guest"
    assert u.balance == Decimal("0")


@pytest.mark.django_db
def test_insert_vehicle_minimal():
    owner = User.objects.create_user(username="carrier_ins", password="pass", user_type="carrier")
    v = Vehicle.objects.create(owner=owner, plate_number="INS-001", capacity_kg=5000)
    assert v.id is not None
    assert v.owner == owner


@pytest.mark.django_db
def test_insert_cargo_minimal():
    shipper = User.objects.create_user(username="shipper_ins", password="pass", user_type="shipper")
    c = Cargo.objects.create(
        shipper=shipper,
        title="Boxes",
        weight_kg=1000,
        pickup_address="Ashgabat",
        delivery_address="Mary",
        pickup_date=timezone.now().date(),
    )
    assert c.id is not None
    assert c.status == "open"


@pytest.mark.django_db
def test_insert_offer_minimal():
    shipper = User.objects.create_user(username="shipper_io", password="pass", user_type="shipper")
    carrier = User.objects.create_user(username="carrier_io", password="pass", user_type="carrier")
    c = Cargo.objects.create(
        shipper=shipper,
        title="Pipes",
        weight_kg=2000,
        pickup_address="Ashgabat",
        delivery_address="Mary",
        pickup_date=timezone.now().date(),
    )
    o = Offer.objects.create(cargo=c, carrier=carrier, price=Decimal("900"))
    assert o.id is not None
    assert o.status == "pending"


@pytest.mark.django_db
def test_insert_shipment_and_review():
    # Enough deposit path
    carrier = User.objects.create_user(username="carrier_is", password="pass", user_type="carrier", deposit_balance=Decimal("100"))
    shipper = User.objects.create_user(username="shipper_is", password="pass", user_type="shipper")
    c = Cargo.objects.create(
        shipper=shipper,
        title="Steel",
        weight_kg=2000,
        pickup_address="Ashgabat",
        delivery_address="Dashoguz",
        pickup_date=timezone.now().date(),
    )
    s = Shipment.objects.create(cargo=c, carrier=carrier, distance_km=Decimal("50"))  # commission 25
    s.refresh_from_db()
    assert s.commission_amount == Decimal("25.00")
    assert s.payment_status == "paid"

    r = Review.objects.create(shipment=s, reviewer=shipper, rating=4, comment="ok")
    assert r.id is not None


@pytest.mark.django_db
def test_insert_shipment_insufficient_deposit_creates_pending_and_zero_commission():
    carrier = User.objects.create_user(username="carrier_low", password="pass", user_type="carrier", deposit_balance=Decimal("5.00"))
    shipper = User.objects.create_user(username="shipper_low", password="pass", user_type="shipper")
    c = Cargo.objects.create(
        shipper=shipper,
        title="Wood",
        weight_kg=1000,
        pickup_address="Ashgabat",
        delivery_address="Mary",
        pickup_date=timezone.now().date(),
    )
    s = Shipment.objects.create(cargo=c, carrier=carrier, distance_km=Decimal("50"))  # commission would be 25, but insufficient
    s.refresh_from_db()
    assert s.payment_status == "pending"
    # commission_amount remains default 0
    assert s.commission_amount == Decimal("0.00")


@pytest.mark.django_db
def test_insert_wallet_and_topup():
    u = User.objects.create_user(username="u_wallet", password="pass")
    t = TopUpRequest.objects.create(user=u, amount=Decimal("150.00"))
    assert str(t).startswith("Top-up 150.00 TMT for")

    w = WalletTransaction.objects.create(user=u, tx_type="top_up", amount=Decimal("150.00"), description="Stripe")
    assert w.id is not None
