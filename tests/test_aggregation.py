from supplier import Supplier
from product import PhysicalProduct
from inventory import Inventory


def test_aggregation():
    # Create the product before creating the inventories.
    supplier = Supplier(
        "S001",
        "Tech Supplies",
        "sales@techsupplies.com"
    )

    product = PhysicalProduct(
        "P001",
        "Laptop",
        1200.0,
        10,
        2.0,
        supplier
    )

    inventory_a = Inventory()
    inventory_b = Inventory()

    # Add the product to Inventory A.
    inventory_a.add_product(product)
    assert inventory_a.find_product("P001") is product
    print("Product added to Inventory A.")

    # Remove the product from Inventory A.
    inventory_a.remove_product("P001")
    assert inventory_a.find_product("P001") is None
    print("Product removed from Inventory A.")

    # The product still exists and remains usable.
    product.display_information()

    # Add the same product object to Inventory B.
    inventory_b.add_product(product)
    assert inventory_b.find_product("P001") is product
    print("Same product added to Inventory B.")

    print("Aggregation test passed.")


if __name__ == "__main__":
    test_aggregation()