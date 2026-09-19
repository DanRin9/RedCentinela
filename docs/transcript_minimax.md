# Transcript — Implementación de `MinimaxAgent.get_action` (Taller 2, RedCentinela)

Contexto: Punto 4 del taller, curso ISIS-1611 (Uniandes). El objetivo era implementar
`MinimaxAgent.get_action` en `algorithms/adversarial.py`, partiendo de una situación
de bloqueo total ("no sé en qué archivo tengo que hacer mi función") hasta una
solución funcional.

---

## 1. Prompt inicial

> Estoy en el Taller 2 de Inteligencia Artificial (ISIS-1611, Uniandes), proyecto RedCentinela.
> Mi parte es implementar MinimaxAgent.get_action en algorithms/adversarial.py. Un compañero
> del grupo ya resolvió las funciones de optimización (hill climbing, recocido, genético), así
> que céntrate solo en esto.
>
> Mi problema NO es el algoritmo — minimax lo entiendo bien en papel (sé armar el árbol,
> sé razonar MAX/MIN). Mi problema es leer proyectos de código ajenos y acoplados: cuando veo
> varias clases y métodos que se llaman entre sí, no logro entender qué hace cada uno ni cómo
> usarlos para escribir mi solución. Antes solo había programado estructuras de datos propias
> donde yo decidía los métodos; aquí los métodos ya existen y no sé "engancharme" a ellos.
>
> Por eso quiero que trabajes así, en este orden, sin escribirme la función todavía:
>
> 1. Léete GameState (world/game_state.py) y explícame en términos simples qué me da cada
>    método que voy a necesitar (get_legal_actions, generate_successor, is_win, is_lose,
>    get_num_agents) — qué recibe, qué devuelve, si muta el objeto o crea uno nuevo.
> 2. Ayúdame a ver ESTE proyecto como el árbol de minimax que ya sé dibujar: qué es un nodo
>    aquí, qué es una arista, dónde está la profundidad.
> 3. Guíame para escribir yo mismo get_action, paso a paso, revisando lo que yo escriba y
>    corrigiéndome — no me des la función completa de una vez.
>
> Quiero llegar al código yo, entendiéndolo. No me des la solución directa a menos que se lo
> pida explícitamente.

**Respuesta:** explicación de `get_legal_actions`, `generate_successor`, `is_win`/`is_lose`,
`get_num_agents` (qué reciben, qué devuelven, inmutabilidad de `GameState`); mapeo del
proyecto al árbol de minimax (nodo = `GameState`, arista = acción de un agente, la
profundidad cuenta *plies* individuales, no rondas completas MAX+MIN); y la Tarea 1
propuesta: escribir solo el arranque de `get_action` (reset de métricas, acciones legales
de la raíz, caso base si la raíz ya es terminal) sin la recursión todavía.

---

## 2. "No tengo idea de qué archivo"

> Quiero que entiendas que no tengo idea de o que estas hablando. Ni siquiera se en que archivo
> tengo que hacer mi funcion, o mi clase, que no se que es. Explica desde 0. Lo unico que se es
> que es una clase, un metodo y recursion. Pero no entiendo para que sirve cada archivo, y
> cuales tengo que tener en cuenta.

**Respuesta:** reorientación completa desde cero — tabla de qué archivos importan
(`world/game_state.py` para leer, `algorithms/adversarial.py` para escribir) y cuáles ignorar;
señalar la clase `MinimaxAgent` y el método `get_action` línea por línea; explicar la cadena
de llamadas real (`main.py` → `world/runner.py::run_game` → `agent.get_action(state)`) para
que entendiera que él no ejecuta la función a mano; introducción de dónde entra la recursión.

---

## 3. Tres preguntas puntuales

