---
title: Pooling
meta:
  - name: Pooling
---

# Pooling

The `Pooling`{lang=java} node downscales the feature maps of `Conv2D`{lang=java} nodes.
Like the `Conv2D`{lang=java} it uses a kernel that slides over the image. The kernel and slide size can also be configured. The kernel does not have its own values, instead it uses only the values present in the input image. The image belows how max-pooling works. The kernel slides over the image and selects the maximum value and writes it to the output map. Average-pooling calculates the average of all values.
<img class="w-1/3" src="../../../../assets/maxpool.gif">
The goal is to only keep the most relevant features of the image. This reduces the dimensions of the features maps and improves the training speed and performance in general.

---

## Node Parameters

### `Kernel`{lang=java}

Defines the size of each kernel. Normally, only symmetric kernels are used, e.g. $3 \times 3$ or $5 \times 5$.

### `Stride`{lang=java}

Defines how many pixels the kernel should in each step for every direction. Normally, these values are equal in both directions.

### `Type`{lang=java}

Wether to use `max`{lang=java}-pooling or `average`{lang=java}-pooling

### `Padding`{lang=java}

Can either be `None`{lang=java}, where no padding is used and the output image can have different dimensions as the input image, or `Same`{lang=java}, where the input and output image dimensions are the same.

---

**Additional information:**

- https://de.wikipedia.org/wiki/Convolutional_Neural_Network#Pooling_Layer
- https://pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html
- https://pytorch.org/docs/stable/generated/torch.nn.AvgPool2d.html
