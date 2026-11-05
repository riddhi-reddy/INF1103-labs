import math

from file_handler import load_inventory, save_inventory
from product import PhysicalProduct, DigitalProduct


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

#Add a helper for weight and download size
def read_positive_number(prompt):
    while True:
        try:
            value = float(input(prompt))

            if math.isfinite(value) and value > 0:
                return value

            print("Enter a number greater than zero.")

        except ValueError:
            print("Enter a valid number.")

def add_product(inventory):
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")

    product_type = input("Choose product type: ").strip()

    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return

    product_id = read_non_empty("Product ID: ").upper()

    if inventory.search_product(product_id) is not None:
        print("Product ID already exists.")
        return

    name = read_non_empty("Product Name: ")
    price = read_price()
    stock = read_stock("Stock Quantity: ")

    if product_type == "1":
        weight = read_positive_number("Weight in kg: ")

        product = PhysicalProduct(
            product_id, name, price, stock, weight
        )

    else:
        download_size = read_positive_number(
            "Download size in MB: "
        )

        product = DigitalProduct(
            product_id, name, price, stock, download_size
        )

    inventory.add_product(product)

    print("Product added successfully!")
    product.display_information()
    print(product.get_fulfilment_info())


def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = read_non_empty("Enter Product ID: ").upper()

    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")

    quantity = read_stock("New Stock Quantity: ")
    inventory.update_stock(product_id, quantity)

    print("Stock updated successfully!")


def display_search_result(inventory):
    print("\nSearch Product")
    product_id = read_non_empty("Enter Product ID: ").upper()

    product = inventory.search_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found")
    print("-" * 70)
    product.display_information()
    print("-" * 70)


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

    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        AttributeError
    ) as error:
        print(f"Unable to load inventory: {error}")
        print("Check inventory.json before running the program again.")
        return

    while True:
        display_menu()
        option = input("Enter option: ").strip()

        if option == "1":
            inventory.display_all()

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