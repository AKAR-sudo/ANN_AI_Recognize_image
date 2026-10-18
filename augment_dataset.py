import os
import random
from PIL import Image, ImageEnhance, ImageFilter

CLASSES = ["human", "dog", "cat", "bird", "horse"]

def augment_image(img):
    """Generate an augmented version of an image."""
    img = img.copy()
    
    # Random horizontal flip
    if random.random() > 0.5:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        
    # Random slight rotation (-15 to 15 degrees)
    angle = random.uniform(-15, 15)
    img = img.rotate(angle, resample=Image.BICUBIC)
    
    # Random brightness variation
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(random.uniform(0.8, 1.2))
    
    # Random contrast variation
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(random.uniform(0.85, 1.25))
    
    # Slight color saturation variation
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(random.uniform(0.8, 1.2))

    return img

def expand_dataset(target_train_per_class=30, target_test_per_class=10):
    for cls in CLASSES:
        train_dir = os.path.join("dataset", "train", cls)
        test_dir = os.path.join("dataset", "test", cls)

        train_files = [f for f in os.listdir(train_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        test_files = [f for f in os.listdir(test_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        if not train_files:
            continue

        # Expand train set
        current_count = len(train_files)
        i = 1
        while current_count < target_train_per_class:
            base_file = random.choice(train_files)
            base_path = os.path.join(train_dir, base_file)
            with Image.open(base_path) as img:
                img_rgb = img.convert('RGB')
                aug_img = augment_image(img_rgb)
                out_path = os.path.join(train_dir, f"{cls}_aug_{i}.jpg")
                aug_img.save(out_path, quality=90)
                current_count += 1
                i += 1

        # Expand test set
        base_pool = test_files if test_files else train_files
        current_test_count = len(test_files)
        j = 1
        while current_test_count < target_test_per_class:
            base_file = random.choice(base_pool)
            base_path = os.path.join(test_dir if base_file in test_files else train_dir, base_file)
            with Image.open(base_path) as img:
                img_rgb = img.convert('RGB')
                aug_img = augment_image(img_rgb)
                out_path = os.path.join(test_dir, f"{cls}_test_aug_{j}.jpg")
                aug_img.save(out_path, quality=90)
                current_test_count += 1
                j += 1

        print(f"Class '{cls}': {current_count} train images, {current_test_count} test images.")

if __name__ == "__main__":
    expand_dataset()
