import json
import os
import tempfile

import pytest

from src.store.models import Category, Product
from src.utils.json_loader import load_products_from_json, print_loaded_data


class TestJsonLoader:
    """Тесты для загрузчика данных из JSON."""

    def test_load_products_from_json_valid_file(self):
        """Тест загрузки данных из корректного JSON файла."""
        test_data = [
            {
                "name": "Электроника",
                "description": "Электронные устройства",
                "products": [{"name": "Смартфон", "description": "Мощный смартфон", "price": 50000.0, "quantity": 10}],
            }
        ]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False)
            temp_file = f.name

        try:
            categories = load_products_from_json(temp_file)

            # Проверяем результат
            assert len(categories) == 1
            assert isinstance(categories[0], Category)
            assert categories[0].name == "Электроника"
            assert len(categories[0].products_list) == 1
            assert isinstance(categories[0].products_list[0], Product)
            assert categories[0].products_list[0].name == "Смартфон"
            assert categories[0].products_list[0].price == 50000.0

        finally:
            # Удаляем временный файл
            os.unlink(temp_file)

    def test_load_products_from_json_file_not_found(self):
        """Тест обработки отсутствующего файла."""
        with pytest.raises(FileNotFoundError):
            load_products_from_json("nonexistent_file.json")

    def test_load_products_from_json_invalid_json(self):
        """Тест обработки некорректного JSON."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("invalid json content")
            temp_file = f.name

        try:
            with pytest.raises(json.JSONDecodeError):
                load_products_from_json(temp_file)
        finally:
            os.unlink(temp_file)

    def test_load_products_from_json_missing_required_fields(self):
        """Тест загрузки данных с отсутствующими обязательными полями."""
        test_data = [{"description": "Категория без имени", "products": []}]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
            json.dump(test_data, f, ensure_ascii=False)
            temp_file = f.name

        try:
            with pytest.raises(KeyError, match="Категория должна содержать поле 'name'"):
                load_products_from_json(temp_file)
        finally:
            os.unlink(temp_file)

    def test_print_loaded_data(self, capsys):
        """Тест функции вывода данных."""
        product1 = Product("Товар1", "Описание1", 1000.0, 5)
        product2 = Product("Товар2", "Описание2", 2000.0, 3)
        category = Category("Категория", "Описание категории", [product1, product2])

        print_loaded_data([category])

        captured = capsys.readouterr()
        output = captured.out

        assert "ДАННЫЕ ЗАГРУЖЕННЫЕ ИЗ JSON" in output
        assert "Категория 1: Категория" in output
        assert "Товар1 - 1000.0₽" in output or "Товар1" in output
        assert "ОБЩАЯ СТАТИСТИКА" in output
