from django.core.management.base import BaseCommand
from decimal import Decimal
from django.utils import timezone
from dasha.models import User, Vehicle, Cargo, Offer, Shipment

class Command(BaseCommand):
    help = "Create 10–15 demo data for testing/admin/demo"

    def handle(self, *args, **options):
        carriers = []
        shippers = []
        vehicles = []
        cargos = []
        offers = []

        # 5 carrier & 5 shipper
        for i in range(1, 6):
            c, _ = User.objects.get_or_create(
                username=f"carrier{i}",
                defaults={
                    "password": "pass",
                    "user_type": "carrier",
                    "deposit_balance": Decimal("500")
                }
            )
            s, _ = User.objects.get_or_create(
                username=f"shipper{i}",
                defaults={
                    "password": "pass",
                    "user_type": "shipper",
                }
            )
            carriers.append(c)
            shippers.append(s)

            v, _ = Vehicle.objects.get_or_create(
                owner=c,
                plate_number=f"AB{i:03d}CD",
                defaults={
                    "capacity_kg": 10000 + i * 100,
                    "brand": f"Brand{i}",
                    "model": f"Model{i}",
                    "year": 2020 + i,
                }
            )
            vehicles.append(v)

            cargo, _ = Cargo.objects.get_or_create(
                shipper=s,
                title=f"Cargo {i}",
                defaults={
                    "description": "Test cargo description",
                    "weight_kg": 1000 + i * 200,
                    "pickup_address": "Ashgabat",
                    "delivery_address": "Mary",
                    "pickup_date": timezone.now().date(),
                }
            )
            cargos.append(cargo)

            offer, _ = Offer.objects.get_or_create(
                cargo=cargo,
                carrier=c,
                defaults={
                    "price": Decimal(1000 + i * 150),
                    "note": f"Offer note {i}"
                }
            )
            offers.append(offer)

        # optional: shipment create for first 3 cargos
        for idx, cargo in enumerate(cargos[:3], start=1):
            Shipment.objects.get_or_create(
                cargo=cargo,
                carrier=carriers[idx-1],
                defaults={
                    "distance_km": Decimal("100"),
                    "total_price": Decimal("2500")
                }
            )

        self.stdout.write(self.style.SUCCESS(
            f"✅ Created {len(carriers)} carriers, {len(shippers)} shippers, "
            f"{len(vehicles)} vehicles, {len(cargos)} cargos, {len(offers)} offers."
        ))
