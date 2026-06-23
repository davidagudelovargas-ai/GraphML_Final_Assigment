# Presentation Summary

> English translation of `03_resumen_para_presentacion.md`.

## Graph construction

- A room graph of the first level of Habitar 7.2 was built.
- The graph contains 35 spaces and 39 undirected connections.
- Nodes represent rooms and edges represent doors or passages.
- `Corridor_002` acts as the shared circulation for the five duplex apartments.

## Node classification result

- Model used: `msd_node_classifier.pt`.
- Correct predictions: 21 of 35.
- Accuracy for this case: 60.0%.
- Bedroom: 100% correct.
- Stairs: 100% correct.
- Living room and dining were mainly confused with kitchen.
- One storeroom was confused with a bathroom (1 of 2).

## Interpretation

The model correctly recognizes spaces with very distinctive topological
positions, such as stairs and bedrooms. It has more difficulty separating
living room, dining and kitchen because they belong to the same dynamic zone
and show similar connectivity patterns.

This shows that the graph represents spatial relationships well, but
connectivity alone does not always carry enough information to distinguish
open architectural programs.

## Limitations

- The graph ended up connected as a single component (35 nodes) after modelling
  the missing door `Door_006A` (`Room_001` <-> `Store_Room_001`). That door is a
  modelling correction, not an opening recovered from the original survey.
- The analysis uses a single building, so it does not represent a general
  statistical evaluation of the model.
- The pretrained model comes from MSD and may have learned spatial conventions
  different from those of Habitar 7.2.

## Future improvements

- Validate the `Door_006A` opening in the Rhino model against the original
  apartment survey.
- Add area, proportion, facade contact and position within the apartment as node
  features.
- Incorporate `apartment_id` to distinguish shared and private circulation.
- Compare the result with other buildings from the MSD dataset.

## Recommended figures

1. `01_room_graph_ground_truth.png`
2. `02_room_graph_predictions.png`
3. `03_prediction_errors.png`
4. `05_confusion_matrix.png`
5. `06_accuracy_by_class.png`
