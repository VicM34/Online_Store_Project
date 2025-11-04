import os
import sys
from contextlib import redirect_stdout
from io import StringIO

from src.main import main

# Добавляем src в путь для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class TestMain:
    """Тесты для main.py"""

    def test_main_output_contains_all_sections(self) -> None:
        """Тест что вывод содержит все ожидаемые секции."""
        output = StringIO()

        with redirect_stdout(output):
            main()

        output_str = output.getvalue()

        # Проверяем ключевые элементы вывода
        assert "=== Информация о товарах ===" in output_str
        assert "Samsung Galaxy S23 Ultra" in output_str
        assert "Iphone 15" in output_str
        assert "Xiaomi Redmi Note 11" in output_str
        assert "=== Первая категория ===" in output_str
        assert "=== Вторая категория ===" in output_str
        assert "=== Общая статистика ===" in output_str
        assert "Всего категорий: 2" in output_str
        assert "Всего товаров: 4" in output_str

    def test_main_product_prices_displayed(self) -> None:
        """Тест что цены товаров отображаются корректно."""
        output = StringIO()

        with redirect_stdout(output):
            main()

        output_str = output.getvalue()

        # Проверяем что цены выводятся корректно
        assert "180000.0" in output_str  # Samsung
        assert "210000.0" in output_str  # iPhone
        assert "31000.0" in output_str  # Xiaomi
        assert "123000.0" in output_str  # Телевизор
