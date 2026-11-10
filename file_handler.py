import json
from pathlib import Path

from inventory import Inventory
from order import Order
from product import Product, PhysicalProduct, DigitalProduct
from supplier import Supplier


INVENTORY_FILE = Path(__file__).resolve().parent / "inventory.json"


def load_system() -> tuple[
    dict[str, Supplier], dict[str, Product],
    dict[str, Inventory], dict[str, Order]
]:
    suppliers: dict[str, Supplier] = {}
    products: dict[str, Product] = {}
    inventories: dict[str, Inventory] = {}
    orders: dict[str, Order] = {}

    if not INVENTORY_FILE.exists():
        return suppliers, products, inventories, orders

    with INVENTORY_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict) or data.get("version") != 2:
        raise ValueError("Expected the current version-2 inventory.json format.")
    for item in data["suppliers"]:
        suppliers[item["id"]] = Supplier(
            item["id"], item["name"], item["contact_email"]
        )
    records = data["products"]

    for item in records:
        supplier = suppliers[item["supplier_id"]]
        details = (item["id"], item["name"], item["price"], item["stock"])
        product: Product
        if item["type"] == "physical":
            product = PhysicalProduct(*details, item["weight"], supplier)
        elif item["type"] == "digital":
            product = DigitalProduct(*details, item["download_size"], supplier)
        else:
            raise ValueError("Unknown product type.")
        products[product.get_product_id()] = product

    for item in data["inventories"]:
        inventory = Inventory()
        for product_id in item["product_ids"]:
            inventory.add_product(products[product_id])
        # Read existing IDs as names, so current saved files still load.
        name = item.get("name", item.get("id"))
        if not isinstance(name, str) or not name.strip():
            raise ValueError("An inventory must have a name.")
        if name in inventories:
            raise ValueError("Duplicate inventory name.")
        inventories[name] = inventory
    for item in data["orders"]:
        order = Order(item["id"])
        for line in item["lines"]:
            order.add_order_line(products[line["product_id"]], line["quantity"])
        orders[order.order_id] = order

    print("Saved data loaded.")
    return suppliers, products, inventories, orders


def save_system(
    suppliers: dict[str, Supplier], products: dict[str, Product],
    inventories: dict[str, Inventory], orders: dict[str, Order]
) -> bool:
    data = {"version": 2, "suppliers": [], "products": [],
            "inventories": [], "orders": []}

    for supplier in suppliers.values():
        data["suppliers"].append({
            "id": supplier.get_supplier_id(), "name": supplier.get_name(),
            "contact_email": supplier.get_contact_email()
        })

    for product in products.values():
        item = {
            "id": product.get_product_id(), "name": product.get_name(),
            "price": product.get_price(), "stock": product.get_stock(),
            "supplier_id": product.get_supplier().get_supplier_id()
        }
        if isinstance(product, PhysicalProduct):
            item.update(type="physical", weight=product.get_weight())
        elif isinstance(product, DigitalProduct):
            item.update(type="digital", download_size=product.get_download_size())
        else:
            raise TypeError("Unsupported product type.")
        data["products"].append(item)

    for name, inventory in inventories.items():
        product_ids: list[str] = []
        for product in inventory.get_products():
            product_ids.append(product.get_product_id())
        data["inventories"].append({"name": name, "product_ids": product_ids})

    for order in orders.values():
        lines = []
        for line in order.order_lines:
            lines.append({"product_id": line.product.get_product_id(),
                          "quantity": line.quantity})
        data["orders"].append({"id": order.order_id, "lines": lines})

    temporary = INVENTORY_FILE.with_suffix(".json.tmp")
    try:
        with temporary.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, allow_nan=False)
        temporary.replace(INVENTORY_FILE)
    except (OSError, ValueError) as error:
        print(f"Unable to save: {error}")
        return False

    print("All data saved.")
    return True
