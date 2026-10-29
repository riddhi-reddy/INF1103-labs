import json
from pathlib import Path

from inventory import Inventory
from product import Product


INVENTORY_FILE = Path(__file__).resolve().parent / "inventory.json"


def load_inventory():
    inventory = Inventory()

    if not INVENTORY_FILE.exists():
        print("inventory.json not found. Starting with empty inventory.")
        return inventory

    print("inventory.json found.")

    with INVENTORY_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Inventory JSON must contain a list.")

    for item in data:
        product = Product(
            item["id"],
            item["name"],
            item["price"],
            item["stock"]
        )

        inventory.add_product(product)

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory):
    data = []

    for product in inventory.get_products():
        data.append({
            "id": product.get_product_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock()
        })

    try:
        with INVENTORY_FILE.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    except OSError as error:
        print(f"Unable to save inventory: {error}")
        return False

    print("Inventory saved successfully to inventory.json.")
    return True