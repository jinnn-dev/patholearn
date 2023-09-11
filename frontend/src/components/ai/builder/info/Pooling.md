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
