# Habitar 7.2 — Graph Machine Learning of an Architectural Floor Plan

Final assignment for the Graph Machine Learning course. Starting from a recreated
residential floor plan (**Habitar 7.2**, level L01), the project turns architecture
into a **graph** — rooms become nodes, doors/passages become edges — then analyzes
its spatial structure and uses a **pretrained Graph Neural Network** (trained on the
*Modified Swiss Dwellings* dataset) to classify each room by type.

![Room connectivity graph](05_Run_Node_Classification/images/04_graph_connectivity_components.png)

## Results at a glance

| Metric | Value |
|---|---|
| Room graph | **35 nodes**, **39 edges**, **1 connected component** |
| Node classification (pretrained MSD model) | **60 % accuracy** (21 / 35) |
| Best-recognized classes | bedroom & stairs (100 %) |
| Hardest classes | living room & dining (0 %) — both predicted as *kitchen* |

**Why living/dining fail:** the model only sees each room's *zone* and *connectivity*.
Living room, dining and kitchen share the same social zone and similar connections, so
they are indistinguishable to the model. Adding window *size* or room *area* as features
would help separate them — see the
[interpretation report](05_Run_Node_Classification/reports/02_node_classification_interpretation.md).

![Accuracy by class](05_Run_Node_Classification/images/06_accuracy_by_class.png)

## Pipeline

The repository follows the five tasks of the assignment brief (details in
[README_PROJECT_FLOW.md](README_PROJECT_FLOW.md)):

| # | Stage | Folder |
|---|---|---|
| 1 | Research dataset & references | `01_Research_Dataset_and_References` |
| 2 | Recreate the floor plan (OBJ geometry) | `02_Recreate_Floor_Plan` |
| 3 | Build the room graph | `03_Build_Graph_Representation` |
| 4 | Spatial / graph analysis | `04_Perform_Spatial_Graph_Analysis` |
| 5 | Node classification (GNN) | `05_Run_Node_Classification` |

### Run order (notebooks)

```text
1. 03_Build_Graph_Representation/notebooks/S06-15A Build Habitar 7.2 Room Graph.ipynb
2. 04_Perform_Spatial_Graph_Analysis/notebooks/.../Graph ML -Spatial Intelligence.ipynb
3. 05_Run_Node_Classification/notebooks/S06-15B Prepare Habitar 7.2 Graph.ipynb
4. 05_Run_Node_Classification/notebooks/S06-15C Predict Habitar 7.2 Nodes.ipynb
```

Node classification uses the pretrained model
`05_Run_Node_Classification/pretrained_model/msd_node_classifier.pt`.

## Setup

Requires **Python 3.12** (avoid 3.14 — the pinned packages have no wheels for it yet).

```bash
# (recommended) isolated environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
```

Then run the notebooks in the order above (`Restart Kernel → Run All`), or headless:

```bash
jupyter nbconvert --to notebook --execute --inplace "<notebook>.ipynb"
```

> Note: `torch` / `torch_geometric` wheels are platform-specific. If install fails,
> use the official PyTorch index: https://pytorch.org/get-started.

## Reproducing the report figures

The six deliverable figures and the presentation slide are generated **from the data**
(not exported by hand), so they always match the pipeline:

```bash
python 05_Run_Node_Classification/generate_report_figures.py   # the 6 report figures
python 05_Run_Node_Classification/generate_slide2_image.py      # presentation slide 2
```

## Reports

Located in `05_Run_Node_Classification/reports/`:

- `01_pipeline_diagnostic.md` — pipeline & connectivity audit
- `02_node_classification_interpretation.md` — results interpretation
- `03_resumen_para_presentacion.md` / `03_presentation_summary_EN.md` — presentation summary (ES / EN)
- `04_slides_model_errors.md` / `04_slides_model_errors_EN.md` — slides (ES / EN)

## Notes

- **Connectivity fix:** the `Room_001` + `Bathroom_001` unit was originally disconnected
  (its only door was internal). It was reconnected by modelling the door `Door_006A`
  (`Room_001 ↔ Store_Room_001`) in `Door.obj`, giving a single 35-node component.
- **Notebook 04** can intermittently crash the kernel at `Grid.EdgesByDistances`
  (an OpenCascade native instability, not a code bug) — just re-run it if it dies.

## Author

**David Agudelo** — IAAC. Built with the pretrained MSD node classifier and `topologicpy`.
