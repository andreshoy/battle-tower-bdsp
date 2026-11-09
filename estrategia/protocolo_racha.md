# Protocolo para no cortar la racha

Llegaste a 89: el equipo funciona. Las rachas largas casi siempre se pierden por **un mal turno de suerte**
(crítico, retroceso, OHKO, sueño, Polvo Brillo) y no por falta de poder. Este protocolo busca reducir esos riesgos.

## Antes de entrar
- **Guarda** antes de cada sesión. Apagar la consola a mitad de un combate o de una serie sin guardar **cuenta como derrota**.
- El equipo y el orden se eligen **al empezar cada serie de 7** (batallas 1, 8, 15, 22, 29, 36, 43, 50…) y quedan
  fijos durante las 7 batallas. Ejemplo: el equipo que elijas en la 43 es el mismo contra Palmer en la 49, y no se
  puede cambiar hasta la 50.
- Ten abierta la app (`ui/app.py` o `index.html`) en el celular.

## Orden para cada set
Cada set de la página es una serie de 7 batallas: Set 1 = batallas 1-7, Set 2 = 8-14, …, Set 7 = 43-49.
Después de la 49 los sets **se reinician** (confirmado en el juego): 50-56 = Set 1, 57-63 = Set 2, …, 92-98 = Set 7, 99-100 = Set 1.
El rival saca primero a uno de sus 3 Pokémon al azar. Por eso el líder se eligió ponderando como el juego
(entrenador al azar → equipo al azar → primer Pokémon al azar) contra los rivales Single de cada set,
contando **solo los equipos B, C, D y E** de cada entrenador (los Team A no cuentan, ni los entrenadores que solo
tienen Team A). Del Set 2 en adelante casi ningún entrenador tiene C, D o E, así que en la práctica es el Team B.
Se elige el líder con mayor diferencia entre *favorable* y *amenazado y más lento*.

| Set | Batallas | Orden | Líder: favorable / amenazado y más lento | Motivo |
|---|---|---|---|---|
| 1 | 1-7 | **Roserade** → Gastrodon → Gyarados | 39% / 0% (Gastrodon 41% / 8%) | Casi igual que Gastrodon, pero sin riesgo |
| 2 | 8-14 | **Gastrodon** → Roserade → Gyarados | 43% / 8% (Roserade 28% / 0%) | Gastrodon claramente mejor |
| 3 | 15-21 | **Gastrodon** → Roserade → Gyarados | 43% / 10% (Roserade 34% / 2%) | **Palmer (batalla 21)**: Gastrodon no tiene debilidades contra su equipo |
| 4 | 22-28 | **Roserade** → Gastrodon → Gyarados | 36% / 0% (Gastrodon 43% / 10%) | Gastrodon corre más riesgo en este set (muchos Planta) |
| 5 | 29-35 | **Roserade** → Gastrodon → Gyarados | 32% / 4% (Gastrodon 36% / 10%) | Igual que el Set 4 |
| 6 | 36-42 | **Gastrodon** → Gyarados → Roserade | 43% / 13% (Gyarados 30% / 1%) | Gyarados queda muy cerca; Roserade sufre mucho en este set (15% / 8%) |
| 7 | 43-49 | **Gastrodon** → Gyarados → Roserade | 51% / 14% (Gyarados 28% / 3%) | El mejor líder contra el Set 7. **Palmer (batalla 49)**: ninguno de sus 3 le pega súper eficaz a Gastrodon; cambia a Gyarados si saca a Cresselia o Regigigas (ver abajo) |
| 50+ | 50-100 | El del set que toque | — | Los sets se reinician: 50-56 = Set 1, 57-63 = Set 2, …, 92-98 = Set 7, 99-100 = Set 1 |

- Los porcentajes son contra los entrenadores normales. Contra Palmer (1 de las 7 batallas de los Sets 3 y 7) el líder
  de la tabla tampoco recibe súper eficaz de ninguno de sus Pokémon.
- El 2.º y el 3.º los eliges tú cuando cae uno. El orden de la tabla es solo el que conviene dejar puesto.

### Tabla completa de líderes
Los tres Pokémon como primero en cada set (Team B-E). Formato: favorable / amenazado y más lento (neto = diferencia).
Para Palmer se compara sin él y con **50%** de peso (lo mismo que las otras 6 batallas juntas; supuesto). Con su peso
natural (1 de 7) el resultado es el mismo que sin él.

