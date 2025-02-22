import time
import glob

import numpy as np
import torch
import cv2 as cv
from torch.utils.data import DataLoader
import matplotlib.pylab as plt


from dataset import TheDataset
from model import ModelV1

device = "cpu"


paths = [filepath for filepath in glob.glob("../data/new_data/*.jpg")]
paths.sort()
dataset_orig = TheDataset(paths[3300:], device=device)
dataset_aug = TheDataset(paths[3300:], device=device, augment=True)

dataloader_orig = DataLoader(dataset_orig, batch_size=1, shuffle=False)
dataloader_aug = DataLoader(dataset_aug, batch_size=1, shuffle=False)


for ((inputs_orig, _), (inputs_aug, _)) in zip(dataloader_orig, dataloader_aug):

    for image_orig, image_aug in zip(inputs_orig, inputs_aug):
        image_orig = image_orig.permute(1, 2, 0).cpu().numpy()
        image_aug = image_aug.permute(1, 2, 0).cpu().numpy()

        plt.subplot(121)
        plt.imshow(image_orig)
        plt.subplot(122)
        plt.imshow(image_aug)
        plt.show()


