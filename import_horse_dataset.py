import os
import zipfile
import random
from PIL import Image
import io

ARCHIVE_PATH = r"C:\Users\dell\Downloads\Compressed\archive_4.zip"
TRAIN_HORSE_DIR = os.path.join("dataset", "train", "horse")
TEST_HORSE_DIR = os.path.join("dataset", "test", "horse")

def import_horse_images():
    if not os.path.exists(ARCHIVE_PATH):
        print(f"Error: Archive not found at {ARCHIVE_PATH}")
        return

    os.makedirs(TRAIN_HORSE_DIR, exist_ok=True)
    os.makedirs(TEST_HORSE_DIR, exist_ok=True)

    # Clean existing placeholders
    for f in os.listdir(TRAIN_HORSE_DIR):
        os.remove(os.path.join(TRAIN_HORSE_DIR, f))
    for f in os.listdir(TEST_HORSE_DIR):
        os.remove(os.path.join(TEST_HORSE_DIR, f))

    print("Opening Horse ZIP archive...")
    with zipfile.ZipFile(ARCHIVE_PATH, 'r') as z:
        all_files = z.namelist()
        image_candidates = [f for f in all_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        print(f"Found {len(image_candidates)} horse images in archive.")

        random.seed(42)
        random.shuffle(image_candidates)

        # 80% train, 20% test
        split_idx = int(len(image_candidates) * 0.8)
        selected_train = image_candidates[:split_idx]
        selected_test = image_candidates[split_idx:]

        print(f"Extracting {len(selected_train)} horse images to {TRAIN_HORSE_DIR}...")
        for idx, member in enumerate(selected_train):
            filename = f"horse_train_{idx+1}_{os.path.basename(member)}"
            dst = os.path.join(TRAIN_HORSE_DIR, filename)
            with z.open(member) as src_file, open(dst, 'wb') as dst_file:
                dst_file.write(src_file.read())

        print(f"Extracting {len(selected_test)} horse images to {TEST_HORSE_DIR}...")
        for idx, member in enumerate(selected_test):
            filename = f"horse_test_{idx+1}_{os.path.basename(member)}"
            dst = os.path.join(TEST_HORSE_DIR, filename)
            with z.open(member) as src_file, open(dst, 'wb') as dst_file:
                dst_file.write(src_file.read())

    train_count = len(os.listdir(TRAIN_HORSE_DIR))
    test_count = len(os.listdir(TEST_HORSE_DIR))

    print("\n--- Completed Horse Dataset Extraction ---")
    print(f"Train Horses: {train_count}")
    print(f"Test Horses:  {test_count}")
    print(f"Total Horses: {train_count + test_count}")

    # Update sample_horse.jpg in samples/
    samples_dir = "samples"
    os.makedirs(samples_dir, exist_ok=True)
    sample_horse_dest = os.path.join(samples_dir, "sample_horse.jpg")
    first_img = os.listdir(TRAIN_HORSE_DIR)[0]
    
    # Save as RGB JPEG for sample
    with Image.open(os.path.join(TRAIN_HORSE_DIR, first_img)) as img:
        img.convert('RGB').save(sample_horse_dest, 'JPEG')
    print(f"Updated {sample_horse_dest} with a new horse sample.")

if __name__ == "__main__":
    import_horse_images()
