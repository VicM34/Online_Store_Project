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

        Args:
            name: Название категории
            description: Описание категории
            products: Список товаров категории (опционально)
        """
        self.name = name
        self.description = description
        self.products = products if products is not None else []

        # Автоматическое обновление атрибутов класса
        Category.category_count += 1
        Category.product_count += len(self.products)

    def __str__(self) -> str:
        """Строковое представление категории."""
        return f"{self.name}, количество товаров: {len(self.products)}"

    def __repr__(self) -> str:
        """Представление для разработчика."""
        return f"Category('{self.name}', products_count={len(self.products)})"

    def __len__(self) -> int:
        """Количество товаров в категории."""
        return len(self.products)

    def add_product(self, product: Product) -> None:
        """Добавить товар в категорию."""
        self.products.append(product)
        Category.product_count += 1

    @classmethod
    def reset_counters(cls) -> None:
        """Сбросить счетчики категорий и товаров."""
        cls.category_count = 0
        cls.product_count = 0
