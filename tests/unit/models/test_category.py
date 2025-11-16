import pytest

from src.store.models import Category, Product


@pytest.fixture
def reset_counters():
    """Фикстура для сброса счетчиков."""
    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_product():
    """Фикстура для создания тестового товара."""
    return Product("Тестовый товар", "Описание", 1000.0, 5)


@pytest.fixture
def sample_products():
    """Фикстура для создания нескольких товаров."""
    return [
        Product("Товар 1", "Описание 1", 100.0, 2),
        Product("Товар 2", "Описание 2", 200.0, 3),
    ]


@pytest.fixture
def sample_category(sample_products):
    """Фикстура для создания тестовой категории."""
    return Category("Тестовая категория", "Описание категории", sample_products)


@pytest.fixture
def empty_category():
    """Фикстура для создания пустой категории."""
    return Category("Пустая категория", "Описание")


class TestCategory:
    """Тесты для класса Category."""

    def test_category_creation(self, sample_category, sample_products):
        """Тест создания категории."""
        assert sample_category.name == "Тестовая категория"
        assert sample_category.description == "Описание категории"
        # ИСПРАВЛЕНО: используем products_list вместо products
        assert sample_category.products_list == sample_products
        assert len(sample_category) == 2

    def test_empty_category_creation(self, empty_category):
        """Тест создания пустой категории."""
        assert empty_category.name == "Пустая категория"
        assert empty_category.description == "Описание"
        # ИСПРАВЛЕНО: проверяем products как строку
        assert empty_category.products == ""
        assert len(empty_category) == 0

    def test_category_counters(self, reset_counters, sample_products):
        """Тест счетчиков категорий и товаров."""
        category1 = Category("Кат1", "Описание", sample_products)
        assert Category.category_count == 1
        assert Category.product_count == 2
        # ИСПРАВЛЕНО: используем products_list
        assert len(category1.products_list) == 2

        category2 = Category("Кат2", "Описание", [Product("Т3", "D3", 300.0, 3)])
        assert Category.category_count == 2
        assert Category.product_count == 3
        # ИСПРАВЛЕНО: используем products_list
        assert len(category2.products_list) == 1
        assert category2.products_list[0].name == "Т3"

    def test_category_str(self, sample_category):
        """Тест строкового представления категории."""
        expected = "Тестовая категория, количество товаров: 2"
        assert str(sample_category) == expected

    def test_category_str_empty(self, empty_category):
        """Тест строкового представления пустой категории."""
        expected = "Пустая категория, количество товаров: 0"
        assert str(empty_category) == expected

    def test_category_repr(self, sample_category):
        """Тест представления для разработчика."""
        assert "Category(" in repr(sample_category)
        assert "Тестовая категория" in repr(sample_category)

    def test_category_class_attributes_access(self, reset_counters, sample_category):
        """Тест доступа к атрибутам класса из объекта."""
        assert Category.category_count == 1
        assert Category.product_count == 2

    def test_add_product_to_category(self, empty_category, sample_product):
        """Тест добавления товара в категорию."""
        initial_product_count = Category.product_count
        empty_category.add_product(sample_product)

        assert len(empty_category) == 1
        # ИСПРАВЛЕНО: используем products_list
        assert empty_category.products_list[0] == sample_product
        assert Category.product_count == initial_product_count + 1

    def test_add_multiple_products(self, empty_category):
        """Тест добавления нескольких товаров в категорию."""
        product1 = Product("Товар A", "Описание A", 100.0, 1)
        product2 = Product("Товар B", "Описание B", 200.0, 2)

        empty_category.add_product(product1)
        empty_category.add_product(product2)

        assert len(empty_category) == 2
        # ИСПРАВЛЕНО: используем products_list
        assert empty_category.products_list[0] == product1
        assert empty_category.products_list[1] == product2

    def test_category_counters_after_adding_products(self, reset_counters, empty_category):
        """Тест счетчиков после добавления товаров."""
        assert Category.category_count == 1
        assert Category.product_count == 0

        empty_category.add_product(Product("Товар", "Описание", 100.0, 1))
        assert Category.product_count == 1

        empty_category.add_product(Product("Товар2", "Описание2", 200.0, 2))
        assert Category.product_count == 2

    def test_reset_counters_method(self, reset_counters):
        """Тест метода сброса счетчиков."""
        Category("Кат1", "Описание", [Product("Т1", "D1", 100.0, 1)])
        assert Category.category_count == 1
        assert Category.product_count == 1

        Category.reset_counters()
        assert Category.category_count == 0
        assert Category.product_count == 0

    def test_category_with_none_products(self):
        """Тест создания категории с явным None."""
        category = Category("Категория", "Описание", None)
        # ИСПРАВЛЕНО: проверяем products как строку
        assert category.products == ""
        assert len(category) == 0