> ok ya entiendo. Tengo otro par de preguntas puntuales:
> 1. Por que el enunciado dice quer solo se usa evaluation_funciotn en el limite de profundidad?
>    no se supone que esa es la funcion que evalua que escoge la accion que MIN va a tomar?
> 2. Generate successors esw una funciona con la que me muevo entre profudndiades? o nodos?
> 3. COmo decido que opcion es mejor? normalmente tengo un arbol con numeros al final y entre
>    mayor sea el numero mas gana MAX, entonces MIN siempre escoge el menor. Aca como defino
>    esos numeros?

**Respuesta:** aclaración de que `evaluation_function` solo pone número en las *hojas*
(terminal o corte de profundidad), nunca es la "función de decisión" de MIN; que
`generate_successor` mueve entre nodos (un edge a la vez), no entre profundidades; y que
los números de los nodos intermedios salen solos por recursión (`max`/`min` de los hijos),
nunca se inventan a mano salvo en las hojas.

---

## 4. "¿Debo tocar evaluation_function?"

> espera, si yo solo voy a hacer el punto 4, debo manioular la evaluation function?

**Respuesta:** no — `evaluation_function` (en `algorithms/evaluation.py`) tiene su propio TODO
(Punto 5, de otro integrante), pero ya funciona como placeholder (cae a
`base_evaluation_function`, que devuelve `state.get_score()` o ±1000 en terminales). Para el
Punto 4 solo se llama como caja negra.

---

## 5. "¿Cómo sé qué camino le conviene más a MAX?"

> Ok ya empiezo a entender. pero aun no me queda claro, como se que camino le conviene mas a max?

**Respuesta:** ejemplo con números concretos (`North → 40`, `East → 85`, `Stop → -10`) mostrando
que MAX no necesita ver el camino completo, solo comparar el número que la recursión le
devuelve por cada acción de la raíz; introducción del patrón `mejor_valor` / `mejor_accion`
con comparación estricta `>` para conservar el primer empate.

---

## 6. `agent_index`: ¿variable dada o contador propio?

> Hay alguna variable o metodo que me diga a quien le toca (agent index) en ese momento? o eso
> lo manejo yo como un contador entre 0 y 1?

**Respuesta:** `GameState` no lleva memoria de turnos — `agent_index` es un parámetro que el
propio estudiante debe pasar y actualizar en su recursión, usando
`(agent_index + 1) % state.get_num_agents()`.

---

## 7. `is_win`, `get_score`, `evaluation_function`: diferencias

> no entiendo la diferencia entre is_win, get_score y evaluation_function. Lo estoy pensando
> para el caso base, verificar si ya gane o perdi es el caso base, y para eso puedo verificar
> con is win o is lose, o el score o la eval func.

**Respuesta:** `is_win`/`is_lose` son la *condición* de parada; `get_score()` es un ingrediente
interno que ya usa `evaluation_function` por debajo; `evaluation_function(state)` es el
*valor* que se retorna una vez decidido parar (por terminal o por profundidad agotada).

---

## 8. ¿La eval function tiene en cuenta el historial?

> eval function calcula el puntaje de ese estado sin tener el cuenta el historial? osea evalua
> cuantas terminales se han activado, proximidad entre min y max... y con eso saca un puntaje
> en ese momento?

**Respuesta:** aclaración de que, en su estado actual (antes del Punto 5), `evaluation_function`
no calcula proximidad ni cuenta terminales — solo devuelve `state.get_score()`, que sí es un
acumulado histórico cargado dentro del propio `GameState` (no una métrica instantánea). La
heurística de proximidad es exactamente lo que falta en el Punto 5, fuera de su alcance.

---

## 9. Primer borrador de código (con `recursiva` como método abstracto propio)

El usuario compartió, vía selección de IDE, un primer borrador con `mejor_camino = []`,
`self.recursiva(...)`, uso incorrecto de `state.defender_position.index`, llamada a
`nuevo.get_legal_actions()` sin argumento, y una pregunta suelta:

> en python hay alguna manera de devolver la llave de un diccionario teniendo el valor?

