from supplier import Supplier
from product import Product, PhysicalProduct, DigitalProduct
from inventory import Inventory


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())
    print()


def test_polymorphism() -> None:
    # Prediction:
    # Laptop: This product requires physical shipping.
    # E-book: This product is delivered digitally.

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

    inventory = Inventory()
    inventory.add_product(laptop)
    inventory.add_product(ebook)

    # One Product collection and one loop for both subclasses.
    products: list[Product] = inventory.get_products()

    print("PRODUCT DETAILS")
    print("-" * 40)

    for product in products:
        show_product_details(product)

    # Compare actual fulfilment messages with the predictions.
    assert laptop.get_fulfilment_info() == (
        "This product requires physical shipping."
    )

    assert ebook.get_fulfilment_info() == (
        "This product is delivered digitally."
    )

    print("Both fulfilment messages match the predictions.")
    print("Polymorphism test passed.")


if __name__ == "__main__":
    test_polymorphism()