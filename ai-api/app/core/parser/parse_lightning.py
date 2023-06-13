from string import Template

from app.schema.parser import LossFunctionString, OptimizerString, LossFunctionModule
from app.core.parser.parse_graph import OutputNode
from app.utils.logger import logger


class LightningModel:
    def __init__(self, output_node: OutputNode) -> None:
        self.learning_rate = output_node.learning_rate

        with open("/app/core/parser/templates/lightning_model.txt", "r") as f:
            src = Template(f.read())
            replacements = {
                "learning_rate": self.learning_rate,
                "loss": LossFunctionString._member_map_[
                    output_node.loss_function.name
                ].value,
                "optimizer": OptimizerString._member_map_[
                    output_node.optimizer.name
                ].value,
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