| Set | Batallas | Gastrodon | Roserade | Gyarados | Mejor primero |
|---|---|---|---|---|---|
| 1 | 1-7 | 41/8 (+33) | **39/0 (+39)** | 26/0 (+26) | Roserade |
| 2 | 8-14 | **43/8 (+35)** | 28/0 (+28) | 17/0 (+17) | Gastrodon |
| 3 sin Palmer | 15-21 | **43/10 (+33)** | 34/2 (+32) | 31/0 (+31) | Gastrodon |
| 3 con Palmer 50% | 15-21 | **55/5 (+50)** | 51/1 (+49) | 16/0 (+16) | Gastrodon |
| 4 | 22-28 | 43/10 (+33) | **36/0 (+36)** | 23/0 (+23) | Roserade |
| 5 | 29-35 | 36/10 (+26) | **32/4 (+28)** | 12/8 (+4) | Roserade |
| 6 | 36-42 | **43/13 (+30)** | 15/8 (+7) | 30/1 (+29) | Gastrodon (Gyarados casi empata) |
| 7 sin Palmer | 43-49 | **51/14 (+37)** | 26/4 (+22) | 28/3 (+25) | Gastrodon |
| 7 con Palmer 50% | 43-49 | 42/7 (+35) | 13/2 (+11) | **47/2 (+46)** | **Gyarados** |
| 50+ | 50-100 | — | — | — | El del set que toque (los sets se reinician) |

- Solo contra Palmer: en el Set 3, Gastrodon y Roserade 67/0, Gyarados 0/0. En el Set 7, Gyarados 67/0, Gastrodon 33/0,
  Roserade 0/0.
- Set 7: si Palmer pesa más de ~26% de la serie, conviene Gyarados primero; si pesa menos, Gastrodon.
- Los netos salen de los valores sin redondear (pueden diferir en 1 punto de restar a mano).

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

### Batalla 49 (Set 7): Cresselia, Regigigas, Heatran — empiezas con Gastrodon (orden fijo del Set 7)
Ninguno de los tres le pega súper eficaz a Gastrodon. Gastrodon gana a Heatran y a Regigigas; Gyarados se guarda
solo para Cresselia (la única a la que nadie más gana), así no depende de él para dos.
| Si sale | Plan |
|---|---|
| **Heatran** (Absorbe Fuego, **Polvo Brillo**, Vel 97) | **Quédate: Gastrodon → Tierra Viva** (x4). Heatran es más rápido, pero Gastrodon resiste Lluvia Ígnea y Foco Resplandor. Si fallas por el Polvo Brillo, repite. Respaldo: Gyarados → Terremoto (x4), es inmune a su Tierra Viva |
| **Regigigas** (Inicio Lento, Baya Chople, Vel 121) | **Quédate: Gastrodon → Tierra Viva** (20-24% por golpe). Durante sus primeros **5 turnos** tiene la mitad de Ataque y Velocidad: Agarrón le quita a Gastrodon solo 30-35% con la vida llena (y menos cuanto menos vida le queda), Roca Afilada 17-20% y Puño Hielo 13-15%; Restos recupera 6%. Ataca los 5 turnos (Recuperación solo si baja de 40%): llega casi KO al final del Inicio Lento. Después, Agarrón contra Gastrodon a media vida hace ~25-30%: remátalo con Tierra Viva. Respaldo: **Roserade → Bomba Lodo** (32-38%, más rápida). Gyarados solo si los otros dos ya cayeron (Danza Dragón + Cascada) |
| **Cresselia** (Levitación, Restos, Vel 150) | Gastrodon le hace poco: **cambia a Gyarados**. Triturar sin mejoras le quita solo **33-40%**, y ella se cura con Luz Lunar y Restos. Sus ataques le hacen poco a Gyarados (Poder Reserva es débil hasta que acumula mejoras). Por eso: **Danza Dragón 1-2 veces** primero (con +1 ya eres más rápido que ella) y luego **Triturar** cada turno (+2: ~65-80% por golpe; puede bajarle la Defensa). Si usa Sustituto, rómpelo con Triturar |
| Roserade solo de respaldo | Cresselia (Poder Reserva), Regigigas (Puño Hielo) y Heatran (Lluvia Ígnea) le pegan súper eficaz: úsala solo para rematar a Regigigas |
| Gyarados para Cresselia | Es la única respuesta. No lo gastes en Regigigas ni en Heatran mientras Cresselia no haya salido |

## Después de una derrota
Anota en `estrategia/derrotas.md` el número de batalla, el rival, qué pasó y qué cambiarías.
Así el equipo mejora con datos.
