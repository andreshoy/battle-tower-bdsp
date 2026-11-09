# Protocolo para no cortar la racha

Llegaste a 89: el equipo funciona. Las rachas largas casi siempre se pierden por **un mal turno de suerte**
(crítico, retroceso, OHKO, sueño, Polvo Brillo) y no por falta de poder. Este protocolo busca reducir esos riesgos.

## Antes de entrar
- **Guarda** antes de cada sesión. Apagar la consola a mitad de un combate o de una serie sin guardar **cuenta como derrota**.
- Puedes descansar y cambiar de equipo **solo hasta la batalla 4 de cada serie de 7**. Las batallas 5, 6 y 7 se
  juegan con el mismo equipo.
- Ten abierta la app (`ui/app.py` o `index.html`) en el celular.

## Cada batalla
1. **Identifica al rival** por su clase y su nombre. En la app: Single → Set 7 → clase → nombre. Ahí ves **todos los
   Pokémon posibles** de ese entrenador, con objeto, movimientos y stats. Cada entrenador tiene un roster fijo, así
   que es casi como ver su equipo antes de empezar.
2. **Elige quién sale primero** con la tabla *Líder recomendado por entrenador* de [matchups.md](matchups.md).
   El rival saca primero a **uno de sus 3 Pokémon al azar**, así que el líder recomendado es el que mejor le va en
   promedio contra todos los posibles. Si el entrenador no está en la tabla, sal con **Gastrodon**: es el mejor
   líder general (enfrentamiento favorable contra el 53% de los Pokémon del Set 7).
3. **Cuando veas qué sacó el rival,** busca ese Pokémon en la tabla principal de [matchups.md](matchups.md) y cambia si tu
   líder está en la columna *Cuidado*.
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
Según los datos, Palmer aparece en las batallas 21 y 49 de la Clase Normal. Si vuelve a aparecer después, su equipo
del Set 7 es Cresselia (Paz Mental + Poder Reserva), Regigigas (Inicio Lento) y Heatran (Polvo Brillo).
Lo importante: **no dejes que Cresselia acumule Paz Mental**, y aprovecha los 5 turnos de Inicio Lento de Regigigas.

## Después de una derrota
Anota en `estrategia/derrotas.md` el número de batalla, el rival, qué pasó y qué cambiarías.
Así el equipo mejora con datos.
