class PhoneNumber:
    def __init__(self, number: str):
        if not number.isdigit() or len(number) != 11 or not number.startswith("7"):
            raise ValueError("Номер телефона должен содержать 11 цифр и начинаться с '7'.")
        self._number = number

    @property
    def number(self):
        return self._number

    def to_dict(self):
        """Сериализовать объект в строку."""
        return self._number

    @classmethod
    def from_dict(cls, data):
        """Десериализовать объект из строки."""
        return cls(data)

    def __str__(self):
        return self._number