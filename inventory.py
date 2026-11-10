from product import Product


class Inventory:
    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError(
                "Inventory can only contain Product objects."
            )

        if self.find_product(product.get_product_id()) is not None:
            raise ValueError("Product ID already exists.")

        self.__products.append(product)

    def find_product(self, product_id: str) -> Product | None:
        product_id = product_id.strip().upper()

        for product in self.__products:
            if product.get_product_id().upper() == product_id:
                return product

        return None

    def search_product(self, product_id: str) -> Product | None:
        return self.find_product(product_id)

    def remove_product(self, product_id: str) -> None:
        product = self.find_product(product_id)

        if product is None:
            raise ValueError("Product not found.")

        self.__products.remove(product)

    def display_all(self) -> None:
        if not self.__products:
            print("\nInventory is empty.")
            return

        print("\nCurrent Inventory")
        print("-" * 70)

        for product in self.__products:
            product.display_information()

        print("-" * 70)

    def update_stock(
        self,
        product_id: str,
        quantity: int
    ) -> None:
        product = self.find_product(product_id)

        if product is None:
            raise ValueError("Product not found.")

        product.update_stock(quantity)

    def get_products(self) -> list[Product]:
        return self.__products.copy()