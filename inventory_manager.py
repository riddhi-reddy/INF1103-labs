"""Interactive entry point for the inventory and order application."""
import math

from file_handler import load_system, save_system
from inventory import Inventory
from order import Order
from product import Product, PhysicalProduct, DigitalProduct
from supplier import Supplier


def read_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")


def read_integer(prompt: str, minimum: int = 0) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value >= minimum:
                return value
        except ValueError:
            pass
        print(f"Enter a whole number of {minimum} or more.")


def read_number(prompt: str, positive: bool = False) -> float:
    while True:
        try:
            value = float(input(prompt))
            if math.isfinite(value):
                if (positive and value > 0) or (not positive and value >= 0):
                    return value
        except ValueError:
            pass
        if positive:
            print("Enter a finite number greater than zero.")
        else:
            print("Enter a finite number of zero or more.")


def create_supplier(suppliers: dict[str, Supplier]) -> Supplier:
    while True:
        supplier_id = read_non_empty("Supplier ID: ").upper()
        if supplier_id not in suppliers:
            break
        print("That supplier ID already exists.")
    supplier = Supplier(
        supplier_id,
        read_non_empty("Supplier name: "),
        read_non_empty("Contact email: ")
    )
    suppliers[supplier_id] = supplier
    print("Supplier created.")
    return supplier


def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier:
    while True:
        print("\nCHOOSE SUPPLIER")
        choices: list[Supplier] = list(suppliers.values())
        for number, supplier in enumerate(choices, start=1):
            print(f"{number}. {supplier.get_name()} (ID: {supplier.get_supplier_id()})")
        print(f"{len(choices) + 1}. Create a new supplier")
        print("0. Cancel / go back")
        option = read_integer("Choose an option: ")
        if option == 0:
            raise ValueError("Action cancelled.")
        if option == len(choices) + 1:
            return create_supplier(suppliers)
        if 1 <= option <= len(choices):
            return choices[option - 1]
        print("Choose one of the displayed options.")


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())
    print(f"Supplier: {product.get_supplier().get_name()}")


def choose_number(count: int, prompt: str) -> int:
    while True:
        number = read_integer(prompt)
        if number <= count:
            return number
        print("Choose a number from the displayed list, or 0 to go back.")


def choose_product(products: dict[str, Product]) -> Product | None:
    if not products:
        print("No products available here. Create or add a product first.")
        return None
    choices: list[Product] = list(products.values())
    print("\nSELECT A PRODUCT")
    for number, product in enumerate(choices, start=1):
        print(f"{number}. {product.get_name()} (Product ID: {product.get_product_id()})")
    print("0. Back")
    number = choose_number(len(choices), "Select product NUMBER: ")
    if number == 0:
        return None
    return choices[number - 1]


def create_product(
    products: dict[str, Product], suppliers: dict[str, Supplier]
) -> None:
    print("1. Physical product\n2. Digital product")
    product_type = input("Choose product type: ").strip()
    if product_type not in ("1", "2"):
        print("Invalid product type.")
        return
    product_id = read_non_empty("Product ID: ").upper()
    if product_id in products:
        print("Product ID already exists.")
        return
    supplier = choose_supplier(suppliers)
    name = read_non_empty("Product name: ")
    price = read_number("Price: ")
    stock = read_integer("Stock quantity: ")
    product: Product
    if product_type == "1":
        product = PhysicalProduct(
            product_id, name, price, stock,
            read_number("Weight in kg: ", positive=True), supplier
        )
    else:
        product = DigitalProduct(
            product_id, name, price, stock,
            read_number("Download size in MB: ", positive=True), supplier
        )
    products[product_id] = product
    print("Product created in the catalogue.")
    print("To add it to an inventory, open Inventories from the main menu.")
    show_product_details(product)


