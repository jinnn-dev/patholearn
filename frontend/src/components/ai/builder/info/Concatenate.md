---
title: Concatenate
meta:
  - name: Concatenate
---

# Concatenate

The `Concatenate`{lang=java} node concats two maps $I_1$ and $I_2$ togehter. The width and height of both must be equal. The number of channels can be different. Given the channels of $I_1$ as $C_{I_1}$ and the channels $I_2$ as $C_{I_2}$. The number of channels after the concatination is given as $C_{con} = C_{I_1} + C_{I_2}$

**Additional information:**

- https://pytorch.org/docs/stable/generated/torch.cat.html
