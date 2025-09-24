import json
from state import State

def load_levels(filename="levels.json"):
    with open(filename, "r") as f:
        levels = json.load(f)
    return levels


def parse_level(level):
    """
    Convierte un nivel (lista de strings) en un State inicial (saca las posiciones de personaje y entorno).
    Ejemplo de nivel:
    [
        "#########",
        "#.$ @   #",
        "#########"
    ]
    """
    player = None
    boxes = set()
    goals = set()

    for y, row in enumerate(level):
        for x, cell in enumerate(row):
            if cell == "@":  # jugador
                player = (x, y)
            elif cell == "$":  # caja
                boxes.add((x, y))
            elif cell == ".":  # meta
                goals.add((x, y))
            elif cell == "*":  # caja en meta
                boxes.add((x, y))
                goals.add((x, y))
            elif cell == "+":  # jugador en meta
                player = (x, y)
                goals.add((x, y))
    
    # Crear y retornar el estado inicial
    return State(player, boxes, goals, level)
