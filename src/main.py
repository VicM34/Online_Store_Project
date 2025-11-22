import json
import os

from src.store.models import Category, Product
from src.utils.json_loader import load_products_from_json, print_loaded_data


def main() -> None:
    """Основная функция приложения."""
    # Сбрасываем счетчики
    Category.category_count = 0
    Category.product_count = 0

    print("=== ДЕМОНСТРАЦИЯ РУЧНОГО СОЗДАНИЯ ОБЪЕКТОВ ===")

    # Существующий код создания объектов вручную
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print("=== Информация о товарах ===")
    print(product1)
    print(product2)
    print(product3)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print("\n=== Первая категория ===")
    print(category1)

    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product4],
    )

    print("\n=== Вторая категория ===")
    print(category2)
    print("Товары в категории:")
    # ИСПРАВЛЕНО: используем products_list вместо products
    for product in category2.products_list:
        print(f"  - {product}")

    print("\n=== Общая статистика ===")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")

    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ ЗАГРУЗКИ ИЗ JSON ФАЙЛА")
    print("=" * 50)

    # Сбрасываем счетчики для чистого теста JSON загрузки
    original_category_count = Category.category_count
    original_product_count = Category.product_count
    Category.category_count = 0
    Category.product_count = 0

    try:
        # Создаем абсолютный путь к файлу
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_file_dir)  # Поднимаемся на уровень выше (из src в корень)
        json_path = os.path.join(project_root, "data", "products.json")

        print(f"Ищем файл по пути: {json_path}")

        # Загружаем данные из JSON
        categories_from_json = load_products_from_json(json_path)
        print_loaded_data(categories_from_json)

        # Восстанавливаем оригинальные счетчики
        Category.category_count += original_category_count
        Category.product_count += original_product_count

        print("\n=== ИТОГОВАЯ СТАТИСТИКА (включая ручное создание) ===")
        print(f"Всего категорий: {Category.category_count}")
        print(f"Всего товаров: {Category.product_count}")

    except FileNotFoundError:
        print("Файл data/products.json не найден. Создайте файл для демонстрации.")

        # Показываем правильный путь для создания файла
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_file_dir)
        correct_data_path = os.path.join(project_root, "data", "products.json")
        print(f"Создайте файл по пути: {correct_data_path}")

    except json.JSONDecodeError as e:
        print(f"Ошибка в формате JSON: {e}")
    except KeyError as e:
        print(f"Ошибка в структуре данных: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