def choose_inventory(inventories: dict[str, Inventory]) -> Inventory | None:
    if not inventories:
        print("No inventories yet. Create one in the Inventories section.")
        return None
    choices: list[str] = list(inventories)
    print("\nSELECT AN INVENTORY")
    for number, inventory_id in enumerate(choices, start=1):
        print(f"{number}. {inventory_id}")
    print("0. Back")
    number = choose_number(len(choices), "Select inventory NUMBER: ")
    if number == 0:
        return None
    return inventories[choices[number - 1]]


def manage_inventory(
    inventory: Inventory,
    inventories: dict[str, Inventory],
    products: dict[str, Product]
) -> None:
    inventory_name = ""
    for inventory_id, current in inventories.items():
        if current is inventory:
            inventory_name = inventory_id
            break
    while True:
        print(f"\nMANAGING INVENTORY: {inventory_name}")
        print("1. Display products\n2. Add product from catalogue")
        print("3. Remove product\n4. Transfer product to another inventory")
        print("5. Update stock\n6. Search product\n0. Back")
        option = read_non_empty("Menu option: ")
        if option == "0":
            return
        if option == "1":
            if not inventory.get_products():
                print("Inventory is empty.")
            # One Product collection; each subclass supplies its own behaviour.
            for product in inventory.get_products():
                show_product_details(product)
        elif option == "2":
            product = choose_product(products)
            if product is not None:
                inventory.add_product(product)
                print(f"{product.get_name()} added to inventory {inventory_name}.")
        elif option in ("3", "4", "5", "6"):
            available: dict[str, Product] = {}
            for current in inventory.get_products():
                available[current.get_product_id()] = current
            product = choose_product(available)
            if product is None:
                continue
            product_id = product.get_product_id()
            if option == "3":
                inventory.remove_product(product_id)
                print("Removed from inventory. The product remains in the catalogue.")
            elif option == "4":
                destination = choose_inventory(inventories)
                if destination is None:
                    continue
                if destination is inventory:
                    print("Choose a different destination inventory.")
                    continue
                # Add first so an unsuccessful destination update cannot lose the source.
                destination.add_product(product)
                inventory.remove_product(product_id)
                print("The same product object was transferred.")
            elif option == "5":
                inventory.update_stock(product_id, read_integer("New stock quantity: "))
                print("Stock updated.")
            else:
                show_product_details(product)
        else:
            print("Invalid option.")


def display_order(order: Order) -> None:
    print(f"\nOrder: {order.order_id}")
    if not order.order_lines:
        print("Order has no lines.")
    for number, line in enumerate(order.order_lines, start=1):
        print(f"\nLine {number}")
        show_product_details(line.product)
        print(f"Quantity ordered: {line.quantity}")
        print(f"Subtotal: ${line.calculate_subtotal():.2f}")
    print(f"Order total: ${order.calculate_total():.2f}")


def manage_order(order: Order, products: dict[str, Product]) -> None:
    while True:
        print(f"\nMANAGING ORDER: {order.order_id}")
        print("1. View order and total\n2. Add product to order")
        print("3. Remove order line\n0. Back")
        option = read_non_empty("Menu option: ")
        if option == "0":
            return
        if option == "1":
            display_order(order)
        elif option == "2":
            product = choose_product(products)
            if product is not None:
                quantity = read_integer("Quantity ordered: ", minimum=1)
                # Order creates the OrderLine internally.
                order.add_order_line(product, quantity)
                print("Order line created.")
                display_order(order)
        elif option == "3":
            if not order.order_lines:
                print("Order has no lines.")
                continue
            display_order(order)
            number = read_integer("Line number to remove: ", minimum=1)
            if number > len(order.order_lines):
                print("Line number not found.")
                continue
            order.remove_order_line(number - 1)
            print("Order line removed. The product remains in the catalogue.")
        else:
            print("Invalid option.")


