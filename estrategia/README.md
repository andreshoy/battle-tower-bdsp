# Estrategia: racha de 100 en la Torre Batalla y tarjeta de 5 estrellas

## Objetivo
1. **Inmediato:** racha de **100 victorias seguidas** en la Torre Batalla. Da una estrella de la tarjeta.
2. **Final:** tarjeta de entrenador **negra**, con las 5 estrellas → ver [estrellas_tarjeta.md](estrellas_tarjeta.md).

## Estado actual
| Dato | Valor |
|---|---|
| Juego | Perla Reluciente |
| Modo | Single, **Clase Normal** (la racha cuenta en cualquier clase) |
| Mejor racha | **89** |
| Estrellas | 3/5 (faltan racha de 100 y Pokédex Nacional) |
| Equipo actual | Gyarados / Gastrodon / Roserade |
| Recomendación | **Mantener el equipo actual** y jugar con [matchups.md](matchups.md) → [equipo.md](equipo.md) |

## Archivos
| Archivo | Para qué |
|---|---|
| [estrellas_tarjeta.md](estrellas_tarjeta.md) | Checklist de las 5 estrellas con los pasos de cada una |
| [equipo.md](equipo.md) | Análisis de los 3 actuales y los 4 candidatos, y el trío recomendado |
| [matchups.md](matchups.md) | Rival por rival: quién de tu equipo lo enfrenta y con qué ataque (archivo generado) |
| [amenazas.md](amenazas.md) | Rivales, objetos y movimientos peligrosos de las batallas 50 a 100 (archivo generado) |
| [protocolo_racha.md](protocolo_racha.md) | Cómo jugar cada batalla sin arriesgar la racha |
| [crianza.md](crianza.md) | Cómo criar y entrenar Pokémon competitivos en BDSP |
| `capturas/` | Tus capturas de stats (no se suben a git) |
| `analisis/` | Scripts: `amenazas.py`, `cobertura.py`, `matchups.py`, `rival.py`, `equipo.yaml` |

## Durante una batalla
En Claude Code escribe `/rival <clase> <nombre> set <N> team <X>` (o simplemente el entrenador y qué sacó).
La skill (`.claude/skills/rival/`) consulta `analisis/rival.py` y te devuelve los pasos a seguir.

## Cómo usar los scripts
Desde la raíz del repo:
```bash
.venv/bin/python estrategia/analisis/amenazas.py      # regenera amenazas.md
.venv/bin/python estrategia/analisis/cobertura.py     # compara los equipos de equipo.yaml contra el pool rival
.venv/bin/python estrategia/analisis/cobertura.py --trios   # ranking de todas las combinaciones de 3
.venv/bin/python estrategia/analisis/matchups.py      # regenera matchups.md para el equipo 'actual'
.venv/bin/python estrategia/analisis/rival.py Mikaela --set 2 --team B   # un entrenador, con daño estimado
```
Supuesto de los scripts: a partir de la batalla 50 de la Clase Normal los rivales salen del **Set 7**. Si en el
juego ves rivales de otros Sets, se ajusta con `--sets "Set 6,Set 7"`.
