import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APIClient
from django.utils import timezone
from dasha.models import User, Vehicle, Cargo, Offer, Shipment


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def carrier_user(db):
    user = User.objects.create_user(
        username="carrier_api",
        password="testpass",
        user_type="carrier",
        deposit_balance=Decimal("500")
    )
    return user


@pytest.fixture
def shipper_user(db):
    user = User.objects.create_user(
        username="shipper_api",
        password="testpass",
        user_type="shipper",
    )
    return user


@pytest.fixture
def auth_client_carrier(api_client, carrier_user):
    """Carrier hökmünde login edip token goýýar"""
    response = api_client.post(reverse("token_obtain_pair"), {
        "username": carrier_user.username,
        "password": "testpass"
    })
    assert response.status_code == 200
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.fixture
def auth_client_shipper(api_client, shipper_user):
    """Shipper hökmünde login edip token goýýar"""
    response = api_client.post(reverse("token_obtain_pair"), {
        "username": shipper_user.username,
        "password": "testpass"
    })
    assert response.status_code == 200
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.mark.django_db
def test_register_and_me(api_client):
    """Register we /auth/me/ test"""
    register_url = reverse("auth-register")
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "StrongPass123!",
        "user_type": "shipper"
    }
    r = api_client.post(register_url, data)
    assert r.status_code == 201

    # login etmek
    token_url = reverse("token_obtain_pair")
    r = api_client.post(token_url, {"username": "newuser", "password": "StrongPass123!"})
    assert r.status_code == 200
    token = r.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    me_url = reverse("auth-me")
    r = api_client.get(me_url)
    assert r.status_code == 200
    assert r.data["username"] == "newuser"


@pytest.mark.django_db
def test_vehicle_create(auth_client_carrier):
    """Carrier täze ulag goşýar"""
    url = reverse("vehicle-list")
    data = {
        "plate_number": "API123",
        "capacity_kg": 12000
    }
    r = auth_client_carrier.post(url, data)
    assert r.status_code == 201
    assert Vehicle.objects.filter(plate_number="API123").exists()


@pytest.mark.django_db
def test_cargo_create(auth_client_shipper):
    """Shipper täze ýük döredýär"""
    url = reverse("cargo-list")
    data = {
        "title": "API Cargo",
        "weight_kg": 2000,
        "pickup_address": "Ashgabat",
        "delivery_address": "Mary",
        "pickup_date": timezone.now().date(),
    }
    r = auth_client_shipper.post(url, data)
    assert r.status_code == 201
    assert Cargo.objects.filter(title="API Cargo").exists()

@pytest.mark.django_db
def test_offer_and_shipment(auth_client_carrier, auth_client_shipper, shipper_user, carrier_user):
    cargo = Cargo.objects.create(
        shipper=shipper_user,
        title="Offer Cargo",
        weight_kg=3000,
        pickup_address="Ashgabat",
        delivery_address="Balkanabat",
        pickup_date=timezone.now().date()
    )
    url_offer = reverse("offer-list")
    data_offer = {
        "cargo": cargo.id,
        "price": "1000",
        "note": "Test offer"
    }
    r = auth_client_carrier.post(url_offer, data_offer)
    print("OFFER RESP:", r.status_code, r.data)
    assert r.status_code == 201

    url_shipment = reverse("shipment-list")
    data_shipment = {
        "cargo": cargo.id,
        "carrier_id": carrier_user.id,
        "distance_km": "50"
    }
    r = auth_client_carrier.post(url_shipment, data_shipment)
    print("SHIPMENT RESP:", r.status_code, r.data)
    assert r.status_code == 201
