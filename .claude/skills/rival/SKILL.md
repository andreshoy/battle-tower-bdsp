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
- **Set** (1-7) y **equipo** (A/B/C), si los da. Si no da el set, deduce por el número de batalla: Set 1 = batallas 1-7,
  Set 2 = 8-14, …, Set 7 = 43-49. Desde la 50 es el Set 7.
- **Qué Pokémon sacó el rival** y **quién tiene él en campo**, si lo dice. Si no dice quién tiene en campo, mira la
  tabla *Orden para cada set* de `estrategia/protocolo_racha.md` para saber con quién empezó.

## 2. Consulta los datos (desde la raíz del repo)
```bash
.venv/bin/python estrategia/analisis/rival.py "<nombre>" --set <N> [--team <A|B|C>] [--clase "<clase>"]
```
- Si no sabes el equipo, omite `--team`: el script muestra todos los del set. Si el usuario dijo qué Pokémon sacó el
  rival, identifica el equipo que lo contiene y responde solo sobre ese equipo.
- Palmer funciona con `palmer --set 3` (batalla 21) o `palmer --set 7` (batalla 49). Para Palmer usa además los planes de
  la sección *Palmer* de `estrategia/protocolo_racha.md`.
- Si el script no encuentra al entrenador o hay varios parecidos, dilo y pregunta en una línea. No inventes datos.

El script da, para cada Pokémon rival: tipos, habilidad, objeto, movimientos (con tipo), stats a nivel 50, trampas, y
para cada miembro del equipo del usuario: si es más rápido, qué le pega súper eficaz y el **daño estimado** de cada
ataque (% de los PS del rival, ya con STAB, efectividad, habilidad y bayas que reducen daño).

## 3. Decide con criterio (no solo con la tabla)
- **Primero lo urgente:** si el Pokémon del usuario en campo recibe súper eficaz de un rival más rápido (sobre todo x4,
  como Planta contra Gastrodon o Eléctrico contra Gyarados), di de entrada que **cambie** y a quién.
- Prefiere quien **deja KO de un golpe siendo más rápido**. Si nadie lo logra, el que aguanta mejor y gana en 2 golpes.
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
Corto. Sin explicar el método.

1. Una línea para identificar: **Clase Nombre, Set N, equipo X**, con sus 3 Pokémon.
2. Si ya sabes qué sacó el rival: **qué hacer ahora**, en negrita (quedarse o cambiar, y qué ataque usar), con 1-3
   viñetas de por qué y los números clave (velocidad, % de daño).
3. Una tabla **Si saca → Usa → Ojo** con los otros Pokémon del equipo (o con los tres, si no ha salido ninguno).
4. Como mucho una línea final con un riesgo especial.

Ejemplo de tono (Parasol Lady Mikaela, Set 2, equipo B): «**Quédate con Gastrodon y usa Escaldar**: le pega x2 y lo
deja KO de un golpe. Su Hierba Lazo te pega x4, pero solo te quita más o menos la mitad.»

Si el usuario cuenta cómo terminó la batalla, o algo que contradice los datos (por ejemplo, un movimiento que no
aparece), anótalo brevemente en `estrategia/derrotas.md` si fue una derrota, o avísale que los datos podrían estar mal.
No modifiques los datos (`data/`) ni `utils/merge_pokemon_data.py`: el usuario confirmó que están bien.
