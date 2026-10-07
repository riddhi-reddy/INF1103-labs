"""Load and display inventory from a JSON file."""

import json
from pathlib import Path


inventory_file = Path(__file__).resolve().parent / "inventory.json"


def load_inventory():
    """Load existing inventory or return an empty list."""
    if not inventory_file.exists():
        print("inventory.json not found. Starting with empty inventory.")
        return []

    print("inventory.json found.")

    with inventory_file.open("r", encoding="utf-8") as file:
        inventory = json.load(file)

    print("Inventory loaded successfully.")
    return inventory


def display_all(inventory):
    """Display every product."""
    if not inventory:
        print("Inventory is empty.")
        return

    print("\nCurrent Inventory")
    print("-" * 60)

    for product in inventory:
        print(
            f"ID: {product['id']} | "
            f"Name: {product['name']} | "
            f"Price: ${product['price']:.2f} | "
            f"Stock: {product['stock']}"
        )

    print("-" * 60)


def main():
    """Load and display stored products."""
    inventory = load_inventory()
    display_all(inventory)


if __name__ == "__main__":
    main()