import time

import glob
import numpy as np
import matplotlib.pylab as plt
import cv2 as cv
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader

from dataset import TheDataset
from model import ModelV1

class MultiTaskLoss(nn.Module):
    def __init__(self):
        super().__init__()
        self.regression_loss = nn.BCEWithLogitsLoss()
        self.classification_loss = nn.CrossEntropyLoss()

    def forward(self, preds, targets):
        reg_preds, cls_preds = preds[:, :2], preds[:, 2:]
        reg_targets, cls_targets = targets[:, :2].float(), targets[:, 2:].float()  # Ensure correct types

        reg_loss = self.regression_loss(reg_preds, reg_targets)
        cls_loss = self.classification_loss(cls_preds, cls_targets)

        return reg_loss + cls_loss


DEBUG = False

device = "cuda"
epochs = 10000
batch_size = 16

if DEBUG:
    paths = [filepath for filepath in glob.glob("../data/new_data/*.jpg")]
else:
    paths = [filepath for filepath in glob.glob("new_data/*.jpg")]

paths.sort()

if DEBUG:
    train_dataset = TheDataset(paths[:300], device=device, augment=True)
    val_dataset = TheDataset(paths[300:400], device=device)
else:
    train_dataset = TheDataset(paths[:3300], device=device, augment=True)
    val_dataset = TheDataset(paths[3300:], device=device)

train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

model = ModelV1().to(device)

criterion = nn.MSELoss()  # For regression tasks
# criterion = nn.HuberLoss(delta=1.0)
# criterion = MultiTaskLoss()
# criterion = nn.BCELoss()
# criterion = nn.CrossEntropyLoss()

optimizer = optim.AdamW(model.parameters(), lr=0.0001)
# scheduler = optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.99)
scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=50)

train_losses = np.zeros(epochs)
val_losses = np.zeros(epochs)

best_mae = 1000

for epoch in range(epochs):
    model.train()
    for train_inputs, train_targets in train_dataloader:
        train_outputs = model(train_inputs)
        train_loss = criterion(train_outputs, train_targets)
        optimizer.zero_grad()
        train_loss.backward()
        optimizer.step()
        train_losses[epoch] += train_loss

    model.eval()
    errors = []
    for val_inputs, val_targets in val_dataloader:
        val_outputs = model(val_inputs)
        val_loss = criterion(val_outputs, val_targets)
        val_losses[epoch] += val_loss
        epoch_error = np.abs(val_targets.to("cpu").numpy() - val_outputs.detach().to("cpu").numpy())
        errors.append(epoch_error[:,:2])
    mae = np.concatenate(errors).mean()

    scheduler.step()

    if epoch % 1 == 0:
        print(
            f'Epoch [{epoch}/{epochs}], Training Loss: {train_losses[epoch]:.5f},  Validation Loss: {val_losses[epoch]:.5f}, "MAE: {mae:.3f}')

    if mae < best_mae and not DEBUG:
        torch.save(model.state_dict(), f"checkpoints/model_v1.pt")
        print("saving")
        best_mae = mae

plt.plot(train_losses, label="Training loss")
plt.plot(val_losses, label="Validation loss")
plt.legend()
plt.title(f"Best validation loss occur in epoch {val_losses.argmin()}")
plt.xlabel("Epoch index")
plt.ylabel("Loss [-]")
plt.yscale('log')
plt.show()