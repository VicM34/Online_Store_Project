from typing import List, Optional

from src.store.models.product import Product


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
        """Строковое представление категории."""
        return f"{self.name}, количество товаров: {len(self.__products)}"

    def __repr__(self) -> str:
        """Представление для разработчика."""
        return f"Category('{self.name}', products_count={len(self.__products)})"

    def __len__(self) -> int:
        """Количество товаров в категории."""
        return len(self.__products)

    def add_product(self, product: Product) -> None:
        """Добавить товар в категорию."""
        if isinstance(product, Product):
            self.__products.append(product)
            Category.product_count += 1
        else:
            raise TypeError("Можно добавлять только объекты класса Product")

    @property
    def products(self) -> str:
        """Геттер для получения списка товаров в виде строк (СООТВЕТСТВИЕ ТЗ)."""
        products_list = []
        for product in self.__products:
            products_list.append(str(product))
        return "\n".join(products_list)

    @property
    def products_list(self) -> List[Product]:
        """Геттер для получения списка товаров (для обратной совместимости)."""
        return self.__products

    @classmethod
    def reset_counters(cls) -> None:
        """Сбросить счетчики категорий и товаров."""
        cls.category_count = 0
        cls.product_count = 0
