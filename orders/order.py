from products.product import Product
from orders.order_line import OrderLine
from discounts.discount_strategy import DiscountStrategy
from discounts.no_discount import NoDiscount


class Order:
    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = NoDiscount() if discount is None else discount


    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.discount = discount
        
    def calculate_total(self) -> float:
        total: float = 0.0

        for order_line in self.order_lines:
            total += order_line.calculate_subtotal()

        return self.discount.apply(total)

    def remove_order_line(self, line_index: int) -> None:
        if line_index < 0 or line_index >= len(self.order_lines):
            raise IndexError("Order line index is out of range.")

        self.order_lines.pop(line_index)

