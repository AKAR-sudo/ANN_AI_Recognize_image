import torch
import torch.nn as nn
from torchvision import models

class ResidualANNBlock(nn.Module):
    """
    Residual Block for Artificial Neural Network (Res-MLP).
    Enables deep gradient flow using skip connections to solve vanishing gradients.
    """
    def __init__(self, hidden_dim=512, bottleneck_dim=256, dropout=0.2):
        super(ResidualANNBlock, self).__init__()
        self.block = nn.Sequential(
            # [Formula 2 - Linear Layer]: z = x * W^T + b
            # (لێکدانی وێکتەری چووەژوورەوە لە ماتریکسی کێشەکان + لادان)
            nn.Linear(hidden_dim, bottleneck_dim),

            # [Formula 3 - Layer Normalization]: x_hat = ((x - mu) / sqrt(sigma^2 + eps)) * gamma + beta
            # (هاوسەنگکردنی نۆدەکانی ناو چینەکە بۆ تێکڕای 0 و بڵاوبوونەوەی 1)
            nn.LayerNorm(bottleneck_dim),

            # [Formula 4 - GELU Activation]: GELU(x) = x * P(X <= x), X ~ N(0, 1)
            # (ناهێڵییەتی بە چەماوەیەکی نەرم؛ چارەسەری کێشەی مردنی نۆدەکان - Dying ReLU)
            nn.GELU(),

            # Regularization: randomly turns off 20% of neurons during training to prevent Overfitting
            nn.Dropout(dropout),

            nn.Linear(bottleneck_dim, hidden_dim),
            nn.LayerNorm(hidden_dim)
        )
        self.act = nn.GELU()

    def forward(self, x):
        # [Formula 5 - Residual Skip Connection]: y = GELU(x + F(x, W))
        # [Formula 6 - Backprop Gradient Proof]:  dL/dx = (dL/dy) * (I + dF/dx)
        # (بوونی ماتریکسی یەکە I ڕێگری دەکات گرادیێنت ببێتە سفر - چارەسەری Vanishing Gradient)
        return self.act(x + self.block(x))

class ANNClassifier(nn.Module):
    """
    High-Accuracy Deep Representation Artificial Neural Network (Deep Res-MLP)
    Tailored for High Accuracy and Generalization on 5-Class Computer Vision.

    Architecture Overview (7 Node Layers / 6 Trainable nn.Linear Weight Matrices):
    ------------------------------------------------------------------------------
    Stage 1 - Visual Semantic Feature Projection:
       - Maps 128x128x3 RGB image into a 1,280-D latent semantic vector (Layer 1: Input).

    Stage 2 - Deep Res-MLP ANN Classification Engine:
       - Layer 1 (Input):    1,280-D Semantic Latent Vector
       - Layer 2 (Hidden 1): Linear(1280 -> 512) + LayerNorm + GELU + Dropout(0.3)
       - Layer 3 (Hidden 2): ResidualANNBlock Down: Linear(512 -> 256) + LayerNorm + GELU
       - Layer 4 (Hidden 3): ResidualANNBlock Up:   Linear(256 -> 512) + Skip (x + F(x)) -> GELU
       - Layer 5 (Hidden 4): Linear(512 -> 256) + BatchNorm1d + GELU + Dropout(0.2)
       - Layer 6 (Hidden 5): Linear(256 -> 128) + BatchNorm1d + GELU + Dropout(0.15)
       - Layer 7 (Output):   Linear(128 -> 5 Classes) -> Raw Classification Logits
    """
    def __init__(self, img_size=128, in_channels=3, num_classes=5, dropout_rate=0.25):
        super(ANNClassifier, self).__init__()
        self.img_size = img_size
        self.in_channels = in_channels
        self.num_classes = num_classes

        # Stage 1: Frozen Visual Representation Feature Extractor -> 1,280-D Semantic Vector
        # (دەرهێنانی وێکتەری ١,٢٨٠ ڕەهەندی مانایی؛ کێشەکانی سڕکراون requires_grad=False)
        backbone_model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
        self.feature_extractor = backbone_model.features
        for param in self.feature_extractor.parameters():
            param.requires_grad = False
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))

        # Stage 2: Deep Res-MLP ANN Classification Engine (100% Trainable)
        self.ann_engine = nn.Sequential(
            # Hidden Layer 1 (Projection: 1280 -> 512)
            # [Formula 2]: z = x * W^T + b
            nn.Linear(1280, 512),
            # [Formula 3]: LayerNorm -> x_hat = ((x - mu) / sqrt(sigma^2 + eps)) * gamma + beta
            nn.LayerNorm(512),
            # [Formula 4]: GELU(x) = x * P(X <= x)  (Non-Linearity without Dying ReLU)
            nn.GELU(),
            # Dropout(0.3): turns off 30% of neurons during training only to prevent Overfitting
            nn.Dropout(0.3),

            # Hidden Layers 2 & 3 (Residual Bottleneck Block: 512 -> 256 -> 512 + Skip Connection)
            # [Formula 5 & 6]: y = GELU(x + F(x, W))  |  dL/dx = (dL/dy) * (I + dF/dx)
            ResidualANNBlock(hidden_dim=512, bottleneck_dim=256, dropout=0.2),

            # Hidden Layer 4 (Compression: 512 -> 256)
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.GELU(),
            nn.Dropout(0.2),

            # Hidden Layer 5 (Bottleneck: 256 -> 128)
            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.GELU(),
            nn.Dropout(0.15),

            # Output Layer (Multi-Class Classifier: 128 -> 5 Logits for [bird, cat, dog, horse, human])
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        # Stage 1: Raw Image Tensor [B, 3, 128, 128] -> 1,280-D Semantic Latent Vector [B, 1280]
        with torch.no_grad():
            features = self.avgpool(self.feature_extractor(x)).flatten(1)
        # Stage 2: Deep Res-MLP Engine [B, 1280] -> 5 Raw Class Logits [B, 5]
        logits = self.ann_engine(features)
        return logits

    def count_parameters(self):
        """Returns total and trainable parameters."""
        total = sum(p.numel() for p in self.parameters())
        trainable = sum(p.numel() for p in self.parameters() if p.requires_grad)
        return {"total": total, "trainable": trainable}
