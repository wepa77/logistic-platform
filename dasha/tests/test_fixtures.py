import pytest
from decimal import Decimal
from django.utils import timezone
from dasha.models import User, Vehicle, Cargo, Offer

@pytest.fixture
def sample_data(db):
    """10-15 sany test maglumatlary döredýär."""
    carriers = [User.objects.create_user(username=f"carrier{i}", password="pass", user_type="carrier", deposit_balance=Decimal("500")) for i in range(1,6)]
    shippers = [User.objects.create_user(username=f"shipper{i}", password="pass", user_type="shipper") for i in range(1,6)]

    vehicles = []
    for i, carrier in enumerate(carriers, start=1):
        vehicles.append(Vehicle.objects.create(owner=carrier, plate_number=f"AB{i}CD", capacity_kg=10000+i*100))

    cargos = []
    for i, shipper in enumerate(shippers, start=1):
        cargos.append(Cargo.objects.create(
            shipper=shipper,
            title=f"Cargo {i}",
            weight_kg=1000+i*100,
            pickup_address="Ashgabat",
            delivery_address="Mary",
            pickup_date=timezone.now().date(),
        ))

    offers = []
    for i in range(5):
        offers.append(Offer.objects.create(
            cargo=cargos[i],
            carrier=carriers[i],
            price=Decimal(1000 + i * 100),
        ))

    return {
        "carriers": carriers,
        "shippers": shippers,
        "vehicles": vehicles,
        "cargos": cargos,
        "offers": offers,
    }


@pytest.mark.django_db
def test_sample_data_fixture(sample_data):
    assert len(sample_data["carriers"]) == 5
    assert len(sample_data["cargos"]) == 5
    assert sample_data["offers"][0].price > 0
