class Car:
    VALID_DIRECTIONS = {"N", "E", "S", "W"}
    _DIRECTIONS_SEQUENCE = ["N", "E", "S", "W"]

    def __init__(self, name: str, x: int, y: int, direction: str):
        if direction not in self.VALID_DIRECTIONS:
            raise ValueError("Direction must be one of N, E, S, W")

        self.name = name
        self.x = x
        self.y = y
        self.direction = direction

    def turn_left(self):
        current_index = self._DIRECTIONS_SEQUENCE.index(self.direction)
        new_index = (current_index - 1) % 4
        self.direction = self._DIRECTIONS_SEQUENCE[new_index]

    def turn_right(self):
        current_index = self._DIRECTIONS_SEQUENCE.index(self.direction)
        new_index = (current_index + 1) % 4
        self.direction = self._DIRECTIONS_SEQUENCE[new_index]

    def calculate_forward_position(self) -> tuple[int, int]:
        pass

    def __repr__(self) -> str:
        return (
            f"Car(name={self.name}, x={self.x}, y={self.y}, direction={self.direction})"
        )
