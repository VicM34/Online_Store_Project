from abc import ABC

import pytest

from src.store.models.category import Category
from src.store.models.countable import Countable, Order
from src.store.models.product import Product, Smartphone


class TestCountable:
    """Тесты для абстрактного класса Countable."""

    def test_countable_is_abstract(self):
        """Тест что Countable является абстрактным классом."""
        assert issubclass(Countable, ABC)

    def test_category_implements_countable(self):
        """Тест что Category реализует Countable."""
        category = Category("Тест", "Описание")

        assert hasattr(category, "__len__")
        assert hasattr(category, "total_quantity")
        assert isinstance(category, Countable)

    def test_order_implements_countable(self):
        """Тест что Order реализует Countable."""
        product = Product("Тест", "Описание", 100.0, 5)
        order = Order(product, 2)

        assert hasattr(order, "__len__")
        assert hasattr(order, "total_quantity")
        assert isinstance(order, Countable)

    def test_cannot_instantiate_countable(self):
        """Тест что нельзя создать экземпляр Countable."""
        with pytest.raises(TypeError):
            Countable()


class TestOrder:
    """Тесты для класса Order."""

    def test_order_creation(self):
        """Тест создания заказа."""
        product = Product("Телефон", "Смартфон", 1000.0, 10)
        order = Order(product, 3)

        assert order.product == product
        assert order.quantity == 3
        assert order.total_cost == 3000.0

    def test_order_len(self):
        """Тест метода __len__ заказа."""
        product = Product("Телефон", "Смартфон", 1000.0, 10)
        order = Order(product, 5)

        assert len(order) == 5

    def test_order_total_quantity(self):
        """Тест свойства total_quantity заказа."""
        product = Product("Телефон", "Смартфон", 1000.0, 10)
        order = Order(product, 2)

        assert order.total_quantity == 2

    def test_order_with_smartphone(self):
        """Тест заказа со смартфоном."""
        smartphone = Smartphone("iPhone", "Смартфон", 100000.0, 5, 3.5, "15 Pro", 256, "Black")
        order = Order(smartphone, 2)

        assert order.product == smartphone
        assert order.total_cost == 200000.0

    def test_order_str(self):
        """Тест строкового представления заказа."""
        product = Product("Телефон", "Смартфон", 1000.0, 10)
        order = Order(product, 3)

        order_str = str(order)
        assert "Заказ: Телефон" in order_str
        assert "количество: 3" in order_str
        assert "стоимость: 3000" in order_str

    def test_order_repr(self):
        """Тест представления для разработчика."""
        product = Product("Телефон", "Смартфон", 1000.0, 10)
        order = Order(product, 3)

        repr_str = repr(order)
        assert "Order(" in repr_str
        assert "product=Product(" in repr_str
        assert "quantity=3" in repr_str

    def test_type_checking_imports(self):
        """Тест что TYPE_CHECKING импорты работают корректно."""
        from src.store.models.countable import Order
        from src.store.models.product import Product

        product = Product("Тест", "Описание", 100.0, 5)
        order = Order(product, 2)

        assert order.product == product
