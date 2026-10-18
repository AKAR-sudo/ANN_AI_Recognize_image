import torch
import torch.nn as nn

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
    State-of-the-Art Deep Artificial Neural Network (Deep Res-MLP)
    Tailored for High Accuracy and Generalization on Computer Vision.

    Architecture Overview:
    ----------------------
    1. Input Projection:
       - Flatten(Input: 3 x H x W)
       - Linear(input_dim -> 1024)
       - LayerNorm(1024)
       - GELU Activation
       - Dropout(0.25)
    
    2. Deep Residual Hidden Layers (Res-MLP Blocks):
       - Block 1: 1024 -> 512 -> 1024 + Skip Connection (x + F(x)) -> GELU
       - Block 2: 1024 -> 512 -> 1024 + Skip Connection (x + F(x)) -> GELU
    
    3. Compression & Regularization:
       - Linear(1024 -> 256)
       - BatchNorm1d(256)
       - GELU
       - Dropout(0.3)
    
    4. Representation Layer:
       - Linear(256 -> 64)
       - BatchNorm1d(64)
       - GELU
       - Dropout(0.15)
    
    5. Output Classification Layer:
       - Linear(64 -> num_classes)
    """
    def __init__(self, img_size=128, in_channels=3, num_classes=5, dropout_rate=0.25):
        super(ANNClassifier, self).__init__()
        self.img_size = img_size
        self.in_channels = in_channels
        self.input_dim = in_channels * img_size * img_size
        self.num_classes = num_classes

        self.flatten = nn.Flatten()

        # 1. Input Projection
        self.input_proj = nn.Sequential(
            nn.Linear(self.input_dim, 1024),
            nn.LayerNorm(1024),
            nn.GELU(),
            nn.Dropout(dropout_rate)
        )

        # 2. Residual Blocks
        self.res_block1 = ResidualANNBlock(hidden_dim=1024, bottleneck_dim=512, dropout=dropout_rate)
        self.res_block2 = ResidualANNBlock(hidden_dim=1024, bottleneck_dim=512, dropout=dropout_rate)

        # 3. Dense Classifier Head
        self.classifier_head = nn.Sequential(
            nn.Linear(1024, 256),
            nn.BatchNorm1d(256),
            nn.GELU(),
            nn.Dropout(dropout_rate + 0.05),

            nn.Linear(256, 64),
            nn.BatchNorm1d(64),
            nn.GELU(),
            nn.Dropout(0.15),

            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        flat_x = self.flatten(x)
        h = self.input_proj(flat_x)
        h = self.res_block1(h)
        h = self.res_block2(h)
        logits = self.classifier_head(h)
        return logits

    def count_parameters(self):
        """Returns total trainable and total parameters."""
        total = sum(p.numel() for p in self.parameters())
        trainable = sum(p.numel() for p in self.parameters() if p.requires_grad)
        return {"total": total, "trainable": trainable}
