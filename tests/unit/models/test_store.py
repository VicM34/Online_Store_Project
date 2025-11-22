from unittest.mock import patch

import pytest

from src.store.models.category import Category
from src.store.models.product import Product


class TestCategory:
    def test_private_products(self):
        """Тест приватного атрибута продуктов."""
        category = Category("Тест", "Тест описание")

        # Нельзя получить доступ напрямую
        with pytest.raises(AttributeError):
            _ = category.__products

    def test_add_product(self):
        """Тест добавления товара через метод."""
        category = Category("Электроника", "Техника")
        product = Product("Телефон", "Смартфон", 1000.0, 5)

        # Добавляем товар
        category.add_product(product)

        assert "Телефон, 1000.0 руб. Остаток: 5 шт." in category.products

        assert len(category.products_list) == 1
        assert category.products_list[0].name == "Телефон"

    def test_products_property(self):
        """Тест геттера продуктов."""
        category = Category("Электроника", "Техника")
        product = Product("Телефон", "Смартфон", 1000.0, 5)

        category.add_product(product)

        # Проверяем, что products возвращает строку - ИЗМЕНЕНО
        assert isinstance(category.products, str)
        assert "Телефон" in category.products

        # Проверяем, что products_list возвращает список - ИЗМЕНЕНО
        assert isinstance(category.products_list, list)
        assert len(category.products_list) == 1


class TestProduct:
    def test_new_product(self):
        """Тест создания товара через класс-метод."""
        product_data = {"name": "Телефон", "description": "Смартфон", "price": 1000.0, "quantity": 5}

        product = Product.new_product(product_data)
        assert product.name == "Телефон"
        assert product.price == 1000.0

    def test_price_validation(self):
        """Тест валидации цены."""
        product = Product("Телефон", "Смартфон", 1000.0, 5)

        # Нельзя установить отрицательную цену
        product.price = -100
        assert product.price == 1000.0

        # Нельзя установить нулевую цену
        product.price = 0
        assert product.price == 1000.0

    def test_duplicate_products(self):
        """Тест обработки дубликатов."""
        existing_products = [Product("Телефон", "Смартфон", 1000.0, 5)]

        new_data = {"name": "Телефон", "price": 1200.0, "quantity": 3}

        updated = Product.new_product(new_data, existing_products)
        assert updated.quantity == 8  # 5 + 3
        assert updated.price == 1200.0  # Максимальная цена

    def test_new_product_without_duplicates(self):
        """Тест создания товара без дубликатов."""
        product_data = {"name": "Новый товар", "description": "Описание", "price": 500.0, "quantity": 10}

        product = Product.new_product(product_data)
        assert product.name == "Новый товар"
        assert product.price == 500.0
        assert product.quantity == 10

    def test_private_price_attribute(self):
        """Тест что цена является приватным атрибутом."""
        product = Product("Телефон", "Смартфон", 1000.0, 5)

        # Нельзя получить доступ напрямую
        with pytest.raises(AttributeError):
            _ = product.__price

    def test_price_getter(self):
        """Тест геттера цены."""
        product = Product("Телефон", "Смартфон", 1000.0, 5)
        assert product.price == 1000.0

    @patch("builtins.input", return_value="y")
    def test_price_decrease_confirmation_accepted(self, mock_input):
        """Тест подтверждения понижения цены (пользователь согласен)."""
        product = Product("Телефон", "Смартфон", 1000.0, 5)

        # Понижаем цену (пользователь соглашается)
        product.price = 800.0

        assert product.price == 800.0

    @patch("builtins.input", return_value="n")
    def test_price_decrease_confirmation_rejected(self, mock_input):
        """Тест подтверждения понижения цены (пользователь отказывается)."""
        product = Product("Телефон", "Смартфон", 1000.0, 5)

        # Пытаемся понизить цену (пользователь отказывается)
        product.price = 800.0

        # Цена должна остаться прежней
        assert product.price == 1000.0

    def test_price_increase_no_confirmation(self):
        """Тест, что повышение цены не требует подтверждения."""
        product = Product("Телефон", "Смартфон", 1000.0, 5)

        # Повышаем цену
        product.price = 1200.0

        assert product.price == 1200.0

    def test_new_product_without_name(self):
        """Тест создания товара без имени."""
        product_data = {"description": "Описание", "price": 500.0, "quantity": 10}

        with pytest.raises(ValueError) as exc_info:
            Product.new_product(product_data)
        assert "Имя товара обязательно" in str(exc_info.value)

    def test_new_product_with_empty_name(self):
        """Тест создания товара с пустым именем."""
        product_data = {"name": "", "description": "Описание", "price": 500.0, "quantity": 10}

        with pytest.raises(ValueError) as exc_info:
            Product.new_product(product_data)
        assert "Имя товара обязательно" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
