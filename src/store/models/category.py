from typing import Iterator, List, Optional

from src.store.models.countable import Countable
from src.store.models.product import Product, ZeroQuantityError


class CategoryIterator:
    """Итератор для перебора товаров в категории."""

    def __init__(self, category: "Category") -> None:
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

    def get_average_price(self) -> float:
        """
        Возвращает среднюю цену всех товаров в категории.
        """
        if not self.__products:
            return 0.0

        total_price = float(sum(product.price for product in self.__products))

        try:
            return total_price / len(self.__products)
        except ZeroDivisionError:
            return 0.0

    def add_product(self, product: Product) -> None:
        """Добавляет товар в категорию с обработкой исключений."""
        try:
            if not isinstance(product, Product):
                raise TypeError("Можно добавлять только объекты класса Product или его наследников")

            if product.quantity <= 0:
                raise ZeroQuantityError(f"Товар '{product.name}' имеет нулевое количество")

            self.__products.append(product)
            Category.product_count += 1
            print(f"Товар '{product.name}' успешно добавлен в категорию '{self.name}'")

        except (TypeError, ZeroQuantityError) as e:
            print(f"Ошибка добавления товара: {e}")
            raise

        finally:
            print("Обработка добавления товара завершена")

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
