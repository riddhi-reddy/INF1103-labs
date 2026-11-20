import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

from file_handler import load_products
from inventory import Inventory
from supplier import Supplier


class TestLoadProducts(unittest.TestCase):
    def setUp(self) -> None:
        self.inventory = Inventory()
        self.supplier = Supplier("S001", "Test Supplier", "test@example.com")

    def test_missing_file_reports_error_and_finishes(self) -> None:
        output = StringIO()

        with TemporaryDirectory() as folder:
            path = Path(folder) / "missing.csv"
            with redirect_stdout(output):
                load_products(str(path), self.inventory, self.supplier)

        self.assertEqual(self.inventory.get_products(), [])
        self.assertEqual(
            output.getvalue().splitlines(),
            [
                f"Products file not found: {path}",
                "Load attempt finished.",
            ],
        )

    def test_skips_bad_rows_and_loads_valid_products(self) -> None:
        csv_data = (
            "product_type,product_id,name,price,stock_quantity\n"
            "physical,P001,Desk Lamp,25.00,10\n"
            "digital,D001,Photo Editor,49.90,100\n"
            "service,S001,Installation,30.00,5\n"
            "physical,P002,Office Chair,abc,3\n"
            "physical,P003,Monitor Stand,39.50,7\n"
        )
        output = StringIO()

        with TemporaryDirectory() as folder:
            path = Path(folder) / "products.csv"
            path.write_text(csv_data, encoding="utf-8")
            with redirect_stdout(output):
                load_products(str(path), self.inventory, self.supplier)

        product_ids = [
            product.get_product_id() for product in self.inventory.get_products()
        ]
        self.assertEqual(product_ids, ["P001", "D001", "P003"])

        messages = output.getvalue().splitlines()
        self.assertEqual(messages[0], "Row 4 skipped: Unknown product type: service")
        self.assertIn("Row 5 skipped:", messages[1])
        self.assertIn("abc", messages[1])
        self.assertEqual(messages[2:], ["3 products loaded.", "Load attempt finished."])