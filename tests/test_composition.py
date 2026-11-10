from supplier import Supplier
from product import PhysicalProduct
from order import Order


def test_composition() -> None:
    # Prediction:
    # Adding the same product once to each of two orders creates
    # two separate OrderLine objects referring to one Product object.

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

    mouse = PhysicalProduct(
        "P002",
        "Mouse",
        25.0,
        20,
        0.1,
        supplier
    )

    # Order A creates its own order lines.
    order_a = Order("ORD001")
    order_a.add_order_line(laptop, 2)
    order_a.add_order_line(mouse, 3)

    print(f"Order: {order_a.order_id}")
    print()

    for order_line in order_a.order_lines:
        order_line.product.display_information()
        print(f"Quantity ordered: {order_line.quantity}")
        print(f"Subtotal: ${order_line.calculate_subtotal():.2f}")
        print()

    assert order_a.calculate_total() == 2475.0
    print(f"Order total: ${order_a.calculate_total():.2f}")

    # Order B creates its own line for the same laptop.
    order_b = Order("ORD002")
    order_b.add_order_line(laptop, 1)

    assert order_b.calculate_total() == 1200.0

    same_order_line = (
        order_a.order_lines[0] is order_b.order_lines[0]
    )

    same_product = (
        order_a.order_lines[0].product
        is order_b.order_lines[0].product
    )

    assert same_order_line is False
    assert same_product is True

    print(f"\nSame OrderLine object: {same_order_line}")
    print(f"Same Product object: {same_product}")

    # Remove the laptop line through Order A.
    order_a.remove_order_line(0)

    assert len(order_a.order_lines) == 1
    assert order_a.order_lines[0].product is mouse
    assert order_a.calculate_total() == 75.0

    # Order B and the original laptop remain usable.
    assert order_b.order_lines[0].product is laptop
    assert order_b.calculate_total() == 1200.0

    print("\nAfter removing the laptop line from Order A:")
    print(f"Order A total: ${order_a.calculate_total():.2f}")
    print(f"Order B total: ${order_b.calculate_total():.2f}")

    print("\nThe original laptop product still works:")
    laptop.display_information()

    print("\nComposition test passed.")


if __name__ == "__main__":
    test_composition()