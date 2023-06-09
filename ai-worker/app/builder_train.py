import sys
import multiprocessing
import torch
import pytorch_lightning as pl
import torchvision.datasets as datasets
from torch.utils.data import random_split, DataLoader
from torchvision import transforms
import torchmetrics
from clearml import Task

Task.add_requirements("/clearml.requirements.txt")
task: Task = Task.init(project_name="Test 2", task_name="64823f9580b04ece0b6d4c20")
task.execute_remotely(queue_name="default", clone=False, exit_process=True)

# Data Module for loading data and setting up data loaders
class MNISTDataModule(pl.LightningDataModule):
    def __init__(self, data_dir: str = "./", batch_size: int = 32):
        super().__init__()
        self.data_dir = data_dir
        self.transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
        self.batch_size = batch_size

    def prepare_data(self):
        # download
        datasets.MNIST(self.data_dir, train=True, download=True)
        datasets.MNIST(self.data_dir, train=False, download=True)

    def setup(self, stage: str):
        # Assign train/val datasets for use in dataloaders
        if stage == "fit":
            mnist_full = datasets.MNIST(self.data_dir, train=True, transform=self.transform)
            self.mnist_train, self.mnist_val = random_split(mnist_full, [55000, 5000])

        # Assign test dataset for use in dataloader(s)
        if stage == "test":
            self.mnist_test = datasets.MNIST(self.data_dir, train=False, transform=self.transform)

        if stage == "predict":
            self.mnist_predict = datasets.MNIST(self.data_dir, train=False, transform=self.transform)

    def train_dataloader(self):
        return DataLoader(
                self.mnist_train, 
                batch_size=self.batch_size, 
                num_workers=multiprocessing.cpu_count(),  
                shuffle=True, 
                drop_last=True
            )

    def val_dataloader(self):
        return DataLoader(
                self.mnist_val, 
                batch_size=self.batch_size, 
                num_workers=multiprocessing.cpu_count(),  
                shuffle=False, 
                drop_last=False
            )

    def test_dataloader(self):
        return DataLoader(
                self.mnist_test, 
                batch_size=self.batch_size, 
                num_workers=multiprocessing.cpu_count(), 
                shuffle=False, 
                drop_last=False
            )

    def predict_dataloader(self):
        return DataLoader(
                self.mnist_predict, 
                batch_size=self.batch_size, 
                num_workers=multiprocessing.cpu_count(), 
                shuffle=False, 
                drop_last=False
            )


class ClassificationModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.model = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels=1, out_channels=32, kernel_size=(3, 3), stride=(1, 1)),
            torch.nn.ReLU(),
            torch.nn.Conv2d(in_channels=32, out_channels=64, kernel_size=(3, 3), stride=(1, 1)),
            torch.nn.ReLU(),
            torch.nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2)),
            torch.nn.Dropout(p=0.25),
            torch.nn.Flatten(),
            torch.nn.Linear(in_features=9216, out_features=128),
            torch.nn.ReLU(),
            torch.nn.Dropout(p=0.5),
            torch.nn.Linear(in_features=128, out_features=10),
            torch.nn.LogSoftmax(dim=1)
        )
    def forward(self, x):
        logits = self.model(x)
        return logits
        

class LightningModel(pl.LightningModule):
    def __init__(self, model):
        super().__init__()

        self.learning_rate = 0.01
        # The inherited PyTorch module
        self.model = model

        # Save settings and hyperparameters to the log directory
        # but skip the model parameters
        self.save_hyperparameters(ignore=['model'])

        # Set up attributes for computing the accuracy
        self.train_acc = torchmetrics.Accuracy(task='multiclass', num_classes=10)
        self.valid_acc = torchmetrics.Accuracy(task='multiclass', num_classes=10)
        self.test_acc = torchmetrics.Accuracy(task='multiclass', num_classes=10)
        
    # Defining the forward method is only necessary 
    # if you want to use a Trainer's .predict() method (optional)
    def forward(self, x):
        return self.model(x)
        
    # A common forward step to compute the loss and labels
    # this is used for training, validation, and testing below
    def _shared_step(self, batch):
        features, true_labels = batch
        logits = self(features)
        loss = torch.nn.functional.cross_entropy(logits, true_labels)
        # predicted_labels = torch.argmax(logits, dim=1)
        predicted_labels = logits
        return loss, true_labels, predicted_labels

    def training_step(self, batch, batch_idx):
        loss, true_labels, predicted_labels = self._shared_step(batch)
        self.log("train_loss", loss)
        
        # To account for Dropout behavior during evaluation
        self.model.eval()
        with torch.no_grad():
            _, true_labels, predicted_labels = self._shared_step(batch)
        self.train_acc.update(predicted_labels, true_labels)
        self.log("train_acc", self.train_acc, on_epoch=True, on_step=False)
        self.model.train()
        return loss  # this is passed to the optimzer for training

    def validation_step(self, batch, batch_idx):
        loss, true_labels, predicted_labels = self._shared_step(batch)
        self.log("valid_loss", loss)
        self.valid_acc(predicted_labels, true_labels)
        self.log("valid_acc", self.valid_acc,
                    on_epoch=True, on_step=False, prog_bar=True)

    def test_step(self, batch, batch_idx):
        loss, true_labels, predicted_labels = self._shared_step(batch)
        self.test_acc(predicted_labels, true_labels)
        self.log("test_acc", self.test_acc, on_epoch=True, on_step=False)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(),  lr=self.learning_rate)
        return optimizer
    

model = ClassificationModel()

data_module = MNISTDataModule(data_dir="./", batch_size=50)

lightning_model = LightningModel(model)

trainer = pl.Trainer(
    max_epochs=10,
    accelerator="auto",  # Uses GPUs or TPUs if available
    devices="auto",  # Uses all available GPUs/TPUs if applicable
    log_every_n_steps=100
)
        

trainer.fit(model=lightning_model, datamodule=data_module)