import unittest

from discounts.bulk_discount import BulkDiscount
from order import Order
from discounts.percentage_discount import PercentageDiscount
from products.physical_product import PhysicalProduct
from discounts.student_discount import StudentDiscount
from supplier import Supplier


class TestDiscountStrategies(unittest.TestCase):
    def setUp(self) -> None:
        supplier = Supplier("S001", "Test Supplier", "test@example.com")
        product = PhysicalProduct("P001", "Lamp", 125.0, 10, 1.0, supplier)
        self.order = Order("ORD001")
        self.order.add_order_line(product, 2)

    def test_default_returns_full_total(self) -> None:
        self.assertEqual(self.order.calculate_total(), 250.0)

    def test_can_switch_discount_on_existing_order(self) -> None:
        self.order.set_discount(BulkDiscount(200, 20))
        self.assertEqual(self.order.calculate_total(), 230.0)

        self.order.set_discount(PercentageDiscount(10))
        self.assertEqual(self.order.calculate_total(), 225.0)

    def test_student_discount_works_with_order(self) -> None:
        self.order.set_discount(StudentDiscount())
        self.assertEqual(self.order.calculate_total(), 225.0)