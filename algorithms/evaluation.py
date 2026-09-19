import math

from world.game_state import GameState


def base_evaluation_function(state: GameState) -> float:
    """
    Retorna la evaluación base entregada para desarrollar el punto 4.

    Esta función no forma parte del código que debe modificar el estudiante y
    permite probar Minimax antes de desarrollar la heurística del punto 5.
    """
    if state.is_win():
        return 1000.0
    if state.is_lose():
        return -1000.0
    return float(state.get_score())


def evaluation_function(state: GameState) -> float:
    """
    Evalúa un estado desde la perspectiva del defensor MAX.

    Debe conservar las utilidades terminales de la evaluación base y diseñar
    una valoración no trivial para estados de corte. Minimax y alfa-beta usan
    esta misma función al comparar sus decisiones en el punto 5.

    Tips:
    - Los estados terminales ya se resuelven antes del bloque TODO; diseñe allí
      únicamente la valoración de estados no terminales.
    - Consulte state.defender_position, state.intruder_position,
      state.pending_terminals, state.get_score() y state.get_legal_actions(0).
    - state.layout.distance(start, goal) calcula y almacena en caché la distancia
      real por el mapa respetando los muros.
    - Maneje conjuntos vacíos y distancias infinitas, y mantenga todo estado no
      terminal estrictamente entre -1000 y +1000.
    """
    if state.is_win() or state.is_lose():
        return base_evaluation_function(state)

    posicion_defensor = state.defender_position
    mapa = state.layout

    distancia_terminal_cercana = math.inf
    for terminal in state.pending_terminals:
        distancia = mapa.distance(posicion_defensor, terminal)
        distancia_terminal_cercana = min(distancia_terminal_cercana, distancia)

    # penalizar intruso cercano
    distancia_intruso = mapa.distance(
        posicion_defensor,
        state.intruder_position,
    )

    if math.isinf(distancia_intruso):
        valor_seguridad = 60.0
    elif distancia_intruso <= 1:
        valor_seguridad = -300.0
    elif distancia_intruso == 2:
        valor_seguridad = -140.0
    else:
        distancia_segura = min(distancia_intruso, 12)
        valor_seguridad = 6.0 * distancia_segura

    if math.isinf(distancia_terminal_cercana):
        valor_terminal = -300.0
    else:
        valor_terminal = -6.0 * distancia_terminal_cercana

    acciones_legales = state.get_legal_actions(0)
    cantidad_movimientos = len(acciones_legales) - 1
    valor_movilidad = 3.0 * cantidad_movimientos

    valor = float(state.get_score())
    valor -= 20.0 * len(state.pending_terminals)
    valor += valor_terminal
    valor += valor_seguridad
    valor += valor_movilidad

    if valor >= 1000.0:
        return 999.0
    if valor <= -1000.0:
        return -999.0
    return valor
