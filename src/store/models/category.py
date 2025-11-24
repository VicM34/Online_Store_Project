from typing import List, Optional

from src.store.models.product import Product


class CategoryIterator:
    """Итератор для перебора товаров в категории."""

    def __init__(self, category: "Category") -> None:
        """
        Инициализация итератора.
        """
        self.category = category
        self.index = 0

    def __iter__(self) -> "CategoryIterator":
        """Возвращает сам итератор."""
        return self

    def __next__(self) -> Product:
        """Возвращает следующий товар в категории."""
        if self.index < len(self.category.products_list):
            product = self.category.products_list[self.index]
            self.index += 1
            return product
        raise StopIteration


class Category:
    """Класс для представления категории товаров."""

    # Атрибуты класса (общие для всех объектов)
    category_count = 0  # Количество категорий
    product_count = 0  # Количество товаров

    def __init__(self, name: str, description: str, products: Optional[List[Product]] = None) -> None:
        """
        Инициализация объекта Category.
        """
        self.name = name
        self.description = description
        self.__products = products if products is not None else []  # Приватный атрибут

        # Автоматическое обновление атрибутов класса
        Category.category_count += 1
        Category.product_count += len(self.__products)

    def __str__(self) -> str:
        """Строковое представление категории в формате: Название, количество продуктов: X шт."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __repr__(self) -> str:
        """Представление для разработчика."""
        return f"Category('{self.name}', products_count={len(self.__products)})"

    def __len__(self) -> int:
        """Количество товаров в категории."""
        return len(self.__products)

    def __iter__(self) -> CategoryIterator:
        """Возвращает итератор для перебора товаров категории."""
        return CategoryIterator(self)

    def add_product(self, product: Product) -> None:
        """Добавить товар в категорию."""
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Можно добавлять только объекты класса Product")

    @property
    def products(self) -> str:
        """Геттер для получения списка товаров в виде строк."""
        return "\n".join(str(product) for product in self.__products)

    @property
    def products_list(self) -> List[Product]:
        """Геттер для получения списка товаров (для обратной совместимости)."""
        return self.__products

    @classmethod
    def reset_counters(cls) -> None:
        """Сбросить счетчики категорий и товаров."""
        cls.category_count = 0
        cls.product_count = 0
