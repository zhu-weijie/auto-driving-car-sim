from app.car import Car
from app.field import Field
from app.simulation import Simulation


class CLI:
    def __init__(self):
        self.field = None
        self.cars = []
        self.commands = []

    def _ask_for_field_dimensions(self) -> Field:
        while True:
            try:
                raw_input = input(
                    "Please enter the width and height of the simulation field "
                    "in x y format: "
                )
                parts = raw_input.split()
                if len(parts) != 2:
                    raise ValueError

                width = int(parts[0])
                height = int(parts[1])

                field = Field(width, height)
                print(f"\nYou have created a field of {width} x {height}.")
                return field
            except ValueError:
                print(
                    "Invalid input. Please enter two positive integers separated "
                    "by a space."
                )

    def _ask_for_car_name(self) -> str:
        while True:
            name = input("Please enter the name of the car: ")
            if not name:
                print("Car name cannot be empty.")
            elif name in [car.name for car in self.cars]:
                print(f"Car with name '{name}' already exists.")
            else:
                return name

    def _ask_for_car_position(self, car_name: str) -> tuple[int, int, str]:
        prompt = (
            f"Please enter initial position of car {car_name} in x y Direction format: "
        )
        while True:
            raw = input(prompt)
            parts = raw.split()
            try:
                if len(parts) != 3:
                    raise ValueError("Invalid format.")

                x, y = int(parts[0]), int(parts[1])
                direction = parts[2].upper()

                if direction not in Car.VALID_DIRECTIONS:
                    raise ValueError("Invalid format.")
                if not self.field.is_within_bounds(x, y):
                    raise ValueError("Position is outside the field boundaries.")

                return x, y, direction
            except ValueError as e:
                print(e)

    def _ask_for_car_commands(self, car_name: str) -> str:
        prompt = f"Please enter the commands for car {car_name}: "
        while True:
            commands = input(prompt).upper()
            if all(c in "FLR" for c in commands):
                return commands
            else:
                print("Commands can only contain 'F', 'L', 'R'.")

    def _display_car_list(self):
        print("\nYour current list of cars are:")
        for i, car in enumerate(self.cars):
            print(
                f"- {car.name}, ({car.x},{car.y}) {car.direction}, {self.commands[i]}"
            )

    def _add_car(self):
        name = self._ask_for_car_name()
        x, y, direction = self._ask_for_car_position(name)
        commands = self._ask_for_car_commands(name)

        new_car = Car(name=name, x=x, y=y, direction=direction)
        self.cars.append(new_car)
        self.commands.append(commands)

        self._display_car_list()

    def _display_simulation_result(self, result: dict):
        print("\nAfter simulation, the result is:")
        if result["status"] == "OK":
            for car in result["cars"]:
                print(f"- {car.name}, ({car.x},{car.y}) {car.direction}")
        elif result["status"] == "COLLISION":
            collided_cars = result["cars"]
            for car in collided_cars:
                other_name = next(c.name for c in collided_cars if c.name != car.name)
                print(
                    f"- {car.name}, collides with {other_name} at "
                    f"{result['location']} at step {result['step']}"
                )

    def _show_end_menu(self) -> str:
        print("\nPlease choose from the following options:")
        print("[1] Start over")
        print("[2] Exit")
        while True:
            choice = input("> ")
            if choice == "1":
                return "START_OVER"
            elif choice == "2":
                return "EXIT"
            else:
                print("Invalid option. Please choose 1 or 2.")

    def _run_simulation(self):
        if not self.cars:
            print("\nThere are no cars to simulate.")
            return "CONTINUE"

        self._display_car_list()

        simulation = Simulation(self.field, self.cars, self.commands)
        result = simulation.run()

        self._display_simulation_result(result)

        return self._show_end_menu()

    def _show_main_menu(self):
        print("\nPlease choose from the following options:")
        print("[1] Add a car to field")
        print("[2] Run simulation")

        while True:
            choice = input("> ")
            if choice == "1":
                self._add_car()
                return "CONTINUE"
            elif choice == "2":
                return "RUN_SIMULATION"
            else:
                print("Invalid option. Please choose 1 or 2.")

    def start(self):
        while True:
            print("Welcome to Auto Driving Car Simulation!")
            self.field = self._ask_for_field_dimensions()
            self.cars = []
            self.commands = []

            while True:
                choice = self._show_main_menu()
                if choice == "RUN_SIMULATION":
                    final_action = self._run_simulation()
                    break

            if final_action == "EXIT":
                print("\nThank you for running the simulation. Goodbye!")
                break
