import os
import argparse
import json
import time
import random
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np

from models import ANNClassifier

def get_data_loaders(data_dir="dataset", img_size=128, batch_size=64, max_train_per_class=600, max_test_per_class=150):
    train_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.ColorJitter(brightness=0.15, contrast=0.15),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    test_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    train_path = os.path.join(data_dir, "train")
    test_path = os.path.join(data_dir, "test")

    full_train = datasets.ImageFolder(train_path, transform=train_transform)
    full_test = datasets.ImageFolder(test_path, transform=test_transform)

    random.seed(42)

    # Subsetting for perfect class balance and lightning-fast training
    if max_train_per_class is not None:
        train_indices_by_class = {i: [] for i in range(len(full_train.classes))}
        for idx, (_, label) in enumerate(full_train.samples):
            train_indices_by_class[label].append(idx)

        selected_train = []
        for label, indices in train_indices_by_class.items():
            random.shuffle(indices)
            selected_train.extend(indices[:max_train_per_class])
        train_dataset = Subset(full_train, selected_train)
    else:
        train_dataset = full_train

    if max_test_per_class is not None:
        test_indices_by_class = {i: [] for i in range(len(full_test.classes))}
        for idx, (_, label) in enumerate(full_test.samples):
            test_indices_by_class[label].append(idx)

        selected_test = []
        for label, indices in test_indices_by_class.items():
            random.shuffle(indices)
            selected_test.extend(indices[:max_test_per_class])
        test_dataset = Subset(full_test, selected_test)
    else:
        test_dataset = full_test

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)

    return train_loader, test_loader, full_train.classes

def train_model(model_type="ann", epochs=10, batch_size=64, lr=0.0015, img_size=128, max_per_class=600):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type == "cpu":
        torch.set_num_threads(os.cpu_count() or 4)
    print(f"Using device: {device} (threads: {torch.get_num_threads()})", flush=True)

    train_loader, test_loader, class_names = get_data_loaders(
        "dataset", img_size=img_size, batch_size=batch_size,
        max_train_per_class=max_per_class, max_test_per_class=150
    )
    num_classes = len(class_names)
    print(f"Classes ({num_classes}): {class_names}", flush=True)

    model = ANNClassifier(img_size=img_size, num_classes=num_classes)
    model_name = "ann_mlp"
    model = model.to(device)

    # Calculate balanced class weights
    class_counts = [0] * num_classes
    if hasattr(train_loader.dataset, 'samples'):
        for _, label in train_loader.dataset.samples:
            class_counts[label] += 1
    else:
        for idx in train_loader.dataset.indices:
            _, label = train_loader.dataset.dataset.samples[idx]
            class_counts[label] += 1

    total_samples = sum(class_counts)
    class_weights = [total_samples / (num_classes * max(1, count)) for count in class_counts]
    class_weights_tensor = torch.tensor(class_weights, dtype=torch.float).to(device)
    print(f"Sample distribution for training: {dict(zip(class_names, class_counts))}", flush=True)
    print(f"Total training images: {total_samples} | Total test images: {len(test_loader.dataset)}", flush=True)

    # Optimize ANN Engine weights
    criterion = nn.CrossEntropyLoss(weight=class_weights_tensor, label_smoothing=0.05)
    optimizer = torch.optim.AdamW(model.ann_engine.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-5)

    history = {
        "train_loss": [],
        "train_acc": [],
        "val_loss": [],
        "val_acc": []
    }

    best_val_acc = 0.0
    os.makedirs("saved_models", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    best_weights_path = os.path.join("saved_models", f"{model_name}_best.pth")

    print(f"\n--- Starting Training for {model_name.upper()} ({epochs} Epochs) ---", flush=True)
    start_time = time.time()

    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        correct_train = 0
        total_train = 0
        total_batches = len(train_loader)

        for batch_idx, (images, labels) in enumerate(train_loader, 1):
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()

            torch.nn.utils.clip_grad_norm_(model.ann_engine.parameters(), max_norm=1.0)
            optimizer.step()

            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            correct_train += torch.sum(preds == labels.data).item()
            total_train += labels.size(0)

            if batch_idx % 10 == 0 or batch_idx == total_batches:
                curr_acc = (correct_train / total_train) * 100.0
                curr_loss = running_loss / total_train
                print(f"  Epoch [{epoch:02d}/{epochs:02d}] Step [{batch_idx:02d}/{total_batches:02d}] "
                      f"Loss: {curr_loss:.4f} | Train Acc: {curr_acc:.1f}%", flush=True)

        scheduler.step()
        epoch_train_loss = running_loss / total_train
        epoch_train_acc = (correct_train / total_train) * 100.0

        # Validation Phase
        model.eval()
        running_val_loss = 0.0
        correct_val = 0
        total_val = 0

        with torch.no_grad():
            for images, labels in test_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)

                running_val_loss += loss.item() * images.size(0)
                _, preds = torch.max(outputs, 1)
                correct_val += torch.sum(preds == labels.data).item()
                total_val += labels.size(0)

        epoch_val_loss = running_val_loss / total_val
        epoch_val_acc = (correct_val / total_val) * 100.0

        history["train_loss"].append(epoch_train_loss)
        history["train_acc"].append(epoch_train_acc)
        history["val_loss"].append(epoch_val_loss)
        history["val_acc"].append(epoch_val_acc)

        print(f"Epoch [{epoch:02d}/{epochs:02d}] "
              f"Train Loss: {epoch_train_loss:.4f} | Train Acc: {epoch_train_acc:.1f}% | "
              f"Val Loss: {epoch_val_loss:.4f} | Val Acc: {epoch_val_acc:.1f}%", flush=True)

        # Save best weights
        if epoch_val_acc >= best_val_acc:
            best_val_acc = epoch_val_acc
            torch.save({
                "model_state_dict": model.state_dict(),
                "class_names": class_names,
                "img_size": img_size,
                "model_type": model_type,
                "val_acc": best_val_acc
            }, best_weights_path)

    elapsed = time.time() - start_time
    print(f"\nTraining completed in {elapsed:.1f}s. Best Val Accuracy: {best_val_acc:.2f}%", flush=True)
    print(f"Best model weights saved to: {best_weights_path}", flush=True)

    with open(os.path.join("outputs", f"{model_name}_metrics.json"), "w") as f:
        json.dump(history, f, indent=4)

    plot_training_curves(history, model_name)
    evaluate_model(model, test_loader, class_names, device, model_name)

    return model, history

