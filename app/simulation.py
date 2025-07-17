import copy

from app.car import Car
from app.field import Field


class Simulation:
    def __init__(self, field: Field, cars: list[Car], commands: list[str]):
        self.field = field
        self.cars = [copy.deepcopy(c) for c in cars]
        self.commands = commands

    def run(self) -> dict:
        if not self.cars:
            return {"status": "OK", "cars": self.cars}

        max_steps = max((len(c) for c in self.commands), default=0)

        for step in range(max_steps):
            for i, car in enumerate(self.cars):
                if step < len(self.commands[i]):
                    command = self.commands[i][step]
                    if command == "L":
                        car.turn_left()
                    elif command == "R":
                        car.turn_right()

            potential_positions = {}
            for i, car in enumerate(self.cars):
                current_pos = (car.x, car.y)
                next_pos = current_pos
                if step < len(self.commands[i]) and self.commands[i][step] == "F":
                    calculated_pos = car.calculate_forward_position()
                    if self.field.is_within_bounds(
                        calculated_pos[0], calculated_pos[1]
                    ):
                        next_pos = calculated_pos
                potential_positions[car.name] = next_pos

            occupied_positions = {}
            for car_name, pos in potential_positions.items():
                if pos not in occupied_positions:
                    occupied_positions[pos] = []
                occupied_positions[pos].append(car_name)

            for pos, occupants in occupied_positions.items():
                if len(occupants) > 1:
                    collided_cars = [c for c in self.cars if c.name in occupants]
                    for car in collided_cars:
                        car.x, car.y = pos

                    return {
                        "status": "COLLISION",
                        "step": step + 1,
                        "location": pos,
                        "cars": collided_cars,
                    }

            for car in self.cars:
                car.x, car.y = potential_positions[car.name]

        return {"status": "OK", "cars": self.cars}
