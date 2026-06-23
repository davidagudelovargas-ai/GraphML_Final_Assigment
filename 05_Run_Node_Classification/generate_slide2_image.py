"""Compose slide 2 ('why living/dining = 0%') as a single 16:9 PNG, embedding
the existing accuracy-by-class bar chart.

Output: 05_Run_Node_Classification/reports/04_slide2_visual_EN.png
Run:    python 05_Run_Node_Classification/generate_slide2_image.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.lines import Line2D


def find_project_root():
    for c in (Path(__file__).resolve(), *Path(__file__).resolve().parents):
        if (c / "01_Research_Dataset_and_References").exists():
            return c
    raise FileNotFoundError("root not found")


ROOT = find_project_root()
WORK = ROOT / "05_Run_Node_Classification"
CHART = WORK / "images" / "06_accuracy_by_class.png"
OUT = WORK / "reports" / "04_slide2_visual_EN.png"

fig = plt.figure(figsize=(13.33, 7.5), dpi=150)
fig.patch.set_facecolor("white")

# --- Title + accent line ---
fig.text(0.035, 0.905, "Why the model confuses living room, dining & kitchen",
         fontsize=22, fontweight="bold", color="#1a1a1a", va="center")
fig.add_artist(Line2D([0.035, 0.965], [0.85, 0.85], color="#e6194B",
                      lw=3, transform=fig.transFigure))

# --- Left column: explanation ---
intro = (
    "The model classifies each room knowing ONLY:\n"
    "    -  which zone it is in  (social / private / service)\n"
    "    -  how it connects to other rooms (doors, passages)\n\n"
    "Living room, dining and kitchen share the same zone\n"
    "and have similar connections, so they look identical\n"
    "to the model -- it labels them all \"kitchen\"."
)
fig.text(0.035, 0.79, intro, fontsize=14, va="top", color="#222222", linespacing=1.45)

highlight = (
    "Living rooms      ->  0% correct  (all 5 -> \"kitchen\")\n"
    "Dining            ->  0% correct  (all 3 -> \"kitchen\")\n"
    "Stairs & bedrooms ->  100% correct"
)
fig.text(0.035, 0.45, highlight, fontsize=12.5, va="top",
         family="DejaVu Sans Mono", color="#1a1a1a",
         bbox=dict(boxstyle="round,pad=0.7", facecolor="#fdecea",
                   edgecolor="#e6194B", linewidth=1.5))

takeaway = (
    "Not a bug: the features (zone + connectivity) cannot\n"
    "separate open-plan rooms.    Overall accuracy: 60%."
)
fig.text(0.035, 0.20, takeaway, fontsize=13.5, va="top", color="#444444",
         fontstyle="italic", linespacing=1.4)

# --- Right column: the existing bar chart ---
ax = fig.add_axes([0.50, 0.08, 0.47, 0.70])
ax.imshow(mpimg.imread(str(CHART)))
ax.axis("off")

fig.savefig(OUT, dpi=150, facecolor="white")
plt.close(fig)
print("wrote", OUT)
