import math
import random

from optimization.problem import SmartGridOptimizationProblem
from optimization.result import Configuration, OptimizationResult


def configuration_score(
    problem: SmartGridOptimizationProblem, configuration: Configuration
) -> float:
    """
    Combina cobertura, redundancia y exposición en un puntaje a maximizar.

    Tips:
    - Use problem.score_components(configuration); ya retorna cobertura,
      redundancia y exposición en ese orden.
    """

    cobertura, redundancia, exposicion = problem.score_components(configuration)
    return cobertura - redundancia - exposicion


def hill_climbing(
    problem: SmartGridOptimizationProblem,
    initial_configuration: Configuration,
    max_iterations: int = 500,
) -> OptimizationResult:
    """
    Ejecuta ascenso de colina con mejora estricta.

    Debe examinar todos los vecinos, seleccionar el de mayor puntaje y
    conservar el orden entregado por el problema para desempatar. La búsqueda
    termina cuando no existe una mejora estricta o se alcanza el límite.

    Tips:
    - problem.neighbors(current) retorna vecinos válidos en el orden que debe
      usarse para desempatar.
    - Inicialice los historiales con la configuración inicial y agregue solo las
      mejoras aceptadas antes de retornar el OptimizationResult.
    """
    current = initial_configuration
    current_score = configuration_score(problem, current)

    evaluations = 1
    iterations = 0

    history = [current]
    score_history = [current_score]

    while iterations < max_iterations:
        neighbors = problem.neighbors(current)

        best_neighbor = None
        best_neighbor_score = None
        for neighbor in neighbors:
            score = configuration_score(problem, neighbor)
            evaluations += 1
            if best_neighbor_score is None or score > best_neighbor_score:
                best_neighbor = neighbor
                best_neighbor_score = score

        if best_neighbor is None or best_neighbor_score <= current_score:
            break

        current = best_neighbor
        current_score = best_neighbor_score
        iterations += 1

        history.append(current)
        score_history.append(current_score)

    return OptimizationResult(
        best_configuration=current,
        best_score=current_score,
        evaluations=evaluations,
        iterations=iterations,
        history=history,
        score_history=score_history,
    )


def cooling_schedule(initial_temperature: float, cooling_rate: float, iteration: int) -> float:
    """
    Retorna el programa geométrico T(t) = T0 * alpha**t.

    Esta función se invoca desde simulated_annealing en cada iteración.
    """
    return initial_temperature * cooling_rate ** iteration


def simulated_annealing(
    problem: SmartGridOptimizationProblem,
    initial_configuration: Configuration,
    initial_temperature: float = 20.0,
    cooling_rate: float = 0.97,
    max_iterations: int = 500,
    rng: random.Random | None = None,
) -> OptimizationResult:
    """
    Ejecuta recocido simulado para un problema de maximización.

    Debe proponer un vecino aleatorio por iteración, aceptar siempre las
    mejoras y aplicar exp(delta / temperature) en los demás casos. El estado
    actual y el mejor estado encontrado deben conservarse por separado.

    Tips:
    - Seleccione el candidato con rng.choice(problem.neighbors(current)) y use
      exclusivamente rng para conservar la reproducibilidad.
    - Obtenga la temperatura con cooling_schedule(...) y calcule la aceptación
      con delta = puntaje_candidato - puntaje_actual y math.exp(...).
    - Mantenga separados el estado actual y el mejor encontrado; registre el
      estado actual después de cada intento, incluso si se rechaza.
    - Detenga la ejecución cuando la temperatura alcance minimum_temperature.
    """
    rng = rng or random.Random()
    minimum_temperature = 1e-9

    current = initial_configuration
    best = current 
    t = 0
    evaluations = 0

    current_score = configuration_score(problem, current)
    best_score = current_score 

    temp = cooling_schedule(initial_temperature, cooling_rate, t )
    history = [current]
    score_history = [current_score]

    while temp > minimum_temperature and t < max_iterations: 
        vecino = rng.choice(problem.neighbors(current))
        vecino_score = configuration_score(problem, vecino)
        evaluations += 1
        delta = vecino_score - current_score
        if delta > 0: 
            current = vecino
            current_score = vecino_score

        else: 
            if rng.random() < math.exp(delta/temp): 
                current = vecino
                current_score = vecino_score
        
        if current_score > best_score: 
            best = current 
            best_score = current_score

        score_history.append(current_score)
        history.append(current)

        t += 1
        temp = cooling_schedule(initial_temperature, cooling_rate, t)

    return OptimizationResult(
        best_configuration=best,
        best_score=best_score,
        evaluations=evaluations,
        iterations=t,
        history=history,
        score_history=score_history,
    )



