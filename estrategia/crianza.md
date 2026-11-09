# Crianza y entrenamiento competitivo en BDSP

En la Torre todo se ajusta a **nivel 50**, así que lo que importa son la naturaleza, los IVs, los EVs, la habilidad
y los movimientos.

## 1. Preparar a los padres
| Herramienta | Qué hace | Dónde |
|---|---|---|
| **Lazo Destino** | Pasa 5 IVs de los padres al huevo | Canje de PB en la Torre Batalla |
| **Piedra Eterna** | Asegura la naturaleza del padre que la lleva | Canje de PB / objeto |
| **Ditto** | Cría con cualquier especie que no sea del grupo Desconocido | Gran Subsuelo / rutas |
| **Ditto extranjero** (de otro idioma) | Sube mucho la probabilidad de shiny (Método Masuda) | Intercambio |
| **Amuleto Iris** | Más shinies | Premio por completar la Pokédex Nacional |

Ciclo típico:
1. Padre 1 con buenos IVs + **Lazo Destino**. Padre 2 con la naturaleza deseada + **Piedra Eterna**.
2. Eclosiona huevos con un Pokémon con **Cuerpo Llama** o **Escudo Magma** en el equipo, que reduce los pasos a la mitad. Ve en bici por una recta larga.
3. Cuando salga una cría con más IVs perfectos que un padre, reemplaza a ese padre.

**Habilidad oculta:** la heredan las hembras (o el macho criado con Ditto) que la tengan. En BDSP la vía principal
para conseguirla es atrapar Pokémon en las grutas del Gran Subsuelo, que pueden traerla.
La **Cápsula Habilidad** solo cambia entre las dos habilidades normales.

**Movimientos huevo:** el padre que conoce el movimiento debe criar con la hembra de la especie destino.

## 2. Corregir y pulir
| Herramienta | Qué hace |
|---|---|
| **Mentas** (canje de PB) | Cambian el efecto de la naturaleza sin criar de nuevo |
| **Chapas plateadas / doradas** (canje de PB) | Entrenamiento Extremo: IVs a 31 (solo Pokémon de **nivel 100**) |
| **Bayas reductoras** (Grana, Algama, Ispero, Meluce, Uvav, Tamate) | Bajan EVs para redistribuir |

## 3. EVs
- Máximo 252 por stat y 510 en total. Reparto típico: **252 / 252 / 4**.
- Objetos **Recios** (Pesa Recia, Brazal Recio, Cinto Recio, Lente Recia, Banda Recia, Franja Recia), del canje de
  PB: +8 EVs por combate en su stat.
- **Vitaminas** (Más PS, Proteína, Hierro, Calcio, Zinc, Carburante): +10 EVs cada una y llegan hasta 252.
- En BDSP no hay un medidor visible de EVs, así que anota cuántos llevas.

## 4. Movimientos
- MTs: tiendas, canje de PB y el Gran Subsuelo.
- Recordador de movimientos: Ciudad Pradera (Pastoria), con escamas corazón.

## Fichas de Pokémon a criar
Se completa cuando decidamos el trío a partir de [equipo.md](equipo.md). Formato:

```
### <Pokémon>
- Rol: …
- Naturaleza: …        Habilidad: …        Objeto: …
- EVs: …               IVs clave: …
- Movimientos: …
- Por qué: (qué amenazas del Set 7 cubre según cobertura.py)
- Cómo conseguirlo: (ruta/Subsuelo, padres, movimientos huevo)
```
