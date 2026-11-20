import unittest

from products.digital_product import DigitalProduct
from products.physical_product import PhysicalProduct
from products.product_factory import ProductFactory
from supplier import Supplier


class TestProductFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")

    def test_creates_physical_product(self) -> None:
        product = ProductFactory.create(
            "physical", "P001", "Laptop", 1000.0, 5, self.supplier, 2.0
        )

        self.assertIsInstance(product, PhysicalProduct)
        self.assertEqual(product.get_weight(), 2.0)

    def test_creates_digital_product(self) -> None:
        product = ProductFactory.create(
            "digital", "D001", "Ebook", 20.0, 10, self.supplier, 15.0
        )

        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.get_download_size(), 15.0)

    def test_rejects_unknown_product_type(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create(
                "service", "SVC001", "Test Service", 50.0, 1, self.supplier, 0.0
            )