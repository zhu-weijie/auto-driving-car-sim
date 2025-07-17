from app.car import Car
from app.field import Field


class Simulation:
    def __init__(self, field: Field, cars: list[Car], commands: list[str]):
        self.field = field
        self.cars = cars
        self.commands = commands

    def run(self) -> dict:
        if not self.cars:
            return {"status": "OK", "cars": []}

        max_steps = max(len(cmd) for cmd in self.commands) if self.commands else 0

        for step in range(max_steps):
            for i, car in enumerate(self.cars):
                command_sequence = self.commands[i]
                if step < len(command_sequence):
                    command = command_sequence[step]
                    if command == "L":
                        car.turn_left()
                    elif command == "R":
                        car.turn_right()
                    elif command == "F":
                        next_x, next_y = car.calculate_forward_position()
                        if self.field.is_within_bounds(next_x, next_y):
                            car.x = next_x
                            car.y = next_y

        return {"status": "OK", "cars": self.cars}
