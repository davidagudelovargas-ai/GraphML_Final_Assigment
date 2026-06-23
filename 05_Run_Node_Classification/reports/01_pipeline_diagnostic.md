# Habitar 7.2 - Pipeline Diagnostic

## Scope

This report audits the final room graph, MSD dataset and node-classification
outputs. It does not modify the geometry, graph or predictions.

## Pipeline status

- Room graph: 35 nodes and 39 undirected edges.
- ML export: one graph, 35 node rows and 78 directed edge rows.
- Predictions: 35 node predictions with probabilities for nine classes.
- Notebooks A, B and C: re-executed end to end (`Restart Kernel -> Run All`)
  with saved outputs and execution counts.

## Connectivity audit

The graph is fully connected: one component containing all 35 nodes.

An earlier version had two components, because the `Room_001` + `Bathroom_001`
bedroom unit was only linked to itself by the internal door `Door_006` and had
no door to the circulation. This was repaired by modelling the missing door
`Door_006A` (`Room_001` <-> `Store_Room_001`) in `Door.obj` and rerunning the
pipeline. `Store_Room_001` already routes to `Corridor_001` through
`Kitchen_001`, so the unit now reaches the whole building graph.

![Graph components](../images/04_graph_connectivity_components.png)

## Data integrity

- All 35 prediction rows have ground-truth and predicted labels.
- The exported edge list is symmetric: 78 directed rows represent 39 unique
  undirected connections.
- No isolated single node was found.
- Class 8 (`balcony`) has no instances, consistent with the modelled level.
- The original tables report 35 rooms, 44 doors and 21 windows. The ML graph
  correctly uses only room nodes and access relationships.

## Residual risks

1. The previously disconnected room-bathroom pair is now linked to the building
   through `Door_006A`. Connectivity is complete, but this single added door is a
   modelled correction and should be validated against the original survey.
2. The dataset contains only one building graph, so the reported result is a
   case-study inference, not a statistical evaluation.
3. The confidence value is the model's probability for its selected class; a
   high value does not guarantee architectural correctness.
4. Room names are recovered by matching graph coordinates to the room table.
   The maximum matching difference is below 0.001 model units.

## Deliverable figures

- Ground truth: `01_room_graph_ground_truth.png`
- Predictions: `02_room_graph_predictions.png`
- Error locations: `03_prediction_errors.png`
- Connectivity components: `04_graph_connectivity_components.png`
- Confusion matrix: `05_confusion_matrix.png`
- Accuracy by class: `06_accuracy_by_class.png`
