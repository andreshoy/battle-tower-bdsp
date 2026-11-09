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
| Equipo actual | pendiente: capturas en `capturas/` → [equipo.md](equipo.md) |

## Archivos
| Archivo | Para qué |
|---|---|
| [estrellas_tarjeta.md](estrellas_tarjeta.md) | Checklist de las 5 estrellas con los pasos de cada una |
| [equipo.md](equipo.md) | Análisis de los 3 actuales y los 4 candidatos, y el trío recomendado |
| [amenazas.md](amenazas.md) | Rivales, objetos y movimientos peligrosos de las batallas 50 a 100 (archivo generado) |
| [protocolo_racha.md](protocolo_racha.md) | Cómo jugar cada batalla sin arriesgar la racha |
| [crianza.md](crianza.md) | Cómo criar y entrenar Pokémon competitivos en BDSP |
| `capturas/` | Tus capturas de stats (no se suben a git) |
| `analisis/` | Scripts: `amenazas.py`, `cobertura.py`, `equipo.yaml` |

## Cómo usar los scripts
Desde la raíz del repo:
```bash
.venv/bin/python estrategia/analisis/amenazas.py      # regenera amenazas.md
.venv/bin/python estrategia/analisis/cobertura.py     # compara los equipos de equipo.yaml contra el pool rival
```
Supuesto de los scripts: a partir de la batalla 50 de la Clase Normal los rivales salen del **Set 7**. Si en el
juego ves rivales de otros Sets, se ajusta con `--sets "Set 6,Set 7"`.
