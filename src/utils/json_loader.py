import json
import os
from typing import List

from src.store.models import Category, Product


def load_products_from_json(file_path: str = "products.json") -> List[Category]:
    """
    Загружает данные о товарах и категориях из JSON файла.

    Args:
        file_path: Путь к JSON файлу (по умолчанию products.json)

    Returns:
        List[Category]: Список объектов Category с товарами

    Raises:
        FileNotFoundError: Если файл не найден
        json.JSONDecodeError: Если файл содержит некорректный JSON
        KeyError: Если в JSON отсутствуют обязательные поля
    """
    # Проверяем существование файла
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден")

    # Читаем и парсим JSON
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = []

    # Обрабатываем каждую категорию из JSON
    for category_data in data:
        # Проверяем обязательные поля
        if "name" not in category_data:
            raise KeyError("Категория должна содержать поле 'name'")

        products = []

        # Создаем товары для категории
        for product_data in category_data.get("products", []):
            # Проверяем обязательные поля товара
            if "name" not in product_data:
                raise KeyError("Товар должен содержать поле 'name'")
            if "price" not in product_data:
                raise KeyError(f"Товар '{product_data['name']}' должен содержать поле 'price'")

            product = Product(
                name=product_data["name"],
                description=product_data.get("description", ""),
                price=float(product_data["price"]),
                quantity=int(product_data.get("quantity", 0)),
            )
            products.append(product)

        # Создаем категорию
        category = Category(
            name=category_data["name"], description=category_data.get("description", ""), products=products
        )

        categories.append(category)

    return categories


def print_loaded_data(categories: List[Category]) -> None:
    """
    Выводит информацию о загруженных категориях и товарах.

    Args:
        categories: Список категорий для вывода
    """
    print("=== ДАННЫЕ ЗАГРУЖЕННЫЕ ИЗ JSON ===")

    for i, category in enumerate(categories, 1):
        print(f"\n--- Категория {i}: {category.name} ---")
        print(f"Описание: {category.description}")
        print(f"Количество товаров: {len(category)}")

        for j, product in enumerate(category.products, 1):
            print(f"  {j}. {product.name} - {product.price}₽ (остаток: {product.quantity} шт.)")

    print("\n=== ОБЩАЯ СТАТИСТИКА ===")
    print(f"Всего категорий: {len(categories)}")
    print(f"Всего товаров: {sum(len(category.products) for category in categories)}")
    print(f"Счетчик категорий: {Category.category_count}")
    print(f"Счетчик товаров: {Category.product_count}")
