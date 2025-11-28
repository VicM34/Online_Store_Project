from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product


class Countable(ABC):
    """Абстрактный класс для объектов, которые можно подсчитать."""

    @abstractmethod
    def __len__(self) -> int:
        """Абстрактный метод для получения количества."""
        pass

    @property
    @abstractmethod
    def total_quantity(self) -> int:
        """Абстрактное свойство для общего количества."""
        pass


class Order(Countable):
    """Класс для представления заказа с одним товаром."""

    def __init__(self, product: "Product", quantity: int) -> None:
        self.product = product
        self.quantity = quantity
        self.total_cost = product.price * quantity

    def __len__(self) -> int:
        """Количество товаров в заказе."""
        return self.quantity

    @property
    def total_quantity(self) -> int:
        """Общее количество товаров в заказе."""
        return self.quantity

    def __str__(self) -> str:
        """Строковое представление заказа."""
        return f"Заказ: {self.product.name}, количество: {self.quantity}, стоимость: {self.total_cost} руб."

    def __repr__(self) -> str:
        """Представление для разработчика."""
        return f"Order(product={repr(self.product)}, quantity={self.quantity})"
