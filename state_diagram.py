import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
from search import heuristic

def build_state_tree(initial_state, explored):
    """Construye un árbol de estados a partir de los estados explorados."""
    tree = nx.DiGraph()
    
    # Añadir todos los estados explorados y sus padres al árbol
    for state in explored:
        tree.add_node(state)
        if state.parent is not None:
            tree.add_edge(state.parent, state)
            
    # Garantizar que el estado inicial se encuentra en la raíz
    if initial_state not in tree:
        tree.add_node(initial_state)

    return tree

def hierarchical_pos(G, root, max_depth=5):
    """
    Posición jerárquica para dibujar el árbol limitado a una profundidad.
    Esta función es más robusta y previene KeyErrors.
    """
    pos = {root: (0, 0)}
    queue = deque([(root, 0)])
    visited = {root}
    
    layer_nodes = {0: [root]}
    
    while queue:
        parent, depth = queue.popleft()
        if depth >= max_depth:
            continue
            
        for child in sorted(list(G.successors(parent)), key=lambda s: s.cost):
            if child not in visited:
                visited.add(child)
                new_depth = depth + 1
                if new_depth not in layer_nodes:
                    layer_nodes[new_depth] = []
                layer_nodes[new_depth].append(child)
                pos[child] = (0, 0)
                queue.append((child, new_depth))

    for depth, nodes_at_depth in layer_nodes.items():
        num_nodes = len(nodes_at_depth)
        for i, node in enumerate(nodes_at_depth):
            x = (i - (num_nodes - 1) / 2) * 2
            y = -depth * 1.5
            pos[node] = (x, y)
    
    limited_tree = nx.DiGraph()
    for u, v in G.edges():
        if u in pos and v in pos:
            limited_tree.add_edge(u, v)

    return limited_tree, pos


class SokobanDiagram:
    def __init__(self, parent_frame, initial_state, explored, algorithm, max_depth=5):
        self.parent_frame = parent_frame
        self.initial_state = initial_state
        self.explored = explored
        self.algorithm = algorithm # 🔹 Nuevo parámetro
        self.max_depth = max_depth
        self.current_step = 0
        self.after_id = None

        self.fig, self.ax = plt.subplots(figsize=(6,6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.parent_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.full_tree = build_state_tree(self.initial_state, self.explored)
        
        # 🔹 Lógica para crear las etiquetas dinámicamente
        self.node_labels = {}
        for state in self.full_tree.nodes():
            if self.algorithm == "A*":
                g = state.cost
                h = heuristic(state)
                f = g + h
                self.node_labels[state] = f"{state.player}\ng:{g}, h:{h}\nf:{f}"
            else:
                self.node_labels[state] = f"{state.player}\n"
        
        # 🔹 Vínculo para detener la animación al cerrar la ventana
        self.parent_frame.bind("<Destroy>", self.stop_animation)

    def draw_step(self):
        if not self.parent_frame.winfo_exists():
            return
        
        if self.current_step >= len(self.explored):
            return

        step_state = self.explored[self.current_step]
        
        limited_tree, self.pos = hierarchical_pos(self.full_tree, root=self.initial_state, max_depth=self.max_depth)
        
        self.ax.clear()
        
        colors = []
        for n in limited_tree.nodes():
            if n == step_state:
                colors.append("lightgreen")
            elif step_state.parent and n == step_state.parent:
                colors.append("orange")
            else:
                colors.append("lightblue")

        nx.draw(
            limited_tree,
            self.pos,
            ax=self.ax,
            with_labels=True,
            labels=self.node_labels,
            node_color=colors,
            node_size=800,
            font_size=8,
            arrows=True
        )

        self.ax.set_title(f"Árbol de estados - Paso {self.current_step+1} / {len(self.explored)}")
        self.canvas.draw()

        self.current_step += 1
        self.after_id = self.parent_frame.after(500, self.draw_step)

    def stop_animation(self, event=None):
        if self.after_id:
            self.parent_frame.after_cancel(self.after_id)
            self.after_id = None

def show_sokoban_diagram(frame, initial_state, explored, algorithm):
    """Inicializa y muestra el diagrama, limitado a 3 niveles y jerárquico."""
    diagram = SokobanDiagram(frame, initial_state, explored, algorithm, max_depth=5)
    diagram.draw_step()
    return diagram