def suppliers_menu(suppliers: dict[str, Supplier]) -> None:
    while True:
        print("\nSUPPLIERS")
        if not suppliers:
            print("No suppliers yet.")
        for supplier in suppliers.values():
            supplier.display_information()
        print("\n1. Create supplier\n0. Main menu")
        option = read_non_empty("Supplier menu option: ")
        if option == "0":
            return
        if option == "1":
            create_supplier(suppliers)
        else:
            print("Choose 1 or 0.")


def products_menu(
    products: dict[str, Product], suppliers: dict[str, Supplier]
) -> None:
    while True:
        print("\nPRODUCT CATALOGUE")
        if not products:
            print("No products yet.")
        for product in products.values():
            show_product_details(product)
            print()
        print("1. Create product\n0. Main menu")
        option = read_non_empty("Product menu option: ")
        if option == "0":
            return
        if option == "1":
            create_product(products, suppliers)
        else:
            print("Choose 1 or 0.")


def inventories_menu(
    inventories: dict[str, Inventory], products: dict[str, Product]
) -> None:
    while True:
        print("\nINVENTORIES")
        if not inventories:
            print("No inventories yet.")
        for name, inventory in inventories.items():
            print(f"{name}: {len(inventory.get_products())} product(s)")
        print("\n1. Create inventory\n2. Open inventory\n0. Main menu")
        option = read_non_empty("Inventory menu option: ")
        if option == "0":
            return
        if option == "1":
            name = read_non_empty("Inventory name (e.g. Store A): ")
            duplicate = False
            for existing_name in inventories:
                if existing_name.casefold() == name.casefold():
                    duplicate = True
            if duplicate:
                print("That inventory name already exists.")
            else:
                inventories[name] = Inventory()
                print(f"Inventory '{name}' created.")
        elif option == "2":
            inventory = choose_inventory(inventories)
            if inventory is not None:
                manage_inventory(inventory, inventories, products)
        else:
            print("Choose 1, 2 or 0.")


def orders_menu(orders: dict[str, Order], products: dict[str, Product]) -> None:
    while True:
        print("\nORDERS")
        if not orders:
            print("No orders yet.")
        for order in orders.values():
            print(f"{order.order_id}: {len(order.order_lines)} line(s), "
                  f"total ${order.calculate_total():.2f}")
        print("\n1. Create order\n2. Open order\n0. Main menu")
        option = read_non_empty("Order menu option: ")
        if option == "0":
            return
        if option == "1":
            order_id = read_non_empty("New order ID: ").upper()
            if order_id in orders:
                print("Order ID already exists.")
            else:
                orders[order_id] = Order(order_id)
                manage_order(orders[order_id], products)
        elif option == "2":
            choices: list[str] = list(orders)
            if not choices:
                print("Create an order first.")
                continue
            for number, order_id in enumerate(choices, start=1):
                print(f"{number}. {order_id}")
            print("0. Back")
            number = choose_number(len(choices), "Select order NUMBER: ")
            if number != 0:
                manage_order(orders[choices[number - 1]], products)
        else:
            print("Choose 1, 2 or 0.")


def main() -> None:
    try:
        suppliers, products, inventories, orders = load_system()
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        print(f"Unable to load data: {error}")
        print("Your saved file has not been changed.")
        return

    while True:
        print("\nINVENTORY MANAGEMENT SYSTEM")
        print("1. Suppliers\n2. Products\n3. Inventories\n4. Orders")
        print("5. Save all data\n0. Save and exit")
        option = read_non_empty("Main menu option: ")
        try:
            if option == "1":
                suppliers_menu(suppliers)
            elif option == "2":
                products_menu(products, suppliers)
            elif option == "3":
                inventories_menu(inventories, products)
            elif option == "4":
                orders_menu(orders, products)
            elif option in ("5", "0"):
                if save_system(suppliers, products, inventories, orders):
                    if option == "0":
                        print("Data saved. Goodbye.")
                        return
            else:
                print("Choose an option from 0 to 5.")
        except (OSError, ValueError, KeyError, TypeError, IndexError) as error:
            print(f"Action stopped: {error}")


if __name__ == "__main__":
    main()