**Respuesta:** explicación de `max(dict, key=dict.get)`, con advertencia de que ese patrón
rompe el requisito de "conservar la primera acción en empates" si dos acciones dan el mismo
score; sugerencia de volver al patrón de variables sueltas (`mejor_valor`/`mejor_accion`) en
vez de diccionario.

---

## 10. "Ya acabé mi solución" (primera revisión completa)

> Ya acabe mi solucion. Realmente creo que llegue a una solucion. Solo dime, del 1 al 10 que
> tan util está? (no supe como manejar depth, es lo unico que siento que falle. no se por que
> importa)

**Respuesta:** calificación **3/10**. Se identificaron y explicaron sin corregir:
- `IndexError` inmediato por `mejor_camino = []` sin inicializar.
- `TypeError` por `nuevo.get_legal_actions()` sin `agent_index`.
- `generate_successor` llamado con `next_agent` en vez de `agent_i` (el agente equivocado
  ejecuta la acción).
- `recursiva` devolviendo el `GameState` en vez de un número, perdiendo información de niveles
  intermedios del árbol.
- `nodes_evaluated` sin contar la raíz ni el caso base.
- Aclaración puntual sobre por qué `depth` importa (único freno contra recursión infinita,
  dado que `Stop` siempre es una acción legal) y por qué el chequeo del caso base estaba
  "atrasado" un paso respecto al estado real.

---

## 11. Segunda revisión (crashes arreglados, pero comportamiento incorrecto)

> ya corregi unas cosas. Ya funciona al menos, pero no funciona bien. Vuelve a darle puntaje

**Respuesta:** calificación **4/10**. Los dos crashes ya no ocurrían, pero el nuevo bug era que
`recursiva` nunca llamaba a `generate_successor` en ningún punto (el parámetro `accion` quedaba
sin usar), por lo que el árbol nunca avanzaba de estado y `get_action` terminaba siempre
devolviendo la primera acción legal. Se señaló el parámetro `accion` no usado como pista de
depuración transferible, además de recordar el problema pendiente de `nodes_evaluated` sin
reset y el `next_agent` mal usado para pedir acciones legales.

---

## 12. Pedido explícito de la solución

> Bueno ya llevo 3 hroas en esto. Genera la solcuion con base en lo que yo tengo. Modifica la
> menor cantidad de codigo.

**Respuesta:** entregada la solución final, con el mínimo de cambios sobre la estructura ya
escrita por el usuario (se conservó el patrón `mejor_camino = [accion, score]` con lista de
dos elementos, y el patrón `scores.index(min/max(scores))` para el desempate). Cambios
aplicados en `algorithms/adversarial.py`:

- `get_action`: reset de `self.nodes_evaluated`, conteo de la raíz, manejo de raíz terminal
  (`return None`), limpieza de `print`/variables de depuración sueltas.
- `recursiva`: `state.generate_successor(agent_i, accion)` (antes usaba `next_agent`, agente
  equivocado); chequeo de terminal/corte de profundidad movido al estado *después* de mover
  (`state2`) en vez del estado anterior; decisión `min`/`max` corregida para usar `next_agent`
  (a quién pertenecen las acciones expandidas) en vez de `agent_i`.

Se verificó ejecutando `main.py` sobre varios layouts (`bottleneck`, `dual_terminal`,
`forked_routes`, `fortified_city`, `deceptive_distance`) confirmando que la acción inicial
cambia según el mapa y que el conteo de nodos escala de forma consistente con la profundidad
(240 nodos a `depth=2` → 2071 a `depth=3` en el mismo mapa), evidencia de que el árbol ya se
recorre correctamente. Se aclaró que ningún caso llegó a "victoria" dentro del límite de
rondas porque `evaluation_function` sigue usando el placeholder plano del Punto 5 (tarea de
otro integrante), no por un defecto de `MinimaxAgent`.

---

## 13. Este archivo

> Despues de eso genera un MD con el transcript de toda nuestra conversacion (sobre todo mis
> prompts).
