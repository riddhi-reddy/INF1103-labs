from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


class ProductFactory:
    @staticmethod
    def create(
        product_type: str,
        product_id: str,
        name: str,
        price: float,
        stock_quantity: int,
        supplier: Supplier,
        extra_value: float,
    ) -> Product:
        if product_type == "physical":
            return PhysicalProduct(
                product_id, name, price, stock_quantity, extra_value, supplier
            )

        if product_type == "digital":
            return DigitalProduct(
                product_id, name, price, stock_quantity, extra_value, supplier
            )

        raise ValueError(f"Unknown product type: {product_type}")