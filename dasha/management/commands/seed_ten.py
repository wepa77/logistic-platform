from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
import random
from datetime import timedelta

from dasha.models import (
    User, Vehicle, Cargo, Offer, Shipment, WalletTransaction, Review, TopUpRequest
)


class Command(BaseCommand):
    help = "Create 10 records for each model in the dasha app (Users, Vehicles, Cargos, Offers, Shipments, WalletTransactions, Reviews, TopUpRequests)"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding 10 records for each model..."))

        users = self._create_users()
        carriers = [u for u in users if u.user_type == 'carrier']
        shippers = [u for u in users if u.user_type == 'shipper']

        vehicles = self._create_vehicles(carriers)
        cargos = self._create_cargos(shippers)
        offers = self._create_offers(cargos, carriers, vehicles)
        shipments = self._create_shipments(cargos, carriers, vehicles)
        reviews = self._create_reviews(shipments, shippers)
        wallet_txs = self._create_wallet_transactions(users)
        topups = self._create_topups(users)

        self.stdout.write(self.style.SUCCESS(
            f"Done. Created: Users={len(users)}, Vehicles={len(vehicles)}, Cargos={len(cargos)}, "
            f"Offers={len(offers)}, Shipments={len(shipments)}, Reviews={len(reviews)}, "
            f"WalletTxs={len(wallet_txs)}, TopUps={len(topups)}"
        ))

    # --- helpers ---
    def _create_users(self):
        users = []
        # 5 carriers (with sufficient deposit), 5 shippers
        for i in range(1, 6):
            u = User.objects.create_user(
                username=f"carrier_seed_{i}",
                password="pass",
                user_type="carrier",
                deposit_balance=Decimal("10000.00"),
                phone=f"+99365{i:07d}",
                company_name=f"Carrier Co {i}",
            )
            users.append(u)
        for i in range(1, 6):
            u = User.objects.create_user(
                username=f"shipper_seed_{i}",
                password="pass",
                user_type="shipper",
                phone=f"+99364{i:07d}",
                company_name=f"Shipper LLC {i}",
            )
            users.append(u)
        return users

    def _create_vehicles(self, carriers):
        vehicles = []
        body_types = [bt[0] for bt in Vehicle.BODY_TYPES]
        load_types = [lt[0] for lt in Vehicle.LOAD_TYPES]
        cities = ["Ashgabat", "Mary", "Balkanabat", "Turkmenabat", "Dashoguz"]
        for i in range(1, 11):
            owner = carriers[(i - 1) % len(carriers)]
            v = Vehicle.objects.create(
                owner=owner,
                plate_number=f"TM-SEED-{i:04d}",
                capacity_kg=8000 + i * 100,
                city=random.choice(cities),
                body_type=random.choice(body_types),
                load_type=random.choice(load_types),
                rate_mode='has_rate',
                rate_cash=Decimal(str(1000 + i * 50)),
                rate_currency='tmt',
            )
            vehicles.append(v)
        return vehicles

    def _create_cargos(self, shippers):
        cargos = []
        cities = ["Ashgabat", "Mary", "Balkanabat", "Turkmenabat", "Dashoguz"]
        today = timezone.now().date()
        for i in range(1, 11):
            shipper = shippers[(i - 1) % len(shippers)]
            c = Cargo.objects.create(
                shipper=shipper,
                title=f"Seed Cargo {i}",
                description="Auto-generated seed cargo",
                weight_kg=1000 + i * 100,
                volume_m3=Decimal("10.50"),
                quantity=10 + i,
                pickup_date=today + timedelta(days=i),
                pickup_address=random.choice(cities),
                delivery_date=today + timedelta(days=i + 2),
                delivery_address=random.choice(cities),
                body_type='tent',
                load_type='top',
                rate_mode='has_rate',
                rate_cash=Decimal(str(1500 + i * 75)),
                rate_currency='tmt',
                prepayment_percent=20,
                payment_method='cash',
                payment_days=7,
                city=random.choice(cities),
                status='open',
            )
            cargos.append(c)
        return cargos

    def _create_offers(self, cargos, carriers, vehicles):
        offers = []
        for i in range(1, 11):
            cargo = cargos[i - 1]
            carrier = carriers[(i - 1) % len(carriers)]
            vehicle = vehicles[i - 1]
            o = Offer.objects.create(
                cargo=cargo,
                carrier=carrier,
                vehicle=vehicle,
                price=Decimal(str(1200 + i * 100)),
                note="Seed offer",
                status='pending',
            )
            offers.append(o)
        return offers

    def _create_shipments(self, cargos, carriers, vehicles):
        shipments = []
        # Use the same 10 cargos (Shipment is OneToOne with Cargo)
        for i in range(1, 11):
            cargo = cargos[i - 1]
            carrier = carriers[(i - 1) % len(carriers)]
            vehicle = vehicles[i - 1]
            # distance grows to produce commissions via signal
            distance_km = Decimal(str(10 + i))
            s = Shipment.objects.create(
                cargo=cargo,
                carrier=carrier,
                vehicle=vehicle,
                distance_km=distance_km,
                total_price=Decimal(str(3000 + i * 100)),
            )
            shipments.append(s)
        return shipments

    def _create_reviews(self, shipments, shippers):
        reviews = []
        for i in range(1, 11):
            shipment = shipments[i - 1]
            reviewer = shippers[(i - 1) % len(shippers)]
            r = Review.objects.create(
                shipment=shipment,
                reviewer=reviewer,
                rating=5 if i % 2 == 0 else 4,
                comment="Seed review",
            )
            reviews.append(r)
        return reviews

    def _create_wallet_transactions(self, users):
        txs = []
        for i in range(1, 11):
            user = users[(i - 1) % len(users)]
            t = WalletTransaction.objects.create(
                user=user,
                tx_type='top_up',
                amount=Decimal(str(100 + i * 10)),
                description='Seed top up',
                success=True,
            )
            txs.append(t)
        return txs

    def _create_topups(self, users):
        tups = []
        for i in range(1, 11):
            user = users[(i - 1) % len(users)]
            t = TopUpRequest.objects.create(
                user=user,
                amount=Decimal(str(200 + i * 5)),
                paid=(i % 3 == 0),
            )
            tups.append(t)
        return tups
