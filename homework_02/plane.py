"""
создайте класс `Plane`, наследник `Vehicle`
"""


from homework_02.base import Vehicle
from homework_02.exceptions import CargoOverload


class Plane(Vehicle):
    def __init__(self, weight: float = 0, fuel: float = 0, fuel_consumption: float = 0, max_cargo: float = 0):
        super().__init__(weight, fuel, fuel_consumption)
        self.cargo = 0
        self.max_cargo = max_cargo

    def load_cargo(self, new_cargo: float):
        if new_cargo + self.cargo > self.max_cargo:
            raise CargoOverload(self.max_cargo - self.cargo)
        else:
            self.cargo += new_cargo

    def remove_all_cargo(self):
        total_shipped = self.cargo
        self.cargo = 0
        return total_shipped
