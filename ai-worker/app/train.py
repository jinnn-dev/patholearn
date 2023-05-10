from clearml import Dataset, Task
import argparse
import torch
from torch import nn
from torch.utils.data import DataLoader
import pytorch_lightning as pl
import numpy as np
import multiprocessing
from sklearn.model_selection import train_test_split
import pathlib
from os import listdir
import pandas as pd
from PIL import Image
import albumentations as A
from albumentations.pytorch import ToTensorV2
from torchvision.models import (
    resnet50,
    ResNet50_Weights,
    resnet18,
    ResNet18_Weights,
)
from sklearn.utils import compute_class_weight
import torchmetrics.classification as metrics
import torchmetrics
from pytorch_lightning.callbacks.progress import TQDMProgressBar
from pytorch_lightning import loggers as pl_loggers
import tensorboardX


def main(project_name, task_name, dataset_id, model_name):
    Task.add_requirements("/clearml.requirements.txt")
    task: Task = Task.init(project_name=project_name, task_name=task_name)
    task.execute_remotely(queue_name="default", clone=False, exit_process=True)
    NUM_EPOCHS = 5

    def my_transform(key="train"):
        train_sequence = A.Compose(
            [
                A.Resize(height=50, width=50),
                A.ShiftScaleRotate(
                    shift_limit=0.05, scale_limit=0.05, rotate_limit=15, p=0.5
                ),
                A.RGBShift(r_shift_limit=15, g_shift_limit=15, b_shift_limit=15, p=0.5),
                A.RandomBrightnessContrast(p=0.5),
                A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
                ToTensorV2(),
            ]
        )

        val_sequence = A.Compose(
            [
                A.Resize(height=50, width=50),
                A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
                ToTensorV2(),
            ]
        )

        data_transforms = {"train": train_sequence, "val": val_sequence}
        return data_transforms[key]

    class BHIDataset(Dataset):
        def __init__(self, *, transform=None, split="train"):
            self.transform = transform
            self.split = split
            self.data = None

            self.init_dataset()

        @property
        def save_file_path(self):
            return (
                pathlib.Path(__file__)
                .parent.resolve()
                .joinpath("cache", f"bhi_{self.split}.pt")
            )

        def init_dataset(self):
            dataset = Dataset.get(dataset_id=dataset_id, alias="BHI")
            dataset_path = dataset.get_local_copy()
            # dataset_path = "/data2/datasets/datasets/BHI"
            base_path = f"{dataset_path}/IDC_regular_ps50_idx5/"
            folder = listdir(base_path)
            total_images = 0
            for n in range(len(folder)):
                patient_id = folder[n]
                for c in [0, 1]:
                    patient_path = base_path + patient_id
                    class_path = patient_path + "/" + str(c) + "/"
                    subfiles = listdir(class_path)
                    total_images += len(subfiles)
            data = pd.DataFrame(
                index=np.arange(0, total_images),
                columns=["patient_id", "path", "target"],
            )
            k = 0
            for n in range(len(folder)):
                patient_id = folder[n]
                patient_path = base_path + patient_id
                for c in [0, 1]:
                    class_path = patient_path + "/" + str(c) + "/"
                    subfiles = listdir(class_path)
                    for m in range(len(subfiles)):
                        image_path = subfiles[m]
                        data.iloc[k]["path"] = class_path + image_path
                        data.iloc[k]["target"] = c
                        data.iloc[k]["patient_id"] = patient_id
                        k += 1
            patients = data.patient_id.unique()

            train_ids, sub_test_ids = train_test_split(
                patients, test_size=0.3, random_state=0
            )

            test_ids, val_ids = train_test_split(
                sub_test_ids, test_size=0.5, random_state=0
            )

            if self.split == "train":
                data = data.loc[data.patient_id.isin(train_ids), :].copy()
            elif self.split == "test":
                data = data.loc[data.patient_id.isin(test_ids), :].copy()
            else:
                data = data.loc[data.patient_id.isin(val_ids), :].copy()

            coord = data.path.str.rsplit("_", n=4, expand=True)
            coord = coord.drop([0, 1, 4], axis=1)
            coord = coord.rename({2: "x", 3: "y"}, axis=1)
            coord.loc[:, "x"] = (
                coord.loc[:, "x"].str.replace("x", "", case=False).astype(np.int64)
            )
            coord.loc[:, "y"] = (
                coord.loc[:, "y"].str.replace("y", "", case=False).astype(np.int64)
            )
            data.loc[:, "x"] = coord.x.values
            data.loc[:, "y"] = coord.y.values

            self.data = data
            # self.__save()

        def __len__(self):
            return len(self.data)

        def __getitem__(self, idx):
            image_path = self.data.path.values[idx]
            image = Image.open(image_path)
            image = image.convert("RGB")
            image = np.array(image)
            if self.transform:
                image = self.transform(image=image)["image"]
            if "target" in self.data.columns.values:
                target = np.int64(self.data.target.values[idx])
            else:
                target = None
            return image, torch.tensor(target)

    BATCH_SIZE = 256
    train_dataset = BHIDataset(split="train", transform=my_transform(key="train"))
    test_dataset = BHIDataset(split="test", transform=my_transform(key="val"))
    val_dataset = BHIDataset(split="val", transform=my_transform(key="val"))
    train_loader = DataLoader(
        train_dataset,
        batch_size=256,
        shuffle=True,
        drop_last=True,
        num_workers=multiprocessing.cpu_count(),
    )
    valid_loader = DataLoader(
        test_dataset,
        batch_size=256,
        shuffle=False,
        drop_last=True,
        num_workers=multiprocessing.cpu_count(),
    )
    test_loader = DataLoader(
        val_dataset,
        batch_size=256,
        shuffle=False,
        drop_last=False,
        num_workers=multiprocessing.cpu_count(),
    )

    if model_name == "ResNet-50":
        model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
    else:
        model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
    num_features = model.fc.in_features
    NUM_CLASSES = 2
    model.fc = nn.Sequential(
        nn.Linear(num_features, 512),
        nn.ReLU(),
        nn.BatchNorm1d(512),
        nn.Dropout(0.5),
        nn.Linear(512, 1024),
        nn.ReLU(),
        nn.BatchNorm1d(1024),
        nn.Dropout(0.5),
        nn.Linear(1024, 512),
        nn.ReLU(),
        nn.BatchNorm1d(512),
        nn.Dropout(0.5),
        nn.Linear(512, 512),
        nn.ReLU(),
        nn.BatchNorm1d(512),
        nn.Dropout(0.5),
        nn.Linear(512, 256),
        nn.ReLU(),
        nn.BatchNorm1d(256),
        nn.Dropout(0.5),
        nn.Linear(256, NUM_CLASSES),
    )

    weights = compute_class_weight(
        y=train_dataset.data.target.values,
        class_weight="balanced",
        classes=train_dataset.data.target.unique(),
    )
    class_weights = torch.FloatTensor(weights)

    class_weights = class_weights.cuda()

    criterion = nn.CrossEntropyLoss(weight=class_weights)

    def get_scheduler(optimiser, min_lr, max_lr, stepsize):
        # suggested_stepsize = 2*num_iterations_within_epoch
        stepsize_up = np.int64(stepsize / 2)
        scheduler = torch.optim.lr_scheduler.CyclicLR(
            optimizer=optimiser,
            base_lr=min_lr,
            max_lr=max_lr,
            step_size_up=stepsize_up,
            step_size_down=stepsize_up,
            mode="triangular",
        )
        scheduler = torch.optim.lr_scheduler.ExponentialLR(optimiser, gamma=0.9)
        return scheduler

    class LitResNet(pl.LightningModule):
        def __init__(self, model):
            super().__init__()
            self.save_hyperparameters()
            self.train_acc = metrics.BinaryAccuracy()
            self.train_auc = metrics.BinaryAUROC()
            self.train_precision = metrics.BinaryPrecision()
            self.train_f1 = torchmetrics.F1Score(task="binary", num_classes=2)
            self.train_dice = torchmetrics.Dice(num_classes=2)

            self.val_acc = metrics.BinaryAccuracy()
            self.val_auc = metrics.BinaryAUROC()
            self.val_precision = metrics.BinaryPrecision()
            self.val_f1 = torchmetrics.F1Score(task="binary", num_classes=2)
            self.val_dice = torchmetrics.Dice(num_classes=2)

            self.test_acc = metrics.BinaryAccuracy()
            self.test_auc = metrics.BinaryAUROC()
            self.test_precision = metrics.BinaryPrecision()
            self.test_f1 = torchmetrics.F1Score(task="binary", num_classes=2)
            self.test_dice = torchmetrics.Dice(num_classes=2)

            self.model = model

        def training_step(self, batch, batch_idx):
            x, y = batch
            x_hat = self.model(x)
            _, preds = torch.max(x_hat, 1)
            loss = criterion(x_hat, y)

            self.train_acc(preds, y)
            self.train_auc(preds, y)
            self.train_precision(preds, y)
            self.train_f1(preds, y)
            self.train_dice(preds, y)
            self.log("train_loss", loss, on_step=True, on_epoch=True, prog_bar=True)
            self.log("train_acc", self.train_acc, on_step=True, on_epoch=True)
            self.log("train_auc", self.train_auc, on_step=False, on_epoch=True)
            self.log(
                "train_precision", self.train_precision, on_step=False, on_epoch=True
            )
            self.log("train_f1", self.train_f1, on_step=False, on_epoch=True)
            self.log("train_dice", self.train_dice, on_step=False, on_epoch=True)
            return loss

        def test_step(self, batch, batch_idx):
            # this is the test loop
            x, y = batch
            x_hat = self.model(x)
            _, preds = torch.max(x_hat, 1)
            loss = criterion(x_hat, y)

            self.test_acc(preds, y)
            self.test_auc(preds, y)
            self.test_precision(preds, y)
            self.test_f1(preds, y)
            self.test_dice(preds, y)
            self.log("test_loss", loss, on_step=True, on_epoch=True, prog_bar=True)
            self.log("test_acc", self.test_acc, on_step=True, on_epoch=True)
            self.log("test_auc", self.test_auc, on_step=False, on_epoch=True)
            self.log(
                "test_precision", self.test_precision, on_step=False, on_epoch=True
            )
            self.log("test_f1", self.test_f1, on_step=False, on_epoch=True)
            self.log("test_dice", self.test_dice, on_step=False, on_epoch=True)
            return loss

        def validation_step(self, batch, batch_idx):
            # this is the validation loop
            x, y = batch
            x_hat = self.model(x)
            _, preds = torch.max(x_hat, 1)
            loss = criterion(x_hat, y)

            self.val_acc(preds, y)
            self.val_auc(preds, y)
            self.val_precision(preds, y)
            self.val_f1(preds, y)
            self.val_dice(preds, y)
            self.log("val_loss", loss, on_step=True, on_epoch=True, prog_bar=True)
            self.log("val_acc", self.val_acc, on_step=True, on_epoch=True)
            self.log("val_auc", self.val_auc, on_step=False, on_epoch=True)
            self.log("val_precision", self.val_precision, on_step=False, on_epoch=True)
            self.log("val_f1", self.val_f1, on_step=False, on_epoch=True)
            self.log("val_dice", self.val_dice, on_step=False, on_epoch=True)
            return loss

        def configure_optimizers(self):
            optimizer = torch.optim.SGD(
                self.parameters(), lr=0.01, momentum=0.9, weight_decay=5e-4
            )
            start_lr = 1e-3
            end_lr = 0.1
            lr_scheduler = {
                "scheduler": get_scheduler(optimizer, start_lr, end_lr, 2 * NUM_EPOCHS),
                "name": "my_logging_name",
            }
            return [optimizer], [lr_scheduler]

    listResNet = LitResNet(model)
    torch.set_float32_matmul_precision("high")

    tb_logger = pl_loggers.TensorBoardLogger(
        save_dir="./",
        name="reset_net_albumentations_clear_ml_lr=1e-3",
    )
    trainer = pl.Trainer(
        accelerator="gpu",
        max_epochs=NUM_EPOCHS,
        logger=tb_logger,
        default_root_dir="./ckpt",
        devices=1,
        callbacks=[TQDMProgressBar(refresh_rate=1)],
    )

    trainer.fit(
        model=listResNet, train_dataloaders=train_loader, val_dataloaders=valid_loader
    )
    trainer.test(model=listResNet, dataloaders=test_loader)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_id")
    parser.add_argument("--model_name")
    parser.add_argument("--project_name")
    parser.add_argument("--task_name")

    args = parser.parse_args()

    main(args.project_name, args.task_name, args.dataset_id, args.model_name)
