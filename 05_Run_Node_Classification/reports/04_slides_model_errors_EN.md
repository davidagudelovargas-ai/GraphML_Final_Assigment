---
marp: true
paginate: true
---

<!--
Presentation slides (Marp format — render with the "Marp for VS Code"
extension, or copy the text into PowerPoint / Google Slides).
English version of 04_slides_model_errors.md.
-->

# How does the model decide what each room is?

**The model guesses each room "blindfolded".**

It only knows 2 clues about each room:

1. Which **zone** it belongs to (private / social / service)
2. How it **connects** to the others (doors and passages)

> It cannot see the size, the furniture or the windows.

<!--
Reminder: node = room; graph = rooms linked by doors/passages.
The model (a neural network pretrained on the MSD dataset) classifies each node.
-->

---

# Living room, dining and kitchen "feel" the same

In an open-plan layout, all three:
- are in the **same zone** (social), and
- have **similar connections**.

To the model they are like **triplets dressed alike** → it cannot tell them
apart and calls them all **"kitchen"**.

| Room (true) | Prediction | Correct |
|---|---|---|
| 🛋️ Living room (5) | kitchen, kitchen… | **0 %** |
| 🍽️ Dining (3) | kitchen, kitchen… | **0 %** |
| 🪜 Stairs (6) | stairs | 100 % |
| 🛏️ Bedroom (2) | bedroom | 100 % |

**This is not a project bug:** the clues are not enough to separate open
spaces. *(Overall accuracy: 60 %.)*

<!--
Stairs, bedrooms and corridors DO have a distinctive connection signature, so
they are recognized well. Living/dining/kitchen share zone and connectivity.
-->

---

# Would adding the window as a feature help?

**Just "has a window? yes/no" → does NOT help** (living, dining and kitchen
nearly all have one).

**The window SIZE → would help**, according to the building's data:

| Type | Average window |
|---|---|
| 🛋️ Living room | **5.9 m²** (always large) |
| 🍳 Kitchen | **2.0 m²** (small or none) |
| 🍽️ Dining | 5.7 m² but **very variable** (1.9 → 10) |

- It would separate **living room vs kitchen** well (large vs small glazing).
- **Dining would stay ambiguous** (its windows vary a lot).
- ⚠️ Note: the pretrained model uses 7 fixed features; to use the window you
  would have to **retrain** a new model, not just add the value.

<!--
Honest takeaway: window size helps partially, mostly living-vs-kitchen.
Best combined with room area and proportion.
-->
