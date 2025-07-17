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

    def _add_car(self):
        pass

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
