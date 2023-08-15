from string import Template
from typing import List

from app.schema.parser import (
    LossFunctionString,
    OptimizerString,
    LossFunctionModule,
    ArchitectureString,
)
from app.core.parser.parse_graph import (
    DatasetNode,
    MetricNode,
    OutputNode,
    SegmentationNode,
)
from app.utils.logger import logger


metric_functions = {
    "Accuracy": "torchmetrics.Accuracy",
    "ROC AUC": "torchmetrics.AUROC",
    "Average Precision": "torchmetrics.AveragePrecision",
    "Cohen Kappa": "torchmetrics.CohenKappa",
    "F1 Score": "torchmetrics.F1Score",
    "Precision": "torchmetrics.Precision",
}

metrics_variable_name = {
    "Accuracy": "accuracy",
    "ROC AUC": "roc_auc",
    "Average Precision": "average_precision",
    "Cohen Kappa": "cohen_kappa",
    "F1 Score": "f1_score",
    "Precision": "precision",
}

metric_functions_segmentation = {
    "Accuracy": "smp.metrics.accuracy",
    "F1 Score": "smp.metrics.f1_score",
    "Precision": "smp.metrics.precision",
    "IOU": "smp.metrics.iou_score",
}

metric_variable_name_segmentation = {
    "Accuracy": "accuracy",
    "F1 Score": "f1_score",
    "Precision": "precision",
    "IOU": "iou",
}


class SegmentationModel:
    def __init__(self, output_node: OutputNode, metric_nodes: List[MetricNode]):
        self.learning_rate = output_node.learning_rate

        with open("/app/core/parser/templates/segmentation/model.txt", "r") as f:
            src = Template(f.read())
            metric_calls = []
            metric_instances = []
            for metric in metric_nodes:
                metric_call, metric_instance = self.construct_metric_calc(metric)
                if metric_call is not None and metric_instance is not None:
                    metric_calls.append(metric_call)
                    metric_instances.append(metric_instance)

            replacements = {
                "learning_rate": self.learning_rate,
                "loss": LossFunctionString._member_map_[
                    output_node.loss_function.name
                ].value,
                "metric_calls": "\n        ".join(metric_calls),
                "metrics": ",\n".join(metric_instances),
                "optimizer": OptimizerString._member_map_[
                    output_node.optimizer.name
                ].value,
            }
        result = src.substitute(replacements)
        self.model_class = result
        with open(
            "/app/core/parser/templates/segmentation/trainer_instance.txt", "r"
        ) as f:
            src = Template(f.read())
            replacements = {"epochs": output_node.epoch}
            result = src.substitute(replacements)
            self.trainer = result

    def construct_metric_calc(self, metric_node: MetricNode):
        selected_metric = metric_node.value
        if selected_metric in metric_functions_segmentation:
            metric_function = metric_functions_segmentation[selected_metric]
            metric_variable_name = metric_variable_name_segmentation[selected_metric]
            metric_call = f"""{metric_variable_name} = {metric_function}(tp, fp, fn, tn, reduction="micro")"""
            metric_instance = (
                """f"{stage}"""
                + f"""_{metric_variable_name}": {metric_variable_name}"""
            )
            return metric_call, metric_instance
        return None, None

    def get_instance(self, variable_name: str, segmentation_node: SegmentationNode):
        return f"""{variable_name} = MaskModel(arch="{ArchitectureString[segmentation_node.version]}", encoder_name="{segmentation_node.encoderVersion}", in_channels=3, out_classes=len(data_module.data_train.rgb_to_int_map.values()))"""


class LightningModel:
    def __init__(
        self,
        dataset_node: DatasetNode,
        output_node: OutputNode,
        metric_nodes: List[MetricNode],
    ) -> None:
        self.learning_rate = output_node.learning_rate
        (
            constructor_elements,
            train_elements,
            valid_elements,
            test_elements,
        ) = self.get_metrics(dataset_node, metric_nodes)
        with open("/app/core/parser/templates/lightning_model.txt", "r") as f:
            src = Template(f.read())
            replacements = {
                "metrics_constructors": "\n".join(
                    "        " + element for element in constructor_elements
                ),
                "learning_rate": self.learning_rate,
                "loss": LossFunctionString._member_map_[
                    output_node.loss_function.name
                ].value,
                "optimizer": OptimizerString._member_map_[
                    output_node.optimizer.name
                ].value,
                "metrics_train_updates": "\n".join(
                    "        " + element for element in train_elements
                ),
                "metrics_valid_updates": "\n".join(
                    "        " + element for element in valid_elements
                ),
                "metrics_test_updates": "\n".join(
                    "        " + element for element in test_elements
                ),
            }
            result = src.substitute(replacements)
            self.model_class = result

        with open("/app/core/parser/templates/trainer_instance.txt", "r") as f:
            src = Template(f.read())
            replacements = {"epochs": output_node.epoch}
            result = src.substitute(replacements)
            self.trainer = result

    def get_instance(self, variable_name: str, model_name: str):
        return f"{variable_name} = LightningModel({model_name})"

    def get_metrics(self, dataset_node: DatasetNode, metric_nodes: List[MetricNode]):
        constructor_elements = set()
        train_elements = set()
        valid_elements = set()
        test_elements = set()

        for metric_node in metric_nodes:
            if metric_node.value == "Loss" or metric_node.value == "Epoch":
                continue

            for stage in ["train", "valid", "test"]:
                metric_name = f"{stage}_{metrics_variable_name[metric_node.value]}"
                variable_name = f"self.{metric_name}"
                metric = f"{variable_name} = {metric_functions[metric_node.value]}(task='multiclass', num_classes={dataset_node.classes})"
                constructor_elements.add(metric)
                update = f"{variable_name}(predicted_labels, true_labels)"
                log = f"self.log('{metric_name}', {variable_name}, on_epoch=True, on_step=False)"
                if stage == "train":
                    train_elements.add(update)
                    train_elements.add(log)
                if stage == "valid":
                    valid_elements.add(update)
                    valid_elements.add(log)
                if stage == "test":
                    test_elements.add(update)
                    test_elements.add(log)

        return (
            list(constructor_elements),
            list(train_elements),
            list(valid_elements),
            list(test_elements),
        )
