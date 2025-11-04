class Product:
    """Класс для представления товара в магазине."""

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        """
        Инициализация объекта Product.
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self) -> str:
        """Строковое представление товара."""
        return f"{self.name}, {self.price}₽. Остаток: {self.quantity} шт."

    def __repr__(self) -> str:
        """Представление для разработчика."""
        return f"Product('{self.name}', {self.price}, {self.quantity})"
