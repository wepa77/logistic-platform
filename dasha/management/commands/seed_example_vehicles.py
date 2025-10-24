from django.core.management.base import BaseCommand
from decimal import Decimal

from dasha.models import User, Vehicle


EXAMPLE_VEHICLES = [
    # From example payloads in the task description
    {
        "plate_number": "TM-1001",
        "brand": "Volvo",
        "model": "FH",
        "body_type": "tent",
        "load_type": "side",
        "truck_category": "truck",
        "capacity_kg": 10000,
        "rate_mode": "has_rate",
        "rate_currency": "tmt",
    },
    {
        "plate_number": "TM-1002",
        "brand": "DAF",
        "model": "XF",
        "body_type": "refrigerator",
        "load_type": "rear",
        "truck_category": "semi_trailer",
        "capacity_kg": 10000,
        "rate_mode": "has_rate",
        "rate_currency": "tmt",
    },
    {
        "plate_number": "TM-2001",
        "brand": "MAN",
        "model": "TGX",
        "body_type": "open",
        "load_type": "top",
        "truck_category": "truck",
        "capacity_kg": 12000,
        "rate_mode": "has_rate",
        "rate_currency": "tmt",
    },
    {
        "plate_number": "TM-2002",
        "brand": "Mercedes",
        "model": "Actros",
        "body_type": "isotherm",
        "load_type": "rear",
        "truck_category": "semi_trailer",
        "capacity_kg": 13000,
        "rate_mode": "has_rate",
        "rate_currency": "tmt",
    },
    {
        "plate_number": "TM-3001",
        "brand": "IVECO",
        "model": "S-Way",
        "body_type": "tank",
        "load_type": "rear",
        "truck_category": "coupling",
        "capacity_kg": 15000,
        "rate_mode": "has_rate",
        "rate_currency": "tmt",
    },
    {
        "plate_number": "TM-3002",
        "brand": "Scania",
        "model": "R",
        "body_type": "container",
        "load_type": "side",
        "truck_category": "truck",
        "capacity_kg": 11000,
        "rate_mode": "has_rate",
        "rate_currency": "tmt",
    },
]


class Command(BaseCommand):
    help = "Insert the example vehicles (from task description) into the database in an idempotent way."

    def add_arguments(self, parser):
        parser.add_argument(
            "--owner",
            dest="owner_username",
            default="carrier_bulk_owner",
            help="Username of the carrier user who will own the vehicles (will be created if missing)",
        )

    def handle(self, *args, **options):
        owner_username = options["owner_username"]

        # Ensure an owner user with carrier role exists
        owner, _ = User.objects.get_or_create(
            username=owner_username,
            defaults={
                "user_type": "carrier",
                "password": "!",  # unusable (set unusable below)
            },
        )
        if not owner.has_usable_password():
            owner.set_unusable_password()
            owner.save(update_fields=["password"])

        created, updated = 0, 0
        for item in EXAMPLE_VEHICLES:
            defaults = {
                # Required + common fields
                "owner": owner,
                "brand": item.get("brand"),
                "model": item.get("model"),
                "body_type": item.get("body_type"),
                "load_type": item.get("load_type"),
                "truck_category": item.get("truck_category", "truck"),
                "capacity_kg": int(item.get("capacity_kg", 10000)),
                # Reasonable defaults for rate fields
                "rate_mode": item.get("rate_mode", "has_rate"),
                "rate_cash": Decimal(item.get("rate_cash", 0)),
                "rate_currency": item.get("rate_currency", "tmt"),
            }
            obj, was_created = Vehicle.objects.update_or_create(
                plate_number=item["plate_number"],
                defaults=defaults,
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Example vehicles processed. Created={created}, Updated={updated}, Owner={owner.username}"
            )
        )
