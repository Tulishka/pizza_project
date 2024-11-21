from model import Pizza


class State:
    current_pizza: Pizza = Pizza(0, 1, 40, 1)


def current_pizza() -> Pizza:
    return State.current_pizza


def new_pizza(dough_type: int, size: int, souse: int):
    State.current_pizza = Pizza(0, dough_type, size, souse)
