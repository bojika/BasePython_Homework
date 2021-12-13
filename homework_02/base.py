from abc import ABC
from homework_02.exceptions import NotEnoughFuel, LowFuelError


class Vehicle(ABC):
    def __init__(self, weight: float = 0, fuel: float = 0, fuel_consumption: float = 0):
        self.weight = weight
        self.fuel = fuel
        self.fuel_consumption = fuel_consumption
        self.started = False

    def start(self):
        """
        Try to start the vehicle. If there is no fuel to start rise the LowFuelError exception.
        :return: None
        """
        if self.fuel > 0:
            self.started = True
        else:
            raise LowFuelError(self.fuel)

    def move(self, distance: float):
        """
        Try to move the vehicle. If there is no enough fuel to move rise the LowFuelError exception.
        :return: None
        """
        if self.fuel < self.fuel_consumption * distance:
            raise NotEnoughFuel(self.fuel * self.fuel_consumption)
        else:
            self.fuel -= self.fuel_consumption * distance
        if self.fuel == 0:
            self.started = False
