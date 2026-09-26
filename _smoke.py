"""Smoke test: hit every application page and report HTTP status codes.

Run:  python _smoke.py
"""
import os

os.environ["DJANGO_ALLOWED_HOSTS"] = "localhost,127.0.0.1,testserver"

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()
user = User.objects.filter(username="admin").first()
if user is None:
    user = User.objects.create_superuser("admin", "admin@example.com", "admin123")

client = Client()
client.force_login(user)

URLS = [
    "/",
    "/accounts/profile/",
    # Herd
    "/herd/",
    "/herd/animals/add/",
    "/herd/breeds/",
    "/herd/breeds/add/",
    "/herd/movements/",
    "/herd/movements/add/",
    "/herd/history/",
    # Milk
    "/milk/morning/",
    "/milk/morning/add/",
    "/milk/evening/",
    "/milk/evening/add/",
    "/milk/yield/",
    "/milk/yield/targets/",
    "/milk/lactations/",
    "/milk/lactations/add/",
    "/milk/quality/",
    "/milk/quality/add/",
    # Breeding
    "/breeding/heat/",
    "/breeding/heat/add/",
    "/breeding/insemination/",
    "/breeding/insemination/add/",
    "/breeding/pregnancy/",
    "/breeding/pregnancy/add/",
    "/breeding/calving/",
    "/breeding/calving/add/",
    # Health
    "/health/medicine/",
    "/health/medicine/add/",
    "/health/vaccination/",
    "/health/vaccination/add/",
    "/health/treatment/",
    "/health/treatment/add/",
    "/health/vet-visits/",
    "/health/vet-visits/add/",
    # Feed
    "/feed/items/",
    "/feed/items/add/",
    "/feed/consumption/",
    "/feed/consumption/add/",
    "/feed/purchases/",
    "/feed/purchases/add/",
    "/feed/cost/",
    # Inventory
    "/inventory/",
    "/inventory/items/add/",
    "/inventory/movements/",
    "/inventory/movements/add/",
    # Sales
    "/sales/",
    "/sales/add/",
    "/sales/customers/",
    "/sales/customers/add/",
    # Purchases
    "/purchases/",
    "/purchases/add/",
    "/purchases/suppliers/",
    "/purchases/suppliers/add/",
    # Finance
    "/finance/",
    "/finance/transactions/add/",
    "/finance/categories/",
    "/finance/categories/add/",
    # Employees
    "/employees/",
    "/employees/directory/",
    "/employees/directory/add/",
    "/employees/attendance/",
    "/employees/attendance/add/",
    "/employees/leave/",
    "/employees/leave/add/",
    "/employees/expenses/",
    "/employees/expenses/add/",
    "/employees/salaries/",
    "/employees/salaries/add/",
    "/employees/advances/",
    "/employees/advances/add/",
    "/employees/reports/",
    # Deliveries & invoicing
    "/deliveries/",
    "/deliveries/add/",
    "/invoicing/",
    "/invoicing/add/",
    # Exports
    "/milk/export/",
    "/deliveries/export/",
    "/invoicing/export/",
    "/employees/directory/export/",
        # Reports
    "/reports/milk/",
    "/reports/milk/?format=xlsx",
    "/reports/herd/",
    "/reports/herd/?format=xlsx",
    "/reports/breeding/",
    "/reports/breeding/?format=xlsx",
    "/reports/health/",
    "/reports/health/?format=xlsx",
    "/reports/feed/",
    "/reports/feed/?format=xlsx",
    "/reports/finance/",
    "/reports/finance/?format=xlsx",
    "/reports/sales/",
    "/reports/sales/?format=xlsx",
    "/reports/inventory/",
    "/reports/inventory/?format=xlsx",
    # HR reports export
    "/employees/reports/",
    "/employees/reports/?format=xlsx",
    "/reports/herd/",
    "/reports/breeding/",
    "/reports/health/",
    "/reports/feed/",
    "/reports/finance/",
    "/reports/sales/",
    "/reports/inventory/",
    # Admin
    "/admin/",
]

# Detail / print / edit pages for the first delivery note & invoice
from deliveries.models import DeliveryNote
from invoicing.models import Invoice

dn_id = DeliveryNote.objects.values_list("id", flat=True).first()
inv_id = Invoice.objects.values_list("id", flat=True).first()
if dn_id:
    URLS += [f"/deliveries/{dn_id}/", f"/deliveries/{dn_id}/print/", f"/deliveries/{dn_id}/edit/"]
if inv_id:
    URLS += [f"/invoicing/{inv_id}/", f"/invoicing/{inv_id}/print/", f"/invoicing/{inv_id}/edit/"]

fails = []
for url in URLS:
    try:
        response = client.get(url)
    except Exception as exc:  # noqa: BLE001
        fails.append((url, f"EXC {exc!r}"))
        print(f"EXC  {url} -> {exc!r}")
        continue
    tag = "OK " if response.status_code == 200 else "FAIL"
    print(f"{tag} {response.status_code} {url}")
    if response.status_code != 200:
        fails.append((url, response.status_code))

if fails:
    print(f"\nRESULT: {len(fails)} FAILURES -> {fails}")
    raise SystemExit(1)
print("\nRESULT: ALL PAGES OK")