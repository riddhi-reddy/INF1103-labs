from supplier import Supplier
from product import PhysicalProduct, DigitalProduct


def test_association() -> None:
    supplier = Supplier(
        "S001",
        "Tech Supplies",
        "sales@techsupplies.com"
    )

    physical = PhysicalProduct(
        "P001", "Laptop", 1200.0, 10, 2.0, supplier
    )

    digital = DigitalProduct(
        "D001", "Python Guide", 20.0, 100, 15.0, supplier
    )

    print("Both products share the same Supplier object:")
    print(physical.get_supplier() is digital.get_supplier())

    del supplier
    print("\nThe supplier variable has been deleted.")

    print("\nPhysical product supplier:")
    physical.get_supplier().display_information()

    print("\nDigital product supplier:")
    digital.get_supplier().display_information()


if __name__ == "__main__":
    test_association()