import time
import glob

import numpy as np
import torch
import cv2 as cv
from torch.utils.data import DataLoader
import matplotlib.pylab as plt


from dataset import TheDataset
from model import ModelV1


device = "cuda"

model = ModelV1()
model_data = "checkpoints/model_v1.pt"
model.load_state_dict(torch.load(model_data, weights_only=True))
model.to(device)

paths = [filepath for filepath in glob.glob("../data/new_data/*.jpg")]
paths.sort()
val_dataset = TheDataset(paths[3300:], device=device, augment=True)

dataloader = DataLoader(val_dataset, batch_size=1, shuffle=False)

model.eval()

wi = 7

for val_inputs, val_targets in dataloader:
    t0 = time.time()
    val_outputs = model(val_inputs)
    t_end = time.time() - t0
    print(f"Estimated time: {t_end}")

    for image, target, output in zip(val_inputs, val_targets, val_outputs):
        image = image.permute(1, 2, 0).cpu().numpy()

        ts = target.cpu().numpy()
        os = output.detach().cpu().numpy()

        t1, t2 = (ts[0:2] * 479)
        o1, o2 = (os[0:2] * 479)

        print(ts[2:], os[2:])

        image[0:int(t1), 0:wi] = (0, 1, 0)
        image[480-int(t2):-1, wi:2*wi] = (0, 1, 0)
        image[int(t1)] = (0, 1, 0)
        image[479-int(t2)] = (0, 1, 0)

        image[0:int(o1), -wi:] = (0, 0, 1)
        image[480-int(o2):-1, -2*wi:-wi] = (0, 0, 1)
        image[int(o1)] = (0, 0, 1)
        image[479-int(o2)] = (0, 0, 1)

        plt.imshow(image)
        plt.show()


