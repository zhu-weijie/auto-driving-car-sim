from app.car import Car
from app.field import Field


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

    def _run_simulation(self):
        return "STOP"

    def _show_main_menu(self):
        print("\nPlease choose from the following options:")
        print("[1] Add a car to field")
        print("[2] Run simulation")

        while True:
            choice = input("> ")
            if choice == "1":
                self._add_car()
                return None
            elif choice == "2":
                return self._run_simulation()
            else:
                print("Invalid option. Please choose 1 or 2.")

    def start(self):
        print("Welcome to Auto Driving Car Simulation!")
        self.field = self._ask_for_field_dimensions()

        while True:
            result = self._show_main_menu()
            if result == "STOP":
                break
