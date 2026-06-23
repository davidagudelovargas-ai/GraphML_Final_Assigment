"""Regenerate the six deliverable figures used by the Task-5 reports.

The room-graph PNGs in ``images/`` were originally exported by hand and were not
produced by any notebook, so they drifted out of sync after the room graph was
reconnected (``Door_006A``) and the pipeline was re-run. This script rebuilds all
six figures deterministically from the regenerated ML dataset and predictions so
they always match the reports.

Inputs : 05_Run_Node_Classification/ml_dataset/{nodes,edges}.csv
         05_Run_Node_Classification/predictions/node_predictions_habitar72.csv
Outputs: 05_Run_Node_Classification/images/*.png

Run:  python 05_Run_Node_Classification/generate_report_figures.py
"""
from collections import defaultdict, deque
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def find_project_root(start=None):
    current = Path(__file__).resolve() if start is None else Path(start).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "01_Research_Dataset_and_References").exists():
            return candidate
    raise FileNotFoundError("Project root not found.")


ROOT = find_project_root()
WORK = ROOT / "05_Run_Node_Classification"
DATASET = WORK / "ml_dataset"
IMAGES = WORK / "images"
IMAGES.mkdir(parents=True, exist_ok=True)

CLASS_NAMES = ["bedroom", "livingroom", "kitchen", "dining", "corridor",
               "stairs", "storeroom", "bathroom", "balcony"]
CLASS_COLORS = ["#e6194B", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
                "#911eb4", "#42d4f4", "#f032e6", "#9A6324"]

nodes = pd.read_csv(DATASET / "nodes.csv")
edges = pd.read_csv(DATASET / "edges.csv")
preds = pd.read_csv(WORK / "predictions" / "node_predictions_habitar72.csv")

# node_id -> (x, z) using the planar axes (Y is the constant vertical level).
xy = {int(r.node_id): (float(r.X), float(r.Z)) for r in nodes.itertuples()}
true_by_id = {int(r.node_id): int(r.y_true) for r in preds.itertuples()}
pred_by_id = {int(r.node_id): int(r.y_pred) for r in preds.itertuples()}
node_ids = sorted(xy)

# Undirected edge set.
undirected = set()
for r in edges.itertuples():
    a, b = int(r.src_id), int(r.dst_id)
    undirected.add((min(a, b), max(a, b)))


def draw_edges(ax):
    for a, b in undirected:
        (xa, za), (xb, zb) = xy[a], xy[b]
        ax.plot([xa, xb], [za, zb], color="#b0b0b0", lw=1.0, zorder=1)


def class_scatter(ax, color_of, title):
    draw_edges(ax)
    used = set()
    for nid in node_ids:
        c = color_of(nid)
        x, z = xy[nid]
        ax.scatter(x, z, s=140, color=CLASS_COLORS[c], edgecolors="black",
                   linewidths=0.6, zorder=2,
                   label=CLASS_NAMES[c] if c not in used else None)
        used.add(c)
    ax.set_title(title)
    ax.set_aspect("equal")
    ax.set_xlabel("X"); ax.set_ylabel("Z")
    handles, lbls = ax.get_legend_handles_labels()
    order = sorted(range(len(lbls)), key=lambda i: CLASS_NAMES.index(lbls[i]))
    ax.legend([handles[i] for i in order], [lbls[i] for i in order],
              loc="center left", bbox_to_anchor=(1.01, 0.5), fontsize=8, frameon=False)


def save(fig, name):
    out = IMAGES / name
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote", out)


# 1. Ground truth
fig, ax = plt.subplots(figsize=(11, 4))
class_scatter(ax, lambda n: true_by_id[n], "Room graph - ground truth (35 nodes)")
save(fig, "01_room_graph_ground_truth.png")

# 2. Predictions
fig, ax = plt.subplots(figsize=(11, 4))
class_scatter(ax, lambda n: pred_by_id[n], "Room graph - model predictions")
save(fig, "02_room_graph_predictions.png")

