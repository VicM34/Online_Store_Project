from typing import Optional, List, Iterator
from src.store.models.product import Product
from src.store.models.countable import Countable


class CategoryIterator:
    """Итератор для перебора товаров в категории."""

    def __init__(self, category: 'Category') -> None:
        self.category = category
        self.index = 0

    def __iter__(self) -> Iterator[Product]:
        return self

    def __next__(self) -> Product:
        if self.index < len(self.category.products_list):
            product = self.category.products_list[self.index]
            self.index += 1
            return product
        raise StopIteration


class Category(Countable):
    """Класс для представления категории товаров."""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None) -> None:
        self.name = name
        self.description = description
        self.__products = products if products is not None else []

        Category.category_count += 1
        Category.product_count += len(self.__products)

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __repr__(self) -> str:
        return f"Category('{self.name}', products_count={len(self.__products)})"

    def __len__(self) -> int:
        return len(self.__products)

    @property
    def total_quantity(self) -> int:
        """Общее количество всех товаров в категории."""
        return sum(product.quantity for product in self.__products)

    def __iter__(self) -> Iterator[Product]:
        return CategoryIterator(self)

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        return "\n".join(str(product) for product in self.__products)

    @property
    def products_list(self) -> List[Product]:
        return self.__products

    @classmethod
    def reset_counters(cls) -> None:
        cls.category_count = 0
        cls.product_count = 0
