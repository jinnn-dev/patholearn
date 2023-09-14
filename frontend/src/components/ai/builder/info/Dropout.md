---
title: Dropout
meta:
  - name: Dropout
---

# Dropout

The `Dropout`{lang=java} disables some neurons in the neural network. The **probability** value determines how likely a neuron is to be disabled. Disabling neurons lets the network learn more robust features, therefore improving the generalization on new data.

---

## Node Parameters

### `Probability`{lang=java}

The probability of a neuron to be disabled.

---

**Additional information:**

- https://en.wikipedia.org/wiki/Dilution_(neural_networks)
- https://pytorch.org/docs/stable/generated/torch.nn.Dropout.html