# 3. Prediction errors
n_err = sum(true_by_id[n] != pred_by_id[n] for n in node_ids)
fig, ax = plt.subplots(figsize=(11, 4))
draw_edges(ax)
for nid in node_ids:
    x, z = xy[nid]
    wrong = true_by_id[nid] != pred_by_id[nid]
    ax.scatter(x, z, s=180 if wrong else 70,
               color="#e6194B" if wrong else "#bdbdbd",
               edgecolors="black", linewidths=0.6, zorder=2)
    if wrong:
        ax.annotate(f"{CLASS_NAMES[true_by_id[nid]]}->{CLASS_NAMES[pred_by_id[nid]]}",
                    (x, z), fontsize=6, ha="center", va="bottom",
                    xytext=(0, 7), textcoords="offset points")
ax.set_title(f"Prediction errors ({n_err} of {len(node_ids)})")
ax.set_aspect("equal"); ax.set_xlabel("X"); ax.set_ylabel("Z")
save(fig, "03_prediction_errors.png")

# 4. Connectivity components (BFS, no networkx)
adj = defaultdict(set)
for a, b in undirected:
    adj[a].add(b); adj[b].add(a)
comp_of = {}
comp_id = 0
for start in node_ids:
    if start in comp_of:
        continue
    q = deque([start]); comp_of[start] = comp_id
    while q:
        u = q.popleft()
        for w in adj[u]:
            if w not in comp_of:
                comp_of[w] = comp_id; q.append(w)
    comp_id += 1
n_comp = comp_id
comp_palette = ["#3cb44b", "#e6194B", "#4363d8", "#f58231"]
fig, ax = plt.subplots(figsize=(11, 4))
draw_edges(ax)
for nid in node_ids:
    x, z = xy[nid]
    ax.scatter(x, z, s=140, color=comp_palette[comp_of[nid] % len(comp_palette)],
               edgecolors="black", linewidths=0.6, zorder=2)
ax.set_title(f"Graph connectivity - {n_comp} connected component"
             f"{'s' if n_comp != 1 else ''} ({len(node_ids)} nodes)")
ax.set_aspect("equal"); ax.set_xlabel("X"); ax.set_ylabel("Z")
save(fig, "04_graph_connectivity_components.png")

# 5. Confusion matrix
K = len(CLASS_NAMES)
cm = np.zeros((K, K), dtype=int)
for nid in node_ids:
    cm[true_by_id[nid], pred_by_id[nid]] += 1
fig, ax = plt.subplots(figsize=(7.5, 6.5))
im = ax.imshow(cm, cmap="Blues")
ax.set_xticks(range(K)); ax.set_yticks(range(K))
ax.set_xticklabels(CLASS_NAMES, rotation=45, ha="right", fontsize=8)
ax.set_yticklabels(CLASS_NAMES, fontsize=8)
ax.set_xlabel("Predicted"); ax.set_ylabel("True")
ax.set_title("Confusion matrix")
thr = cm.max() / 2 if cm.max() else 0
for i in range(K):
    for j in range(K):
        if cm[i, j]:
            ax.text(j, i, cm[i, j], ha="center", va="center",
                    color="white" if cm[i, j] > thr else "black", fontsize=8)
fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
save(fig, "05_confusion_matrix.png")

# 6. Accuracy by class
present = [c for c in range(K) if (cm[c].sum() > 0)]
acc = [cm[c, c] / cm[c].sum() * 100 for c in present]
fig, ax = plt.subplots(figsize=(9, 4.5))
bars = ax.bar([CLASS_NAMES[c] for c in present], acc,
              color=[CLASS_COLORS[c] for c in present], edgecolor="black")
overall = sum(cm[c, c] for c in range(K)) / cm.sum() * 100
ax.axhline(overall, color="black", ls="--", lw=1,
           label=f"overall {overall:.1f}%")
ax.set_ylim(0, 105); ax.set_ylabel("Accuracy (%)")
ax.set_title("Accuracy by class")
for b, a in zip(bars, acc):
    ax.text(b.get_x() + b.get_width() / 2, a + 1.5, f"{a:.0f}%",
            ha="center", fontsize=8)
ax.legend(loc="upper right", fontsize=8)
plt.xticks(rotation=30, ha="right")
save(fig, "06_accuracy_by_class.png")

print(f"\nDone. components={n_comp}, errors={n_err}/{len(node_ids)}, "
      f"overall_accuracy={overall:.1f}%")
