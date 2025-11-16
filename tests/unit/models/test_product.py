import pytest

from src.store.models import Product


@pytest.fixture
def sample_product():
    """Фикстура для создания тестового товара."""
    return Product("Тестовый товар", "Тестовое описание", 1000.0, 5)


@pytest.fixture
def different_product():
    """Фикстура для создания другого товара."""
    return Product("Другой товар", "Другое описание", 500.0, 10)


class TestProduct:
    """Тесты для класса Product."""

    def test_product_creation(self, sample_product):
        """Тест создания товара."""
        assert sample_product.name == "Тестовый товар"
        assert sample_product.description == "Тестовое описание"
        assert sample_product.price == 1000.0
        assert sample_product.quantity == 5

    def test_product_creation_with_default_values(self):
        """Тест создания товара с разными значениями."""
        product = Product("Новый товар", "Новое описание", 750.50, 3)
        assert product.name == "Новый товар"
        assert product.description == "Новое описание"
        assert product.price == 750.50
        assert product.quantity == 3

    def test_product_str(self, sample_product):
        """Тест строкового представления товара."""
        expected = "Тестовый товар, 1000.0 руб. Остаток: 5 шт."
        assert str(sample_product) == expected

    def test_product_str_different_values(self, different_product):
        """Тест строкового представления другого товара."""
        expected = "Другой товар, 500.0 руб. Остаток: 10 шт."
        assert str(different_product) == expected

    def test_product_repr(self, sample_product):
        """Тест представления для разработчика."""
        repr_str = repr(sample_product)
        assert "Product(" in repr_str
        assert "Тестовый товар" in repr_str
        assert "1000.0" in repr_str
        assert "5" in repr_str

    def test_product_repr_different_values(self, different_product):
        """Тест представления для другого товара."""
        repr_str = repr(different_product)
        assert "Product(" in repr_str
        assert "Другой товар" in repr_str
        assert "500.0" in repr_str
        assert "10" in repr_str

    def test_product_equality(self):
        """Тест сравнения товаров."""
        product1 = Product("Товар", "Описание", 100.0, 5)
        product2 = Product("Товар", "Описание", 100.0, 5)
        product3 = Product("Другой", "Описание", 100.0, 5)

        # Товары с одинаковыми атрибутами должны быть равны
        assert product1.name == product2.name
        assert product1.description == product2.description
        assert product1.price == product2.price
        assert product1.quantity == product2.quantity

        assert product1 is not product2
        assert product1 is not product3

    def test_product_attributes_modification(self, sample_product):
        """Тест изменения атрибутов товара."""
        sample_product.name = "Измененное имя"
        sample_product.price = 1500.0
        sample_product.quantity = 8

        assert sample_product.name == "Измененное имя"
        assert sample_product.price == 1500.0
        assert sample_product.quantity == 8
        assert str(sample_product) == "Измененное имя, 1500.0 руб. Остаток: 8 шт."

    @pytest.mark.parametrize(
        "name,description,price,quantity,expected_str",
        [
            ("Товар1", "Описание1", 100.0, 1, "Товар1, 100.0 руб. Остаток: 1 шт."),
            ("Товар2", "Описание2", 0.0, 0, "Товар2, 0.0 руб. Остаток: 0 шт."),
            ("Товар3", "Описание3", 999.99, 999, "Товар3, 999.99 руб. Остаток: 999 шт."),
        ],
    )
    def test_product_with_different_parameters(self, name, description, price, quantity, expected_str):
        """Параметризованный тест для товаров с разными параметрами."""
        product = Product(name, description, price, quantity)
        assert product.name == name
        assert product.description == description
        assert product.price == price
        assert product.quantity == quantity
        assert str(product) == expected_str
