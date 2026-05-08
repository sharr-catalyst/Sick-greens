# Sick-greens

A deep learning system for **plant disease detection and progression tracking** built on the PlantVillage dataset. Given a leaf image, the model identifies the disease, classifies its stage (healthy → early → mid → late), estimates days since infection, and computes a treatment urgency score.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sharr-catalyst/Sick-greens/blob/main/YourGreensAreSick_v2.ipynb)

---

## 🧠 What It Does

- **Disease Classification** — identifies plant disease across 38 classes (e.g. Apple Scab, Tomato Late Blight, Potato Early Blight)
- **Stage Classification** — maps each disease to one of 4 progression stages:
  - `Stage 0` — Healthy
  - `Stage 1` — Early
  - `Stage 2` — Mid-stage
  - `Stage 3` — Late-stage
- **Days Estimation** — regression head estimates days since infection onset
- **Urgency Scoring** — outputs a 0–10 urgency score with action recommendations (Low / Moderate / High / Critical)
- **Temporal Tracking** — tracks disease progression across multiple images over time and plots stage & urgency curves

---

## 📊 Dataset

**PlantVillage** via TensorFlow Datasets (`tfds.load('plant_village')`)

- 38 disease/healthy classes across crops including Tomato, Potato, Apple, Grape, Corn, Peach, Pepper, Strawberry, and more
- Capped at ~100–102 images per class for balanced training
- Split: **70% train / 15% validation / 15% test**

---

## 🏗️ Model Architecture

- **Backbone**: MobileNetV2 (pretrained on ImageNet, fine-tuned)
- **Heads**:
  - Disease classification head (38-class softmax)
  - Stage classification head (4-class softmax)
  - Days regression head (single neuron)
- Class weights applied to handle imbalance

---

## 📈 Evaluation Metrics

| Task | Metric |
|------|--------|
| Disease Classification | Accuracy, Weighted F1 |
| Stage Classification | Accuracy, Weighted F1 |
| Days Estimation | MAE, RMSE |

---

## 🛠️ Tech Stack

- Python, TensorFlow / Keras
- TensorFlow Datasets
- MobileNetV2
- Pandas, NumPy
- Matplotlib, Seaborn, Plotly
- scikit-learn
- OpenCV, Pillow
- Streamlit (deployment)

---

## 🚀 Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/sharr-catalyst/Sick-greens.git
   ```

2. Open `YourGreensAreSick_v2.ipynb` in Google Colab

3. Run all cells: **Runtime → Run all**

   > The notebook will auto-install all dependencies in the first cell.

---

## 📂 Project Structure

```
Sick-greens/
│
├── YourGreensAreSick_v2.ipynb      # Main notebook
├── models/
│   ├── final_progression_model.h5  # Saved model
│   └── metadata.json               # Class names, mappings, metrics
├── outputs/
│   ├── limited_class_distribution.png
│   ├── sample_images.png
│   ├── confusion_matrices.png
│   ├── sample_predictions.png
│   └── progression_curve.png
└── README.md
```

---
## 📄 Project Report
[View Report](https://github.com/sharr-catalyst/Sick-greens/blob/main/Plant%20project%20report%20.pdf)

## Author
**sharr-catalyst** — [GitHub](https://github.com/sharr-catalyst)
