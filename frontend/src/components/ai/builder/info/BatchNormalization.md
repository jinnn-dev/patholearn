---
title: Batch Normalization
meta:
  - name: Batch Normalization
---

# Batch Normalization

The `Batch Normalization`{lang=java} node normalizes the data that is passed through. Normalization allows faster and more stable training.

---

## Node Parameters

### `Momentum`{lang=java}

Describes how much the information of the previous data should be reused. $0$ meaning only the statistics of the current data is used, and $1$ that the statistics over all data is used.

---

**Additional information:**

- https://pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html
- https://en.wikipedia.org/wiki/Batch_normalization