def plot_training_curves(history, model_name):
    epochs_range = range(1, len(history["train_loss"]) + 1)
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, history["train_loss"], 'b-o', label='Train Loss')
    plt.plot(epochs_range, history["val_loss"], 'r-s', label='Val Loss')
    plt.title(f"{model_name.upper()} - Loss Curve", fontsize=12, fontweight='bold')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, history["train_acc"], 'b-o', label='Train Accuracy')
    plt.plot(epochs_range, history["val_acc"], 'g-s', label='Val Accuracy')
    plt.title(f"{model_name.upper()} - Accuracy Curve", fontsize=12, fontweight='bold')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    chart_path = os.path.join("outputs", f"{model_name}_training_curves.png")
    plt.savefig(chart_path, dpi=200)
    plt.close()
    print(f"Saved training curves to: {chart_path}", flush=True)

def evaluate_model(model, test_loader, class_names, device, model_name):
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            outputs = model(images)
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.numpy())

    cm = confusion_matrix(all_labels, all_preds)
    report = classification_report(all_labels, all_preds, target_names=class_names, output_dict=True)

    print("\nClassification Report:", flush=True)
    print(classification_report(all_labels, all_preds, target_names=class_names), flush=True)

    with open(os.path.join("outputs", f"{model_name}_report.json"), "w") as f:
        json.dump(report, f, indent=4)

    plt.figure(figsize=(7, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names)
    plt.title(f"{model_name.upper()} - Confusion Matrix", fontsize=13, fontweight='bold')
    plt.xlabel("Predicted Class")
    plt.ylabel("Actual True Class")
    plt.tight_layout()

    cm_path = os.path.join("outputs", f"{model_name}_confusion_matrix.png")
    plt.savefig(cm_path, dpi=200)
    plt.close()
    print(f"Saved Confusion Matrix to: {cm_path}", flush=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train ANN model for image recognition.")
    parser.add_argument("--model", type=str, default="ann", choices=["ann"],
                        help="Model architecture: 'ann' (Deep Res-MLP)")
    parser.add_argument("--epochs", type=int, default=10, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=64, help="Batch size")
    parser.add_argument("--lr", type=float, default=0.0015, help="Learning rate")
    parser.add_argument("--img_size", type=int, default=128, help="Input image dimension (default: 128)")
    parser.add_argument("--max_per_class", type=int, default=600, help="Max training samples per class for balance")

    args = parser.parse_args()
    train_model(
        model_type=args.model, epochs=args.epochs, batch_size=args.batch_size,
        lr=args.lr, img_size=args.img_size, max_per_class=args.max_per_class
    )
