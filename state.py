class State:
    def __init__(self, player, boxes, goals, level, parent=None, action=None, cost=0):
        """
        Representa un estado del juego Sokoban.
        - player: (x,y) posición del jugador
        - boxes: frozenset de posiciones de cajas {(x1,y1), (x2,y2), ...}
        - goals: frozenset de metas {(x1,y1), (x2,y2), ...}
        - level: el mapa (lista de strings con paredes)
        - parent: referencia al estado anterior (para reconstruir camino)
        - action: movimiento que llevó a este estado ("U","D","L","R")
        - cost: costo acumulado (para A*)
        """
        self.player = player
        self.boxes = frozenset(boxes)
        self.goals = frozenset(goals if goals is not None else [])
        self.level = level
        self.parent = parent
        self.action = action
        self.cost = cost

    # ---------------------------
    # Reglas del juego
    # ---------------------------
    def is_goal(self):
        """Un estado es objetivo si todas las cajas están en las metas."""
        return self.boxes == self.goals
    
    def is_deadlock(self, boxes):
        """
        Detecta deadlocks simples:
        - Caja contra esquina (pared arriba/izquierda, etc.)
        - Caja contra pared en celda que no es meta
        """
        for (x, y) in boxes:
            if (x, y) not in self.goals:
                # Revisar esquinas
                if (self.level[y-1][x] == "#" or self.level[y+1][x] == "#") and \
                (self.level[y][x-1] == "#" or self.level[y][x+1] == "#"):
                    return True
        return False

    def expand(self):
        """Genera los estados vecinos (jugador moviéndose arriba/abajo/izq/der)."""
        moves = {
            "U": (0, -1),
            "D": (0, 1),
            "L": (-1, 0),
            "R": (1, 0)
        }

        neighbors = []
        for action, (dx, dy) in moves.items():
            new_player = (self.player[0] + dx, self.player[1] + dy)

            # 1. Si choca con pared, no es válido
            if self.level[new_player[1]][new_player[0]] == "#":
                continue

            new_boxes = set(self.boxes)

            # 2. Si hay caja en la nueva posición del jugador
            if new_player in self.boxes:
                new_box = (new_player[0] + dx, new_player[1] + dy)

                # Si detrás hay pared o caja → no se puede empujar
                if self.level[new_box[1]][new_box[0]] == "#" or new_box in self.boxes:
                    continue

                # Mover la caja
                new_boxes.remove(new_player)
                new_boxes.add(new_box)

                # Chequeo de deadlocks  -> por ejemplo cajas en esquinas
                if self.is_deadlock(new_boxes):
                    continue

            # Crear nuevo estado
            neighbors.append(
                State(
                    new_player,
                    new_boxes,
                    self.goals,
                    self.level,
                    parent=self,
                    action=action,
                    cost=self.cost + 1
                )
            )

        return neighbors

    def get_solution_path(self):
        """Reconstruye el camino desde el estado inicial hasta aquí."""
        path = []
        state = self
        while state.parent is not None:
            path.append(state.action)
            state = state.parent
        return list(reversed(path))
    
    


    # ---------------------------
    # Necesario para sets y dicts
    # ---------------------------
    def __hash__(self):
        return hash((self.player, self.boxes))

    def __eq__(self, other):
        return (self.player, self.boxes) == (other.player, other.boxes)

