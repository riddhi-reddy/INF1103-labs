import json
import math
from pathlib import Path


inventory_file = Path(__file__).resolve().parent / "inventory.json"


def load_inventory():
    if not inventory_file.exists():
        print("inventory.json not found. Starting with empty inventory.")
        return []

    print("inventory.json found.")

    with inventory_file.open("r", encoding="utf-8") as file:
        inventory = json.load(file)

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory):
    try:
        with inventory_file.open("w", encoding="utf-8") as file:
            json.dump(inventory, file, indent=4)

    except OSError as error:
        print(f"Unable to save inventory: {error}")
        return False

    print("Inventory saved successfully to inventory.json.")
    return True


def search_product(inventory, product_id):
    for product in inventory:
        if product["id"] == product_id:
            return product

    return None


def read_non_empty(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def read_price():
    while True:
        try:
            price = float(input("Price: "))

            if math.isfinite(price) and price >= 0:
                return price

            print("Enter a valid price of zero or more.")

        except ValueError:
            print("Enter a number, such as 25.50.")


def read_stock(prompt):
    while True:
        try:
            stock = int(input(prompt))

            if stock >= 0:
                return stock

            print("Stock cannot be negative.")

        except ValueError:
            print("Enter a whole number, such as 10.")


def add_product(inventory):
    print("\nAdd New Product")
    product_id = read_non_empty("Product ID: ").upper()

    if search_product(inventory, product_id) is not None:
        print("Product ID already exists.")
        return

    name = read_non_empty("Product Name: ")
    price = read_price()
    stock = read_stock("Stock Quantity: ")

    product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    }

    inventory.append(product)
    print("Product added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = read_non_empty("Enter Product ID: ").upper()
    product = search_product(inventory, product_id)

    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")

    product["stock"] = read_stock("New Stock Quantity: ")
    print("Stock updated successfully!")


def display_all(inventory):
    if not inventory:
        print("\nInventory is empty.")
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


def display_search_result(inventory):
    print("\nSearch Product")
    product_id = read_non_empty("Enter Product ID: ").upper()
    product = search_product(inventory, product_id)

    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found")
    print("-" * 40)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print("-" * 40)


def display_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    try:
        inventory = load_inventory()

    except (OSError, json.JSONDecodeError) as error:
        print(f"Unable to load inventory: {error}")
        print("Check inventory.json before running the program again.")
        return

    while True:
        display_menu()
        option = input("Enter option: ").strip()

        if option == "1":
            display_all(inventory)

        elif option == "2":
            add_product(inventory)

        elif option == "3":
            update_stock(inventory)

        elif option == "4":
            display_search_result(inventory)

        elif option == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)

        elif option == "6":
            print("\nSaving inventory before exit...")

            if save_inventory(inventory):
                print("Thank you for using Inventory Management System.")
                print("Program terminated.")
                break

            print("Inventory was not saved. Please retry before exiting.")

        else:
            print("Invalid option. Choose a number from 1 to 6.")


if __name__ == "__main__":
    main()