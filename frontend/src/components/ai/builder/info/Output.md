---
title: Output
meta:
  - name: Output
---

# Output

The `Output`{lang=java} node configures the different parameters for training.

---

## Node Parameters

### `Optimizer`{lang=java}

The optimizer function to use.

### `Loss Function`{lang=java}

The loss function to use.

### `Learning Rate`{lang=java}

The learning rate determines the speed of learning. High learning rate result in fast training, but the learning could fail. Small learning can result in very slow training, where convergence of the training will never happen.

### `Epochs`{lang=java}

The number of training iterations. One iterations is processing the entire dataset once.

### `Batch Size`{lang=java}

How many elements of the dataset should be used per training step. Each batch must fit on the GPU, therefore small values are better.

---

**Additional information:**

- https://en.wikipedia.org/wiki/Loss_function
