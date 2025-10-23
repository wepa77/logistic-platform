from django.core.management.base import BaseCommand
from dasha import models as M


def upsert(model, items):
    created, updated = 0, 0
    for idx, item in enumerate(items, start=1):
        defaults = {
            "name_tk": item.get("name_tk") or item.get("name") or item["code"],
            "name_ru": item.get("name_ru") or item.get("name") or item["code"],
            "name_en": item.get("name_en") or item.get("name") or item["code"],
            "is_active": item.get("is_active", True),
            "ordering": item.get("ordering", idx),
        }
        obj, was_created = model.objects.update_or_create(code=item["code"], defaults=defaults)
        if was_created:
            created += 1
        else:
            updated += 1
    return created, updated


class Command(BaseCommand):
    help = "Seed all dictionary tables with tri-language data (idempotent)."

    def handle(self, *args, **options):
        total_created, total_updated = 0, 0

        # User types
        user_types = [
            {"code": "shipper", "name_tk": "Ýük ugradýan", "name_ru": "Грузоотправитель", "name_en": "Shipper"},
            {"code": "carrier", "name_tk": "Ýük gatnadýan", "name_ru": "Перевозчик", "name_en": "Carrier"},
            {"code": "both", "name_tk": "Ugradýan-gatnadýan", "name_ru": "Оба (совмещает)", "name_en": "Both"},
            {"code": "expeditor", "name_tk": "Ekspeditor", "name_ru": "Экспедитор", "name_en": "Expeditor"},
            {"code": "guest", "name_tk": "Myhman", "name_ru": "Гость", "name_en": "Guest"},
            {"code": "operator", "name_tk": "Operator", "name_ru": "Оператор", "name_en": "Operator"},
            {"code": "merchant", "name_tk": "Söwdagar", "name_ru": "Продавец", "name_en": "Merchant"},
            {"code": "admin", "name_tk": "Administrator", "name_ru": "Администратор", "name_en": "Admin"},
        ]
        c, u = upsert(M.UserTypeDict, user_types); total_created += c; total_updated += u

        # Shipment payment types
        shipment_payment_types = [
            {"code": "stripe", "name_tk": "Stripe onlaýn", "name_ru": "Stripe онлайн", "name_en": "Stripe online"},
            {"code": "cash", "name_tk": "Nagt / offline", "name_ru": "Наличные / офлайн", "name_en": "Cash / offline"},
            {"code": "bank", "name_tk": "Bank geçirim", "name_ru": "Банковский перевод", "name_en": "Bank transfer"},
        ]
        c, u = upsert(M.ShipmentPaymentTypeDict, shipment_payment_types); total_created += c; total_updated += u

        # Shipment payment statuses
        shipment_payment_statuses = [
            {"code": "pending", "name_tk": "Garaşylýar", "name_ru": "Ожидается", "name_en": "Pending"},
            {"code": "paid", "name_tk": "Tölenildi", "name_ru": "Оплачено", "name_en": "Paid"},
            {"code": "failed", "name_tk": "Şowsuz boldy", "name_ru": "Неудачно", "name_en": "Failed"},
        ]
        c, u = upsert(M.ShipmentPaymentStatusDict, shipment_payment_statuses); total_created += c; total_updated += u

        # Wallet transaction types
        wallet_tx_types = [
            {"code": "top_up", "name_tk": "Balans doldurmak", "name_ru": "Пополнение баланса", "name_en": "Top up"},
            {"code": "commission", "name_tk": "Komissiýa tutuldy", "name_ru": "Списана комиссия", "name_en": "Commission charged"},
            {"code": "refund", "name_tk": "Pul yzyna gaýtaryldy", "name_ru": "Возврат средств", "name_en": "Refund"},
            {"code": "deposit_top_up", "name_tk": "Depozit goýmak", "name_ru": "Пополнение депозита", "name_en": "Deposit top up"},
            {"code": "deposit_commission", "name_tk": "Depozitden tutuldy", "name_ru": "Списано с депозита", "name_en": "From deposit"},
        ]
        c, u = upsert(M.WalletTransactionTypeDict, wallet_tx_types); total_created += c; total_updated += u

        # Vehicle body types
        body_types = [
            {"code": "tent", "name_tk": "Tent (çadyrly)", "name_ru": "Тент", "name_en": "Curtain side"},
            {"code": "refrigerator", "name_tk": "Sowadyjy", "name_ru": "Рефрижератор", "name_en": "Refrigerated"},
            {"code": "open", "name_tk": "Açyk platforma", "name_ru": "Открытая платформа", "name_en": "Flatbed"},
            {"code": "isotherm", "name_tk": "Izotermik", "name_ru": "Изотерм", "name_en": "Isotherm"},
            {"code": "tank", "name_tk": "Sýisternaly", "name_ru": "Цистерна", "name_en": "Tanker"},
            {"code": "container", "name_tk": "Konteýner daşaýjy", "name_ru": "Контейнеровоз", "name_en": "Container carrier"},
            {"code": "car_transporter", "name_tk": "Awtodaşaýjy", "name_ru": "Автовоз", "name_en": "Car transporter"},
            {"code": "other", "name_tk": "Beýleki görnüş", "name_ru": "Другое", "name_en": "Other"},
        ]
        for Model in (M.VehicleBodyTypeDict, M.CargoBodyTypeDict):
            c, u = upsert(Model, body_types); total_created += c; total_updated += u

        # Load types (vehicle + cargo; also used for unload)
        load_types = [
            {"code": "top", "name_tk": "Üstden", "name_ru": "Сверху", "name_en": "Top"},
            {"code": "side", "name_tk": "Gapdal tarapyndan", "name_ru": "Сбоку", "name_en": "Side"},
            {"code": "rear", "name_tk": "Yzdan", "name_ru": "Сзади", "name_en": "Rear"},
            {"code": "full_open", "name_tk": "Doly açylýan tent", "name_ru": "Полностью открывающийся тент", "name_en": "Full open curtain"},
            {"code": "crossbar_remove", "name_tk": "Ştangasy aýrylýan", "name_ru": "Съёмная перекладина", "name_en": "Removable crossbar"},
            {"code": "stand_remove", "name_tk": "Stoýkasy aýrylýan", "name_ru": "Съёмные стойки", "name_en": "Removable stands"},
        ]
        for Model in (M.VehicleLoadTypeDict, M.CargoLoadTypeDict):
            c, u = upsert(Model, load_types); total_created += c; total_updated += u

        # Truck categories
        truck_categories = [
            {"code": "semi_trailer", "name_tk": "Polupriýep", "name_ru": "Полуприцеп", "name_en": "Semi-trailer"},
            {"code": "truck", "name_tk": "Ýük maşyny", "name_ru": "Грузовик", "name_en": "Truck"},
            {"code": "coupling", "name_tk": "Skeçka", "name_ru": "Сцепка", "name_en": "Coupling"},
        ]
        c, u = upsert(M.VehicleTruckCategoryDict, truck_categories); total_created += c; total_updated += u

        # Vehicle/Cargo rate types
        rate_types = [
            {"code": "has_rate", "name_tk": "Bar stawka", "name_ru": "Есть ставка", "name_en": "Has rate"},
            {"code": "request_rate", "name_tk": "Stawka soralýar", "name_ru": "Запросить ставку", "name_en": "Request rate"},
        ]
        for Model in (M.VehicleRateTypeDict, M.CargoRateTypeDict):
            c, u = upsert(Model, rate_types); total_created += c; total_updated += u

        # Currencies
        currencies = [
            {"code": "tmt", "name_tk": "TMT", "name_ru": "TMT", "name_en": "TMT"},
            {"code": "rub", "name_tk": "RUB", "name_ru": "RUB", "name_en": "RUB"},
            {"code": "usd", "name_tk": "USD", "name_ru": "USD", "name_en": "USD"},
            {"code": "eur", "name_tk": "EUR", "name_ru": "EUR", "name_en": "EUR"},
        ]
        c, u = upsert(M.CurrencyDict, currencies); total_created += c; total_updated += u

        # Cargo payment methods
        payment_methods = [
            {"code": "cash", "name_tk": "Nagt", "name_ru": "Наличные", "name_en": "Cash"},
            {"code": "bank", "name_tk": "Bank geçirim", "name_ru": "Банковский перевод", "name_en": "Bank transfer"},
            {"code": "stripe", "name_tk": "Onlaýn töleg", "name_ru": "Онлайн оплата", "name_en": "Online payment"},
        ]
        c, u = upsert(M.CargoPaymentMethodDict, payment_methods); total_created += c; total_updated += u

        # Company types
        company_types = [
            {"code": "ooo", "name_tk": "ООО", "name_ru": "ООО", "name_en": "LLC"},
            {"code": "ip", "name_tk": "IP", "name_ru": "ИП", "name_en": "IE"},
            {"code": "fl", "name_tk": "Fiziki şahs", "name_ru": "Физическое лицо", "name_en": "Individual"},
            {"code": "self", "name_tk": "Özbaşdak", "name_ru": "Самозанятый", "name_en": "Self-employed"},
        ]
        c, u = upsert(M.CompanyTypeDict, company_types); total_created += c; total_updated += u

        # Cargo lifecycle statuses
        cargo_statuses = [
            {"code": "open", "name_tk": "Açyk", "name_ru": "Открыт", "name_en": "Open"},
            {"code": "in_progress", "name_tk": "Ýolda", "name_ru": "В пути", "name_en": "In progress"},
            {"code": "delivered", "name_tk": "Gowşuryldy", "name_ru": "Доставлен", "name_en": "Delivered"},
            {"code": "cancelled", "name_tk": "Ýatyryldy", "name_ru": "Отменён", "name_en": "Cancelled"},
        ]
        c, u = upsert(M.CargoStatusDict, cargo_statuses); total_created += c; total_updated += u

        # Cargo types (from selects.txt)
        cargo_types = [
            {"code": "general", "name_tk": "Adaty", "name_ru": "Общий груз", "name_en": "General"},
            {"code": "fragile", "name_tk": "Eýerilýän", "name_ru": "Хрупкий", "name_en": "Fragile"},
            {"code": "hazardous", "name_tk": "Howply", "name_ru": "Опасный", "name_en": "Hazardous"},
            {"code": "refrigerated", "name_tk": "Temperaturaly", "name_ru": "Температурный", "name_en": "Refrigerated"},
            {"code": "oversized", "name_tk": "Nägabarit", "name_ru": "Негабарит", "name_en": "Oversized"},
            {"code": "bulk", "name_tk": "Gury dökme", "name_ru": "Навалочный", "name_en": "Bulk"},
            {"code": "liquid", "name_tk": "Suwuk", "name_ru": "Жидкий", "name_en": "Liquid"},
        ]
        c, u = upsert(M.CargoTypeDict, cargo_types); total_created += c; total_updated += u

        # Ready statuses (from selects.txt)
        ready_statuses = [
            {"code": "ready", "name_tk": "Taýýar", "name_ru": "Готов", "name_en": "Ready"},
            {"code": "in_3_days", "name_tk": "3 günden", "name_ru": "Через 3 дня", "name_en": "In 3 days"},
            {"code": "in_7_days", "name_tk": "7 günden", "name_ru": "Через 7 дней", "name_en": "In 7 days"},
        ]
        c, u = upsert(M.ReadyStatusDict, ready_statuses); total_created += c; total_updated += u

        # Vehicle truck types (from selects.txt)
        vehicle_truck_types = [
            {"code": "box", "name_tk": "Furgon (Box)", "name_ru": "Фургон", "name_en": "Box truck"},
            {"code": "flatbed", "name_tk": "Platforma", "name_ru": "Платформа", "name_en": "Flatbed"},
            {"code": "refrigerated", "name_tk": "Sowadyjy", "name_ru": "Рефрижератор", "name_en": "Refrigerated"},
            {"code": "tanker", "name_tk": "Sýisternaly", "name_ru": "Цистерна", "name_en": "Tanker"},
            {"code": "other", "name_tk": "Beýleki", "name_ru": "Другое", "name_en": "Other"},
        ]
        c, u = upsert(M.VehicleTruckTypeDict, vehicle_truck_types); total_created += c; total_updated += u

        self.stdout.write(self.style.SUCCESS(
            f"Dictionaries seeded. Created={total_created}, Updated={total_updated}"
        ))
