from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from .models import Shipment, WalletTransaction

@receiver(post_save, sender=Shipment)
def deduct_commission_by_distance(sender, instance, created, **kwargs):
    """
    Shipment döredilende, geçilen km boýunça komissiýa awtomatiki tut.
    Mysal: 0.5 TMT / km komissiýa.
    """
    if created and instance.distance_km:
        carrier = instance.carrier
        COMMISSION_PER_KM = Decimal("0.50")  # her km üçin 0.50 TMT
        commission = instance.distance_km * COMMISSION_PER_KM

        # Carrier-de ýeterlik depozit bar bolsa tut
        if carrier.deposit_balance >= commission:
            carrier.deposit_balance -= commission
            carrier.save()

            WalletTransaction.objects.create(
                user=carrier,
                tx_type="deposit_commission",
                amount=commission,
                description=f"{instance.distance_km} km üçin komissiýa tutuldy (Shipment #{instance.id})"
            )

            # Shipment maglumatlaryny hem täzeläp goýýarys
            instance.commission_amount = commission
            instance.payment_status = 'paid'
            instance.payment_type = 'cash'
            instance.save(update_fields=["commission_amount", "payment_status", "payment_type"])
        else:
            # Depozit ýeterlik däl ýagdaý:
            # - Statusy 'pending' goýmak ýa-da bildiriş ugratmak bolýar
            instance.payment_status = 'pending'
            instance.save(update_fields=["payment_status"])
