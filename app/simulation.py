from app.car import Car
from app.field import Field


class Simulation:
    def __init__(self, field: Field, cars: list[Car], commands: list[str]):
        self.field = field
        self.cars = cars
        self.commands = commands

    def run(self):
        car = self.cars[0]
        command_sequence = self.commands[0]

        for command in command_sequence:
            if command == "L":
                car.turn_left()
            elif command == "R":
                car.turn_right()
            elif command == "F":
                next_x, next_y = car.calculate_forward_position()
                if self.field.is_within_bounds(next_x, next_y):
                    car.x = next_x
                    car.y = next_y
