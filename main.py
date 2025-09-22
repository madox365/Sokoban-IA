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
        tk.Button(control_frame, text="Mostrar pasos", command=self.show_steps).pack(anchor="w", pady=5)


        # Etiquetas para métricas
        self.steps_label = tk.Label(control_frame, text="Pasos: -")
        self.steps_label.pack(anchor="w", pady=(10,0))
        self.time_label = tk.Label(control_frame, text="Tiempo: -")
        self.time_label.pack(anchor="w")

        # Canvas
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(side="left")

        self.game = None  # se inicializará al resolver
        self.solution = None
        self.explored = None
        self.initial_state = None
        self.speed = 200

    def run_solver(self):
        level_index = self.current_level_index.get()
        level = self.levels[level_index]
        self.initial_state = parse_level(level)

        print("Jugador:", self.initial_state.player)
        print("Cajas:", self.initial_state.boxes)
        print("Metas:", self.initial_state.goals)

        # Ejecutar algoritmo con medición de tiempo
        start_time = time.time()
        if self.algorithm.get() == "BFS":
            print("=== BFS ===")
            self.solution, self.explored = bfs(self.initial_state)
        else:
            print("=== A* ===")
            self.solution, self.explored = a_star(self.initial_state, heuristic)
        tiempoEjecucion = time.time() - start_time

        # Mostrar métricas
        if self.solution:
            print("Solución encontrada:", self.solution)
            print("Longitud:", len(self.solution))
            self.steps_label.config(text=f"Pasos: {len(self.solution)}")
        else:
            print("No se encontró solución")
            self.steps_label.config(text="Pasos: -")

        self.time_label.config(text=f"Tiempo: {tiempoEjecucion:.3f} s")

        # Crear o resetear GUI del tablero
        if self.game:
            if self.game.animation_id: 
                self.root.after_cancel(self.game.animation_id)
            self.game.canvas.destroy()

        
        self.game = SokobanGame(self.canvas_frame, level, self.initial_state , solution = self.solution, exploration = self.explored)
        self.game.draw_board(self.initial_state)
        
        if self.solution:
           self.root.after(100, lambda: self.game.animate_solution(self.initial_state))

    def show_steps(self):
            """Muestra el paso a paso de la exploración"""
            if not self.game or not self.explored:
                print("Primero ejecuta Resolver para generar estados")
                return

            # Reiniciar canvas con el estado inicial
            self.game.canvas.destroy()
            level_index = self.current_level_index.get()
            level = self.levels[level_index]
            self.game = SokobanGame(self.canvas_frame, level, self.initial_state, solution=self.solution, exploration=self.explored)
            self.game.draw_board(self.initial_state)

            # Animar exploración
            self.root.after(100, self.game.animate_exploration)

def main():
    root = tk.Tk()
    app = SokobanApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
