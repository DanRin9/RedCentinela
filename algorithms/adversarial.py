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
      
    @abstractmethod
    def recursiva(self, state: GameState):
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
        
        
        
        mejor_camino = ["", -1001] #camino, score
        
        eval_func = evaluation_function(state) #0.0
        print(eval_func)
        
        agent_index = state.defender_position.index #<built-in method index of tuple object at 0x109f2fc00>
        print(f"Agent index {agent_index}") 
        
        defender_pos = state.defender_position #(4, 7)
        print(f"defender pos: {defender_pos}")
        
     
        
        legal_acts = state.get_legal_actions(0) #['North', 'South', 'Stop']
        print(f"legal acts: {legal_acts}")
        
        num_agents = state.get_num_agents() #2
        print(f"Num agents: {num_agents}")
        
        score = state.get_score() #0.0
        print(f"score: {score}")
        
        for act in legal_acts:
          
          nodo_n = self.recursiva(state, act, 0, self.depth)
          score_nodo = evaluation_function(nodo_n)
          
          if score_nodo > mejor_camino[1]:
            mejor_camino[0] = act
            mejor_camino[1] = score_nodo
            
        return mejor_camino[0]
      
        
        
      
    
    def recursiva(self, state: GameState, accion: str, agent_i: int, depth: int) -> GameState: #por que debo pasarle la depth??

        if state.is_win() or state.is_lose() or depth == 0:
          return state
        
        
        
        self.nodes_evaluated += 1
        next_agent = (agent_i + 1) % state.get_num_agents()
        
        state2 = state.generate_successor(next_agent, accion)
        
        estados = []
        scores = []
         
        acciones = state2.get_legal_actions(next_agent)
        
        
        
        
        #recursivo
        for act in acciones:
          
          estado = self.recursiva(state2,act,next_agent,depth-1)
          score = evaluation_function(estado)
          
          estados.append(estado)
          scores.append(score)
          
        if agent_i == 1:
          score_minimo = min(scores)
          pos = scores.index(score_minimo) #primera aparicion
          
        else:
          score_max = max(scores)
          pos = scores.index(score_max) #priemra 
          
        
          
        return estados[pos]
          
          
          
        
          
          
        
        
        
        
  
        
        


class AlphaBetaAgent(MultiAgentSearchAgent):
    """Agente Minimax que evita explorar ramas mediante poda alfa-beta."""

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
        # TODO: Add your code here
        raise NotImplementedError("Punto 5: implemente AlphaBetaAgent.get_action")
