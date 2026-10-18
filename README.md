# پڕۆژەی ناسینەوەی وێنەی مرۆڤ و ئاژەڵ بە بەکارهێنانی ANN
## Artificial Neural Networks (Deep Res-MLP) & Computer Vision

ئەم پڕۆژەیە بە تەواوی تەرخانکراوە بۆ کۆرسی **Artificial Neural Networks (ANN)** بۆ ناسینەوە و پۆلێنکردنی وێنەی پێنج پۆلی سەرەکی:
1. 🧑 **مرۆڤ (Human)**
2. 🐶 **سەگ (Dog)**
3. 🐱 **پشیلە (Cat)**
4. 🐦 **باڵندە (Bird)**
5. 🐴 **ئەسپ (Horse)**

---

### 🧠 تەلارسازی مۆدێلەکە (Architecture):
* **جۆری تۆڕی دەماری:** Deep Residual Multi-Layer Perceptron (Res-MLP ANN)
* **ژمارەی چینە شاردراوەکان:** ٧ چینی قووڵ (7 Deep Hidden Layers)
* **کۆی پارامیتەرەکان:** نزیکەی ١٤.٩ بۆ ٥٢.٧ ملیۆن کێشی ڕاهێنراو
* **تەکنیکە سەرەکییەکان:** Skip Connections ($x + F(x)$), Layer Normalization, GELU Activation, Batch Normalization, and Dropout.
* **داتاسێت:** زیاتر لە ٣١,٨٥٠ وێنەی ڕاستەقینە

---

### 🚀 چۆنیەتی کارپێکردنی خێرای وێب ئەپەکە (How to Run):
ئاسانترین ڕێگا بۆ کارپێکردن:
1. دەست بنێ بە دوو-کلیک لەسەر فایلی:
   👉 **`run_app.bat`**
2. وێب ئەپەکە لە براوزەرەکەتدا دەکرێتەوە لە:
   `http://localhost:8501`

یان لە ڕێگەی تێرمیناڵەوە:
```bash
.\.venv\Scripts\streamlit.exe run app.py
```

---

### 📂 پێکهاتەی فایلەکانی پڕۆژە (Project Structure):
```
ai progect/
├── models/
│   ├── __init__.py
│   └── ann_mlp.py         # تەلارسازی پێشکەوتووی Deep Res-MLP ANN (٧ چینی شاردراوە)
├── dataset/
│   ├── train/             # وێنەکانی ڕاهێنان (٢٥,٤٧٦ وێنە)
│   └── test/              # وێنەکانی تاقیکردنەوە (٦,٣٧٤ وێنە)
├── saved_models/
│   └── ann_mlp_best.pth   # باشترین کێشە خەزنکراوەکانی مۆدێلی ANN
├── outputs/
│   ├── ann_mlp_training_curves.png   # هێڵکاری دادۆشینی هەڵە و Accuracy
│   ├── ann_mlp_confusion_matrix.png  # ماتریکسی هەڵەسەنگاندنی تاقیکردنەوە
│   ├── ann_mlp_report.json           # ڕاپۆرتی فەرمی (Precision, Recall, F1)
│   └── ann_mlp_metrics.json          # ژمارە وردەکانی هەموو خولەکان
├── samples/               # وێنەی نموونەیی بۆ تاقیکردنەوەی خێرا
├── app.py                 # وێب ئەپڵیکەیشنی کارلێککار بە Streamlit (وێنە + کامێرا)
├── train.py               # کۆدی فەرمی مەشقپێکردن و هەڵسەنگاندن
├── run_app.bat            # فایلی جێبەجێکردنی خێرا بە یەک کلیک
├── requirements.txt       # پاکێجە پێویستەکان
└── PROJECT_REPORT.md      # ڕاپۆرتی ئەکادیمی تەواو بۆ مامۆستا بە زمانی کوردی
```

---

### ⚙️ دووبارە ڕاهێنان (Retraining):
```bash
.\.venv\Scripts\python.exe train.py --model ann --epochs 12 --batch_size 64
```
