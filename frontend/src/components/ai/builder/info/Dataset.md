---
title: Dataset
meta:
  - name: Dataset
---

# Dataset

The Dataset node is the entrypoint to every neural network. It contains the data needed for training. Select a dataset that you would like to train a neural network on. Connect either a convolutional node or a complete architecture node to it.

The set of images is split into three different datasets: `training`, `validation` and `test`. The training dataset is used for the actual learning of the neural network. The validation dataset is used to evaluate the performance of the neural network and compare them to other neural networks. The test dataset shows how the neural network would perform in real-life use.

---

## Node Parameters

### `Dataset`{lang=java}

The dataset on which the neural network should be trained on.

---
