from product import Product, PhysicalProduct, DigitalProduct
from supplier import Supplier
from inventory import Inventory


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())
    print()


def test_lsp() -> None:
    supplier = Supplier(
        "S001",
        "Tech Supplies",
        "sales@techsupplies.com"
    )

    laptop = PhysicalProduct(
        "P001",
        "Laptop",
        1200.0,
        10,
        2.0,
        supplier
    )

    ebook = DigitalProduct(
        "P002",
        "Python E-book",
        25.0,
        50,
        15.0,
        supplier
    )

    # The same function accepts both Product subclasses.
    print("PRODUCT SUBSTITUTABILITY")
    print("-" * 40)

    show_product_details(laptop)
    show_product_details(ebook)

    # Inventory manages both through the Product abstraction.
    inventory = Inventory()
    inventory.add_product(laptop)
    inventory.add_product(ebook)

    assert inventory.find_product("P001") is laptop
    assert inventory.find_product("P002") is ebook

    inventory.display_all()

    # Both subclasses preserve the stock update behaviour.
    inventory.update_stock("P001", 8)
    inventory.update_stock("P002", 45)

    assert laptop.get_stock() == 8
    assert ebook.get_stock() == 45

    print("\nUPDATED STOCK")
    print(f"Laptop stock: {laptop.get_stock()}")
    print(f"E-book stock: {ebook.get_stock()}")

    # Both reject negative stock, as required by Product.
    products: list[Product] = [laptop, ebook]

    for product in products:
        previous_stock = product.get_stock()

        try:
            product.update_stock(-1)
        except ValueError:
            assert product.get_stock() == previous_stock
            print(
                f"{product.get_name()}: "
                "negative stock rejected correctly."
            )
        else:
            raise AssertionError("Negative stock should be rejected.")

    # Normal removal works for both subclasses.
    inventory.remove_product("P001")
    inventory.remove_product("P002")

    assert inventory.find_product("P001") is None
    assert inventory.find_product("P002") is None

    print("\nLSP test passed.")


if __name__ == "__main__":
    test_lsp()