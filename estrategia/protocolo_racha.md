# Protocolo para no cortar la racha

Llegaste a 89: el equipo funciona. Las rachas largas casi siempre se pierden por **un mal turno de suerte**
(crítico, retroceso, OHKO, sueño, Polvo Brillo) y no por falta de poder. Este protocolo busca reducir esos riesgos.

## Antes de entrar
- **Guarda** antes de cada sesión. Apagar la consola a mitad de un combate o de una serie sin guardar **cuenta como derrota**.
- Puedes descansar y cambiar el equipo y el orden **antes de la batalla 1 y hasta antes de la batalla 5** de cada
  serie. Las batallas 5, 6 y 7 se juegan con el mismo equipo y orden (fuente: altissimo1).
- Ten abierta la app (`ui/app.py` o `index.html`) en el celular.

## Orden para cada set
Cada set de la página es una serie de 7 batallas: Set 1 = batallas 1-7, Set 2 = 8-14, …, Set 7 = 43-49.
Desde la 50 los rivales siguen saliendo del **Set 7** (supuesto; ver [amenazas.md](amenazas.md)).
El rival saca primero a uno de sus 3 Pokémon al azar. Por eso el líder se eligió ponderando como el juego
(entrenador al azar → equipo al azar → primer Pokémon al azar) contra los rivales Single de cada set.

| Set | Batallas | Orden | Líder: favorable / amenazado y más lento | Motivo |
|---|---|---|---|---|
| 1 | 1-7 | **Roserade** → Gastrodon → Gyarados | 39% / 0% (Gastrodon 42% / 7%) | Casi igual que Gastrodon, pero sin riesgo |
| 2 | 8-14 | **Gastrodon** → Roserade → Gyarados | 47% / 5% (Roserade 32% / 0%) | Gastrodon claramente mejor |
| 3 | 15-21 | **Gastrodon** → Roserade → Gyarados | 44% / 12% (Roserade 35% / 2%) | **Palmer (batalla 21)**: Gastrodon no tiene debilidades contra su equipo |
| 4 | 22-28 | **Roserade** → Gastrodon → Gyarados | 35% / 0% (Gastrodon 41% / 13%) | Gastrodon corre más riesgo en este set (muchos Planta) |
| 5 | 29-35 | **Roserade** → Gastrodon → Gyarados | 28% / 4% (Gastrodon 36% / 16%) | Igual que el Set 4 |
| 6 | 36-42 | **Gastrodon** → Gyarados → Roserade | 46% / 13% (Roserade 13% / 13%) | Roserade sufre mucho en este set |
| 7 | 43-46 | **Gastrodon** → Gyarados → Roserade | 55% / 10% (Gyarados 29% / 10%) | El mejor líder contra el Set 7 |
| 7 | **47-49** | **Gyarados** → Gastrodon → Roserade | — | **Palmer (batalla 49)**: Gyarados le gana a sus 3 Pokémon (ver abajo) |
| 50+ | 50-100 | **Gastrodon** → Gyarados → Roserade | 55% / 10% | Rivales del Set 7 |

- **Cambio a mitad del Set 7:** se puede descansar y cambiar el equipo hasta antes de la batalla 5 de cada serie
  (fuente: altissimo1; compruébalo en el juego). Entonces: juega las batallas 43-46 con Gastrodon primero, **descansa
  después de la 46** y cambia a Gyarados primero para las batallas 47-49. Si el juego no te deja, usa Gastrodon
  primero en todo el Set 7 y cambia a Gyarados en cuanto Palmer saque a Cresselia o a Regigigas.
- El 2.º y el 3.º los eliges tú cuando cae uno. El orden de la tabla es solo el que conviene dejar puesto.

**Única debilidad de Gastrodon: Planta, que le pega x4.** Qué hacer si el rival sale con uno de estos:

| Rival | Ataque Planta | Qué hacer |
|---|---|---|
| Torterra (Vel 54) | Lluevehojas | **Quédate**: eres más rápido y Rayo Hielo le pega x4 |
| Tangrowth (67), Venusaur (97), Leafeon (121), Meganium (128), Roserade rival (105), Sceptile (184) | Gigadrenado, Hoja Aguda, Rayo Solar, Energibola | **Cambia a Roserade**: recibe Planta x0.25 y les pega con Bomba Lodo |
| Abomasnow | Gigadrenado | **Cambia a Gyarados**: recibe neutral, y sus ataques Hielo le pegan x2 a Roserade |
| Gengar (171, Banda Focus) | Energibola | **Cambia a Gyarados** → Terremoto x2. Recuerda que la Banda Focus le permite aguantar un golpe |
| Alakazam (166) | Energibola | **Cambia a Gyarados** → Triturar x2 |

## Cada batalla
1. **Identifica al rival** por su clase y su nombre. En la app: Single → Set 7 → clase → nombre. Ahí ves **todos los
   Pokémon posibles** de ese entrenador, con objeto, movimientos y stats. Cada entrenador tiene un roster fijo, así
   que es casi como ver su equipo antes de empezar.
2. **Cuando veas qué sacó el rival,** búscalo en la tabla de [matchups.md](matchups.md). Si tu Pokémon en campo
   aparece con ⚠ (recibe súper eficaz) y el rival es más rápido, cambia al Pokémon de la columna *Respuesta*.
3. **Cuando uno de tus Pokémon caiga,** elige el reemplazo con la misma tabla. El 2.º y el 3.º los eliges tú en ese
   momento, así que su orden en el equipo no importa.
