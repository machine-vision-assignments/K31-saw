import glob
import numpy as np
import matplotlib.pylab as plt
import cv2 as cv
import torch
from torchvision import transforms
from torch.utils.data import Dataset
import albumentations as A
from albumentations.pytorch import ToTensorV2
from albumentations.core.composition import OneOf


class TheDataset(Dataset):

    def __init__(self, paths, device="cpu", augment=False):
        self._augment = augment
        self._transform = transforms.Compose([
            transforms.ToTensor(),
        ])
        self._augmentation = A.Compose([
            # A.HorizontalFlip(p=0.4),  # Random horizontal flip
            A.RandomBrightnessContrast(p=0.2),  # Random brightness/contrast
            A.HueSaturationValue(hue_shift_limit=15,
                                 sat_shift_limit=15,
                                 val_shift_limit=15,
                                 p=0.5),  # Adjust hue, saturation, and value
            A.OneOf([
                A.GaussNoise(p=0.5),  # Add Gaussian noise
                A.MotionBlur(p=0.5),  # Apply motion blur
            ], p=0.2),
        ])

        self._device = device
        self._height = 480
        self.inputs = [self._load_image(img_path) for img_path in paths]
        self.targets = [self._load_target(img_path) for img_path in paths]

    def _load_image(self, path):
        img = cv.imread(path, cv.IMREAD_COLOR)
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        return img

    def _load_target(self, path):
        y1, y2, st = path.split("-")[-2].split("_")
        one_hot_tensor = torch.tensor(np.eye(5)[int(st)], dtype=torch.float32)
        coord_tensor = torch.tensor([float(y1) / self._height, float(y2) / self._height]).float()
        return torch.cat((coord_tensor, one_hot_tensor))

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        img = self.inputs[idx]
        if self._augment:
            img = self._augmentation(image=img.copy())["image"]
        image = self._transform(img)
        return image.to(self._device), self.targets[idx].to(self._device)

if __name__ == "__main__":

    paths = [filepath for filepath in glob.glob("../data/dataset/train/images/*.jpg")]
    dataset = TheDataset(paths[:100])

