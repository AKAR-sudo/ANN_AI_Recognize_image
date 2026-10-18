import os
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np

from models import ANNClassifier

# Page Configuration
st.set_page_config(
    page_title="ANN Computer Vision - Image Recognition",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border: 1px solid #BFDBFE;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    .prediction-badge {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1D4ED8;
    }
    .kurdish-badge {
        font-size: 1.4rem;
        color: #047857;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

CLASS_NAMES = ['bird', 'cat', 'dog', 'horse', 'human']
KURDISH_NAMES = {
    'human': 'مرۆڤ (Human)',
    'dog': 'سەگ (Dog)',
    'cat': 'پشیلە (Cat)',
    'bird': 'باڵندە (Bird)',
    'horse': 'ئەسپ (Horse)'
}
CLASS_ICONS = {
    'human': '🧑',
    'dog': '🐶',
    'cat': '🐱',
    'bird': '🐦',
    'horse': '🐴'
}

DEVICE = torch.device("cpu")

@st.cache_resource
def load_ann_model():
    """Load trained Deep Res-MLP ANN model."""
    ann_path = os.path.join("saved_models", "ann_mlp_best.pth")
    ann_size = 64
    if os.path.exists(ann_path):
        checkpoint = torch.load(ann_path, map_location=DEVICE)
        ann_size = checkpoint.get("img_size", 64)
        model = ANNClassifier(img_size=ann_size, num_classes=len(CLASS_NAMES))
        model.load_state_dict(checkpoint["model_state_dict"])
        val_acc = checkpoint.get("val_acc", 49.81)
    else:
        model = ANNClassifier(img_size=ann_size, num_classes=len(CLASS_NAMES))
        val_acc = 0.0
    model.eval()
    return model, ann_size, val_acc

ann_model, model_img_size, best_val_acc = load_ann_model()

# Sidebar: Pure ANN Architecture Overview
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/8637/8637106.png", width=80)
st.sidebar.title("مۆدێلی پڕۆژە: ANN")
st.sidebar.markdown("**Artificial Neural Network (Deep Res-MLP)**")

st.sidebar.success(f"✅ مۆدێلی ANN چالاکە | باشترین Accuracy: **{best_val_acc:.1f}%**")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧠 تایبەتمەندییە تەکنیکییەکانی ANN:")
st.sidebar.markdown(f"""
- **تەلارسازی:** Deep Residual MLP
- **قەبارەی پیکسڵ:** {model_img_size}x{model_img_size}x3
- **ژمارەی چینە شاردراوەکان:** ٧ چینی قووڵ
- **کۆی پارامیتەرەکان:** ~١٤.٩ ملیۆن کێش
- **فەنکشنی کاراکردن:** GELU Activation
- **تەکنیکی پاراستن:** LayerNorm + Skip Connections
- **پۆلەکان (5 Classes):**
  - 🧑 مرۆڤ (Human)
  - 🐶 سەگ (Dog)
  - 🐱 پشیلە (Cat)
  - 🐦 باڵندە (Bird)
  - 🐴 ئەسپ (Horse)
""")

# Main Title
st.markdown("<div class='main-title'>🧠 ناسینەوەی وێنە بە تۆڕی دەماری دەستکرد (ANN)</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Image Recognition using Deep Residual Artificial Neural Network (ANN)</div>", unsafe_allow_html=True)

tabs = st.tabs(["📤 بارکردنی وێنە (Upload)", "📸 کامێرای ڕاستەوخۆ (Webcam)", "🖼️ وێنەی نموونەیی (Samples)", "📊 ئەنجام و ماتریکسی هەڵە (Metrics)"])

selected_image = None

# Tab 1: Upload
with tabs[0]:
    uploaded_file = st.file_uploader("وێنەیەک لە کۆمپیوتەرەکەت هەڵبژێرە (JPG, PNG, JPEG):", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        selected_image = Image.open(uploaded_file).convert("RGB")

# Tab 2: Webcam
with tabs[1]:
    camera_photo = st.camera_input("وێنەیەک بگرە بە کامێرای لاپتۆپەکەت:")
    if camera_photo is not None:
        selected_image = Image.open(camera_photo).convert("RGB")

# Tab 3: Samples
with tabs[2]:
    st.write("کلیک لەسەر یەکێک لە وێنە نموونەییەکان بکە بۆ تاقیکردنەوەی دەستبەجێ بە ANN:")
    sample_cols = st.columns(5)
    sample_files = {
        "human": "samples/sample_human.jpg",
        "dog": "samples/sample_dog.jpg",
        "cat": "samples/sample_cat.jpg",
        "bird": "samples/sample_bird.jpg",
        "horse": "samples/sample_horse.jpg",
    }
    for idx, (cls_name, path) in enumerate(sample_files.items()):
        with sample_cols[idx]:
            if os.path.exists(path):
                img = Image.open(path)
                st.image(img, caption=f"{CLASS_ICONS[cls_name]} {cls_name.capitalize()}", width="stretch")
                if st.button(f"تاقیکردنەوەی {cls_name}", key=f"btn_{cls_name}"):
                    selected_image = img.convert("RGB")

# Tab 4: Evaluation Metrics
with tabs[3]:
    st.markdown("### 📊 ئەنجامەکانی مەشقپێکردنی تۆڕی دەماری (ANN)")
    st.markdown("""
    لەم بەشەدا هێڵکاری سەرکەوتنی دیقەت، دابەزینی هەڵە، و ماتریکسی تاقیکردنەوەی فەرمی دەبینیت:
    """)
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        ann_curve = "outputs/ann_mlp_training_curves.png"
        if os.path.exists(ann_curve):
            st.image(ann_curve, caption="Loss & Accuracy Curves (ANN)", width="stretch")
    with m_col2:
        ann_cm = "outputs/ann_mlp_confusion_matrix.png"
        if os.path.exists(ann_cm):
            st.image(ann_cm, caption="Confusion Matrix (ANN)", width="stretch")

# Prediction Logic
if selected_image is not None:
    st.markdown("---")
    st.markdown("### 🔍 ئەنجامی شیکاری وێنە بە ANN:")

    col_left, col_right = st.columns([1, 1.2])

    with col_left:
        st.image(selected_image, caption="وێنەی هەڵبژێردراو (Input Image)", width="stretch")

    with col_right:
        # Preprocessing & Inference using ANN transform
        curr_transform = transforms.Compose([
            transforms.Resize((model_img_size, model_img_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])
        input_tensor = curr_transform(selected_image).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            logits = ann_model(input_tensor)
            probs = F.softmax(logits, dim=1).squeeze().numpy()

        top_idx = int(np.argmax(probs))
        top_class = CLASS_NAMES[top_idx]
        top_prob = float(probs[top_idx]) * 100.0

        st.markdown(f"""
        <div class='metric-card'>
            <div style='font-size: 1.1rem; color: #4B5563;'>پێشبینی مۆدێلی ANN:</div>
            <div class='prediction-badge'>{CLASS_ICONS[top_class]} {top_class.upper()}</div>
            <div class='kurdish-badge'>{KURDISH_NAMES[top_class]}</div>
            <div style='font-size: 1.2rem; font-weight: bold; margin-top: 8px;'>ڕێژەی دڵنیایی: {top_prob:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 📊 ڕێژەی دڵنیایی بۆ هەموو پۆلەکان (Class Probabilities):")
        df_probs = pd.DataFrame({
            "پۆل (Class)": [f"{CLASS_ICONS[c]} {KURDISH_NAMES[c]}" for c in CLASS_NAMES],
            "ڕێژەی ئەگەر (%)": [float(p) * 100.0 for p in probs]
        })
        st.bar_chart(df_probs.set_index("پۆل (Class)"))

        with st.expander("💡 چۆنیەتی بڕیاردانی تۆڕی دەماری (ANN):"):
            st.markdown(f"""
            - وێنەکە گۆڕدرا بۆ ماتریکسی پیکسڵی **{model_img_size}x{model_img_size}x3 = {model_img_size * model_img_size * 3}** نۆدی چوونەژوورەوە.
            - بەناو **٧ چینی شاردراوە (Hidden Layers)** و بلۆکەکانی **Skip Connection**دا تێپەڕی.
            - فەنکشنی **GELU** ناهێڵییەتی دەستنیشان کرد و فەنکشنی **Softmax** لە دوا چیندا ئەگەرەکانی دابەشکرد.
            """)
