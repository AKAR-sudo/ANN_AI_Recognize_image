import os
import sys
import urllib.request
from PIL import Image

CLASSES = ["human", "dog", "cat", "bird", "horse"]

# Curated high quality public domain / open sample images
SAMPLE_URLS = {
    "human": [
        "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=80",
        "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&q=80",
        "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&q=80",
        "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&q=80",
        "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=400&q=80",
    ],
    "dog": [
        "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=400&q=80",
        "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400&q=80",
        "https://images.unsplash.com/photo-1517849845537-4d257902454a?w=400&q=80",
        "https://images.unsplash.com/photo-1561037404-61cd46aa615b?w=400&q=80",
        "https://images.unsplash.com/photo-1537151625747-768eb6cf92b2?w=400&q=80",
    ],
    "cat": [
        "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=400&q=80",
        "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=400&q=80",
        "https://images.unsplash.com/photo-1495360010541-f48722b34f7d?w=400&q=80",
        "https://images.unsplash.com/photo-1533738363-b7f9aef128ce?w=400&q=80",
        "https://images.unsplash.com/photo-1518791841217-8f162f1e1131?w=400&q=80",
    ],
    "bird": [
        "https://images.unsplash.com/photo-1444464666168-49d633b86797?w=400&q=80",
        "https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=400&q=80",
        "https://images.unsplash.com/photo-1522926193341-e9ffd686c60f?w=400&q=80",
        "https://images.unsplash.com/photo-1452570053594-1b985d6ea890?w=400&q=80",
        "https://images.unsplash.com/photo-1516606449221-5c45e54d3701?w=400&q=80",
    ],
    "horse": [
        "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?w=400&q=80",
        "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=400&q=80",
        "https://images.unsplash.com/photo-1558788353-f76d92427f16?w=400&q=80",
        "https://images.unsplash.com/photo-1598974357801-cbca100e65d3?w=400&q=80",
        "https://images.unsplash.com/photo-1566251037378-5e04e3bec343?w=400&q=80",
    ]
}

def setup_dataset():
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for cls in CLASSES:
        train_dir = os.path.join("dataset", "train", cls)
        test_dir = os.path.join("dataset", "test", cls)
        samples_dir = "samples"
        os.makedirs(train_dir, exist_ok=True)
        os.makedirs(test_dir, exist_ok=True)
        os.makedirs(samples_dir, exist_ok=True)

        urls = SAMPLE_URLS.get(cls, [])
        for idx, url in enumerate(urls):
            filename = f"{cls}_{idx+1}.jpg"
            dest = os.path.join(train_dir if idx < 3 else test_dir, filename)
            
            # Also save one sample in samples/ for the UI demo
            sample_dest = os.path.join(samples_dir, f"sample_{cls}.jpg")

            if not os.path.exists(dest):
                try:
                    req = urllib.request.Request(url, headers=headers)
                    with urllib.request.urlopen(req, timeout=10) as response, open(dest, 'wb') as out_file:
                        out_file.write(response.read())
                    print(f"Downloaded: {dest}")
                except Exception as e:
                    print(f"Could not download {url}: {e}")
            
            # Copy first image of each class to samples/
            if idx == 0 and os.path.exists(dest) and not os.path.exists(sample_dest):
                with open(dest, 'rb') as src, open(sample_dest, 'wb') as dst:
                    dst.write(src.read())

    print("\nDataset preparation completed successfully!")

if __name__ == "__main__":
    setup_dataset()
