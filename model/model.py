import torch
import torch.nn as nn

from torchvision.models import resnet50, ResNet50_Weights

class ModelV1(nn.Module):
    def __init__(self):
        super(ModelV1, self).__init__()

        self.resnet = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
        self.fc_in_features = self.resnet.fc.in_features
        # self.resnet = torch.nn.Sequential(*(list(self.resnet.children())[:-1]))

        self.resnet = nn.Sequential(
            *(list(self.resnet.children())[:-2]),  # Keep until last convolutional layer
            nn.AdaptiveAvgPool2d((1, 1))
        )

        num_features = 256
        self.fc = nn.Sequential(
            nn.Linear(self.fc_in_features, num_features * 2),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(num_features * 2, num_features),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(num_features, 7),
        )

    def forward(self, x):
        x = self.resnet(x)
        x = x.view(x.size()[0], -1)
        x = self.fc(x)
        # sigmoid_part = torch.sigmoid(x[:, :2])
        sigmoid_part = torch.clamp(x[:, :2], min=0.0, max=1.0)
        softmax_part = torch.softmax(x[:, 2:], dim=1)
        return torch.cat([sigmoid_part, softmax_part], dim=1)


        # return self.fc(output).squeeze(-1)
