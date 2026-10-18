import os
import zipfile
import random

ARCHIVE_PATH = r"C:\Users\dell\Downloads\Compressed\archive_2.zip"
TRAIN_CAT_DIR = os.path.join("dataset", "train", "cat")
TEST_CAT_DIR = os.path.join("dataset", "test", "cat")

def import_cat_images(target_train=8000, target_test=2000):
    if not os.path.exists(ARCHIVE_PATH):
        print(f"Error: Archive not found at {ARCHIVE_PATH}")
        return

    os.makedirs(TRAIN_CAT_DIR, exist_ok=True)
    os.makedirs(TEST_CAT_DIR, exist_ok=True)

    print("Opening Cat ZIP archive...")
    with zipfile.ZipFile(ARCHIVE_PATH, 'r') as z:
        all_files = z.namelist()
        
        # Only take actual image files, ignore .cat annotation files
        image_candidates = [f for f in all_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        print(f"Found {len(image_candidates)} cat images in archive.")

        random.seed(42)
        random.shuffle(image_candidates)

        selected_train = image_candidates[:target_train]
        selected_test = image_candidates[target_train:target_train + target_test]

        print(f"Extracting {len(selected_train)} cat images to {TRAIN_CAT_DIR}...")
        for idx, member in enumerate(selected_train):
            filename = f"cat_train_{idx+1}_{os.path.basename(member)}"
            dst = os.path.join(TRAIN_CAT_DIR, filename)
            if not os.path.exists(dst):
                with z.open(member) as src_file, open(dst, 'wb') as dst_file:
                    dst_file.write(src_file.read())
            if (idx + 1) % 2000 == 0:
                print(f"  Extracted {idx + 1}/{len(selected_train)} train cat images...")

        print(f"Extracting {len(selected_test)} cat images to {TEST_CAT_DIR}...")
        for idx, member in enumerate(selected_test):
            filename = f"cat_test_{idx+1}_{os.path.basename(member)}"
            dst = os.path.join(TEST_CAT_DIR, filename)
            if not os.path.exists(dst):
                with z.open(member) as src_file, open(dst, 'wb') as dst_file:
                    dst_file.write(src_file.read())
            if (idx + 1) % 1000 == 0:
                print(f"  Extracted {idx + 1}/{len(selected_test)} test cat images...")

    train_count = len(os.listdir(TRAIN_CAT_DIR))
    test_count = len(os.listdir(TEST_CAT_DIR))

    print("\n--- Completed Cat Dataset Extraction ---")
    print(f"Train Cats: {train_count}")
    print(f"Test Cats:  {test_count}")
    print(f"Total Cats: {train_count + test_count}")

    # Update sample_cat.jpg in samples/
    samples_dir = "samples"
    os.makedirs(samples_dir, exist_ok=True)
    sample_cat_dest = os.path.join(samples_dir, "sample_cat.jpg")
    first_img = os.listdir(TRAIN_CAT_DIR)[0]
    with open(os.path.join(TRAIN_CAT_DIR, first_img), 'rb') as src, open(sample_cat_dest, 'wb') as dst:
        dst.write(src.read())
    print(f"Updated {sample_cat_dest} with a new cat sample.")

if __name__ == "__main__":
    import_cat_images(target_train=8000, target_test=2000)
