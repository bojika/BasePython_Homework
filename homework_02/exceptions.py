"""
Объявите следующие исключения:
- LowFuelError
- NotEnoughFuel
- CargoOverload
"""


class LowFuelError(Exception):
    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f'There is no fuel.'


class NotEnoughFuel(Exception):
    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f'Not enough fuel. Available distance is no more than {self.value}'


class CargoOverload(Exception):
    def __init__(self, value: float):
        self.value = value

    def __str__(self):
        return f"Cargo overload. Available cargo weight is no more than {self.value}"

