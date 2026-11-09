# Equipo para la racha de 100

> Datos de las capturas del 2026-11-08 (`capturas/`).
> - Stats a nivel 50: calculados desde los stats reales y el Juez de IVs (Best = 31, Fantastic = 30,
>   Very good = 21-29, Pretty good = 16-20, Decent = 1-15).
> - Los EVs son aproximados: el juego no los muestra; se deducen de los stats.

## Equipo actual (racha de 89): Gyarados / Gastrodon / Roserade
| Pokémon | Naturaleza | Habilidad | Objeto | Movimientos | Stats nv. 50 (PS/Atk/Def/SpA/SpD/Vel) | EVs aprox. |
|---|---|---|---|---|---|---|
| **Gyarados** | Jolly | Intimidate | Lum Berry | Danza Dragón, Cascada, Terremoto, Triturar | 166/176/99/72/120/**144** | 252 Atk / 252 Vel |
| **Gastrodon** | Bold | Storm Drain | Leftovers | Rayo Hielo, Tierra Viva, Escaldar, Recuperación | **209**/87/**128**/111/102/59 | 252 PS / 252 Def |
| **Roserade** | Timid | Natural Cure | Focus Sash | Gigadrenado, Bomba Lodo, Bola Sombra, Brillo Mágico | 132/81/85/**176**/122/**155** | 252 SpA / 252 Vel |

Los tres están bien entrenados: naturaleza y EVs correctos para su rol, y objetos sin repetir.

## Otros disponibles
| Pokémon | Naturaleza | Habilidad | Objeto | Movimientos | Stats nv. 50 | Veredicto |
|---|---|---|---|---|---|---|
| Scizor | Careful | Technician | Sitrus Berry | Danza Espada, Tijera X, Golpe Aéreo, Puño Bala | 176/180/116/66/106/80 | Reserva válida, pero con él el equipo tiene más huecos (72 contra 38) |
| Dragonite | Bashful (neutra) | Inner Focus | Dragon Fang | Acua Cola, Vuelo, Danza Dragón, Enfado | 185/166/118/121/118/105 | No: naturaleza neutra, EVs repartidos y sin Multiescamas |
| Garchomp | Docile (neutra) | Sand Veil | — | (no aplica) | — | Solo como base para criar uno nuevo |
| Infernape | Hasty | Iron Fist | Black Belt | — | — | Descartado por decisión tuya |

## Resultado del análisis (pool: Single Set 7 + Palmer, 312 sets rivales)
`cobertura.py --trios` compara todas las combinaciones posibles:

| Trío | Rivales sin respuesta súper eficaz | Rivales que amenazan a los 3 |
|---|---|---|
| **Actual: Gyarados / Gastrodon / Roserade** | **38 (12%)** | **0** |
| Gastrodon / Roserade / Scizor | 32 (10%) | 0 |
| Gyarados / Gastrodon / Scizor | 72 (23%) | 0 |
| Gyarados / Gastrodon / Dragonite | 83 (27%) | 6 |
| *Gastrodon / Roserade / Garchomp criado* (propuesta) | 27 (9%) | 1 (Abomasnow) |
| *Gyarados / Gastrodon / Garchomp criado* (propuesta) | 71 (23%) | 0 |

**Conclusión: no cambies el equipo.** Es el mejor con los Pokémon que ya tienes. Ningún rival del Set 7 amenaza a
los tres a la vez, y el Triturar de Gyarados cubre a los Psíquicos (Alakazam, Espeon, Cresselia, Bronzong). La
alternativa con Scizor apenas mejora la cobertura y pierde a Gyarados, tu mejor barredor.
Para llegar a 100 lo que más pesa ahora es **cómo juegas cada batalla**, no cambiar el equipo.

## El hueco que queda: los Normales voluminosos
Nadie del equipo les pega súper eficaz: Blissey, Snorlax, Porygon-Z, Slaking, Miltank, Lickilicky y Regigigas.
Ninguno de tus Pokémon disponibles cubre ese hueco, salvo uno con ataques Lucha.
Cómo enfrentarlos con el equipo actual:

| Rival | Set (Set 7) | Plan |
|---|---|---|
| **Blissey** (7 equipos) | Restos · Rayo Hielo, Rayo, Lanzallamas, Amortiguador · Def 63 | **Gyarados, ataques físicos.** Su Defensa es mínima. Rayo le pega x4 a Gyarados, pero Blissey tiene poco ataque especial (92). Haz Danza Dragón y usa Cascada o Terremoto. No la ataques con Gastrodon ni Roserade: sus ataques son especiales y Blissey tiene SpD 161 |
| **Porygon-Z** (5) | **Gafas Elegidas** · Triataque, Bola Sombra, Rayo Hielo, Rayo · Vel 138 | **Gastrodon.** Es inmune a Rayo, aguanta y usa Recuperación. No dejes a Gyarados frente a él: Rayo con Gafas lo deja KO |
| **Snorlax** (6) | Restos · Golpe Cuerpo, Terremoto, Maldición, Bostezo · Vel 47 | **Gyarados**: Intimidación + Danza Dragón y Cascada antes de que acumule Maldición. Si usa Bostezo, cambia de Pokémon o confía en la Baya Ziuela |
| **Slaking** (3) | Contraataque, Otra Vez, Golpe Cuerpo, Relajo · Ausente | Ataca **con especiales** (Roserade o Gastrodon) por el Contraataque. Aprovecha los turnos en que no se mueve por Ausente |
| **Regigigas** | Inicio Lento · Agarrón, Puño Hielo, Roca Afilada | Tienes 5 turnos con su ataque y velocidad a la mitad: haz Danza Dragón con Gyarados y barre |
| **Starmie** | Banda Focus · Hidrobomba, Rayo, Rayo Hielo, Psíquico · Vel 183 | **Gastrodon**: absorbe Hidrobomba y es inmune a Rayo. Recuerda que hacen falta 2 golpes por la Banda Focus |
| **Weavile** | Garra Afilada · Tajo Umbrío, Puño Hielo, Canto Helado · Vel 188 | **Gyarados**: Intimidación le baja el ataque y luego Cascada. Nunca dejes a Roserade frente a él |
| **Floatzel** | Vidasfera · Cascada, Acua Jet, Rayo Hielo, Onda Certera | **Gastrodon**: Colector anula sus ataques Agua |

La guía completa, rival por rival, está en [matchups.md](matchups.md).

## Orden en cada serie
Cambia según el set y según Palmer: ver la tabla **Orden para cada set** y los planes contra Palmer en
[protocolo_racha.md](protocolo_racha.md). Resumen: Roserade primero en los Sets 1, 4 y 5; Gastrodon en los Sets 2, 3 y 6,
y 7 (incluido Palmer en la 49: cambia a Gyarados si saca a Cresselia o Regigigas); Gastrodon desde la 50.
El orden queda fijo durante las 7 batallas de cada serie.

## Garchomp: ¿vale la pena criarlo?
**Es opcional; la mejora es marginal.**
- En lugar de Gyarados (Gastrodon / Roserade / Garchomp), los huecos bajan de 38 a 27, pero aparece un rival que amenaza a los tres (Abomasnow).
- En lugar de Roserade, el equipo empeora (71 huecos).
- Tampoco cubre el hueco de los Normales.

Si quieres criarlo de todas formas, por gusto o como reserva, la ficha está en [crianza.md](crianza.md#garchomp-opcional).
