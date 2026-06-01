# 🌿 Sick-greens

A deep learning system for **plant disease detection and progression tracking** built on the PlantVillage dataset. Given a leaf image, the model identifies the disease, classifies its stage (healthy → early → mid → late), estimates days since infection, and computes a treatment urgency score.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sharr-catalyst/Sick-greens/blob/main/YourGreensAreSick_v2.ipynb)
[![CI](https://github.com/sharr-catalyst/Sick-greens/actions/workflows/blank.yml/badge.svg?branch=main)](https://github.com/sharr-catalyst/Sick-greens/actions/workflows/blank.yml)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.12%2B-FF6F00?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![Keras](https://img.shields.io/badge/Keras-2.12%2B-D00000?logo=keras&logoColor=white)](https://keras.io/)
[![MobileNetV2](https://img.shields.io/badge/Backbone-MobileNetV2-blue)](https://arxiv.org/abs/1801.04381)
[![Dataset](https://img.shields.io/badge/Dataset-PlantVillage-4CAF50?logo=leaf&logoColor=white)](https://www.tensorflow.org/datasets/catalog/plant_village)
[![Classes](https://img.shields.io/badge/Classes-38-orange)](https://github.com/sharr-catalyst/Sick-greens)
[![Stages](https://img.shields.io/badge/Stages-4-yellowgreen)](https://github.com/sharr-catalyst/Sick-greens)
[![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey)](LICENSE)
[![Hugging Face](https://img.shields.io/badge/🤗%20Model-Hugging%20Face-yellow)](https://huggingface.co/Sharmistha-catalyst/sick-greens-plant-disease)
[![Streamlit App](https://img.shields.io/badge/Streamlit-Plant%20Leaf%20Disease%20Detector-2E7D32?style=flat-square&logo=streamlit&logoColor=white)](https://your-greensaresick.streamlit.app/)
---

## What It Does

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

## Dataset

**PlantVillage** via TensorFlow Datasets (`tfds.load('plant_village')`)
- 38 disease/healthy classes across crops including Tomato, Potato, Apple, Grape, Corn, Peach, Pepper, Strawberry, and more
- Capped at ~100–102 images per class for balanced training
- Split: **70% train / 15% validation / 15% test**

---

## Model Architecture

- **Backbone**: MobileNetV2 (pretrained on ImageNet, fine-tuned)
- **Heads**:
  - Disease classification head (38-class softmax)
  - Stage classification head (4-class softmax)
  - Days regression head (single neuron)
- Class weights applied to handle imbalance

---

## Evaluation Metrics

| Task | Metric |
|------|--------|
| Disease Classification | Accuracy, Weighted F1 |
| Stage Classification | Accuracy, Weighted F1 |
| Days Estimation | MAE, RMSE |

---

## Tech Stack

- Python, TensorFlow / Keras
- TensorFlow Datasets
- MobileNetV2
- Pandas, NumPy
- Matplotlib, Seaborn, Plotly
- scikit-learn
- OpenCV, Pillow

---

## Requirements

Install all dependencies via:

```bash
pip install -r requirements.txt
```

> **Note:** If running on **Google Colab**, the notebook auto-installs all dependencies in its first cell — no manual setup needed.

Key requirements at a glance:

| Package | Version |
|---------|---------|
| tensorflow | ≥ 2.12.0 |
| tensorflow-datasets | ≥ 4.9.0 |
| keras | ≥ 2.12.0 |
| scikit-learn | ≥ 1.2.0 |
| opencv-python-headless | ≥ 4.7.0 |
| Pillow | ≥ 9.4.0 |
| numpy | ≥ 1.23.0 |
| pandas | ≥ 1.5.0 |
| matplotlib | ≥ 3.6.0 |
| seaborn | ≥ 0.12.0 |
| plotly | ≥ 5.14.0 |

See [`requirements.txt`](requirements.txt) for the full pinned list.

---

## Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/sharr-catalyst/Sick-greens.git
   cd Sick-greens
   ```

2. *(Optional — local run only)* Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Open `YourGreensAreSick_v2.ipynb` in Google Colab

4. Run all cells: **Runtime → Run all**
   > The notebook will auto-install all dependencies in the first cell.

---

## 📂 Project Structure

```
Sick-greens/
│
├── models/                         
│   ├── metadata.json                 # Contains training metrics, dataset sizes, and architecture data
│      
│
├── outputs/                          # 📊 Training visualization assets
│   ├── confusion_matrices.png
│   ├── limited_class_distribution.png
│   ├── progression_curve.png
│   ├── sample_images.png
│   ├── sample_predictions.png
│   └── training_history.png
│
├── README.md                         
├── app.py                           
├── requirements.txt                  
└── YourGreensAreSick_v2.ipynb       
```

---

## Model

The trained model is hosted on Hugging Face:

[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-sick--greens--plant--disease-yellow)](https://huggingface.co/Sharmistha-catalyst/sick-greens-plant-disease)

To download programmatically:
```python
from huggingface_hub import hf_hub_download

model_path = hf_hub_download(
    repo_id="Sharmistha-catalyst/sick-greens-plant-disease",
    filename="final_progression_model.h5"
)
```
## Web App
[![Streamlit App](https://img.shields.io/badge/Live%20Demo-Sick--greens-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://your-greensaresick.streamlit.app/)

---

## Project Report

[View Report](https://github.com/sharr-catalyst/Sick-greens/blob/main/Plant%20project%20report%20.pdf)

---

## Author

**sharr-catalyst** — [GitHub](https://github.com/sharr-catalyst)
