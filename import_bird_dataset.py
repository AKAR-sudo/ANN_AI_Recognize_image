import os
import zipfile
import random

ARCHIVE_PATH = r"C:\Users\dell\Downloads\Compressed\archive_3.zip"
TRAIN_BIRD_DIR = os.path.join("dataset", "train", "bird")
TEST_BIRD_DIR = os.path.join("dataset", "test", "bird")

def import_bird_images():
    if not os.path.exists(ARCHIVE_PATH):
        print(f"Error: Archive not found at {ARCHIVE_PATH}")
        return

    os.makedirs(TRAIN_BIRD_DIR, exist_ok=True)
    os.makedirs(TEST_BIRD_DIR, exist_ok=True)

    # Clean previous initial placeholders
    for f in os.listdir(TRAIN_BIRD_DIR):
        os.remove(os.path.join(TRAIN_BIRD_DIR, f))
    for f in os.listdir(TEST_BIRD_DIR):
        os.remove(os.path.join(TEST_BIRD_DIR, f))

    print("Opening Bird ZIP archive...")
    with zipfile.ZipFile(ARCHIVE_PATH, 'r') as z:
        all_files = z.namelist()
        
        # Only take actual image files, ignore .txt annotation files
        image_candidates = [f for f in all_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        print(f"Found {len(image_candidates)} bird images in archive.")

        random.seed(42)
        random.shuffle(image_candidates)

        # 80% train, 20% test
        split_idx = int(len(image_candidates) * 0.8)
        selected_train = image_candidates[:split_idx]
        selected_test = image_candidates[split_idx:]

        print(f"Extracting {len(selected_train)} bird images to {TRAIN_BIRD_DIR}...")
        for idx, member in enumerate(selected_train):
            filename = f"bird_train_{idx+1}_{os.path.basename(member)}"
            dst = os.path.join(TRAIN_BIRD_DIR, filename)
            with z.open(member) as src_file, open(dst, 'wb') as dst_file:
                dst_file.write(src_file.read())

        print(f"Extracting {len(selected_test)} bird images to {TEST_BIRD_DIR}...")
        for idx, member in enumerate(selected_test):
            filename = f"bird_test_{idx+1}_{os.path.basename(member)}"
            dst = os.path.join(TEST_BIRD_DIR, filename)
            with z.open(member) as src_file, open(dst, 'wb') as dst_file:
                dst_file.write(src_file.read())

    train_count = len(os.listdir(TRAIN_BIRD_DIR))
    test_count = len(os.listdir(TEST_BIRD_DIR))

    print("\n--- Completed Bird Dataset Extraction ---")
    print(f"Train Birds: {train_count}")
    print(f"Test Birds:  {test_count}")
    print(f"Total Birds: {train_count + test_count}")

    # Update sample_bird.jpg in samples/
    samples_dir = "samples"
    os.makedirs(samples_dir, exist_ok=True)
    sample_bird_dest = os.path.join(samples_dir, "sample_bird.jpg")
    first_img = os.listdir(TRAIN_BIRD_DIR)[0]
    with open(os.path.join(TRAIN_BIRD_DIR, first_img), 'rb') as src, open(sample_bird_dest, 'wb') as dst:
        dst.write(src.read())
    print(f"Updated {sample_bird_dest} with a new bird sample.")

if __name__ == "__main__":
    import_bird_images()
