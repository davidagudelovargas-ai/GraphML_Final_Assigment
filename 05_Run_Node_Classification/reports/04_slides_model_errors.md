---
marp: true
paginate: true
---

<!--
Diapositivas para la presentación (formato Marp — se pueden renderizar con la
extensión "Marp for VS Code" o copiar el texto a PowerPoint / Google Slides).
-->

# ¿Por qué el modelo confunde sala, comedor y cocina?

**El modelo adivina cada habitación "con los ojos vendados".**

Solo conoce 2 pistas de cada cuarto:

1. En qué **zona** está (privada / social / servicio)
2. Cómo se **conecta** con los demás (puertas y pasajes)

> No ve el tamaño, ni los muebles, ni las ventanas.

<!--
Recordar: nodo = habitación; grafo = habitaciones unidas por puertas/pasajes.
El modelo (red neuronal pre-entrenada en el dataset MSD) clasifica cada nodo.
-->

---

# Sala, comedor y cocina se "sienten" iguales

En planta abierta, los tres:
- están en la **misma zona** (social), y
- tienen **conexiones parecidas**.

Para el modelo son como **trillizos vestidos igual** → no los distingue y dice
**"cocina"** a todos.

| Tipo (real) | Predicción | Acierto |
|---|---|---|
| 🛋️ Sala (5) | cocina, cocina… | **0 %** |
| 🍽️ Comedor (3) | cocina, cocina… | **0 %** |
| 🪜 Escaleras (6) | escaleras | 100 % |
| 🛏️ Dormitorio (2) | dormitorio | 100 % |

**No es un error del proyecto:** las pistas no alcanzan para separar espacios
abiertos. *(Precisión global: 60 %.)*

<!--
Las escaleras, dormitorios y pasillos SÍ tienen una firma de conexión distinta,
por eso se reconocen bien. Sala/comedor/cocina comparten zona y conectividad.
-->

---

# ¿Ayudaría agregar la ventana como característica?

**Solo "¿tiene ventana? sí/no" → NO ayuda** (sala, comedor y cocina casi todas
tienen ventana).

**El TAMAÑO de la ventana → SÍ ayudaría**, según los datos del edificio:

| Tipo | Ventana promedio |
|---|---|
| 🛋️ Sala | **5.9 m²** (siempre grande) |
| 🍳 Cocina | **2.0 m²** (pequeña o ninguna) |
| 🍽️ Comedor | 5.7 m² pero **muy variable** (1.9 → 10) |

- Separaría bien **sala vs cocina** (vidrio grande vs pequeño).
- El **comedor seguiría siendo ambiguo** (sus ventanas varían mucho).
- ⚠️ Ojo: el modelo pre-entrenado usa 7 características fijas; para usar la
  ventana habría que **re-entrenar** un modelo nuevo, no solo añadir el dato.

<!--
Conclusión honesta: la ventana (por tamaño) ayuda parcialmente, sobre todo
sala vs cocina. Lo ideal es combinarla con área y proporción del cuarto.
-->
