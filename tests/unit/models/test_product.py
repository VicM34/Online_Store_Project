import pytest

from src.store.models import LawnGrass, Product, Smartphone


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

    def test_product_str_format(self):
        """Тест строкового представления товара."""
        product = Product("Телефон", "Смартфон", 1000.0, 5)
        expected = "Телефон, 1000.0 руб. Остаток: 5 шт."
        assert str(product) == expected

    def test_product_addition(self):
        """Тест сложения товаров."""
        product1 = Product("Товар1", "Описание1", 100.0, 2)  # 100*2 = 200
        product2 = Product("Товар2", "Описание2", 200.0, 3)  # 200*3 = 600

        total_cost = product1 + product2
        assert total_cost == 800.0  # 200 + 600

    def test_product_addition_type_error(self):
        """Тест ошибки при сложении с неправильным типом."""
        product = Product("Товар", "Описание", 100.0, 2)

        with pytest.raises(TypeError, match="Можно складывать только объекты класса Product"):
            product + "не товар"


class TestSmartphone:
    """Тесты для класса Smartphone."""

    def test_smartphone_creation(self):
        """Тест создания смартфона."""
        smartphone = Smartphone(
            name="iPhone 15",
            description="Новый смартфон",
            price=100000.0,
            quantity=5,
            efficiency=3.5,
            model="15 Pro",
            memory=256,
            color="Black",
        )

        assert smartphone.name == "iPhone 15"
        assert smartphone.price == 100000.0
        assert smartphone.efficiency == 3.5
        assert smartphone.model == "15 Pro"
        assert smartphone.memory == 256
        assert smartphone.color == "Black"

    def test_smartphone_inheritance(self):
        """Тест что Smartphone наследуется от Product."""
        smartphone = Smartphone("Test", "Desc", 1000.0, 1, 2.0, "Model", 128, "Black")
        assert isinstance(smartphone, Product)

    def test_smartphone_repr(self):
        """Тест представления смартфона."""
        smartphone = Smartphone("Test", "Desc", 1000.0, 1, 2.0, "Model", 128, "Black")
        repr_str = repr(smartphone)
        assert "Smartphone(" in repr_str
        assert "efficiency=2.0" in repr_str


class TestLawnGrass:
    """Тесты для класса LawnGrass."""

    def test_lawn_grass_creation(self):
        """Тест создания травы газонной."""
        grass = LawnGrass(
            name="Газонная трава",
            description="Для красивого газона",
            price=500.0,
            quantity=10,
            country="Россия",
            germination_period="14 дней",  # ИЗМЕНЕНО: строка вместо числа
            color="Зеленый",
        )

        assert grass.name == "Газонная трава"
        assert grass.price == 500.0
        assert grass.country == "Россия"
        assert grass.germination_period == "14 дней"  # ИЗМЕНЕНО
        assert grass.color == "Зеленый"

    def test_lawn_grass_inheritance(self):
        """Тест что LawnGrass наследуется от Product."""
        grass = LawnGrass("Test", "Desc", 500.0, 1, "Russia", "10 дней", "Green")  # ИЗМЕНЕНО
        assert isinstance(grass, Product)

    def test_lawn_grass_repr(self):
        """Тест представления травы газонной."""
        grass = LawnGrass("Test", "Desc", 500.0, 1, "Russia", "10 дней", "Green")  # ИЗМЕНЕНО
        repr_str = repr(grass)
        assert "LawnGrass(" in repr_str
        assert "germination_period='10 дней'" in repr_str  # ИЗМЕНЕНО

    def test_add_lawn_grass_same_class(self):
        """Тест сложения травы газонной одного класса."""
        grass1 = LawnGrass("Grass1", "Desc", 500.0, 3, "Rus", "10 дней", "Green")  # ИЗМЕНЕНО
        grass2 = LawnGrass("Grass2", "Desc", 300.0, 2, "Rus", "12 дней", "Dark Green")  # ИЗМЕНЕНО

        total = grass1 + grass2
        assert total == 2100.0  # 500*3 + 300*2
