---
title: Metric
meta:
  - name: Metric
---

# Metric

The `Metric`{lang=java} node calculates and display different metrics for the training, validation and test dataset.
The confision matrix can explain the models performance, especially in binary classification tasks. The matrix contains four differnt values:

1. **True Positives (TP):**

   - These are the cases in which the model correctly predicted the positive class.
   - For example, in a medical test, a TP would mean the patient has the disease (positive class) and the test correctly identified them as having the disease.

2. **False Positives (FP):**

   - These are the cases in which the model incorrectly predicted the positive class when the actual class was negative.
   - In the context of the same medical test, an FP would mean the patient does not have the disease (negative class), but the test incorrectly identified them as having the disease.
     The following metrics are available:

3. **True Negatives (TN):**

   - These are the cases in which the model correctly predicted the negative class.
   - In our medical test example, a TN would mean the patient does not have the disease and the test correctly identified them as not having the disease.

4. **False Negatives (FN):**

   - These are the cases in which the model incorrectly predicted the negative class when the actual class was positive.
   - Back to the medical test, an FN would mean the patient has the disease, but the test missed it and incorrectly identified them as not having the disease.

Based on these four values, different metrics can be calculated:

- **Epoch** \
  Displays the current training iteration

- **Loss** \
  Quantifies the discrepancy between the predicted values and the actual values. A loss of $0$ means that the neural network can predict the data perfectly.

- **Accuracy** \
  Is the ratio of the number of correct predictions to the total number of predictions made.
  $$\frac{TP + TN}{TP + TN + FP + FN}$$

- **Precision** \
   Represents the proportion of predicted positive classes that were actually positive.
  $$\frac{TP}{TP+FP}$$

- **Recall/Sensitivity/True Positive Rate (TPR)**\
  Represents the proportion of actual positive classes that were correctly predicted by the model.
  $$\frac{TP}{TP + FN}$$

- **Specificity/True Negative Rate**\
   Represents the proportion of actual negative classes that were correctly predicted by the model
  $$\frac{TN}{TN + FP}$$

- **F1 Score**\
 Provides a single score that balances between the precision and and recall.
$$2 \times \frac{Precision \times Recall}{Precision + Recall}$$

- **Intersection Over Union (IoU)**\
  Calculates how good the prediceted masks overlaps with the original mask
  $$\frac{TP}{TP + FP + FN}$$ 
