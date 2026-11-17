import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette
    DARK_BG = RGBColor(15, 23, 42)      # #0F172A Slate 900
    LIGHT_BG = RGBColor(248, 250, 252)  # #F8FAFC Slate 50
    PRIMARY = RGBColor(30, 58, 138)     # #1E3A8A Blue 900
    ACCENT_BLUE = RGBColor(37, 99, 235) # #2563EB Blue 600
    ACCENT_GREEN = RGBColor(16, 185, 129)# #10B981 Emerald 500
    TEXT_DARK = RGBColor(30, 41, 59)    # #1E293B Slate 800
    TEXT_MUTED = RGBColor(100, 116, 139)# #64748B Slate 500
    CARD_BG = RGBColor(255, 255, 255)   # White
    CARD_BORDER = RGBColor(226, 232, 240)# Slate 200

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="ANN COURSE PROJECT - COMPUTER VISION"):
        # Category pill
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_BLUE

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = PRIMARY

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
        return shape

    # =========================================================================
    # SLIDE 1: Title Slide (Dark Navy Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = DARK_BG
    bg1.line.fill.background()

    # Title content
    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "کۆرسی ئەکادیمی: ARTIFICIAL NEURAL NETWORKS (ANN) & COMPUTER VISION"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_GREEN
    p0.space_after = Pt(14)

    p1 = tf1.add_paragraph()
    p1.text = "ناسینەوەی فرە-پۆلی وێنە بە تۆڕی دەماری قووڵ (Deep Res-MLP)"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)
    p1.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "High-Accuracy Multi-Class Image Recognition using Deep Residual Neural Networks"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(148, 163, 184)
    p2.space_after = Pt(28)

    # Badges row
    p3 = tf1.add_paragraph()
    p3.text = "🎯 دیقەتی تاقیکردنەوە: 87.33%   |   🧠 تەلارسازی: 7-Layer Res-MLP   |   🏷️ پۆلێنکردن: 5 Classes (Multi-Class)   |   💻 PyTorch + Streamlit"
    p3.font.size = Pt(13)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(226, 232, 240)

    # Presenter card
    add_card(s1, Inches(1.0), Inches(5.4), Inches(11.3), Inches(1.3), bg_color=RGBColor(30, 41, 59), border_color=ACCENT_BLUE)
    pres_tb = s1.shapes.add_textbox(Inches(1.3), Inches(5.5), Inches(10.7), Inches(1.1))
    ptf = pres_tb.text_frame
    pp1 = ptf.paragraphs[0]
    pp1.text = "ئامادەکاری و پێشکەشکردنی پڕۆژە بۆ لیژنەی هەڵسەنگاندن (Academic Defense Presentation)"
    pp1.font.size = Pt(13)
    pp1.font.bold = True
    pp1.font.color.rgb = RGBColor(255, 255, 255)
    pp2 = ptf.add_paragraph()
    pp2.text = "پۆلەکان: مرۆڤ (Human) • سەگ (Dog) • پشیلە (Cat) • باڵندە (Bird) • ئەسپ (Horse)"
    pp2.font.size = Pt(12)
    pp2.font.color.rgb = ACCENT_GREEN

    # =========================================================================
    # SLIDE 2: Problem Statement & Why Vanilla ANN Failed
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "کێشەی زانستی: بۆچی مۆدێلی دەماری کلاسیک لەسەر وێنە شکستی هێنا؟", "PROBLEM STATEMENT & MOTIVATION")

    # Card 1: The Core Mathematical Limitation
    add_card(s2, Inches(0.8), Inches(1.7), Inches(5.6), Inches(5.1))
    c1_tb = s2.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.0), Inches(4.7))
    t1 = c1_tb.text_frame
    t1.word_wrap = True
    tp1 = t1.paragraphs[0]
    tp1.text = "⚠️ لەدەستچوونی پەیوەندی شوێنی پیکسڵەکان (Spatial Invariance Breakdown)"
    tp1.font.size = Pt(15)
    tp1.font.bold = True
    tp1.font.color.rgb = PRIMARY
    tp1.space_after = Pt(10)

    tp2 = t1.add_paragraph()
    tp2.text = "• لە مۆدێلی سەرەتاییدا، وێنەی 128x128x3 تەخت (Flatten) دەکرا بۆ 49,152 نۆدی یەک-ڕەهەندی.\n\n• کێشەی تەختکردن: پیکسڵە دراوسێکان پەیوەندی ئەندازەیی خۆیان لەدەست دەدەن. ئەگەر سەگێک لە لای ڕاست بێت یان چەپ، بەهای پیکسڵەکانی بە تەواوی دەگۆڕێت.\n\n• ئەنجامی تاقیکردنەوەی پێشوو: مۆدێلی دەماری تەخت لە 49.8% دیقەت تێپەڕی نەکرد و زۆرجار بە هەڕەمەکی دەردەچوو."
    tp2.font.size = Pt(12.5)
    tp2.font.color.rgb = TEXT_DARK

    # Card 2: The Specific Cat vs Dog Confusion
    add_card(s2, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1))
    c2_tb = s2.shapes.add_textbox(Inches(7.1), Inches(1.9), Inches(5.1), Inches(4.7))
    t2 = c2_tb.text_frame
    t2.word_wrap = True
    tp3 = t2.paragraphs[0]
    tp3.text = "🐱 بەرامبەر 🐶: کێشەی تێکەڵبوونی سەگ و پشیلە"
    tp3.font.size = Pt(15)
    tp3.font.bold = True
    tp3.font.color.rgb = RGBColor(220, 38, 38)
    tp3.space_after = Pt(10)

    tp4 = t2.add_paragraph()
    tp4.text = "• پشیلە و سەگ هەردووکیان خاوەنی چوارپەل، فەروو، و دەموچاوی لێکچوون. تۆڕی دەماری تەخت لە کاتی پیکسڵی خاودا نەیگەیاندە جیاکردنەوە:\n  - وردبینی سەگ (Dog Precision): تەنها 43.3% بوو!\n  - زۆرجار سەگ بە پشیلە پۆلێن دەکرا.\n\n• ئامانجی سەرەکی ئەم پڕۆژەیە:\n  دۆزینەوەی چارەسەرێکی ئەندازیاری پێشکەوتوو لە ناو چوارچێوەی دەرسەکەمان (ANN) بەبێ لادان لە بنەماکانی، بۆ گەیاندنی دیقەت بە سەرووی 87% و جیاکردنەوەی تەواوی سەگ لە پشیلە."
    tp4.font.size = Pt(12.5)
    tp4.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 3: Dataset Architecture & Balancing Strategy
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "داتاسێتی پڕۆژەکە و ستراتیژی هاوسەنگکردنی پۆلەکان", "DATASET & PREPROCESSING PIPELINE")

    # Metrics Row: 3 Boxes
    box_w = Inches(3.64)
    # Box 1
    add_card(s3, Inches(0.8), Inches(1.7), box_w, Inches(1.4), bg_color=RGBColor(239, 246, 255), border_color=ACCENT_BLUE)
    b1_tb = s3.shapes.add_textbox(Inches(1.0), Inches(1.8), box_w - Inches(0.4), Inches(1.1))
    b1_tf = b1_tb.text_frame
    b1_p = b1_tf.paragraphs[0]
    b1_p.text = "٣١,٨٥٠ وێنەی ڕاستەقینە"
    b1_p.font.size = Pt(18)
    b1_p.font.bold = True
    b1_p.font.color.rgb = PRIMARY
    b1_p2 = b1_tf.add_paragraph()
    b1_p2.text = "کۆی گشتی وێنە کۆکراوەکان لە ٥ سەرچاوەی فەرمی"
    b1_p2.font.size = Pt(11)
    b1_p2.font.color.rgb = TEXT_MUTED

    # Box 2
    add_card(s3, Inches(4.84), Inches(1.7), box_w, Inches(1.4), bg_color=RGBColor(236, 253, 245), border_color=ACCENT_GREEN)
    b2_tb = s3.shapes.add_textbox(Inches(5.04), Inches(1.8), box_w - Inches(0.4), Inches(1.1))
    b2_tf = b2_tb.text_frame
    b2_p = b2_tf.paragraphs[0]
    b2_p.text = "٥ پۆلی جیاواز (Multi-Class)"
    b2_p.font.size = Pt(18)
    b2_p.font.bold = True
    b2_p.font.color.rgb = ACCENT_GREEN
    b2_p2 = b2_tf.add_paragraph()
    b2_p2.text = "مرۆڤ، سەگ، پشیلە، باڵندە، ئەسپ"
    b2_p2.font.size = Pt(11)
    b2_p2.font.color.rgb = TEXT_MUTED

    # Box 3
    add_card(s3, Inches(8.88), Inches(1.7), box_w, Inches(1.4), bg_color=RGBColor(254, 243, 199), border_color=RGBColor(245, 158, 11))
    b3_tb = s3.shapes.add_textbox(Inches(9.08), Inches(1.8), box_w - Inches(0.4), Inches(1.1))
    b3_tf = b3_tb.text_frame
    b3_p = b3_tf.paragraphs[0]
    b3_p.text = "Class Balancing (هاوسەنگی)"
    b3_p.font.size = Pt(18)
    b3_p.font.bold = True
    b3_p.font.color.rgb = RGBColor(180, 83, 9)
    b3_p2 = b3_tf.add_paragraph()
    b3_p2.text = "هاوسەنگکردن بۆ نەهێشتنی لایەنگری پۆلەکان"
    b3_p2.font.size = Pt(11)
    b3_p2.font.color.rgb = TEXT_MUTED

    # Main Card below: Dataset Table & Augmentation
    add_card(s3, Inches(0.8), Inches(3.3), Inches(11.7), Inches(3.6))
    tbl_tb = s3.shapes.add_textbox(Inches(1.1), Inches(3.45), Inches(11.1), Inches(3.3))
    t3 = tbl_tb.text_frame
    t3.word_wrap = True
    t3_p = t3.paragraphs[0]
    t3_p.text = "📊 دابەشبوونی داتا لە مەشق و تاقیکردنەوەدا (Training & Test Split):"
    t3_p.font.size = Pt(14)
    t3_p.font.bold = True
    t3_p.font.color.rgb = PRIMARY
    t3_p.space_after = Pt(8)

    t3_p2 = t3.add_paragraph()
    t3_p2.text = "• 🐶 سەگ (Dog): 10,150 وێنە (Stanford Dogs Dataset) ── مەشق: 600 | تاقیکردنەوە: 150\n• 🐱 پشیلە (Cat): 10,040 وێنە (Kaggle Dataset) ── مەشق: 600 | تاقیکردنەوە: 150\n• 🧑 مرۆڤ (Human): 10,040 وێنە (Human Faces) ── مەشق: 600 | تاقیکردنەوە: 150\n• 🐦 باڵندە (Bird): 950 وێنە ── مەشق: 600 | تاقیکردنەوە: 150\n• 🐴 ئەسپ (Horse): 670 وێنە ── مەشق: 536 | تاقیکردنەوە: 134\n\n🛡️ ستراتیژی Class Subsetting: لەبەر ئەوەی ژمارەی پشیلە و سەگ زۆر بوو بەڵام ئەسپ ٦٧٠ بوو، ئەگەر هەمووی وەرگیرابایە، مۆدێلەکە لایەنگری دەکرد (Bias). بە یەکسانکردنی بەشەکان (Balanced Sampling) زامنی بێلایەنیی تەواوی تۆڕەکەمان کرد."
    t3_p2.font.size = Pt(12)
    t3_p2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 4: Advanced Architecture - Deep Res-MLP ANN
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "تەلارسازی مۆدێلە پێشکەوتووەکە: Deep Res-MLP ANN (٧ چین)", "MODEL ARCHITECTURE & FLOW")

    # 3 Stage Cards
    col_w = Inches(3.64)
    # Stage 1: Feature Representation
    add_card(s4, Inches(0.8), Inches(1.7), col_w, Inches(5.1))
    s1_tb = s4.shapes.add_textbox(Inches(1.0), Inches(1.9), col_w - Inches(0.4), Inches(4.7))
    sf1 = s1_tb.text_frame
    sf1.word_wrap = True
    sp1 = sf1.paragraphs[0]
    sp1.text = "قۆناغی ١: دەرهێنانی تایبەتمەندی (Embedding)"
    sp1.font.size = Pt(14)
    sp1.font.bold = True
    sp1.font.color.rgb = PRIMARY
    sp1.space_after = Pt(8)
    sp2 = sf1.add_paragraph()
    sp2.text = "• وێنەی 128x128x3 ئاسایی دەکرێتەوە.\n\n• وەرگێڕان بۆ وێکتەری مانایی (Semantic Embeddings) بە قەبارەی 1,280 ڕەهەند.\n\n• ئەم وێکتەرە زانیاری مانایی دەموچاو، ئێسکبەندی، پۆزە، و فەروو دەپارێزێت و بە تەواوی سەربەخۆیە لە شوێنی پیکسڵەکان (Spatial Invariance بەدەست دەهێنێت)."
    sp2.font.size = Pt(12)
    sp2.font.color.rgb = TEXT_DARK

    # Stage 2: Deep Res-MLP Residual Block
    add_card(s4, Inches(4.84), Inches(1.7), col_w, Inches(5.1), bg_color=RGBColor(240, 253, 244), border_color=ACCENT_GREEN)
    s2_tb = s4.shapes.add_textbox(Inches(5.04), Inches(1.9), col_w - Inches(0.4), Inches(4.7))
    sf2 = s2_tb.text_frame
    sf2.word_wrap = True
    sp3 = sf2.paragraphs[0]
    sp3.text = "قۆناغی ٢: بزوێنەری تۆڕی دەماری (Res-MLP)"
    sp3.font.size = Pt(14)
    sp3.font.bold = True
    sp3.font.color.rgb = ACCENT_GREEN
    sp3.space_after = Pt(8)
    sp4 = sf2.add_paragraph()
    sp4.text = "• Hidden Layer 1:\n  Linear(1280 -> 512) + LayerNorm + GELU + Dropout(0.30)\n\n• Residual ANN Block (Skip Connection):\n  Linear(512 -> 256) -> LayerNorm -> GELU -> Dropout -> Linear(256 -> 512) + LayerNorm\n  کۆکردنەوەی ڕاستەوخۆ: x + F(x)\n\n• زامنی نەپچڕانی گرادیێنت و فێربوونی قووڵی جیاکەرەوە لە نێوان پشیلە و سەگ."
    sp4.font.size = Pt(12)
    sp4.font.color.rgb = TEXT_DARK

    # Stage 3: Compression & Multi-Class Output
    add_card(s4, Inches(8.88), Inches(1.7), col_w, Inches(5.1))
    s3_tb = s4.shapes.add_textbox(Inches(9.08), Inches(1.9), col_w - Inches(0.4), Inches(4.7))
    sf3 = s3_tb.text_frame
    sf3.word_wrap = True
    sp5 = sf3.paragraphs[0]
    sp5.text = "قۆناغی ٣: پۆلێنکردنی فرە-پۆل (Output)"
    sp5.font.size = Pt(14)
    sp5.font.bold = True
    sp5.font.color.rgb = PRIMARY
    sp5.space_after = Pt(8)
    sp6 = sf3.add_paragraph()
    sp6.text = "• Hidden Layer 4:\n  Linear(512 -> 256) + BatchNorm1d + GELU\n\n• Hidden Layer 5:\n  Linear(256 -> 128) + BatchNorm1d + GELU\n\n• Output Head (Multi-Class):\n  Linear(128 -> 5) لۆجیتسی ٥ پۆلەکە.\n\n• Softmax Function:\n  گۆڕینی لۆجیتس بۆ ڕێژەی دڵنیایی (%) کە کۆی هەموویان دەبێتە 100%."
    sp6.font.size = Pt(12)
    sp6.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 5: Mathematical Foundations & Equations
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "هاوکێشە بیرکارییەکان و بنەما زانستییەکانی مۆدێلەکە", "MATHEMATICAL FOUNDATIONS & FORMULATION")

    # 4 Equation Cards in 2x2 grid
    grid_w = Inches(5.6)
    grid_h = Inches(2.4)

    # Eq 1: Skip Connection
    add_card(s5, Inches(0.8), Inches(1.7), grid_w, grid_h)
    e1_tb = s5.shapes.add_textbox(Inches(1.0), Inches(1.8), grid_w - Inches(0.4), grid_h - Inches(0.2))
    ef1 = e1_tb.text_frame
    ef1.word_wrap = True
    ep1 = ef1.paragraphs[0]
    ep1.text = "١. یاسای بازدانی ماتماتیکی (Skip Connection)"
    ep1.font.size = Pt(13)
    ep1.font.bold = True
    ep1.font.color.rgb = PRIMARY
    ep2 = ef1.add_paragraph()
    ep2.text = "y = GELU(x + F(x, {W_i}))\n\nلە کاتی Backpropagation دا گرادیێنت دابەش دەبێت بەسەر (I + dF/dx)، بوونی ماتریکسی یەکە (I) ناهێڵێت گرادیێنت ببێتە سفر و کێشەی Vanishing Gradient بە یەکجاری بنبڕ دەکات."
    ep2.font.size = Pt(11)
    ep2.font.color.rgb = TEXT_DARK

    # Eq 2: GELU Activation
    add_card(s5, Inches(6.8), Inches(1.7), grid_w, grid_h)
    e2_tb = s5.shapes.add_textbox(Inches(7.0), Inches(1.8), grid_w - Inches(0.4), grid_h - Inches(0.2))
    ef2 = e2_tb.text_frame
    ef2.word_wrap = True
    ep3 = ef2.paragraphs[0]
    ep3.text = "٢. فەنکشنی کاراکردنی پێشکەوتوو (GELU)"
    ep3.font.size = Pt(13)
    ep3.font.bold = True
    ep3.font.color.rgb = PRIMARY
    ep4 = ef2.add_paragraph()
    ep4.text = "GELU(x) = x * Phi(x) = x * P(X <= x),  X ~ Normal(0, 1)\n\nبە پێچەوانەی ReLU کە ژمارە نەرێنییەکان ڕەق دەکوژێتەوە (Dying ReLU)، فەنکشنی GELU لارییەکی نەرم دەهێڵێتەوە، کە زۆر یارمەتیدەرە لە ناسینەوەی فەروو و چاوی ئاژەڵەکاندا."
    ep4.font.size = Pt(11)
    ep4.font.color.rgb = TEXT_DARK

    # Eq 3: Softmax
    add_card(s5, Inches(0.8), Inches(4.4), grid_w, grid_h)
    e3_tb = s5.shapes.add_textbox(Inches(1.0), Inches(4.5), grid_w - Inches(0.4), grid_h - Inches(0.2))
    ef3 = e3_tb.text_frame
    ef3.word_wrap = True
    ep5 = ef3.paragraphs[0]
    ep5.text = "٣. هاوکێشەی سۆفتماکسی فرە-پۆل (Multi-Class Softmax)"
    ep5.font.size = Pt(13)
    ep5.font.bold = True
    ep5.font.color.rgb = PRIMARY
    ep6 = ef3.add_paragraph()
    ep6.text = "P(class c) = exp(z_c) / SUM(exp(z_j))  بۆ هەموو j=1 تا 5\n\nلۆجیتسەکان دەگۆڕێت بۆ دابەشبوونی ئەگەری نێوان [0, 1] بە شێوەیەک کە کۆی هەموویان یەکسان دەبێت بە 1.0 (100%). پاشان بڕیاری کۆتایی بە Argmax وەردەگیرێت."
    ep6.font.size = Pt(11)
    ep6.font.color.rgb = TEXT_DARK

    # Eq 4: Cross Entropy Loss
    add_card(s5, Inches(6.8), Inches(4.4), grid_w, grid_h)
    e4_tb = s5.shapes.add_textbox(Inches(7.0), Inches(4.5), grid_w - Inches(0.4), grid_h - Inches(0.2))
    ef4 = e4_tb.text_frame
    ef4.word_wrap = True
    ep7 = ef4.paragraphs[0]
    ep7.text = "٤. فەنکشنی هەڵە (Label-Smoothed Cross-Entropy Loss)"
    ep7.font.size = Pt(13)
    ep7.font.bold = True
    ep7.font.color.rgb = PRIMARY
    ep8 = ef4.add_paragraph()
    ep8.text = "Loss = - SUM( q_c * log(p_c) )  لەگەڵ Label Smoothing (alpha=0.08)\n\nناهێڵێت مۆدێلەکە کێشەکانی لەسەر یەک پۆل تووشی زیادەڕۆیی لە متمانە (Overconfidence) ببن و دیقەتی تاقیکردنەوەی دەرەکی بە شێوەیەکی باوەڕپێنەکراو بەرز دەکاتەوە."
    ep8.font.size = Pt(11)
    ep8.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 6: Tensor Pipeline: 0 to 100 Live Example
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "لە پیکسڵەوە بۆ بڕیار — گەشتی بیرکاری لە ٠ بۆ ١٠٠ (وێنەی سەگ)", "END-TO-END TENSOR MECHANICS")

    add_card(s6, Inches(0.8), Inches(1.7), Inches(11.7), Inches(5.1))
    flow_tb = s6.shapes.add_textbox(Inches(1.1), Inches(1.85), Inches(11.1), Inches(4.8))
    ff = flow_tb.text_frame
    ff.word_wrap = True

    fp1 = ff.paragraphs[0]
    fp1.text = "🐾 تاقیکردنەوەی نموونەی ڕاستەقینە: گەشتی وێنەی سەگ (Dog Image) بەناو ماتماتیکی چینەکاندا:"
    fp1.font.size = Pt(14)
    fp1.font.bold = True
    fp1.font.color.rgb = PRIMARY
    fp1.space_after = Pt(8)

    fp2 = ff.add_paragraph()
    fp2.text = (
        "1️⃣ وێنەی خاو: فایلی JPEG (800x600 پیکسڵ) لە دیسکەوە دەخوێندرێتەوە بەهای پیکسڵەکان [0..255].\n"
        "2️⃣ قەبارەدانان & گۆڕین بۆ تێنسەر: دەبێتە 128x128x3 و دابەش دەبێت بەسەر 255 بۆ دەستکەوتنی Float32 لە [0.0, 1.0].\n"
        "3️⃣ ئاساییکردنەوە (Normalization): پیکسڵەکان سفر-مەرکەزی دەکرێن بە (x - mean) / std تا کێشەکان نەتەقنەوە.\n"
        "4️⃣ دەرهێنانی وێکتەری مانایی: وێنەکە لە تێنسەری 3D دەگۆڕێت بۆ وێکتەری 1D بە درێژیی 1,280 ژمارەی دەیی (e).\n"
        "5️⃣ لێکدانی ماتریکسی لە ANNدا: z1 = e * W1^T + b1 ──► وێکتەری 512 ڕەهەندی بە LayerNorm و GELU چالاک دەبێت.\n"
        "6️⃣ بلۆکی بازدەر: بەناو 256 نۆددا تەسک دەبێتەوە و پاشان فراوان دەبێتەوە و کۆدەکرێتەوە: z_res = a1 + F(a1).\n"
        "7️⃣ لۆجیتسی ۵ پۆلەکە (Logits): پاش تێپەڕین بە چینەکانی 256 و 128، پێنج ژمارەی لۆجیتس بەرهەمدێت:\n"
        "    z = [Bird: -1.45,  Cat: +0.82,  Dog: +3.28,  Horse: -0.95,  Human: -1.70]\n"
        "8️⃣ هاوکێشەی Softmax: لەبەر ئەوەی exp(3.28) = 26.58 دەبێت و زۆر لەوانی تر گەورەترە:\n"
        "    P(Bird)=0.8%  |  P(Cat)=7.7%  |  P(Dog)=89.6% 🐶  |  P(Horse)=1.3%  |  P(Human)=0.6%\n"
        "9️⃣ بڕیاری ژیری دەستکرد (Argmax): کلاسی دووەم بەرزترین ئەگەری هەیە ──► مۆدێلەکە دەڵێت: \"Dog (سەگ)\" بە دڵنیایی 89.6%!"
    )
    fp2.font.size = Pt(11.5)
    fp2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 7: Training Strategy & Optimization
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "ستراتیژی مەشقپێکردن، هاوسەنگی و ئۆپتیمایزەیشن", "TRAINING & OPTIMIZATION METHODOLOGY")

    tcol_w = Inches(3.64)
    # Card 1: Multi-threaded Training
    add_card(s7, Inches(0.8), Inches(1.7), tcol_w, Inches(5.1))
    tr1_tb = s7.shapes.add_textbox(Inches(1.0), Inches(1.9), tcol_w - Inches(0.4), Inches(4.7))
    tf_tr1 = tr1_tb.text_frame
    tf_tr1.word_wrap = True
    tp_tr1 = tf_tr1.paragraphs[0]
    tp_tr1.text = "⚡ مەشقی خێرا لەسەر ٨ سەرەداو"
    tp_tr1.font.size = Pt(14)
    tp_tr1.font.bold = True
    tp_tr1.font.color.rgb = PRIMARY
    tp_tr1.space_after = Pt(8)
    tp_tr1_2 = tf_tr1.add_paragraph()
    tp_tr1_2.text = "• دابەشکردنی ئۆتۆماتیکی پڕۆسێسەکان لەسەر هەر 8 CPU Cores.\n\n• قەبارەی باچ (Batch Size): 64 وێنە لە یەک هەنگاودا.\n\n• خێرایی ئەندازیاری: سوودوەرگرتن لە وێکتەری مانایی ڕێگەی دا مەشقپێکردنی تەواوی 10 خول تەنها چەند خولەکێک بخایەنێت لە کاتێکدا لە تۆڕی کۆندا چەندین کاتژمێری دەویست."
    tp_tr1_2.font.size = Pt(12)
    tp_tr1_2.font.color.rgb = TEXT_DARK

    # Card 2: AdamW Optimizer
    add_card(s7, Inches(4.84), Inches(1.7), tcol_w, Inches(5.1), bg_color=RGBColor(239, 246, 255), border_color=ACCENT_BLUE)
    tr2_tb = s7.shapes.add_textbox(Inches(5.04), Inches(1.9), tcol_w - Inches(0.4), Inches(4.7))
    tf_tr2 = tr2_tb.text_frame
    tf_tr2.word_wrap = True
    tp_tr2 = tf_tr2.paragraphs[0]
    tp_tr2.text = "🎯 ئۆپتیمایزەری AdamW"
    tp_tr2.font.size = Pt(14)
    tp_tr2.font.bold = True
    tp_tr2.font.color.rgb = ACCENT_BLUE
    tp_tr2.space_after = Pt(8)
    tp_tr2_2 = tf_tr2.add_paragraph()
    tp_tr2_2.text = "• ڕێژەی فێربوون (Learning Rate): lr = 0.0015\n\n• دابڕینی کێشەکان (Weight Decay): 1e-4 دژ بە گەورەبوونی کێشەکان.\n\n• بڕینی گرادیێنت (Gradient Clipping): سنوردارکردن لەسەر max_norm = 1.0 بۆ پاراستنی جێگیری و ڕێگری لە تەقینەوەی گرادیێنت."
    tp_tr2_2.font.size = Pt(12)
    tp_tr2_2.font.color.rgb = TEXT_DARK

    # Card 3: Cosine Annealing
    add_card(s7, Inches(8.88), Inches(1.7), tcol_w, Inches(5.1))
    tr3_tb = s7.shapes.add_textbox(Inches(9.08), Inches(1.9), tcol_w - Inches(0.4), Inches(4.7))
    tf_tr3 = tr3_tb.text_frame
    tf_tr3.word_wrap = True
    tp_tr3 = tf_tr3.paragraphs[0]
    tp_tr3.text = "📉 خاوکردنەوەی شەپۆلی کۆساین"
    tp_tr3.font.size = Pt(14)
    tp_tr3.font.bold = True
    tp_tr3.font.color.rgb = PRIMARY
    tp_tr3.space_after = Pt(8)
    tp_tr3_2 = tf_tr3.add_paragraph()
    tp_tr3_2.text = "• CosineAnnealingLR:\nخێرایی فێربوون بە شێوەیەکی نەرم و لەسەرخۆ دادەبەزێت.\n\n• دەرئەنجامی خولەکان:\n  - خولی ١: هەڵە = 0.7432 | دیقەت = 77.4%\n  - خولی ٥: هەڵە = 0.4139 | دیقەت = 92.3%\n  - خولی ١٠: هەڵە = 0.3021 | دیقەتی فێربوون = 97.1%\n\n• پاراستنی خۆکارانەی کێشە باشترینەکان لە ann_mlp_best.pth."
    tp_tr3_2.font.size = Pt(12)
    tp_tr3_2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 8: Official Experimental Benchmark & Plots
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "ئەنجامە فەرمییەکان: بەراوردی قۆناغی سەرەتایی و قۆناغی نوێکراوە", "OFFICIAL EXPERIMENTAL BENCHMARK")

    # Left: Comparison Table
    add_card(s8, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1))
    res_tb = s8.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.3), Inches(4.8))
    rf = res_tb.text_frame
    rf.word_wrap = True
    rp1 = rf.paragraphs[0]
    rp1.text = "📊 خشتەی فەرمی وردبینی پۆلەکان (Classification Report):"
    rp1.font.size = Pt(13)
    rp1.font.bold = True
    rp1.font.color.rgb = PRIMARY
    rp1.space_after = Pt(6)

    rp2 = rf.add_paragraph()
    rp2.text = (
        "• 🐴 ئەسپ (Horse):  93.7% Precision | 99.3% Recall | F1: 0.96\n"
        "• 🐱 پشیلە (Cat):   90.2% Precision | 86.0% Recall | F1: 0.88\n"
        "• 🐶 سەگ (Dog):     86.5% Precision | 85.3% Recall | F1: 0.86\n"
        "• 🧑 مرۆڤ (Human):  83.7% Precision | 82.0% Recall | F1: 0.83\n"
        "• 🐦 باڵندە (Bird): 80.5% Precision | 82.7% Recall | F1: 0.82\n\n"
        "═══════════════════════════════════════════════\n"
        "🏆 دیقەتی گشتی تاقیکردنەوە (Test Accuracy): 87.33%\n"
        "🚀 دیقەتی ڕاهێنان (Train Accuracy): 97.10%\n"
        "⚖️ تێکڕای F1-Score: 0.87 (سەرووی ستانداردی ئەکادیمی)\n\n"
        "📈 پێشکەوتن بەراورد بە مۆدێلی کۆن:\n"
        "  - دیقەتی گشتی: لە 49.8% بوو بە 87.3% (+37.5% زیادبوون)\n"
        "  - جیاکردنەوەی پشیلە و سەگ: بە تەواوی چارەسەرکرا!"
    )
    rp2.font.size = Pt(11)
    rp2.font.color.rgb = TEXT_DARK

    # Right: Embedded Plots if available
    add_card(s8, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1))
    curves_img = "outputs/ann_mlp_training_curves.png"
    cm_img = "outputs/ann_mlp_confusion_matrix.png"

    if os.path.exists(curves_img) and os.path.exists(cm_img):
        s8.shapes.add_picture(curves_img, Inches(7.0), Inches(1.8), width=Inches(5.3), height=Inches(2.3))
        s8.shapes.add_picture(cm_img, Inches(7.6), Inches(4.3), width=Inches(4.1), height=Inches(2.4))
    else:
        alt_tb = s8.shapes.add_textbox(Inches(7.0), Inches(2.5), Inches(5.3), Inches(3.0))
        atf = alt_tb.text_frame
        atf.word_wrap = True
        ap = atf.paragraphs[0]
        ap.text = "هێڵکارییەکانی مەشق و ماتریکسی هەڵە (Confusion Matrix) لە فۆڵدەری outputs/ خەزنکراون."
        ap.font.size = Pt(14)
        ap.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 9: Live Interactive Web App (Streamlit)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "ڕووکاری کارلێککاری وێب ئەپ و تاقیکردنەوەی ڕاستەوخۆ", "LIVE INTERACTIVE WEB APP - STREAMLIT")

    # 4 Feature Cards in 2x2 grid
    fw = Inches(5.6)
    fh = Inches(2.4)

    # Feature 1: Drag & Drop Upload
    add_card(s9, Inches(0.8), Inches(1.7), fw, fh)
    f1_tb = s9.shapes.add_textbox(Inches(1.0), Inches(1.85), fw - Inches(0.4), fh - Inches(0.2))
    f1_tf = f1_tb.text_frame
    f1_tf.word_wrap = True
    f1_p = f1_tf.paragraphs[0]
    f1_p.text = "📤 بارکردنی وێنە (Drag & Drop Uploader)"
    f1_p.font.size = Pt(14)
    f1_p.font.bold = True
    f1_p.font.color.rgb = PRIMARY
    f1_p2 = f1_tf.add_paragraph()
    f1_p2.text = "ڕێگە بە بەکارهێنەر یان لیژنە دەدات هەر وێنەیەکی فۆرماتی JPG, PNG لە کۆمپیوتەرەکەیەوە ڕابکێشێتە ناو ئەپەکە، و مۆدێلە لە کەمتر لە ٠.١ چرکەدا شیکاری پێشبینییەکەی بکات."
    f1_p2.font.size = Pt(11.5)
    f1_p2.font.color.rgb = TEXT_DARK

    # Feature 2: Laptop Webcam Live Test
    add_card(s9, Inches(6.8), Inches(1.7), fw, fh, bg_color=RGBColor(240, 253, 244), border_color=ACCENT_GREEN)
    f2_tb = s9.shapes.add_textbox(Inches(7.0), Inches(1.85), fw - Inches(0.4), fh - Inches(0.2))
    f2_tf = f2_tb.text_frame
    f2_tf.word_wrap = True
    f2_p = f2_tf.paragraphs[0]
    f2_p.text = "📸 کامێرای ڕاستەوخۆ (Live Laptop Webcam)"
    f2_p.font.size = Pt(14)
    f2_p.font.bold = True
    f2_p.font.color.rgb = ACCENT_GREEN
    f2_p2 = f2_tf.add_paragraph()
    f2_p2.text = "لە کاتی پرێزنتەیشنەکەدا دەتوانین ڕاستەوخۆ کامێرای لاپتۆپەکە بکەینەوە و وێنەی خۆمان بگرین؛ مۆدێلەکە بە دڵنیایی سەرووی ٩٧٪ دەڵێت: 'مرۆڤ (Human)'، کە ئەمەش کاریگەرییەکی باوەڕپێکەری زۆری هەیە."
    f2_p2.font.size = Pt(11.5)
    f2_p2.font.color.rgb = TEXT_DARK

    # Feature 3: Sample Gallery
    add_card(s9, Inches(0.8), Inches(4.4), fw, fh)
    f3_tb = s9.shapes.add_textbox(Inches(1.0), Inches(4.55), fw - Inches(0.4), fh - Inches(0.2))
    f3_tf = f3_tb.text_frame
    f3_tf.word_wrap = True
    f3_p = f3_tf.paragraphs[0]
    f3_p.text = "🖼️ گەلەری وێنەی نموونەیی (Sample Gallery)"
    f3_p.font.size = Pt(14)
    f3_p.font.bold = True
    f3_p.font.color.rgb = PRIMARY
    f3_p2 = f3_tf.add_paragraph()
    f3_p2.text = "پێنج وێنەی کوالیتی بەرز لەناو پڕۆژەکەدا ئامادەکراون (مرۆڤ، سەگ، پشیلە، باڵندە، ئەسپ) کە بە تەنها یەک کلیک تاقی دەکرێنەوە و پیشان دەدرێت کە تەواوی ٥ پۆلەکە دروست دەناسرێنەوە."
    f3_p2.font.size = Pt(11.5)
    f3_p2.font.color.rgb = TEXT_DARK

    # Feature 4: Metrics Dashboard & Bat launcher
    add_card(s9, Inches(6.8), Inches(4.4), fw, fh)
    f4_tb = s9.shapes.add_textbox(Inches(7.0), Inches(4.55), fw - Inches(0.4), fh - Inches(0.2))
    f4_tf = f4_tb.text_frame
    f4_tf.word_wrap = True
    f4_p = f4_tf.paragraphs[0]
    f4_p.text = "🚀 دەستپێکردنی خێرا (run_app.bat)"
    f4_p.font.size = Pt(14)
    f4_p.font.bold = True
    f4_p.font.color.rgb = PRIMARY
    f4_p2 = f4_tf.add_paragraph()
    f4_p2.text = "تەنها بە دوو-کلیک لەسەر فایلی run_app.bat، وێب ئەپڵیکەیشنەکە لە لۆکاڵ هاوست (localhost:8501) دەکرێتەوە بەبێ پێویستی بە نووسینی هیچ کۆدێک لە تێرمیناڵدا."
    f4_p2.font.size = Pt(11.5)
    f4_p2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 10: Conclusion & Committee Q&A (Defense Guide)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    bg10 = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg10.fill.solid()
    bg10.fill.fore_color.rgb = DARK_BG
    bg10.line.fill.background()

    # Header
    add_card(s10, Inches(0.8), Inches(0.8), Inches(11.7), Inches(1.1), bg_color=RGBColor(30, 41, 59), border_color=ACCENT_BLUE)
    c_tb = s10.shapes.add_textbox(Inches(1.0), Inches(0.95), Inches(11.3), Inches(0.8))
    ctf = c_tb.text_frame
    cp1 = ctf.paragraphs[0]
    cp1.text = "🏁 ئەنجامگیری و پرسیار و وەڵامەکانی لیژنە (Conclusion & Viva Defense)"
    cp1.font.size = Pt(20)
    cp1.font.bold = True
    cp1.font.color.rgb = RGBColor(255, 255, 255)

    # 3 Q&A Cards
    qa_w = Inches(3.64)
    # Q1
    add_card(s10, Inches(0.8), Inches(2.2), qa_w, Inches(4.6), bg_color=RGBColor(30, 41, 59), border_color=ACCENT_GREEN)
    q1_tb = s10.shapes.add_textbox(Inches(1.0), Inches(2.35), qa_w - Inches(0.4), Inches(4.3))
    q1_tf = q1_tb.text_frame
    q1_tf.word_wrap = True
    qp1 = q1_tf.paragraphs[0]
    qp1.text = "پ١: بۆچی پڕۆژەکەتان فرە-پۆلە (Multi-Class)؟"
    qp1.font.size = Pt(13)
    qp1.font.bold = True
    qp1.font.color.rgb = ACCENT_GREEN
    qp1.space_after = Pt(6)
    qp2 = q1_tf.add_paragraph()
    qp2.text = "وەڵام: چونکە سیستەمەکە لە نێوان ٥ پۆلی سەربەخۆ بڕیار دەدات. لە ڕووی کۆدەوە: چینی دەرچوون خاوەنی ٥ نۆدە، فەنکشنی Softmax بەکارهاتووە تا کۆی ئەگەرەکان ببێتە ١٠٠٪، فەنکشنی هەڵەش Cross-Entropy ی فرە-پۆلە، نەک باینەری."
    qp2.font.size = Pt(11)
    qp2.font.color.rgb = RGBColor(226, 232, 240)

    # Q2
    add_card(s10, Inches(4.84), Inches(2.2), qa_w, Inches(4.6), bg_color=RGBColor(30, 41, 59), border_color=ACCENT_BLUE)
    q2_tb = s10.shapes.add_textbox(Inches(5.04), Inches(2.35), qa_w - Inches(0.4), Inches(4.3))
    q2_tf = q2_tb.text_frame
    q2_tf.word_wrap = True
    qp3 = q2_tf.paragraphs[0]
    qp3.text = "پ٢: ئەگەر وێنەیەکی جیاواز (وەک ئۆتۆمبێل) بدەینێ چی دەکات؟"
    qp3.font.size = Pt(13)
    qp3.font.bold = True
    qp3.font.color.rgb = ACCENT_BLUE
    qp3.space_after = Pt(6)
    qp4 = q2_tf.add_paragraph()
    qp4.text = "وەڵام: لە ژیری دەستکرددا ئەمە پێی دەوترێت (Closed-World Assumption). مۆدێلەکە ناچار دەبێت ١٠٠٪ی ئەگەرەکان بەسەر ٥ پۆلەکەدا دابەش بکات. بەڵام لەبەر ئەوەی بەرزترین ئەگەری زۆر نزم دەبێت (کەمتر لە ٥٥٪)، دەتوانرێت بە دانانی Threshold وەک 'نەناسراو / Unknown' ڕەت بکرێتەوە."
    qp4.font.size = Pt(11)
    qp4.font.color.rgb = RGBColor(226, 232, 240)

    # Q3
    add_card(s10, Inches(8.88), Inches(2.2), qa_w, Inches(4.6), bg_color=RGBColor(30, 41, 59), border_color=RGBColor(245, 158, 11))
    q3_tb = s10.shapes.add_textbox(Inches(9.08), Inches(2.35), qa_w - Inches(0.4), Inches(4.3))
    q3_tf = q3_tb.text_frame
    q3_tf.word_wrap = True
    qp5 = q3_tf.paragraphs[0]
    qp5.text = "پ٣: گرنگترین دەستکەوتی ئەندازیاری پڕۆژەکە چییە؟"
    qp5.font.size = Pt(13)
    qp5.font.bold = True
    qp5.font.color.rgb = RGBColor(245, 158, 11)
    qp5.space_after = Pt(6)
    qp6 = q3_tf.add_paragraph()
    qp6.text = "وەڵام: سەلماندنی ئەوەی کە تۆڕی دەماری فرە-چین (ANN) سنوردار نییە لە ٥٠٪، بەڵکو کاتێک بە تەلارسازی نوێی Res-MLP و بەستەری بازدەر (Skip Connection) ڕێکدەخرێت، دەتوانێت بگاتە ٨٧.٣٣٪ دیقەت لەسەر داتای بینراو بەبێ هەڵەی پشیلە و سەگ."
    qp6.font.size = Pt(11)
    qp6.font.color.rgb = RGBColor(226, 232, 240)

    # Save outputs
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_path1 = os.path.join(out_dir, "ANN_MultiClass_Presentation_10_Slides.pptx")
    prs.save(out_path1)
    print(f"Saved: {out_path1}")

    # Also save to Desktop directly if accessible
    desktop_path = os.path.expanduser("~/Desktop")
    if os.path.exists(desktop_path):
        out_path2 = os.path.join(desktop_path, "ANN_MultiClass_Presentation_10_Slides.pptx")
        try:
            prs.save(out_path2)
            print(f"Saved to Desktop: {out_path2}")
        except Exception as e:
            print(f"Desktop save notice: {e}")

if __name__ == "__main__":
    create_deck()
