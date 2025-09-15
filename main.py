import tkinter as tk
import time
from utils import load_levels, parse_level
from search import bfs, a_star, heuristic
from game import SokobanGame

class SokobanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sokoban AI")

        # Cargar niveles
        self.levels = load_levels("levels.json")
        self.current_level_index = tk.IntVar(value=0)
        self.algorithm = tk.StringVar(value="BFS")

        # Panel de controles
        control_frame = tk.Frame(root)
        control_frame.pack(side="right", fill="y", padx=10, pady=10)

        tk.Label(control_frame, text="Seleccionar nivel:").pack(anchor="w")
        tk.Spinbox(control_frame, from_=0, to=len(self.levels)-1,
                   textvariable=self.current_level_index, width=5).pack(anchor="w")

        tk.Label(control_frame, text="Algoritmo:").pack(anchor="w", pady=(10,0))
        tk.Radiobutton(control_frame, text="BFS", variable=self.algorithm, value="BFS").pack(anchor="w")
        tk.Radiobutton(control_frame, text="A*", variable=self.algorithm, value="A*").pack(anchor="w")

        tk.Button(control_frame, text="Resolver", command=self.run_solver).pack(anchor="w", pady=10)

        # Etiquetas para métricas
        self.steps_label = tk.Label(control_frame, text="Pasos: -")
        self.steps_label.pack(anchor="w", pady=(10,0))
        self.time_label = tk.Label(control_frame, text="Tiempo: -")
        self.time_label.pack(anchor="w")

        # Canvas
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(side="left")

        self.game = None  # se inicializará al resolver

    def run_solver(self):
        level_index = self.current_level_index.get()
        level = self.levels[level_index]
        initial_state = parse_level(level)

        print("Jugador:", initial_state.player)
        print("Cajas:", initial_state.boxes)
        print("Metas:", initial_state.goals)

        # Ejecutar algoritmo con medición de tiempo
        start_time = time.time()
        if self.algorithm.get() == "BFS":
            print("=== BFS ===")
            solution = bfs(initial_state)
        else:
            print("=== A* ===")
            solution = a_star(initial_state, heuristic)
        tiempoEjecucion = time.time() - start_time

        # Mostrar métricas
        if solution:
            print("Solución encontrada:", solution)
            print("Longitud:", len(solution))
            self.steps_label.config(text=f"Pasos: {len(solution)}")
        else:
            print("No se encontró solución")
            self.steps_label.config(text="Pasos: -")

        self.time_label.config(text=f"Tiempo: {tiempoEjecucion:.3f} s")

        # Crear o resetear GUI del tablero
        if self.game:
            self.game.canvas.destroy()
        self.game = SokobanGame(self.canvas_frame, level, solution)
        self.game.draw_board(initial_state)
        if solution:
            self.root.after(1000, lambda: self.game.animate_solution(initial_state))


def main():
    root = tk.Tk()
    app = SokobanApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
