import os
import shutil
import random

SOURCE_DIR = r"C:\Users\dell\Desktop\images\Images"
TRAIN_DOG_DIR = os.path.join("dataset", "train", "dog")
TEST_DOG_DIR = os.path.join("dataset", "test", "dog")

def import_10k_dogs(target_train=8000, target_test=2000):
    if not os.path.exists(SOURCE_DIR):
        print(f"Error: Source directory {SOURCE_DIR} does not exist.")
        return

    os.makedirs(TRAIN_DOG_DIR, exist_ok=True)
    os.makedirs(TEST_DOG_DIR, exist_ok=True)

    # Collect all image paths across all breed subfolders
    all_images = []
    for root, dirs, files in os.walk(SOURCE_DIR):
        for f in files:
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                all_images.append(os.path.join(root, f))

    total_available = len(all_images)
    print(f"Total dog images found in source: {total_available}")

    random.seed(42)
    random.shuffle(all_images)

    # Pick 8,000 for train and 2,000 for test
    train_pool = all_images[:target_train]
    test_pool = all_images[target_train:target_train + target_test]

    print(f"Copying {len(train_pool)} images to {TRAIN_DOG_DIR}...")
    for idx, src in enumerate(train_pool):
        filename = f"dog_train_{idx+1}_{os.path.basename(src)}"
        dst = os.path.join(TRAIN_DOG_DIR, filename)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
        if (idx + 1) % 2000 == 0:
            print(f"  Copied {idx + 1}/{len(train_pool)} train images...")

    print(f"Copying {len(test_pool)} images to {TEST_DOG_DIR}...")
    for idx, src in enumerate(test_pool):
        filename = f"dog_test_{idx+1}_{os.path.basename(src)}"
        dst = os.path.join(TEST_DOG_DIR, filename)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
        if (idx + 1) % 1000 == 0:
            print(f"  Copied {idx + 1}/{len(test_pool)} test images...")

    train_final = len(os.listdir(TRAIN_DOG_DIR))
    test_final = len(os.listdir(TEST_DOG_DIR))

    print("\n--- Completed Dog Dataset Import ---")
    print(f"Train Dogs Count: {train_final}")
    print(f"Test Dogs Count:  {test_final}")
    print(f"Total Dog Images: {train_final + test_final}")

if __name__ == "__main__":
    import_10k_dogs(target_train=8000, target_test=2000)
