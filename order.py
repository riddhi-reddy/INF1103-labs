from product import Product
from order_line import OrderLine


class Order:
    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        total: float = 0.0

        for order_line in self.order_lines:
            total += order_line.calculate_subtotal()

        return total

    def remove_order_line(self, line_index: int) -> None:
        if line_index < 0 or line_index >= len(self.order_lines):
            raise IndexError("Order line index is out of range.")

        self.order_lines.pop(line_index)