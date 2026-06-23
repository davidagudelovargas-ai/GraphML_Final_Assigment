# Final Assignment - Graph Learning Pipeline for Architectural Floor Plans

This repository is organized using the same five tasks from the final assignment brief.

## 1. Research the Dataset and References

Folder: `01_Research_Dataset_and_References`

Contains the research PDF about the Modified Swiss Dwellings dataset, reference papers, and graph learning context.

## 2. Recreate a Floor Plan

Folder: `02_Recreate_Floor_Plan`

Contains the recreated floor plan geometry and references. The corrected OBJ source geometry is:

```text
02_Recreate_Floor_Plan/Assets2.0/
```

Important correction: `Livingroom.obj` and `Dining.obj` are separated in this version.

## 3. Build a Graph Representation

Folder: `03_Build_Graph_Representation`

Active notebook:

```text
03_Build_Graph_Representation/notebooks/S06-15A Build Habitar 7.2 Room Graph.ipynb
```

Main outputs:

```text
03_Build_Graph_Representation/graph_outputs/habitar72_room_graph.json
03_Build_Graph_Representation/tables/
03_Build_Graph_Representation/images/
```

## 4. Perform Spatial / Graph Analysis

Folder: `04_Perform_Spatial_Graph_Analysis`

Active notebook:

```text
04_Perform_Spatial_Graph_Analysis/notebooks/Perform Spatial  Graph Analysis/Graph ML -Spatial Intelligence.ipynb
```

This step contains spatial graph analysis outputs such as degree centrality, closeness/integration, community detection, and shortest paths.

## 5. Run Node Classification

Folder: `05_Run_Node_Classification`

Active notebooks:

```text
05_Run_Node_Classification/notebooks/S06-15B Prepare Habitar 7.2 Graph.ipynb
05_Run_Node_Classification/notebooks/S06-15C Predict Habitar 7.2 Nodes.ipynb
```

Main outputs:

```text
05_Run_Node_Classification/ml_dataset/graphs.csv
05_Run_Node_Classification/ml_dataset/nodes.csv
05_Run_Node_Classification/ml_dataset/edges.csv
05_Run_Node_Classification/ml_dataset/meta.yaml
05_Run_Node_Classification/predictions/node_predictions_habitar72.csv
05_Run_Node_Classification/images/
05_Run_Node_Classification/reports/
```

## Run Order

After changing the OBJ files, rerun:

```text
1. S06-15A Build Habitar 7.2 Room Graph.ipynb
2. Graph ML -Spatial Intelligence.ipynb
3. S06-15B Prepare Habitar 7.2 Graph.ipynb
4. S06-15C Predict Habitar 7.2 Nodes.ipynb
```

The node classification step uses the pretrained model:

```text
05_Run_Node_Classification/pretrained_model/msd_node_classifier.pt
```

