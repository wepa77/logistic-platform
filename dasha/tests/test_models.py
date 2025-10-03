import pytest
from decimal import Decimal
from django.utils import timezone

from dasha.models import (
    User, Vehicle, Cargo, Offer, Shipment, WalletTransaction, TopUpRequest
)


@pytest.mark.django_db
def test_create_users():
    # Carrier we shipper döret
    shipper = User.objects.create_user(username="shipper1", password="testpass", user_type="shipper")
    carrier = User.objects.create_user(username="carrier1", password="testpass", user_type="carrier", deposit_balance=Decimal("500"))
    assert shipper.user_type == "shipper"
    assert carrier.deposit_balance == Decimal("500")


@pytest.mark.django_db
def test_create_vehicle():
    carrier = User.objects.create_user(username="carrier2", password="pass", user_type="carrier")
    vehicle = Vehicle.objects.create(owner=carrier, plate_number="AB1234", capacity_kg=10000)
    assert vehicle.owner == carrier
    assert vehicle.capacity_kg == 10000


@pytest.mark.django_db
def test_create_cargo():
    shipper = User.objects.create_user(username="shipper2", password="pass", user_type="shipper")
    cargo = Cargo.objects.create(
        shipper=shipper,
        title="Test Cargo",
        weight_kg=1000,
        pickup_address="Ashgabat",
        delivery_address="Mary",
        pickup_date=timezone.now().date(),
    )
    assert cargo.title == "Test Cargo"
    assert cargo.status == "open"


@pytest.mark.django_db
def test_create_offer():
    shipper = User.objects.create_user(username="shipper3", password="pass", user_type="shipper")
    carrier = User.objects.create_user(username="carrier3", password="pass", user_type="carrier")
    cargo = Cargo.objects.create(
        shipper=shipper,
        title="Steel pipes",
        weight_kg=5000,
        pickup_address="Ashgabat",
        delivery_address="Turkmenabat",
        pickup_date=timezone.now().date(),
    )
    offer = Offer.objects.create(cargo=cargo, carrier=carrier, price=Decimal("2500"))
    assert offer.price == Decimal("2500")
    assert offer.status == "pending"


@pytest.mark.django_db
def test_shipment_and_commission_signal():
    # Carrier with deposit
    carrier = User.objects.create_user(username="carrier4", password="pass", user_type="carrier", deposit_balance=Decimal("1000"))
    shipper = User.objects.create_user(username="shipper4", password="pass", user_type="shipper")
    cargo = Cargo.objects.create(
        shipper=shipper,
        title="Wood",
        weight_kg=2000,
        pickup_address="Ashgabat",
        delivery_address="Dashoguz",
        pickup_date=timezone.now().date(),
    )

    # Shipment distance 100 km → commission 100 * 0.5 = 50
    shipment = Shipment.objects.create(cargo=cargo, carrier=carrier, distance_km=Decimal("100"))
    shipment.refresh_from_db()

    assert shipment.commission_amount == Decimal("50.00")
    assert shipment.payment_status == "paid"
    carrier.refresh_from_db()
    assert carrier.deposit_balance == Decimal("950.00")
    tx = WalletTransaction.objects.filter(user=carrier, tx_type="deposit_commission").first()
    assert tx is not None
    assert tx.amount == Decimal("50.00")


@pytest.mark.django_db
def test_topup_request_and_wallet():
    user = User.objects.create_user(username="user_t", password="pass")
    topup = TopUpRequest.objects.create(user=user, amount=Decimal("200"))
    assert topup.amount == Decimal("200")
    topup.paid = True
    topup.save()

    WalletTransaction.objects.create(user=user, tx_type="top_up", amount=Decimal("200"), description="manual test")
    assert WalletTransaction.objects.filter(user=user).count() == 1
