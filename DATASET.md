# Dataset Information

## PlantVillage Dataset

- **Source:** TensorFlow Datasets
- **Link:** https://www.tensorflow.org/datasets/catalog/plant_village
- **Size:** ~820MB
- **Classes:** 38 plant disease categories
- **Total Images:** 54,306

## How to Load
```python
import tensorflow_datasets as tfds
dataset = tfds.load('plant_village', split='train')
```

## Preprocessing
- Images resized to 224x224
- Normalized pixel values between 0 and 1
- Each Class limited to 100-102 images each.
