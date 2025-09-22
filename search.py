from collections import deque
import heapq
import itertools

# ============================================================
# BFS - Búsqueda en anchura (no informada)
# ============================================================
def bfs(initial_state):
    """Implementación de BFS: encuentra la ruta más corta en número de pasos."""
    frontier = deque([initial_state])
    visited = set([initial_state])
    explored = []
    
    while frontier:
        state = frontier.popleft()
        explored.append(state)

        if state.is_goal():
            return state.get_solution_path(), explored

        for neighbor in state.expand():
            if neighbor not in visited:
                visited.add(neighbor)
                frontier.append(neighbor)
    
    return None, explored


# ============================================================
# A* - Algoritmo informado
# ============================================================
def a_star(initial_state, heuristic):
    """
    A*: f(n) = g(n) + h(n)
    - g(n): costo desde el inicio
    - h(n): heurística (estimación a la meta)
    """
    frontier = []
    counter = itertools.count()  # contador incremental único
    h0 = heuristic(initial_state)
    heapq.heappush(frontier, (h0, next(counter), initial_state))
    visited = set()
    explored = []

    while frontier:
        f, _, state = heapq.heappop(frontier)
        explored.append(state)

        if state.is_goal():
            return state.get_solution_path(), explored

        visited.add(state)

        for neighbor in state.expand():
            if neighbor not in visited:
                g = neighbor.cost
                h = heuristic(neighbor)
                f = g + h
                heapq.heappush(frontier, (f, next(counter), neighbor))

    return None, explored



def heuristic(state):
    """Heurística: suma de distancias Manhattan de cada caja a la meta más cercana."""
    total = 0
    for box in state.boxes:
        dist = min(abs(box[0] - goal[0]) + abs(box[1] - goal[1]) for goal in state.goals)
        total += dist
    return total
