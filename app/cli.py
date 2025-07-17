from app.field import Field


class CLI:
    def __init__(self):
        self.field = None

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

    def start(self):
        print("Welcome to Auto Driving Car Simulation!")
        self.field = self._ask_for_field_dimensions()
