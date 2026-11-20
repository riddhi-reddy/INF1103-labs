from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier
    ) -> None:
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        if price <= 0:
            raise ValueError("Product price must be greater than zero.")
        self.__price: float = price
        self.update_stock(stock)
        self.__supplier: Supplier = supplier

    def display_information(self) -> None:
        print(
            f"ID: {self.__product_id} | "
            f"Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | "
            f"Stock: {self.__stock}"
        )

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> None:
        if type(quantity) is not int or quantity < 0:
            raise ValueError(
                "Stock must be a whole number of zero or more."
            )

        self.__stock: int = quantity

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass


