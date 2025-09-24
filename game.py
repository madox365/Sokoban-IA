import tkinter as tk
from PIL import Image, ImageTk
from state import State

TILE_SIZE = 50  # tamaño pixel

class SokobanGame:
    def __init__(self, root, level, initial_state, solution=None, exploration = None):
        self.root = root
        self.level = level
        self.initial_state = initial_state
        self.solution = solution or []
        self.exploration = exploration or []
        self.step = 0

        self.canvas = tk.Canvas(
            root,
            width=len(level[0]) * TILE_SIZE,
            height=len(level) * TILE_SIZE
        )
        self.canvas.pack(side="left")

        # cargar sprites
        self.images = {
            "#": ImageTk.PhotoImage(Image.open("assets/wall.png").resize((TILE_SIZE, TILE_SIZE))),
            ".": ImageTk.PhotoImage(Image.open("assets/goal.png").resize((TILE_SIZE, TILE_SIZE))),
            "$": ImageTk.PhotoImage(Image.open("assets/box.png").resize((TILE_SIZE, TILE_SIZE))),
            "@": ImageTk.PhotoImage(Image.open("assets/player.png").resize((TILE_SIZE, TILE_SIZE))),
            " ": ImageTk.PhotoImage(Image.open("assets/floor.png").resize((TILE_SIZE, TILE_SIZE)))
        }

    def draw_board(self, state: State):
        """Dibuja el tablero según un estado concreto"""
        self.canvas.delete("all")

        for y, row in enumerate(self.level):
            for x, cell in enumerate(row):
                # siempre dibujar primero el suelo
                self.canvas.create_image(
                    x * TILE_SIZE, y * TILE_SIZE,
                    image=self.images[" "], anchor="nw"
                )

                # paredes fijas
                if cell == "#":
                    self.canvas.create_image(
                        x * TILE_SIZE, y * TILE_SIZE,
                        image=self.images["#"], anchor="nw"
                    )

                # metas fijas
                if (x, y) in state.goals:
                    self.canvas.create_image(
                        x * TILE_SIZE, y * TILE_SIZE,
                        image=self.images["."], anchor="nw"
                    )

        # cajas dinámicas
        for bx, by in state.boxes:
            self.canvas.create_image(
                bx * TILE_SIZE, by * TILE_SIZE,
                image=self.images["$"], anchor="nw"
            )

        # jugador dinámico
        px, py = state.player
        self.canvas.create_image(
            px * TILE_SIZE, py * TILE_SIZE,
            image=self.images["@"], anchor="nw"
        )

    #Muestra la solucion final
    def animate_solution(self, state: State):
        """Ejecuta la solución paso a paso"""
        if self.step >= len(self.solution):
            return

        move = self.solution[self.step]
        dx, dy = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}[move]

        new_player = (state.player[0] + dx, state.player[1] + dy)
        new_boxes = set(state.boxes)

        # si empuja caja
        if new_player in new_boxes:
            new_box = (new_player[0] + dx, new_player[1] + dy)
            new_boxes.remove(new_player)
            new_boxes.add(new_box)

        next_state = State(
            new_player,
            new_boxes,
            state.goals,
            state.level,
            parent=state,
            action=move,
            cost=state.cost + 1
        )

        self.draw_board(next_state)
        self.step += 1
        self.animation_id  = self.root.after(500, lambda: self.animate_solution(next_state))

    #Muestra todos los estados posibles dependiendo del algoritmo
    def animate_exploration(self):
        if self.step < len(self.exploration):
            state = self.exploration[self.step]
            self.draw_board(state)
            self.step += 1
            self.animation_id = self.root.after(150, self.animate_exploration)
        else:
            # Reiniciamos step para la solución
            self.step = 0
            self.animate_solution(self.initial_state)
