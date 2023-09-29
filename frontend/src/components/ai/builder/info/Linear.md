---
title: Linear
meta:
  - name: Linear
---

# Linear

The `Linear`{lang=java} node takes a list (vector) as input and maps them to the defined `neurons`{lang=java}.
Each linear layer calculates the following function:
$$y = Wx + b,$$
where $x$ is the input vector. Each value of the vector is multiplied with a weight of the vector $W$ and a bias value $b$ is added. Internally it uses matrix multiplication to map the input matrix to the defined size of the output. $y$ is the resulting matrix.

When doing classification, `Linear`{lang=java} layers are often used at the end of an architecture after the `Conv2D`{lang=java} layers. They enable to map the detected features on the image to the defined classes. Each neuron in the last layer corresponds to a class.

---

## Node Parameters

### `Neurons`{lang=java}

The number of artificial neurons to use in the layer

### `Activation`{lang=java}

The activation function is applied after the convolution operation. Generally `ReLU`{lang=java} is the best fitting function.

---

**Additional information:**

- https://en.wikipedia.org/wiki/Perceptron
- https://pytorch.org/docs/stable/generated/torch.nn.Linear.html
