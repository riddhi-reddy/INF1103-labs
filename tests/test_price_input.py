import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

from inventory_manager import read_price


class TestPriceInput(unittest.TestCase):
    def test_retries_until_price_is_valid(self) -> None:
        output = StringIO()

        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]) as mock_input:
            with redirect_stdout(output):
                price = read_price()

        self.assertEqual(price, 12.5)
        self.assertEqual(mock_input.call_count, 3)
        self.assertEqual(
            output.getvalue().splitlines(),
            [
                "Please enter a number.",
                "Price must be a number greater than zero.",
            ],
        )