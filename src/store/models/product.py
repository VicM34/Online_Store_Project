from abc import ABC, abstractmethod
from typing import Any, List, Optional


class CreationLoggerMixin:
    """Миксин для логирования создания объектов."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        # Вызываем следующий класс в MRO
        super().__init__(*args, **kwargs)
        # Логируем создание объекта
        class_name = self.__class__.__name__
        params = ", ".join([repr(arg) for arg in args])
        print(f"Создан объект {class_name}({params})")


class ZeroQuantityError(Exception):
    """Пользовательское исключение для товаров с нулевым количеством."""

    pass


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        pass

    @abstractmethod
    def __str__(self) -> str:
        """Абстрактный метод строкового представления."""
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """Абстрактный метод представления для разработчика."""
        pass

    @abstractmethod
    def __add__(self, other: Any) -> float:
        """Абстрактный метод сложения продуктов."""
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        """Абстрактный геттер для цены."""
        pass

    @price.setter
    @abstractmethod
    def price(self, value: float) -> None:
        """Абстрактный сеттер для цены."""
        pass


class Product(CreationLoggerMixin, BaseProduct):
    """Базовый класс для представления товара в магазине."""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        super().__init__(name, description, price, quantity)

        if quantity <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")

        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self) -> str:
        """Строковое представление товара в формате: Название, X руб. Остаток: X шт."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self) -> str:
        """Представление для разработчика."""
        return f"Product('{self.name}', '{self.description}', {self.price}, {self.quantity})"

    def __add__(self, other: "Product") -> float:
        """
        Сложение продуктов - возвращает общую стоимость всех товаров на складе.
        """
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product")

        # Проверка, что классы одинаковые
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов")

        return (self.price * self.quantity) + (other.price * other.quantity)

    @classmethod
    def new_product(cls, product_data: dict, products_list: Optional[List["Product"]] = None) -> "Product":
        """
        Создает новый товар или обновляет существующий.
        """
        name = product_data.get("name")
        description = product_data.get("description", "")
        price = product_data.get("price", 0)
        quantity = product_data.get("quantity", 0)

        # Проверка обязательных полей
        if not name:
            raise ValueError("Имя товара обязательно")

        # Приведение типов для безопасности
        name = str(name)
        description = str(description)
        price = float(price)
        quantity = int(quantity)

        # Проверка на дубликаты
        if products_list:
            for existing_product in products_list:
                if existing_product.name.lower() == name.lower():
                    # Объединяем количество и выбираем максимальную цену
                    existing_product.quantity += quantity
                    if price > existing_product.price:
                        existing_product.price = price
                    return existing_product

        # Создаем новый товар
        return cls(name, description, price, quantity)

    @property
    def price(self) -> float:
        """Геттер для цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверкой валидности."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        # Подтверждение понижения цены
        if new_price < self.__price:
            confirmation = input(f"Цена понижается с {self.__price} до {new_price}. Подтвердите (y/n): ")
            if confirmation.lower() != "y":
                print("Изменение цены отменено")
                return

        self.__price = new_price


class Smartphone(Product):
    """Класс для представления смартфона."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __repr__(self) -> str:
        """Представление для разработчика."""
        return (
            f"Smartphone('{self.name}', '{self.description}', {self.price}, {self.quantity}, "
            f"efficiency={self.efficiency}, model='{self.model}', "
            f"memory={self.memory}, color='{self.color}')"
        )


class LawnGrass(Product):
    """Класс для представления травы газонной."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __repr__(self) -> str:
        """Представление для разработчика."""
        return (
            f"LawnGrass('{self.name}', '{self.description}', {self.price}, {self.quantity}, "
            f"country='{self.country}', germination_period='{self.germination_period}', "
            f"color='{self.color}')"
        )
