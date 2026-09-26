"""Management command: seed the database with realistic demo data.

Usage:
    python manage.py seed_data
"""

import random
from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from accounts.models import FarmProfile
from breeding.models import Calving, Heat, Insemination, Pregnancy
from deliveries.models import DeliveryNote
from employees.models import Advance, Employee, SalaryPayment
from feed.models import FeedConsumption, FeedItem, FeedPurchase
from finance.models import FinanceCategory, Transaction
from health.models import Medicine, Treatment, Vaccination, VetVisit
from herd.models import Animal, AnimalMovement, Breed
from inventory.models import InventoryItem, StockTransaction
from invoicing.models import Invoice, InvoiceItem
from milk.models import Lactation, MilkProduction, MilkQuality, YieldTarget
from purchases.models import Purchase, Supplier
from sales.models import Customer, Sale


class Command(BaseCommand):
    help = "Seed the database with realistic demo data"

    def handle(self, *args, **options):
        if Animal.objects.exists():
            self.stdout.write("Database already contains data — skipping seed.")
            return

        today = date.today()
        rng = random.Random(42)

        # ---------- Farm profile for admin ----------
        admin = User.objects.filter(is_superuser=True).first()
        if admin and not FarmProfile.objects.filter(user=admin).exists():
            FarmProfile.objects.create(
                user=admin,
                farm_name="Green Valley Dairy",
                owner_name=admin.get_full_name() or admin.username,
                phone="+1 555 0199",
                email=admin.email or "",
                address="123 Meadow Lane",
                currency="$",
                tagline="Quality milk from happy cows",
            )

        # ---------- Breeds ----------
        breeds = [
            ("Holstein Friesian", "Dairy", "Netherlands", 28.0),
            ("Jersey", "Dairy", "United Kingdom", 20.0),
            ("Guernsey", "Dairy", "United Kingdom", 18.0),
            ("Ayrshire", "Dairy", "Scotland", 19.0),
            ("Brown Swiss", "Dairy", "Switzerland", 24.0),
            ("Sahiwal", "Dual-purpose", "India", 12.0),
        ]
        breed_objs = {}
        for name, purpose, origin, avg in breeds:
            breed_objs[name] = Breed.objects.create(
                name=name, purpose=purpose, origin=origin, avg_milk_yield=avg
            )

        # ---------- Animals ----------
        def make_animal(tag, name, sex, breed, dob, category, status="Active",
                        source="Born", sire=None, dam=None, price=0):
            return Animal.objects.create(
                tag_number=tag, name=name, breed=breed_objs.get(breed), sex=sex,
                dob=dob, category=category, status=status, source=source,
                purchase_price=price, sire=sire, dam=dam,
            )

        dam1 = make_animal("C-0001", "Bella", "Female", "Holstein Friesian",
                           today - timedelta(days=2400), "Dry")
        dam2 = make_animal("C-0002", "Daisy", "Female", "Jersey",
                           today - timedelta(days=2200), "Milker", status="Sold")
        dams = [dam1, dam2]

        animals = []
        milker_specs = [
            ("C-0011", "Lily", "Holstein Friesian", 1500, "Milker", dam1),
            ("C-0012", "Molly", "Jersey", 1600, "Milker", dam1),
            ("C-0013", "Nellie", "Guernsey", 1400, "Milker", dam1),
            ("C-0014", "Rosie", "Holstein Friesian", 1450, "Milker", dam2),
            ("C-0015", "Bessie", "Brown Swiss", 1700, "Milker", dam2),
            ("C-0016", "Clover", "Sahiwal", 1300, "Milker", dam1),
            ("C-0017", "Hazel", "Jersey", 1550, "Milker", dam2),
            ("C-0018", "Ivy", "Holstein Friesian", 1200, "Milker", dam1),
        ]
        sire_bull = make_animal("B-0001", "Thor", "Male", "Holstein Friesian",
                                today - timedelta(days=3000), "Bull")

        for tag, name, breed, days, category, dam in milker_specs:
            animals.append(make_animal(tag, name, "Female", breed,
                                       today - timedelta(days=days), category,
                                       dam=dam, sire=sire_bull))

        for i in range(6):
            animals.append(make_animal(
                f"C-010{i+1}", f"Calf {i + 1}", rng.choice(["Female", "Male"]),
                rng.choice(list(breed_objs)), today - timedelta(days=60 + i * 20),
                "Calf", dam=rng.choice(dams), sire=sire_bull,
            ))
        animals.append(make_animal("H-0001", "Hope", "Female", "Ayrshire",
                                   today - timedelta(days=900), "Heifer"))
        animals.append(make_animal("H-0002", "Fern", "Female", "Guernsey",
                                   today - timedelta(days=800), "Heifer"))
        milkers = [a for a in animals if a.category == "Milker"]

        # ---------- Lactation & milk production (last 21 days) ----------
        for m in milkers:
            Lactation.objects.create(
                animal=m,
                lactation_number=2,
                start_date=today - timedelta(days=180),
                expected_dry_off=today + timedelta(days=90),
            )
            YieldTarget.objects.create(
                animal=m,
                target_daily_liters=Decimal(
                    m.breed.avg_milk_yield if m.breed else 14
                ).quantize(Decimal("0.1")),
            )
            for back in range(21):
                d = today - timedelta(days=back)
                am = Decimal(str(round(rng.uniform(6, 12), 1)))
                pm = Decimal(str(round(rng.uniform(4, 9), 1)))
                MilkProduction.objects.create(
                    animal=m, date=d, session="Morning", quantity=am
                )
                MilkProduction.objects.create(
                    animal=m, date=d, session="Evening", quantity=pm
                )
            fat = Decimal("5.2") if m.breed and m.breed.name == "Jersey" else Decimal("3.8")
            MilkQuality.objects.create(
                animal=m, date=today - timedelta(days=1),
                fat_pct=fat, protein_pct=Decimal("3.2"), snf_pct=Decimal("8.6"),
                density=Decimal("1.031"), temperature=Decimal("4.0"),
                remarks="Within acceptable range",
            )
        self.stdout.write(f"  {len(milkers)} milkers seeded with 21 days of production")

        # ---------- Breeding ----------
        for i, m in enumerate(milkers[:4]):
            Heat.objects.create(
                animal=m, heat_date=today - timedelta(days=35 - i),
                expected_heat_date=today - timedelta(days=14 - i), is_bred=True,
                detected_by="Farm manager",
            )
            ai = Insemination.objects.create(
                animal=m, service_date=today - timedelta(days=32 - i),
                bull_name="Thor", bull_breed="Holstein Friesian",
                semen_source="AI centre", technician="Dr. Evans",
                cost=Decimal("25.00"), result="Conceived",
            )
            Pregnancy.objects.create(
                animal=m, insemination=ai, check_date=today - timedelta(days=10 - i),
                diagnosis="Positive",
                expected_calving_date=today + timedelta(days=250 - i * 5),
            )
            AnimalMovement.objects.create(
                animal=m, movement_date=today - timedelta(days=60),
                movement_type="Barn Transfer", from_location="Free stall",
                to_location="Maternity pen", reason="Pre-calving",
            )
        Heat.objects.create(
            animal=milkers[4], heat_date=today - timedelta(days=18),
            expected_heat_date=today + timedelta(days=3), is_bred=False,
            detected_by="Milking staff",
        )
        Calving.objects.create(
            animal=dam1, calving_date=today - timedelta(days=110),
            calving_type="Single", male_calves=0, female_calves=1,
            complication="None", vet_name="Dr. Evans",
        )
        self.stdout.write("  Breeding records seeded")

        # ---------- Health ----------
        Medicine.objects.create(name="Lumpy Skin Vaccine", category="Vaccine",
                                manufacturer="Agrovet", unit="Dose",
                                stock_quantity=120, unit_cost=Decimal("3.50"),
                                reorder_level=20)
        Medicine.objects.create(name="Oxytetracycline", category="Antibiotic",
                                manufacturer="VetPharm", unit="ml",
                                stock_quantity=40, unit_cost=Decimal("12.00"),
                                reorder_level=10)
        Medicine.objects.create(name="Albendazole", category="Dewormer",
                                manufacturer="Agrovet", unit="Dose",
                                stock_quantity=8, unit_cost=Decimal("2.25"),
                                reorder_level=15)
        for m in milkers[:6]:
            Vaccination.objects.create(
                animal=m, vaccine_name="Foot & Mouth", date=today - timedelta(days=90),
                next_due_date=today + timedelta(days=30), dosage="2 ml",
                administered_by="Dr. Evans", cost=Decimal("5.00"),
            )
            Vaccination.objects.create(
                animal=m, vaccine_name="Lumpy Skin", date=today - timedelta(days=220),
                next_due_date=today + timedelta(days=140), dosage="5 ml",
                administered_by="Farm staff", cost=Decimal("4.00"),
            )
            Treatment.objects.create(
                animal=m, date=today - timedelta(days=15), diagnosis="Mastitis",
                treatment_applied="Intramammary infusion for 3 days",
                cost=Decimal("18.00"), veterinarian="Dr. Evans",
            )
            VetVisit.objects.create(
                animal=m, visit_date=today - timedelta(days=20), reason="Routine check",
                findings="Healthy", vet_name="Dr. Evans", cost=Decimal("25.00"),
            )
        t = Treatment.objects.create(
            animal=milkers[2], date=today - timedelta(days=5), diagnosis="Worm infestation",
            treatment_applied="Deworming", cost=Decimal("10.00"),
            veterinarian="Farm staff",
        )
        t.medicines.add(Medicine.objects.get(name="Albendazole"))
        self.stdout.write("  Health records seeded")

        # ---------- Feed ----------
        feed_items = [
            ("Maize Silage", "Silage", "kg", Decimal("0.20"), 500),
            ("Alfalfa Hay", "Roughage", "kg", Decimal("0.45"), 300),
            ("Dairy Concentrate", "Concentrate", "kg", Decimal("0.75"), 400),
            ("Mineral Mix", "Mineral", "kg", Decimal("2.50"), 100),
        ]
        feed_objs = {}
        for name, cat, unit, cost, reorder in feed_items:
            feed_objs[name] = FeedItem.objects.create(
                name=name, category=cat, unit=unit,
                cost_per_unit=cost, reorder_level=reorder,
            )
        for back in range(14):
            d = today - timedelta(days=back)
            FeedConsumption.objects.create(
                feed_item=feed_objs["Maize Silage"], date=d, quantity=Decimal("300.00"),
                cost_per_unit=Decimal("0.20"), feeding_time="Morning", notes="Herd feeding",
            )
            FeedConsumption.objects.create(
                feed_item=feed_objs["Dairy Concentrate"], date=d,
                quantity=Decimal("120.00"), cost_per_unit=Decimal("0.75"),
                feeding_time="Evening", notes="Milkers ration",
            )
        FeedPurchase.objects.create(feed_item=feed_objs["Maize Silage"],
                                    purchase_date=today - timedelta(days=20),
                                    quantity=Decimal("5000"), unit_cost=Decimal("0.18"),
                                    supplier="GreenAgro Feeds", invoice_number="INV-551")
        FeedPurchase.objects.create(feed_item=feed_objs["Dairy Concentrate"],
                                    purchase_date=today - timedelta(days=12),
                                    quantity=Decimal("2000"), unit_cost=Decimal("0.70"),
                                    supplier="Bluegrass Mills", invoice_number="INV-552")
        self.stdout.write("  Feed records seeded")

        # ---------- Inventory ----------
        inv1 = InventoryItem.objects.create(
            name="Milking Machine Spare Set", category="Equipment", unit="set",
            current_stock=6, reorder_level=2, unit_cost=Decimal("85.00"),
            location="Store A",
        )
        InventoryItem.objects.create(name="Udder Wash", category="Supplies", unit="L",
                                     current_stock=15, reorder_level=20,
                                     unit_cost=Decimal("6.50"), location="Store B")
        StockTransaction.objects.create(item=inv1,
                                        transaction_date=today - timedelta(days=30),
                                        transaction_type="IN", quantity=4,
                                        reference="PO-220")
        self.stdout.write("  Inventory seeded")

        # ---------- Sales / Purchases ----------
        customers = [
            Customer.objects.create(name="Mr. Walker", customer_type="Individual",
                                    phone="+1 555 1010"),
            Customer.objects.create(name="Sunrise Dairy Co-op", customer_type="Cooperative",
                                    phone="+1 555 2020"),
            Customer.objects.create(name="Corner Cafe", customer_type="Retailer",
                                    phone="+1 555 3030"),
        ]
        for back in range(10):
            d = today - timedelta(days=back)
            Sale.objects.create(
                sale_type="Milk", sale_date=d, customer=customers[0],
                item_description="Fresh milk", quantity=Decimal("40.00"),
                unit_price=Decimal("1.10"), payment_status="Paid",
                amount_paid=Decimal("44.00"),
            )
        Sale.objects.create(
            sale_type="Animal", sale_date=today - timedelta(days=40),
            customer=customers[1], item_description="Heifer — Hope (H-0001)",
            quantity=1, unit_price=Decimal("850.00"), payment_status="Partial",
            amount_paid=Decimal("400.00"),
        )
        supplier1 = Supplier.objects.create(name="Agro Equipment Ltd", phone="+1 555 9090")
        Purchase.objects.create(purchase_date=today - timedelta(days=25),
                                supplier=supplier1, item_name="Milking buckets (set)",
                                category="Equipment", quantity=4,
                                unit_cost=Decimal("45.00"), payment_status="Paid",
                                amount_paid=Decimal("180.00"))
        self.stdout.write("  Sales & purchases seeded")

        # ---------- Finance ----------
        income_inc = FinanceCategory.objects.create(name="Milk Sales", category_type="Income")
        income_anim = FinanceCategory.objects.create(name="Animal Sales", category_type="Income")
        exp_feed = FinanceCategory.objects.create(name="Feed", category_type="Expense")
        exp_labour = FinanceCategory.objects.create(name="Labour", category_type="Expense")
        exp_vet = FinanceCategory.objects.create(name="Veterinary", category_type="Expense")
        exp_other = FinanceCategory.objects.create(name="Other", category_type="Expense")
        Transaction.objects.create(transaction_date=today - timedelta(days=2),
                                   category=income_inc, amount=Decimal("440.00"),
                                   description="10 days milk sales", payment_method="Bank Transfer")
        Transaction.objects.create(transaction_date=today - timedelta(days=40),
                                   category=income_anim, amount=Decimal("850.00"),
                                   description="Heifer sale (partial payment)",
                                   payment_method="Bank Transfer")
        Transaction.objects.create(transaction_date=today - timedelta(days=15),
                                   category=exp_feed, amount=Decimal("2300.00"),
                                   description="Silage + concentrate restock",
                                   payment_method="Mobile Money")
        Transaction.objects.create(transaction_date=today - timedelta(days=8),
                                   category=exp_vet, amount=Decimal("120.00"),
                                   description="Treatment supplies")
        self.stdout.write("  Finance seeded")

        # ---------- Employees ----------
        emp1 = Employee.objects.create(employee_code="E-001", name="John Doe",
                                       designation="Milker", department="Milking",
                                       phone="+1 555 7070", hire_date=today - timedelta(days=800),
                                       monthly_salary=Decimal("320.00"))
        emp2 = Employee.objects.create(employee_code="E-002", name="Jane Smith",
                                       designation="Herd Manager", department="Herd",
                                       phone="+1 555 7071", hire_date=today - timedelta(days=1500),
                                       monthly_salary=Decimal("450.00"))
        SalaryPayment.objects.create(employee=emp1,
                                     month=today.replace(day=1),
                                     amount=emp1.monthly_salary, paid_date=today)
        SalaryPayment.objects.create(employee=emp2,
                                     month=today.replace(day=1),
                                     amount=emp2.monthly_salary, bonus=Decimal("50.00"),
                                     deduction=Decimal("20.00"), paid_date=today)
        Advance.objects.create(employee=emp2, advance_date=today - timedelta(days=20),
                               amount=Decimal("80.00"), deduction_month=today.replace(day=1))
        self.stdout.write("  Employees seeded")

        # ---------- Delivery notes & invoices ----------
        dn1 = DeliveryNote.objects.create(
            customer=customers[1], your_order_no="PO-7781",
            your_order_date=today - timedelta(days=5),
            dispatched_date=today - timedelta(days=4),
            driver_name="M. Getahun", branch_name="Addis Branch",
            description_of_goods="Fresh pasteurised milk, 4% butterfat",
            qty_delivered=Decimal("120.00"), checked_by="H. Ali",
            supervisor_name="A. Bekele", supervisor_signed=True,
        )
        DeliveryNote.objects.create(
            customer=customers[2], dispatched_date=today - timedelta(days=1),
            driver_name="T. Solomon", branch_name="Central Branch",
            description_of_goods="Fresh milk & yogurt", qty_delivered=Decimal("60.00"),
            checked_by="H. Ali", supervisor_signed=True,
        )
        inv = Invoice.objects.create(
            invoice_date=today - timedelta(days=3), customer=customers[1],
            ship_to="Sunrise Dairy Co-op", delivery_note=dn1,
            driver_name=dn1.driver_name, tax_percent=Decimal("5.00"), status="Issued",
        )
        InvoiceItem.objects.create(
            invoice=inv, item_code="MILK-4%", description="Fresh milk (litres)",
            quantity=Decimal("120.00"), unit_price=Decimal("1.20"),
        )
        InvoiceItem.objects.create(
            invoice=inv, item_code="YGRT-500", description="Plain yogurt (500ml)",
            quantity=Decimal("40.00"), unit_price=Decimal("1.50"),
        )
        self.stdout.write("  Delivery notes & invoices seeded")

        self.stdout.write(self.style.SUCCESS(
            "Seed complete. Log in and explore the dashboard."))