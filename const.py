import os

MAIN_WINDOW_WIDTH = 1024
MAIN_WINDOW_HEIGHT = 728

PIZZA_SIZE_KOEF = {
    25: 0.625,
    30: 0.75,
    35: 0.875,
    40: 1
}

PIZZA_MAX_SIZE_CM = 40
PIZZA_MAX_SIZE_PIX = 600
PIZZA_MAX_DIAM_PIX = PIZZA_MAX_SIZE_PIX * 0.875

PIZZA_MAX_INGREDIENTS = {
    25: 5,
    30: 8,
    35: 12,
    40: 15
}

APP_DIR = os.path.dirname(__file__) + "/"

PIZZAS_PICTURES_DIR = os.getcwd() + "/pizzas_pictures"
os.makedirs(PIZZAS_PICTURES_DIR, exist_ok=True)
