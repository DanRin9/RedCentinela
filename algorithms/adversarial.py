from abc import ABC, abstractmethod

from algorithms.evaluation import evaluation_function
from world.game_state import GameState


class MultiAgentSearchAgent(ABC):
    """Clase base para los agentes de búsqueda adversaria."""

    def __init__(self, depth: int | str = 2) -> None:
        self.depth = int(depth)
        if self.depth < 1:
            raise ValueError("La profundidad debe ser al menos 1 ply")
        self.nodes_evaluated = 0

    @abstractmethod
    def get_action(self, state: GameState) -> str | None:
        raise NotImplementedError
      
  


class MinimaxAgent(MultiAgentSearchAgent):
    """Agente Minimax para el defensor MAX frente al intruso MIN."""

    def get_action(self, state: GameState) -> str | None:
        """
        Retorna la acción del defensor con mayor valor Minimax.

        El defensor es MAX (agente 0), el intruso es MIN (agente 1) y cada
        acción consume un ply. Debe respetar el orden de las acciones legales,
        usar evaluation_function en terminales y cortes, y contar cada estado
        procesado una vez en self.nodes_evaluated, incluida la raíz.

        Tips:
        - Use state.get_legal_actions(agent_index) y
          state.generate_successor(agent_index, action) para expandir el árbol.
        - Compruebe state.is_win(), state.is_lose() y el corte de profundidad;
          evalúe esos estados con evaluation_function(state).
        - El siguiente agente es (agent_index + 1) % state.get_num_agents().
          depth=1 incluye una acción de MAX y depth=2 una de MAX y una de MIN.
        - Reinicie las métricas y cuente una vez cada estado procesado, incluida
          la raíz. Retorne la acción de MAX y conserve la primera en los empates.
        """
        self.nodes_evaluated = 0
        self.nodes_evaluated += 1  # cuenta la raíz

        legal_acts = state.get_legal_actions(0)
        if not legal_acts:
            return None

        mejor_camino = ["", float("-inf")]  # camino, score

        for act in legal_acts:
            nodo_n = self.recursiva(state, act, 0, self.depth)
            score_nodo = evaluation_function(nodo_n)

            if score_nodo > mejor_camino[1]:
                mejor_camino[0] = act
                mejor_camino[1] = score_nodo

        return mejor_camino[0]
      
        
        
      
    
    def recursiva(self, state: GameState, accion: str, agent_i: int, depth: int) -> GameState:
        state2 = state.generate_successor(agent_i, accion)
        self.nodes_evaluated += 1

        if state2.is_win() or state2.is_lose() or depth == 1:
          return state2

        next_agent = (agent_i + 1) % state2.get_num_agents()
        acciones = state2.get_legal_actions(next_agent)

        estados = []
        scores = []

        #recursivo
        for act in acciones:
          estado = self.recursiva(state2, act, next_agent, depth-1)
          score = evaluation_function(estado)

          estados.append(estado)
          scores.append(score)

        if next_agent == 1:
          score_minimo = min(scores)
          pos = scores.index(score_minimo) #primera aparicion

        else:
          score_max = max(scores)
          pos = scores.index(score_max) #priemra

        return estados[pos]
          
          

class AlphaBetaAgent(MultiAgentSearchAgent):
    """Agente Minimax que evita explorar ramas mediante poda alfa-beta."""
    def yepa (self, depth):
        self.depth = depth
        self.nodes_evaluated = 0

    def get_action(self, state: GameState) -> str | None:
            """
            Retorna la acción de Minimax aplicando poda alfa-beta.
    
            Debe usar la misma profundidad, orden de acciones y función de
            evaluación que Minimax.
    
            Tips:
            - Conserve la misma estructura y casos base de MinimaxAgent.
            - Inicie alpha en -infinito y beta en +infinito, y páselos en las
              llamadas recursivas.
            - En MAX actualice alpha y corte si valor >= beta; en MIN actualice beta
              y corte si valor <= alpha.
            """

            self.nodes_evaluated = 0

            mejor_accion = self.alphabeta(state=state, agent_index=0,depth_left=self.depth, alpha=float("-inf"), beta=float("inf"))

            return mejor_accion

    def alphabeta(self, state: GameState, agent_index, depth_left, alpha, beta):
        self.nodes_evaluated += 1

        if state.is_win() or state.is_lose() or depth_left == 0:
            return evaluation_function(state), None

        acciones = state.get_legal_actions(agent_index)

        if not acciones:
            return evaluation_function(state), None

        num_agents = state.get_num_agents()
        next_agent = (agent_index + 1) % num_agents
        next_depth = depth_left - 1

        if agent_index == 0: 
            mejor_valor = float("-inf")
            for accion in acciones:
                sucesor = state.generate_successor(agent_index, accion)
                valor, _ = self.alphabeta(sucesor, next_agent, next_depth, alpha, beta)

                if valor > mejor_valor:
                    mejor_valor = valor
                    mejor_accion = accion

                alpha = max(alpha, mejor_valor)

                if mejor_valor >= beta:
                    break
                
            return mejor_valor, mejor_accion

        else:
            mejor_valor = float("inf")
            for accion in acciones:
                sucesor = state.generate_successor(agent_index, accion)
                valor, _ = self.alphabeta(sucesor, next_agent, next_depth, alpha, beta)

                if valor < mejor_valor:
                    mejor_valor = valor
                    mejor_accion = accion

                beta = min(beta, mejor_valor)

                if mejor_valor <= alpha:
                    break
                
            return mejor_valor, mejor_accion