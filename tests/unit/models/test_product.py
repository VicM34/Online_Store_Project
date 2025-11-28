import pytest
from abc import ABC

from src.store.models.product import BaseProduct, Product, Smartphone, LawnGrass, CreationLoggerMixin


class TestBaseProduct:
    """Тесты для абстрактного класса BaseProduct."""

    def test_base_product_is_abstract(self):
        """Тест что BaseProduct является абстрактным классом."""
        assert issubclass(BaseProduct, ABC)

    def test_product_implements_all_abstract_methods(self):
        """Тест что Product реализует все абстрактные методы BaseProduct."""
        product = Product("Тест", "Описание", 100.0, 5)

        # Проверяем что все абстрактные методы реализованы
        assert hasattr(product, '__init__')
        assert hasattr(product, '__str__')
        assert hasattr(product, '__repr__')
        assert hasattr(product, '__add__')
        assert hasattr(product, 'price')

    def test_cannot_instantiate_base_product(self):
        """Тест что нельзя создать экземпляр BaseProduct."""
        with pytest.raises(TypeError):
            BaseProduct("Тест", "Описание", 100.0, 5)

    def test_inheritance_chain(self):
        """Тест цепочки наследования."""
        smartphone = Smartphone("Phone", "Desc", 1000.0, 1, 2.0, "M", 128, "Black")
        grass = LawnGrass("Grass", "Desc", 500.0, 1, "Rus", "10 дней", "Green")

        # Проверяем что оба класса наследуются от Product и BaseProduct
        assert isinstance(smartphone, Product)
        assert isinstance(smartphone, BaseProduct)
        assert isinstance(grass, Product)
        assert isinstance(grass, BaseProduct)

        assert smartphone.name == "Phone"
        assert grass.name == "Grass"


class TestCreationLoggerMixin:
    """Тесты для миксина логирования создания объектов."""

    def test_mixin_inheritance(self):
        """Тест что Product наследует CreationLoggerMixin."""
        assert CreationLoggerMixin in Product.__mro__

    def test_mixin_prints_on_creation(self, capsys):
        """Тест что миксин выводит сообщение при создании объекта."""
        product = Product("Тестовый товар", "Описание товара", 1000.0, 5)
        captured = capsys.readouterr()

        expected_output = "Создан объект Product('Тестовый товар', 'Описание товара', 1000.0, 5)"
        assert expected_output in captured.out

        assert product.name == "Тестовый товар"

    def test_mixin_with_smartphone(self, capsys):
        """Тест что миксин работает с наследниками Product."""
        smartphone = Smartphone("iPhone", "Смартфон", 100000.0, 2, 3.5, "15 Pro", 256, "Black")
        captured = capsys.readouterr()

        assert "Создан объект Smartphone(" in captured.out
        assert "iPhone" in captured.out

        assert smartphone.name == "iPhone"

    def test_mixin_with_lawn_grass(self, capsys):
        """Тест что миксин работает с LawnGrass."""
        grass = LawnGrass("Газонная трава", "Для газона", 500.0, 10, "Россия", "14 дней", "Зеленый")
        captured = capsys.readouterr()

        assert "Создан объект LawnGrass(" in captured.out
        assert "Газонная трава" in captured.out

        assert grass.name == "Газонная трава"

    def test_mixin_multiple_inheritance_order(self):
        """Тест порядка наследования MRO."""
        # Проверяем порядок разрешения методов
        mro = Product.__mro__
        assert mro[0] == Product
        assert CreationLoggerMixin in mro
        assert BaseProduct in mro
        # Миксин должен быть перед абстрактным классом
        assert mro.index(CreationLoggerMixin) < mro.index(BaseProduct)

        product = Product("Тест", "Описание", 100.0, 5)
        assert product.name == "Тест"

    def test_base_product_abstract_methods_implementation(self):
        """Тест что все абстрактные методы BaseProduct реализованы в Product."""
        product = Product("Тест", "Описание", 100.0, 5)

        assert str(product) == "Тест, 100.0 руб. Остаток: 5 шт."
        assert "Product(" in repr(product)
        assert product.price == 100.0

        product.price = 150.0
        assert product.price == 150.0

    def test_mixin_functionality(self):
        """Тест конкретной функциональности миксина."""
        product = Product("Тест", "Описание", 100.0, 5)

        assert product.name == "Тест"
        assert product.quantity == 5
