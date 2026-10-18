import os
import zipfile
import random

ARCHIVE_PATH = r"C:\Users\dell\Downloads\Compressed\archive.zip"
TRAIN_HUMAN_DIR = os.path.join("dataset", "train", "human")
TEST_HUMAN_DIR = os.path.join("dataset", "test", "human")

def import_human_images(target_train=8000, target_test=2000):
    if not os.path.exists(ARCHIVE_PATH):
        print(f"Error: Archive not found at {ARCHIVE_PATH}")
        return

    os.makedirs(TRAIN_HUMAN_DIR, exist_ok=True)
    os.makedirs(TEST_HUMAN_DIR, exist_ok=True)

    print("Opening ZIP archive...")
    with zipfile.ZipFile(ARCHIVE_PATH, 'r') as z:
        all_files = z.namelist()
        
        train_candidates = [f for f in all_files if f.startswith("images/train/") and f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        val_candidates = [f for f in all_files if f.startswith("images/val/") and f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        print(f"Found {len(train_candidates)} train candidates and {len(val_candidates)} validation candidates in archive.")

        random.seed(42)
        random.shuffle(train_candidates)
        random.shuffle(val_candidates)

        selected_train = train_candidates[:target_train]
        selected_test = val_candidates[:target_test]

        print(f"Extracting {len(selected_train)} human images to {TRAIN_HUMAN_DIR}...")
        for idx, member in enumerate(selected_train):
            filename = f"human_train_{idx+1}_{os.path.basename(member)}"
            dst = os.path.join(TRAIN_HUMAN_DIR, filename)
            if not os.path.exists(dst):
                with z.open(member) as src_file, open(dst, 'wb') as dst_file:
                    dst_file.write(src_file.read())
            if (idx + 1) % 2000 == 0:
                print(f"  Extracted {idx + 1}/{len(selected_train)} train human images...")

        print(f"Extracting {len(selected_test)} human images to {TEST_HUMAN_DIR}...")
        for idx, member in enumerate(selected_test):
            filename = f"human_test_{idx+1}_{os.path.basename(member)}"
            dst = os.path.join(TEST_HUMAN_DIR, filename)
            if not os.path.exists(dst):
                with z.open(member) as src_file, open(dst, 'wb') as dst_file:
                    dst_file.write(src_file.read())
            if (idx + 1) % 1000 == 0:
                print(f"  Extracted {idx + 1}/{len(selected_test)} test human images...")

    train_count = len(os.listdir(TRAIN_HUMAN_DIR))
    test_count = len(os.listdir(TEST_HUMAN_DIR))

    print("\n--- Completed Human Dataset Extraction ---")
    print(f"Train Humans: {train_count}")
    print(f"Test Humans:  {test_count}")
    print(f"Total Humans: {train_count + test_count}")

    # Update sample_human.jpg in samples/
    samples_dir = "samples"
    os.makedirs(samples_dir, exist_ok=True)
    sample_human_dest = os.path.join(samples_dir, "sample_human.jpg")
    first_img = os.listdir(TRAIN_HUMAN_DIR)[0]
    with open(os.path.join(TRAIN_HUMAN_DIR, first_img), 'rb') as src, open(sample_human_dest, 'wb') as dst:
        dst.write(src.read())
    print(f"Updated {sample_human_dest} with a new human sample.")

if __name__ == "__main__":
    import_human_images(target_train=8000, target_test=2000)