4. Antes de atacar, revisa en la app el **objeto** y la **habilidad** del rival:
   - **Banda Focus** o **Robustez** (Sturdy, muy común en el Set 7): no lo dejarás KO de un golpe. Usa primero un
     ataque débil o de prioridad, o ten listo el segundo golpe.
   - **Polvo Brillo** (Lucario, Dugtrio, Heatran de Palmer…): no te confíes con movimientos de 90% de precisión o menos.
   - **Garra Rápida**, Baya Zidra o Baya Aslac: el rival puede moverse antes que tú.
   - **Absorbe Agua**, Absorbe Elec, Electromotor, Absorbe Fuego, **Levitación**: anulan tu tipo de ataque.
5. Elige el movimiento más seguro, no el más fuerte. Prefiere 100% de precisión a 85% aunque pegue menos.
   El KO de un golpe solo vale la pena si el rival te puede dejar KO a ti.

## Rivales con riesgo especial (Set 7)
Detalle completo en [amenazas.md](amenazas.md).

| Riesgo | Quiénes | Respuesta |
|---|---|---|
| **OHKO** (Frío Polar, Fisura, Guillotina) | Walrein, Gliscor, Pinsir | Golpéalos primero y fuerte. Un Pokémon con **Robustez** (Sturdy) es inmune a los OHKO |
| **Sueño** (Bostezo, Hipnosis, Somnífero) | Jolteon, Umbreon, Hippowdon, Snorlax, Leafeon, Milotic, Venusaur, Kingdra | Baya Ziuela/Atania, cambiar de Pokémon tras el Bostezo, o un Pokémon con Sustituto |
| **Evasión** (Doble Equipo, Ataque Arena, Destello) | Glaceon, Dugtrio, Tangrowth, Luxray | Golpéalos de inmediato antes de que acumulen, o cambia para resetear la evasión |
| **Contraataque / Manto Espejo** | Glaceon, Slaking, Machamp | No uses ataques físicos contra Slaking y Machamp con Contraataque, ni especiales contra Glaceon |
| **Mejoras** (Danza Dragón, Danza Espada, Maquinación, Pulimento) | Gyarados, Garchomp, Lucario, Kingdra, Lapras, Metagross | Elimínalos antes de que suban, o usa Rugido, Niebla o un ataque crítico |
| **Canto Mortal** | Politoed, Altaria | Cambia de Pokémon antes de que termine el contador |

## Palmer
El primer Pokémon de Palmer también es aleatorio. Datos completos en [amenazas.md](amenazas.md).

### Batalla 21 (Set 3): Milotic, Rhyperior, Dragonite — sal con Gastrodon
Ninguno de los tres le pega súper eficaz a Gastrodon.
| Si sale | Plan |
|---|---|
| **Rhyperior** (Roca Sólida, Cinta Experto, Vel 45) | **Gastrodon → Escaldar** (x4; Roca Sólida lo reduce algo, pero su Def. Especial es 65). Su Rayo no te afecta y Rayo Hielo te pega neutral |
| **Dragonite** (Multiescamas, Lupa, Vel 119) | **Gastrodon → Rayo Hielo** (x4): el 1.º le quita ~40% (Multiescamas) y el 2.º ~75-88%, así que **caen 2**. Su Carga Dragón le quita ~45% a Gastrodon por golpe, así que aguantas justo los dos (salvo crítico o retroceso). Acua Cola no te afecta por Colector. Alternativa: Roserade → Brillo Mágico (x2), es más rápida, y la Banda Focus la salva de un golpe |
| **Milotic** (Escama Especial, Baya Aslac, Vel 91) | Su Hidrobomba no le hace nada a Gastrodon (y le sube el Ataque Especial), pero Gastrodon tampoco le hace mucho. **Cambia a Roserade → Gigadrenado** (x2): es más rápida y Cura Natural le quita el sueño si te duerme con Hipnosis |
| No uses a Gyarados | Rayo de Rhyperior (x4) y Roca Afilada de Dragonite (x2) |

### Batalla 49 (Set 7): Cresselia, Regigigas, Heatran — sal con Gyarados
| Si sale | Plan |
|---|---|
| **Heatran** (Absorbe Fuego, **Polvo Brillo**, Vel 97) | **Gyarados → Terremoto** (x4). Es inmune a su Tierra Viva y resiste Lluvia Ígnea y Foco Resplandor. Si fallas por el Polvo Brillo, repite. Respaldo: Gastrodon → Tierra Viva (x4) |
| **Regigigas** (Inicio Lento, Baya Chople, Vel 121) | Es el más duro: Cascada sin mejoras le quita solo **29-34%**. Durante sus primeros **5 turnos** tiene la mitad de Ataque y Velocidad, y con Intimidación te pega más o menos un 40% por turno. Haz **1 Danza Dragón** (mejor si coincide con su Protección) y luego **Cascada** cada turno (+1: ~45-50% por golpe, y Gyarados siempre es más rápido). Si Gyarados baja de 40%, no hagas otra Danza: ataca. Respaldo: **Roserade → Bomba Lodo** (32-38%, es más rápida y tiene Banda Focus) |
| **Cresselia** (Levitación, Restos, Vel 150) | Triturar sin mejoras le quita solo **33-40%**, y ella se cura con Luz Lunar y Restos. Sus ataques le hacen poco a Gyarados (Poder Reserva es débil hasta que acumula mejoras). Por eso: **Danza Dragón 1-2 veces** primero (con +1 ya eres más rápido que ella) y luego **Triturar** cada turno (+2: ~65-80% por golpe; puede bajarle la Defensa). Si usa Sustituto, rómpelo con Triturar |
| Roserade solo de respaldo | Cresselia (Psíquico), Regigigas (Puño Hielo) y Heatran (Fuego) le pegan súper eficaz: úsala solo para rematar a Regigigas |

## Después de una derrota
Anota en `estrategia/derrotas.md` el número de batalla, el rival, qué pasó y qué cambiarías.
Así el equipo mejora con datos.
