# Resumen para la presentación

## Construcción del graph

- Se construyó un room graph del primer nivel de Habitar 7.2.
- El graph contiene 35 espacios y 39 conexiones no dirigidas.
- Los nodos representan habitaciones y los edges representan puertas o
  passages.
- `Corridor_002` actúa como circulación común para los cinco apartamentos
  duplex.

## Resultado de node classification

- Modelo utilizado: `msd_node_classifier.pt`.
- Predicciones correctas: 21 de 35.
- Accuracy del caso: 60.0%.
- Bedroom: 100% de acierto.
- Stairs: 100% de acierto.
- Living room y dining fueron confundidos principalmente con kitchen.
- Un storeroom fue confundido con bathroom (1 de 2).

## Interpretación

El modelo reconoce correctamente espacios con posiciones topológicas muy
distintivas, como escaleras y dormitorios. Tiene más dificultad para separar
living room, dining y kitchen porque pertenecen a la misma zona dinámica y
presentan patrones de conectividad similares.

Esto demuestra que el graph representa bien las relaciones espaciales, pero la
conectividad por sí sola no siempre contiene suficiente información para
distinguir programas arquitectónicos abiertos.

## Limitaciones

- El graph quedó conectado en un solo componente (35 nodos) tras modelar la
  puerta `Door_006A` (`Room_001` <-> `Store_Room_001`). Esa puerta es una
  corrección de modelado, no un vano recuperado del levantamiento original.
- El análisis utiliza un solo edificio, por lo que no representa una evaluación
  estadística general del modelo.
- El modelo pretrained proviene de MSD y puede haber aprendido convenciones
  espaciales diferentes a las de Habitar 7.2.

## Mejoras futuras

- Validar la puerta `Door_006A` en el modelo de Rhino contra el levantamiento
  original del apartamento.
- Añadir área, proporción, contacto con fachada y posición dentro del
  apartamento como node features.
- Incorporar `apartment_id` para distinguir circulación común y privada.
- Comparar el resultado con otros edificios del dataset MSD.

## Figuras recomendadas

1. `01_room_graph_ground_truth.png`
2. `02_room_graph_predictions.png`
3. `03_prediction_errors.png`
4. `05_confusion_matrix.png`
5. `06_accuracy_by_class.png`