def one_point_crossover(
    parent1: Configuration, parent2: Configuration, rng: random.Random
) -> tuple[Configuration, Configuration]:
    """
    Realiza un cruce de un punto y retorna dos descendientes.

    La reparación de la cantidad de módulos se realiza posteriormente.

    Tips:
    - Seleccione con rng un corte interior, entre las posiciones 1 y len-1.
    - Cada descendiente combina el prefijo de un padre con el sufijo del otro.
    - Retorne tuplas y no repare aquí los descendientes.
    """
    if len(parent1) != len(parent2):
        raise ValueError("Los padres deben tener la misma longitud")
    if len(parent1) < 2:
        return parent1, parent2

    rango_corte = rng.randint(1, len(parent1)-1)

    son = parent1[:rango_corte] + parent2[rango_corte:]
    daughter = parent2[:rango_corte] + parent1[rango_corte:]

    return son, daughter


def swap_mutation(
    individual: Configuration, mutation_probability: float, rng: random.Random
) -> Configuration:
    """
    Aplica mutación por intercambio con la probabilidad indicada.

    Cuando ocurre una mutación, intercambia un bit activo y uno inactivo para
    conservar la cantidad de módulos instalados.

    Tips:
    - Use rng.random() para decidir si se aplica la mutación.
    - Identifique por separado los índices activos e inactivos y seleccione uno
      de cada grupo con rng.choice(...).
    - Si alguno de los dos grupos está vacío, no hay un intercambio posible.
    - Retorne una tupla nueva; no modifique el individuo recibido.
    """
    if rng.random() >= mutation_probability: 
        return individual

    activos = [i for i, bit in enumerate(individual) if bit == 1]
    inactivos = [i for i, bit in enumerate(individual) if bit == 0]

    if activos == [] or inactivos == []: 
        return individual
    
    posicion_activa = rng.choice(activos)
    posicion_inactiva =  rng.choice(inactivos)

    nueva = list(individual)
    nueva[posicion_activa] = 0
    nueva[posicion_inactiva] = 1 
          
    return tuple(nueva)


def genetic_algorithm(
    problem: SmartGridOptimizationProblem,
    population_size: int = 40,
    generations: int = 100,
    mutation_probability: float = 0.05,
    elite_size: int = 2,
    rng: random.Random | None = None,
) -> OptimizationResult:
    """
    Ejecuta un algoritmo genético generacional.

    Debe integrar la población inicial, la selección por torneo, el cruce, la
    reparación, la mutación y el elitismo entregados por el proyecto. Retorna
    el mejor individuo encontrado durante toda la ejecución.

    Tips:
    - Use problem.initial_population(...), problem.tournament_select(...) y
      problem.repair_configuration(...) para las operaciones ya entregadas.
    - Aplique one_point_crossover(...) antes de reparar y swap_mutation(...)
      después de la reparación.
    - Conserve los mejores individuos por elitismo y registre en los historiales
      el mejor global de cada generación.
    """
    rng = rng or random.Random()


    if population_size < 2:
        raise ValueError("La población debe tener al menos dos individuos")
    if generations < 0:
        raise ValueError("El número de generaciones no puede ser negativo")
    if not 0.0 <= mutation_probability <= 1.0:
        raise ValueError("La probabilidad de mutación debe estar entre 0 y 1")
    if not 0 <= elite_size <= population_size:
        raise ValueError("elite_size debe estar entre 0 y population_size")

    poblacion = problem.initial_population(population_size, rng)
    evaluaciones = 0

    scores = [configuration_score(problem, ind) for ind in poblacion]
    evaluaciones += len(poblacion)

    mejor_indice = max(range(len(scores)), key=lambda x: scores[x])

    best_global = poblacion[mejor_indice]
    best_score_global = scores[mejor_indice]

    history = [best_global]
    score_history = [best_score_global]

    for _ in range(generations):
        nueva_poblacion = []
        ordenar_poblacion = sorted(poblacion, key=lambda ind: configuration_score(problem, ind), reverse=True)
        primeros_mejores = ordenar_poblacion[:elite_size]

        for m in primeros_mejores:
            nueva_poblacion.append(m)

        while len(nueva_poblacion) < population_size:
            padre1 = problem.tournament_select(poblacion, scores, rng)
            padre2 = problem.tournament_select(poblacion, scores, rng)
            hijo1, hijo2 = one_point_crossover(padre1, padre2, rng)
            hijo1 = problem.repair_configuration(hijo1, rng)
            hijo2 = problem.repair_configuration(hijo2, rng)
            hijo1 = swap_mutation(hijo1, mutation_probability, rng)
            hijo2 = swap_mutation(hijo2, mutation_probability, rng)

            espacio_libre = population_size - len(nueva_poblacion)

            if espacio_libre >= 2:
                nueva_poblacion.append(hijo1)
                nueva_poblacion.append(hijo2)
            else:
                nueva_poblacion.append(hijo1)

        poblacion = nueva_poblacion
        scores = [configuration_score(problem, ind) for ind in poblacion]
        evaluaciones += len(poblacion)

        idx = max(range(len(scores)), key=lambda j: scores[j])
        if scores[idx] > best_score_global:
            best_global = poblacion[idx]
            best_score_global = scores[idx]

        history.append(best_global)
        score_history.append(best_score_global)

    return OptimizationResult(
        best_configuration=best_global,
        best_score=best_score_global,
        evaluations=evaluaciones,
        iterations=generations,
        history=history,
        score_history=score_history,
    )


