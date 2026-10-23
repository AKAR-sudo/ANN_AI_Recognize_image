import torch
import torch.nn as nn
from torchvision import models

class ResidualANNBlock(nn.Module):
    """
    Residual Block for Artificial Neural Network.
    Enables deep gradient flow using skip connections (Res-MLP structure).
    Solves vanishing gradients and allows the network to train much deeper.
    """
    def __init__(self, hidden_dim=512, bottleneck_dim=256, dropout=0.2):
        super(ResidualANNBlock, self).__init__()
        self.block = nn.Sequential(
            nn.Linear(hidden_dim, bottleneck_dim),
            nn.LayerNorm(bottleneck_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(bottleneck_dim, hidden_dim),
            nn.LayerNorm(hidden_dim)
        )
        self.act = nn.GELU()

    def forward(self, x):
        return self.act(x + self.block(x))

class ANNClassifier(nn.Module):
    """
    High-Accuracy Deep Representation Artificial Neural Network (Deep Res-MLP)
    Tailored for High Accuracy and Generalization on Computer Vision.

    Architecture Overview:
    ----------------------
    1. Visual Representation Layer:
       - Maps input image into 1280-dimensional feature embedding.
    
    2. Deep Res-MLP ANN Engine (7 Layers):
       - Hidden Layer 1: Linear(1280 -> 512) + LayerNorm + GELU + Dropout(0.3)
       - Hidden Layer 2 & 3: ResidualANNBlock(512 -> 256 -> 512) + Skip Connection -> GELU
       - Hidden Layer 4: Linear(512 -> 256) + BatchNorm1d + GELU + Dropout(0.2)
       - Hidden Layer 5: Linear(256 -> 128) + BatchNorm1d + GELU + Dropout(0.15)
       - Output Layer: Linear(128 -> num_classes)
    """
    def __init__(self, img_size=128, in_channels=3, num_classes=5, dropout_rate=0.25):
        super(ANNClassifier, self).__init__()
        self.img_size = img_size
        self.in_channels = in_channels
        self.num_classes = num_classes

        # Visual representation feature extractor
        backbone_model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
        self.feature_extractor = backbone_model.features
        for param in self.feature_extractor.parameters():
            param.requires_grad = False
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))

        # Deep Res-MLP ANN Classification Engine
        self.ann_engine = nn.Sequential(
            # Hidden Layer 1 (Projection)
            nn.Linear(1280, 512),
            nn.LayerNorm(512),
            nn.GELU(),
            nn.Dropout(0.3),

            # Hidden Layer 2 & 3 (Residual Res-MLP with Skip Connection)
            ResidualANNBlock(hidden_dim=512, bottleneck_dim=256, dropout=0.2),

            # Hidden Layer 4 (Compression)
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.GELU(),
            nn.Dropout(0.2),

            # Hidden Layer 5 (Bottleneck)
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.GELU(),
            nn.Dropout(0.15),

            # Output Layer
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        with torch.no_grad():
            features = self.avgpool(self.feature_extractor(x)).flatten(1)
        logits = self.ann_engine(features)
        return logits

    def count_parameters(self):
        """Returns total and trainable parameters."""
        total = sum(p.numel() for p in self.parameters())
        trainable = sum(p.numel() for p in self.parameters() if p.requires_grad)
        return {"total": total, "trainable": trainable}
