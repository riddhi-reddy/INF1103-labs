import json
from pathlib import Path

from inventory import Inventory
from product import PhysicalProduct, DigitalProduct


INVENTORY_FILE = Path(__file__).resolve().parent / "inventory.json"


def load_inventory():
    inventory = Inventory()

    if not INVENTORY_FILE.exists():
        print("inventory.json not found. Starting with empty inventory.")
        return inventory

    with INVENTORY_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Inventory JSON must contain a list.")

    for item in data:
        if item["type"] == "physical":
            product = PhysicalProduct(
                item["id"],
                item["name"],
                item["price"],
                item["stock"],
                item["weight"]
            )

        elif item["type"] == "digital":
            product = DigitalProduct(
                item["id"],
                item["name"],
                item["price"],
                item["stock"],
                item["download_size"]
            )

        else:
            raise ValueError(
                f"Unknown product type: {item['type']}"
            )

        inventory.add_product(product)

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory):
    data = []

    for product in inventory.get_products():
        item = {
            "id": product.get_product_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock()
        }

        if isinstance(product, PhysicalProduct):
            item["type"] = "physical"
            item["weight"] = product.get_weight()

        elif isinstance(product, DigitalProduct):
            item["type"] = "digital"
            item["download_size"] = product.get_download_size()

        else:
            raise TypeError("Unsupported product type.")

        data.append(item)

    try:
        with INVENTORY_FILE.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    except OSError as error:
        print(f"Unable to save inventory: {error}")
        return False

    print("Inventory saved successfully to inventory.json.")
    return True