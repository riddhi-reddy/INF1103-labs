import unittest

from order_line import OrderLine
from product import PhysicalProduct
from supplier import Supplier


class TestValidation(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")

    def test_rejects_zero_and_negative_prices(self) -> None:
        for price in (0.0, -1.0):
            with self.subTest(price=price):
                with self.assertRaises(ValueError):
                    PhysicalProduct("P001", "Lamp", price, 5, 1.0, self.supplier)

    def test_rejects_negative_stock(self) -> None:
        with self.assertRaises(ValueError):
            PhysicalProduct("P001", "Lamp", 25.0, -1, 1.0, self.supplier)

    def test_rejects_zero_and_negative_order_quantities(self) -> None:
        product = PhysicalProduct("P001", "Lamp", 25.0, 5, 1.0, self.supplier)

        for quantity in (0, -1):
            with self.subTest(quantity=quantity):
                with self.assertRaises(ValueError):
                    OrderLine(product, quantity)

    def test_accepts_zero_stock(self) -> None:
        product = PhysicalProduct("P001", "Lamp", 25.0, 0, 1.0, self.supplier)
        self.assertEqual(product.get_stock(), 0)