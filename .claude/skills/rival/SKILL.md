---
name: rival
description: Pasos rápidos para una batalla en curso de la Torre Batalla (Pokémon Perla Reluciente, Single). Usar cuando el usuario da el nombre de un entrenador (con o sin clase, set o equipo) o dice qué Pokémon sacó el rival, p. ej. "/rival parasol lady mikaela team B set 2", "pokefan tate, sacó a roselia, set 2", "estoy contra youngster ezequiel".
---

# Rival: qué hacer en esta batalla

El usuario está **en medio de una batalla** y escribe desde el juego: la respuesta debe ser rápida, corta y accionable.
Responde siempre en español.

## 1. Extrae los datos del mensaje
- **Entrenador:** nombre y, si viene, la clase. El usuario escribe a la española o con errores ("laidy", "pokefan",
  "Ezequiel"); el script tolera eso.
- **Set** (1-7) y **equipo** (A/B/C), si los da. Si no dice el equipo, el script omite los **Team A** cuando el
  entrenador tiene otros: el usuario casi solo pide ayuda desde los Team B. Pasa `--team A` solo si lo pide. Si no da el set, deduce por el número de batalla: Set 1 = batallas 1-7,
  Set 2 = 8-14, …, Set 7 = 43-49. Después de la 49 los sets se reinician: 50-56 = Set 1, 57-63 = Set 2, …,
  92-98 = Set 7, 99-100 = Set 1 (set = (batalla − 50) // 7 % 7 + 1).
- **Qué Pokémon sacó el rival** y **quién tiene él en campo**, si lo dice. Si no dice quién tiene en campo, mira la
  tabla *Orden para cada set* de `estrategia/protocolo_racha.md` para saber con quién empezó.

## 2. Consulta los datos (desde la raíz del repo)
```bash
.venv/bin/python estrategia/analisis/rival.py "<nombre>" [--clase "<clase>"] [--set <N>] [--team <A|B|C>] [--saco <Pokémon>] [--campo <tu Pokémon>] --plan
```
(Sin `--saco`, usa `--resumen` en lugar de `--plan`.)
- Pasa siempre `--campo` con tu Pokémon en campo (el que dijo el usuario o el líder del set). El resumen añade una
  línea `= <Pokémon> en campo: … → QUÉDATE / CAMBIA`.
- **Si sabes qué sacó el rival, usa `--plan` en vez de `--resumen`** (incluye el resumen). Simula la batalla completa,
  3 contra 3, turno a turno, y compara las tres formas de empezar (quedarte o cambiar a cada uno). Para cada una
  muestra la línea completa: quién enfrenta a cada Pokémon rival según a quién saque después, y con cuánta vida
  quedan los tuyos. Ordena por el **peor caso** (vida total que te queda, más un poco por cada Pokémon en pie) y, si hay empate, pone
  primero quedarse. Así aprovecha a los 3: si dejar caer a uno casi KO para que otro entre gratis le ahorra
  mucha vida al resto, lo propone.
- **Haz UNA sola llamada.** Si el usuario dijo qué sacó el rival, pasa `--saco <Pokémon>`: el script elige ese equipo
  (y el set, si no lo dio).
- `--resumen` da una línea por Pokémon rival con las 2 mejores respuestas (ataque, % de daño, golpes para KO,
  velocidad) y a quién evitar. Normalmente basta con eso. Usa la salida completa (sin `--resumen`) solo si necesitas
  más detalle, por ejemplo en Palmer o en una situación rara.
- Palmer funciona con `palmer --set 3` (batalla 21) o `palmer --set 7` (batalla 49). Para Palmer usa además los planes de
  la sección *Palmer* de `estrategia/protocolo_racha.md`.
- Si el script no encuentra al entrenador o hay varios parecidos, dilo y pregunta en una línea. No inventes datos.
  No leas otros archivos salvo que haga falta.

El daño estimado ya incluye STAB, efectividad, habilidades (Roca Sólida, Multiescamas…) y bayas que reducen daño.
El ranking del resumen es orientativo: revísalo con los criterios del punto 3.

## 3. Decide con criterio (no solo con la tabla)
- **No sigas a ciegas las ideas tácticas del usuario** (él mismo lo pidió): si propone otra jugada, compárala con los
  números y dile cuál conviene.
- **El objetivo es ganar la batalla completa con tus 3**, no ganar cada enfrentamiento por separado. Con `--plan`,
  toma la opción 1 y su línea como base de la respuesta: el **Si saca** de cada Pokémon rival sale de esa línea.
  Cámbiala solo si un riesgo que la simulación no ve lo hace peligroso (abajo).
- La simulación usa daño promedio y no ve: críticos, fallos, estados (sueño, parálisis, confusión, Pataleta Floral),
  bajadas de precisión (Ataque Arena), Sorpresa, Cinta Focus, Contraataque/Manto Espejo, OHKO, Explosión ni mejoras
  (las tuyas tampoco: Danza Dragón). Si una opción gana con un margen muy justo (alguno queda con menos de ~20%) o
  depende de uno de estos riesgos, prefiere la segunda si está cerca.
- **Primero lo urgente:** si el Pokémon del usuario en campo recibe súper eficaz de un rival más rápido (sobre todo x4,
  como Planta contra Gastrodon o Eléctrico contra Gyarados), di de entrada que **cambie** y a quién.
- **Quédate siempre que se pueda, para guardar a los otros dos.** Si tu Pokémon en campo no recibe súper eficaz y lo
  gana en 3 golpes o menos (`QUÉDATE` en el resumen), quédate aunque otro lo deje KO de un golpe. Cada cambio regala
  un golpe gratis al rival, gasta la Banda Focus de Roserade y la Intimidación de Gyarados (solo sirve al entrar).
  Esto vale sobre todo para Gastrodon, que aguanta mucho y tiene Recuperación.
- **Guarda a cada Pokémon para el rival que solo él gana**, también al que está en campo. El resumen marca
  `★ única respuesta buena: X` en cada Pokémon rival. Si tu Pokémon en campo es la única respuesta buena para **otro**
  Pokémon del rival que todavía no ha salido, y otro de tus Pokémon gana al actual sin riesgo (KO en 1-2 golpes y sin
  recibir súper eficaz), **cambia** para no gastarle vida. Excepción: quédate si el rival actual casi no le hace
  daño (Gastrodon recupera con Recuperación y Restos). Lo mismo con las reservas: no gastes en el primero a quien
  es la única respuesta para uno que viene después.
- Cuando haya que cambiar o elegir reemplazo, prefiere quien **deja KO de un golpe siendo más rápido**. Si nadie lo
  logra, el que aguanta mejor y gana en 2 golpes.
- Ten en cuenta:
  - **Físico o especial.** Mira las stats defensivas del rival: Blissey tiene muy poca Defensa (usa a Gyarados) y
    mucha Defensa Especial.
  - **Banda Focus / Robustez:** hacen falta 2 golpes. **Esfuerzo + Banda Focus:** que lo reciba Gastrodon, porque
    tiene Recuperación.
  - **Inmunidades:** Levitación o tipo Volador contra Tierra, Colector y Absorbe Agua contra Agua, Absorbe Elec y
    Electromotor contra Eléctrico, Absorbe Fuego contra Fuego. Los Pokémon Planta son inmunes a Espora y Somnífero.
  - **Contraataque o Manto Espejo:** usa ataques de la otra categoría.
  - **Mejoras del rival** (Danza Dragón, Maquinación, Paz Mental): elimínalo antes de que acumule.
  - Multiescamas y las bayas que reducen daño solo afectan al **primer** golpe.
- **Usa los nombres en español** de movimientos, objetos y habilidades. Los de su equipo: Gyarados (Danza Dragón,
  Cascada, Terremoto, Triturar · Intimidación · Baya Ziuela), Gastrodon (Rayo Hielo, Tierra Viva, Escaldar,
  Recuperación · Colector · Restos), Roserade (Gigadrenado, Bomba Lodo, Bola Sombra, Brillo Mágico · Cura Natural ·
  Banda Focus).

## 4. Formato de la respuesta
Solo instrucciones, sin explicaciones ni justificaciones. Nada de viñetas de "por qué", tablas ni párrafos.
Siempre en este orden:

1. **Clase Nombre, Set N, equipo X**: sus 3 Pokémon (una línea).
2. **Quédate con <tu Pokémon en campo>** o **Cambia <tu Pokémon> → <cuál>** (una línea, en negrita).
3. **Ataque:** qué movimiento usar contra el Pokémon que sacó el rival (y el 2.º golpe si hace falta).
   Como mucho un dato entre paréntesis: x2, KO de 1 golpe o 2 golpes.
4. **Si saca <otro Pokémon>:** <Pokémon recomendado> → <ataque>. Una línea por cada uno de los otros dos.
5. Como mucho una línea **Ojo:** solo si hay un riesgo que cambia lo que hay que hacer (OHKO, sueño, Ataque Arena,
   Banda Focus, Contraataque…).

Si no ha salido ningún Pokémon todavía, omite los puntos 2 y 3 y pon una línea **Si saca** por cada uno de los tres.

Ejemplo (Poké Fan Tate, Set 3, equipo A, sacó Linoone, Gastrodon en campo):

**Poké Fan Tate, Set 3, equipo A**: Linoone, Monferno, Combusken.
**Quédate con Gastrodon.**
**Ataque:** Escaldar (2-3 golpes).
**Si saca Monferno:** Gyarados → Cascada (KO de 1 golpe).
**Si saca Combusken:** Gastrodon → Tierra Viva (KO de 1 golpe).
**Ojo:** si Linoone usa Ataque Arena 2 veces, cambia de Pokémon.

Si el usuario cuenta cómo terminó la batalla, o algo que contradice los datos (por ejemplo, un movimiento que no
aparece), anótalo brevemente en `estrategia/derrotas.md` si fue una derrota, o avísale que los datos podrían estar mal.
No modifiques los datos (`data/`) ni `utils/merge_pokemon_data.py`: el usuario confirmó que están bien.
