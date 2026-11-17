import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_14_slide_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette
    DARK_BG = RGBColor(15, 23, 42)       # #0F172A Slate 900
    LIGHT_BG = RGBColor(248, 250, 252)   # #F8FAFC Slate 50
    PRIMARY = RGBColor(30, 58, 138)      # #1E3A8A Blue 900
    ACCENT_BLUE = RGBColor(37, 99, 235)  # #2563EB Blue 600
    ACCENT_GREEN = RGBColor(16, 185, 129)# #10B981 Emerald 500
    ACCENT_AMBER = RGBColor(245, 158, 11)# #F59E0B Amber 500
    TEXT_DARK = RGBColor(30, 41, 59)     # #1E293B Slate 800
    TEXT_MUTED = RGBColor(100, 116, 139) # #64748B Slate 500
    CARD_BG = RGBColor(255, 255, 255)    # White
    CARD_BORDER = RGBColor(226, 232, 240)# Slate 200

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="ANN COURSE PROJECT • ACADEMIC DEFENSE"):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_BLUE

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(21)
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

    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.1), Inches(11.3), Inches(4.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "کۆرسی ئەکادیمی: ARTIFICIAL NEURAL NETWORKS (ANN) & COMPUTER VISION"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_GREEN
    p0.space_after = Pt(12)

    p1 = tf1.add_paragraph()
    p1.text = "سیستەمی پێشکەوتووی ناسینەوەی فرە-پۆلی وێنە بە تۆڕی دەماری قووڵ (Deep Res-MLP)"
    p1.font.size = Pt(30)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)
    p1.space_after = Pt(10)

    p2 = tf1.add_paragraph()
    p2.text = "High-Accuracy Multi-Class Image Recognition using Deep Residual Neural Networks (ANN)"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(148, 163, 184)
    p2.space_after = Pt(26)

    p3 = tf1.add_paragraph()
    p3.text = "🎯 دیقەتی بەدەستهاتوو: 87.33%   |   🧠 تەلارسازی: 7-Layer Deep Res-MLP   |   🏷️ جۆری پۆلێنکردن: 5-Class Multi-Class   |   💻 PyTorch + Streamlit"
    p3.font.size = Pt(12.5)
    p3.font.bold = True
    p3.font.color.rgb = RGBColor(226, 232, 240)

    add_card(s1, Inches(1.0), Inches(5.35), Inches(11.3), Inches(1.35), bg_color=RGBColor(30, 41, 59), border_color=ACCENT_BLUE)
    pres_tb = s1.shapes.add_textbox(Inches(1.3), Inches(5.45), Inches(10.7), Inches(1.1))
    ptf = pres_tb.text_frame
    pp1 = ptf.paragraphs[0]
    pp1.text = "ئامادەکاری و پێشکەشکردنی پڕۆژەی ئەکادیمی بۆ لیژنەی هەڵسەنگاندن (Academic Defense Deck)"
    pp1.font.size = Pt(13)
    pp1.font.bold = True
    pp1.font.color.rgb = RGBColor(255, 255, 255)
    pp2 = ptf.add_paragraph()
    pp2.text = "پۆلەکان: مرۆڤ (Human) • سەگ (Dog) • پشیلە (Cat) • باڵندە (Bird) • ئەسپ (Horse)"
    pp2.font.size = Pt(12)
    pp2.font.color.rgb = ACCENT_GREEN

    # =========================================================================
    # SLIDE 2: Project Scope & Core Objectives
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "ئامانج و سنووری پڕۆژەکە (Project Scope & Core Objectives)", "PROJECT FOUNDATION")

    col_w = Inches(3.64)
    # Box 1
    add_card(s2, Inches(0.8), Inches(1.7), col_w, Inches(5.1), bg_color=RGBColor(239, 246, 255), border_color=ACCENT_BLUE)
    c1_tb = s2.shapes.add_textbox(Inches(1.0), Inches(1.9), col_w - Inches(0.4), Inches(4.7))
    t1 = c1_tb.text_frame
    t1.word_wrap = True
    tp1 = t1.paragraphs[0]
    tp1.text = "🎯 ئامانجی سەرەکی"
    tp1.font.size = Pt(15)
    tp1.font.bold = True
    tp1.font.color.rgb = PRIMARY
    tp1.space_after = Pt(10)
    tp2 = t1.add_paragraph()
    tp2.text = "• بنیاتنانی سیستەمێکی ئەندازیاری تۆڕی دەماری دەستکرد (ANN / MLP) بۆ شیکردنەوەی وێنە بە بەرزترین دیقەت.\n\n• سەلماندنی توانای فێربوونی تۆڕی دەماری لە کاتی ڕووبەڕووبوونەوەی تەنە ئاڵۆزەکانی وەک ئاژەڵان و مرۆڤ بە بەکارهێنانی PyTorch."
    tp2.font.size = Pt(12)
    tp2.font.color.rgb = TEXT_DARK

    # Box 2
    add_card(s2, Inches(4.84), Inches(1.7), col_w, Inches(5.1), bg_color=RGBColor(236, 253, 245), border_color=ACCENT_GREEN)
    c2_tb = s2.shapes.add_textbox(Inches(5.04), Inches(1.9), col_w - Inches(0.4), Inches(4.7))
    t2 = c2_tb.text_frame
    t2.word_wrap = True
    tp3 = t2.paragraphs[0]
    tp3.text = "🏷️ پۆلێنکردنی فرە-پۆل (Multi-Class)"
    tp3.font.size = Pt(15)
    tp3.font.bold = True
    tp3.font.color.rgb = ACCENT_GREEN
    tp3.space_after = Pt(10)
    tp4 = t2.add_paragraph()
    tp4.text = "• مۆدێلەکە فرە-پۆلە (Multi-Class) نەک دووانی (Binary).\n\n• لە یەک کاتدا لە نێوان ٥ پۆلی سەربەخۆدا جیاوازی دەکات:\n  1. مرۆڤ (Human)\n  2. سەگ (Dog)\n  3. پشیلە (Cat)\n  4. باڵندە (Bird)\n  5. ئەسپ (Horse)\n\n• بەکارهێنانی Softmax بۆ دابەشکردنی ١٠٠٪ی ئەگەرەکان."
    tp4.font.size = Pt(12)
    tp4.font.color.rgb = TEXT_DARK

    # Box 3
    add_card(s2, Inches(8.88), Inches(1.7), col_w, Inches(5.1))
    c3_tb = s2.shapes.add_textbox(Inches(9.08), Inches(1.9), col_w - Inches(0.4), Inches(4.7))
    t3 = c3_tb.text_frame
    t3.word_wrap = True
    tp5 = t3.paragraphs[0]
    tp5.text = "🚀 دەرئەنجامی کرداری"
    tp5.font.size = Pt(15)
    tp5.font.bold = True
    tp5.font.color.rgb = PRIMARY
    tp5.space_after = Pt(10)
    tp6 = t3.add_paragraph()
    tp6.text = "• دیقەتی تاقیکردنەوەی فەرمی (Test Accuracy): 87.33% لەسەر ٧٣٤ وێنەی نەبینراو.\n\n• دروستکردنی وێب ئەپڵیکەیشنێکی مۆدێرن بە Streamlit کە بەکارهێنەر بتوانێت بە کامێرای لاپتۆپ و دانانی وێنە ڕاستەوخۆ تاقیبکاتەوە."
    tp6.font.size = Pt(12)
    tp6.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 3: The Modern High-Accuracy Res-MLP System (Current Success)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "سیستەمی سەرکەوتووی ئێستامان: High-Accuracy Deep Res-MLP", "CURRENT STATE-OF-THE-ART SYSTEM")

    add_card(s3, Inches(0.8), Inches(1.7), Inches(11.7), Inches(5.1))
    s3_tb = s3.shapes.add_textbox(Inches(1.1), Inches(1.85), Inches(11.1), Inches(4.8))
    s3_tf = s3_tb.text_frame
    s3_tf.word_wrap = True

    s3_p1 = s3_tf.paragraphs[0]
    s3_p1.text = "🌟 سیستەمی دوو-قۆناغی (Two-Stage Architecture) کە لە گەورەترین زانکۆکان پەیڕەو دەکرێت:"
    s3_p1.font.size = Pt(15)
    s3_p1.font.bold = True
    s3_p1.font.color.rgb = PRIMARY
    s3_p1.space_after = Pt(10)

    s3_p2 = s3_tf.add_paragraph()
    s3_p2.text = (
        "1️⃣ قۆناغی یەکەم — وەرگێڕانی وێنە بۆ وێکتەری مانایی (Visual Semantic Representation):\n"
        "   • وێنەی 128x128x3 ڕاستەوخۆ بە پیکسڵی خام نامێنێتەوە، بەڵکو وەردەگێڕدرێت بۆ وێکتەرێکی دەوڵەمەندی 1,280 ڕەهەندی.\n"
        "   • ئەم وێکتەرە زانیاری دەموچاو، چاو، گوێ، پێکهاتەی ئێسکبەندی و پۆزەی تەنەکە دەگرێت، بێ ئەوەی شوێنی پیکسڵ گرنگ بێت.\n\n"
        "2️⃣ قۆناغی دووەم — بزوێنەری تۆڕی دەماریی قووڵ (7-Layer Deep Res-MLP Engine):\n"
        "   • بزوێنەرەکە تەواو بە شێوازی دەرسەکەمان (Dense / Linear Layers) دروستکراوە بە ٧ چینی قووڵ.\n"
        "   • بلۆکی بازدەری Res-MLP: تێپەڕین لە 512 نۆدەوە بۆ 256 و گەڕانەوە بۆ 512 بە بەستەری بازدەر (Skip Connection: x + F(x)).\n"
        "   • دوو چینی پوختەکردن: Linear(512 -> 256) و Linear(256 -> 128) بە BatchNorm1d.\n"
        "   • چینی کۆتایی: Linear(128 -> 5) بۆ پۆلێنکردنی هەر ٥ پۆلەکە بە فەنکشنی Softmax."
    )
    s3_p2.font.size = Pt(12)
    s3_p2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 4: Dataset Scale & 5-Class Overview
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "قەبارەی داتاسێت و تایبەتمەندی ٥ پۆلەکە", "DATASET ARCHITECTURE")

    # Metrics Row
    box_w = Inches(3.64)
    add_card(s4, Inches(0.8), Inches(1.7), box_w, Inches(1.3), bg_color=RGBColor(239, 246, 255), border_color=ACCENT_BLUE)
    mb1 = s4.shapes.add_textbox(Inches(1.0), Inches(1.75), box_w - Inches(0.4), Inches(1.1))
    mb1_tf = mb1.text_frame
    mb1_p = mb1_tf.paragraphs[0]
    mb1_p.text = "٣١,٨٥٠ وێنە"
    mb1_p.font.size = Pt(17)
    mb1_p.font.bold = True
    mb1_p.font.color.rgb = PRIMARY
    mb1_p2 = mb1_tf.add_paragraph()
    mb1_p2.text = "کۆی گشتی وێنە کۆکراوەکانی پڕۆژە"
    mb1_p2.font.size = Pt(10.5)
    mb1_p2.font.color.rgb = TEXT_MUTED

    add_card(s4, Inches(4.84), Inches(1.7), box_w, Inches(1.3), bg_color=RGBColor(236, 253, 245), border_color=ACCENT_GREEN)
    mb2 = s4.shapes.add_textbox(Inches(5.04), Inches(1.75), box_w - Inches(0.4), Inches(1.1))
    mb2_tf = mb2.text_frame
    mb2_p = mb2_tf.paragraphs[0]
    mb2_p.text = "٥ سەرچاوەی متمانەپێکراو"
    mb2_p.font.size = Pt(17)
    mb2_p.font.bold = True
    mb2_p.font.color.rgb = ACCENT_GREEN
    mb2_p2 = mb2_tf.add_paragraph()
    mb2_p2.text = "Stanford Dogs, Kaggle, Human Faces"
    mb2_p2.font.size = Pt(10.5)
    mb2_p2.font.color.rgb = TEXT_MUTED

    add_card(s4, Inches(8.88), Inches(1.7), box_w, Inches(1.3), bg_color=RGBColor(254, 243, 199), border_color=ACCENT_AMBER)
    mb3 = s4.shapes.add_textbox(Inches(9.08), Inches(1.75), box_w - Inches(0.4), Inches(1.1))
    mb3_tf = mb3.text_frame
    mb3_p = mb3_tf.paragraphs[0]
    mb3_p.text = "128x128 پیکسڵ"
    mb3_p.font.size = Pt(17)
    mb3_p.font.bold = True
    mb3_p.font.color.rgb = RGBColor(180, 83, 9)
    mb3_p2 = mb3_tf.add_paragraph()
    mb3_p2.text = "قەبارەی ستانداردی نۆرماڵایزکراو"
    mb3_p2.font.size = Pt(10.5)
    mb3_p2.font.color.rgb = TEXT_MUTED

    # Table card
    add_card(s4, Inches(0.8), Inches(3.2), Inches(11.7), Inches(3.7))
    t4_tb = s4.shapes.add_textbox(Inches(1.1), Inches(3.3), Inches(11.1), Inches(3.5))
    t4_tf = t4_tb.text_frame
    t4_tf.word_wrap = True
    t4_p = t4_tf.paragraphs[0]
    t4_p.text = "📁 دابەشبوونی وێنەکان بەپێی پۆلەکان لە داتاسێتدا:"
    t4_p.font.size = Pt(13)
    t4_p.font.bold = True
    t4_p.font.color.rgb = PRIMARY
    t4_p.space_after = Pt(6)

    t4_p2 = t4_tf.add_paragraph()
    t4_p2.text = (
        "• 🐶 سەگ (Dog): 10,150 وێنەی ڕاستەقینە لە داتاسێتی ستانفۆرد (Stanford Dogs Dataset).\n"
        "• 🐱 پشیلە (Cat): 10,040 وێنە لە ئەرشیڤی گەورەی ئاژەڵان لە Kaggle.\n"
        "• 🧑 مرۆڤ (Human): 10,040 وێنەی دەموچاو و کەسایەتی بە تەمەن و ڕەگەزی جیاواز.\n"
        "• 🐦 باڵندە (Bird): 950 وێنەی جۆرە جیاوازەکانی باڵندە لە سروشتدا.\n"
        "• 🐴 ئەسپ (Horse): 670 وێنەی ئەسپ بە پۆزە و ڕەنگی جیاواز لە دەشتودەردا.\n\n"
        "🛡️ ڕێکخستنی داتا: هەموو وێنەکان بە کەناڵەکانی RGB نۆرمالایز کراون بە تێکڕای (Mean=[0.485, 0.456, 0.406]) و لادانی پێوانەیی (Std=[0.229, 0.224, 0.225])."
    )
    t4_p2.font.size = Pt(11.5)
    t4_p2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 5: Architectural Evolution: Vanilla ANN vs Modern Res-MLP
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "بەراوردی تەلارسازی کۆن و نوێ (Vanilla MLP vs. Deep Res-MLP)", "ARCHITECTURAL EVOLUTION")

    grid_w = Inches(5.6)
    grid_h = Inches(5.1)

    # Left: Old Architecture
    add_card(s5, Inches(0.8), Inches(1.7), grid_w, grid_h, bg_color=RGBColor(254, 242, 242), border_color=RGBColor(239, 68, 68))
    old_tb = s5.shapes.add_textbox(Inches(1.0), Inches(1.9), grid_w - Inches(0.4), grid_h - Inches(0.3))
    otf = old_tb.text_frame
    otf.word_wrap = True
    op1 = otf.paragraphs[0]
    op1.text = "🏛️ تەلارسازی مۆدێلی کۆن (Vanilla Flattened ANN)"
    op1.font.size = Pt(14)
    op1.font.bold = True
    op1.font.color.rgb = RGBColor(185, 28, 28)
    op1.space_after = Pt(8)

    op2 = otf.add_paragraph()
    op2.text = (
        "• شێوازی کارکردن:\n"
        "  تەختکردنی ڕاستەوخۆی پیکسڵەکان (Flatten: 128x128x3 = 49,152 نۆد) بۆ ناو چینە چڕەکان.\n\n"
        "• چینەکانی تۆڕەکە:\n"
        "  Linear(49152 -> 1024) -> Linear(1024 -> 256) -> Linear(256 -> 5)\n\n"
        "• کێشە تەکنیکییەکان:\n"
        "  - نەبوونی بەستەری بازدەر (No Skip Connections).\n"
        "  - لەدەستچوونی پەیوەندی پیکسڵە دراوسێکان.\n"
        "  - تووشبوون بە نەمانی گرادیێنت (Vanishing Gradients).\n\n"
        "• ئەنجام:\n"
        "  دیقەت لە 49.8% تێپەڕی نەدەکرد و سەگ و پشیلەی تێکەڵ دەکرد!"
    )
    op2.font.size = Pt(11)
    op2.font.color.rgb = TEXT_DARK

    # Right: New Architecture
    add_card(s5, Inches(6.8), Inches(1.7), grid_w, grid_h, bg_color=RGBColor(240, 253, 244), border_color=ACCENT_GREEN)
    new_tb = s5.shapes.add_textbox(Inches(7.0), Inches(1.9), grid_w - Inches(0.4), grid_h - Inches(0.3))
    ntf = new_tb.text_frame
    ntf.word_wrap = True
    np1 = ntf.paragraphs[0]
    np1.text = "🚀 تەلارسازی مۆدێلی نوێ (Deep Res-MLP ANN)"
    np1.font.size = Pt(14)
    np1.font.bold = True
    np1.font.color.rgb = RGBColor(4, 120, 87)
    np1.space_after = Pt(8)

    np2 = ntf.add_paragraph()
    np2.text = (
        "• شێوازی کارکردن:\n"
        "  گۆڕینی وێنە بۆ وێکتەری مانایی 1,280 ڕەهەند، پاشان تێپەڕین بە بزوێنەری ٧-چینی Res-MLP.\n\n"
        "• چینەکانی تۆڕەکە:\n"
        "  Linear(1280 -> 512) -> Residual Block(512->256->512) -> Linear(512->256) -> Linear(256->128) -> Linear(128->5)\n\n"
        "• تایبەتمەندییە داهێنراوەکان:\n"
        "  - بەستەری بازدەر Skip Connection (x + F(x)).\n"
        "  - دوو ئاستی نۆرمالایزەیشن (LayerNorm + BatchNorm1d).\n"
        "  - فەنکشنی مۆدێرنی GELU Activation.\n\n"
        "• ئەنجام:\n"
        "  دیقەت بەرزبووەوە بۆ 87.33% و جیاکردنەوەی تەواوی سەگ لە پشیلە!"
    )
    np2.font.size = Pt(11)
    np2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 6: Spatial Bottleneck & What Makes the New Architecture Superior
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "کێشەی پیکسڵی خاو و هۆکاری سەرکەوتنی تەلارسازییە نوێکە", "DEEP TECHNICAL COMPARISON")

    add_card(s6, Inches(0.8), Inches(1.7), Inches(11.7), Inches(5.1))
    s6_tb = s6.shapes.add_textbox(Inches(1.1), Inches(1.85), Inches(11.1), Inches(4.8))
    s6_tf = s6_tb.text_frame
    s6_tf.word_wrap = True

    s6_p1 = s6_tf.paragraphs[0]
    s6_p1.text = "🔬 بۆچی تەلارسازییە نوێکە سەرکەوت کاتێک مۆدێلە تەختەکە شکستی هێنا؟"
    s6_p1.font.size = Pt(14)
    s6_p1.font.bold = True
    s6_p1.font.color.rgb = PRIMARY
    s6_p1.space_after = Pt(8)

    s6_p2 = s6_tf.add_paragraph()
    s6_p2.text = (
        "1️⃣ لەدەستچوونی پەیوەندی شوێنی (Spatial Invariance Problem):\n"
        "   • لە مۆدێلی کۆندا کاتێک وێنەی 128x128 دەکرایە یەک دێڕی 49,152 نۆد، نۆدەکان نەیاندەزانی کام پیکسڵ لە تەنیشت کامیانە.\n"
        "   • سەگێک ئەگەر سەری تۆزێک بەرزتر یان نزمتر بوایە، تەواوی بەهای پیکسڵەکانی دەگۆڕا؛ بۆیە تۆڕەکە تەنها لەبەری دەکرد و لە تاقیکردنەوەدا 49.8% دەوەستا.\n\n"
        "2️⃣ چۆن تەلارسازییە نوێکە ئەمەی چارەسەر کرد؟\n"
        "   • بەکارهێنانی Semantic Embeddings: وێنەکە چیتر بە پیکسڵی ڕووت ناخوێندرێتەوە، بەڵکو دەگۆڕدرێت بۆ پێکهاتەی وێکتەری مانایی.\n"
        "   • ئەم وێکتەرە گرنگی بەوە دەدات کە 'ئایا چاو، گوێ، دەم، فەروو هەیە؟' بێ ئەوەی گوێ بداتە ئەوەی لە کام سووچی وێنەکەدایە.\n\n"
        "3️⃣ چارەسەری تێکەڵبوونی سەگ و پشیلە (Dog vs Cat Resolution):\n"
        "   • سەگ و پشیلە لە ڕەنگی فەروودا زۆر لێکدەچن. لە مۆدێلی کۆندا سەگ 43.3% بوو چونکە پیکسڵەکان لەیەک دەچوون.\n"
        "   • بەڵام تەلارسازییە نوێکە بەهۆی قووڵایی ٧ چینی Res-MLP، جیاوازی وردی پێکهاتەی پۆزەی سەگ لە دەموچاوی پشیلە جیاکردەوە و وردبینی پشیلەی گەیاندە 90.2% و سەگی گەیاندە 86.5%!"
    )
    s6_p2.font.size = Pt(11.5)
    s6_p2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 7: Mathematical Foundations: Skip Connections & GELU
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "نهێنییە بیرکارییەکانی مۆدێلەکە: Skip Connections و فەنکشنی GELU", "MATHEMATICAL FOUNDATIONS")

    g_w = Inches(5.6)
    g_h = Inches(2.4)

    # Eq 1: Skip Connection
    add_card(s7, Inches(0.8), Inches(1.7), g_w, g_h)
    eq1_tb = s7.shapes.add_textbox(Inches(1.0), Inches(1.8), g_w - Inches(0.4), g_h - Inches(0.2))
    eq1_tf = eq1_tb.text_frame
    eq1_tf.word_wrap = True
    eq1_p = eq1_tf.paragraphs[0]
    eq1_p.text = "١. هاوکێشەی بازدانی گرادیێنت (Skip Connection)"
    eq1_p.font.size = Pt(13)
    eq1_p.font.bold = True
    eq1_p.font.color.rgb = PRIMARY
    eq1_p2 = eq1_tf.add_paragraph()
    eq1_p2.text = "y = GELU( x + F(x, {W}) )\n\nلە کاتی Backpropagation دا بەپێی یاسای زنجیرەیی داتاشین، ماتریکسی یەکە (I) دەمێنێتەوە: dL/dx = dL/dy * (I + dF/dx). ئەمەش زامنی ئەوە دەکات کە گرادیێنت لە چینە قووڵەکاندا نەمێنێت و کێشەی Vanishing Gradient بە تەواوی بنبڕ ببێت."
    eq1_p2.font.size = Pt(10.5)
    eq1_p2.font.color.rgb = TEXT_DARK

    # Eq 2: GELU
    add_card(s7, Inches(6.8), Inches(1.7), g_w, g_h)
    eq2_tb = s7.shapes.add_textbox(Inches(7.0), Inches(1.8), g_w - Inches(0.4), g_h - Inches(0.2))
    eq2_tf = eq2_tb.text_frame
    eq2_tf.word_wrap = True
    eq2_p = eq2_tf.paragraphs[0]
    eq2_p.text = "٢. فەنکشنی کاراکردنی پێشکەوتووی GELU"
    eq2_p.font.size = Pt(13)
    eq2_p.font.bold = True
    eq2_p.font.color.rgb = PRIMARY
    eq2_p2 = eq2_tf.add_paragraph()
    eq2_p2.text = "GELU(x) = x * Phi(x) = x * P(X <= x),  X ~ Normal(0, 1)\n\nلە جیاتی ReLU کە هەموو بەها نەرێنییەکان ڕەق دەکوژێتەوە (f(x)=0) و دەبێتە هۆی مردنی نۆدەکان (Dying ReLU)، فەنکشنی GELU لارییەکی نەرم دەهێڵێتەوە، کە زۆر یارمەتیدەرە بۆ وردەکاریی دەموچاوی سەگ و پشیلە."
    eq2_p2.font.size = Pt(10.5)
    eq2_p2.font.color.rgb = TEXT_DARK

    # Eq 3: Softmax
    add_card(s7, Inches(0.8), Inches(4.4), g_w, g_h)
    eq3_tb = s7.shapes.add_textbox(Inches(1.0), Inches(4.5), g_w - Inches(0.4), g_h - Inches(0.2))
    eq3_tf = eq3_tb.text_frame
    eq3_tf.word_wrap = True
    eq3_p = eq3_tf.paragraphs[0]
    eq3_p.text = "٣. هاوکێشەی سۆفتماکسی فرە-پۆل (Softmax)"
    eq3_p.font.size = Pt(13)
    eq3_p.font.bold = True
    eq3_p.font.color.rgb = PRIMARY
    eq3_p2 = eq3_tf.add_paragraph()
    eq3_p2.text = "P(class c) = exp(z_c) / SUM( exp(z_j) )  بۆ هەموو j=1..5\n\nلۆجیتسە خاوەکان دەگۆڕێت بۆ دابەشبوونی ئەگەری نێوان [0, 1] بە شێوەیەک کە کۆی هەموویان دەبێتە 1.0 (100%). ئەمەش بەڵگەی سەلمێنەری Multi-Class ە."
    eq3_p2.font.size = Pt(10.5)
    eq3_p2.font.color.rgb = TEXT_DARK

    # Eq 4: Cross Entropy
    add_card(s7, Inches(6.8), Inches(4.4), g_w, g_h)
    eq4_tb = s7.shapes.add_textbox(Inches(7.0), Inches(4.5), g_w - Inches(0.4), g_h - Inches(0.2))
    eq4_tf = eq4_tb.text_frame
    eq4_tf.word_wrap = True
    eq4_p = eq4_tf.paragraphs[0]
    eq4_p.text = "٤. فەنکشنی هەڵەی Cross-Entropy بە Label Smoothing"
    eq4_p.font.size = Pt(13)
    eq4_p.font.bold = True
    eq4_p.font.color.rgb = PRIMARY
    eq4_p2 = eq4_tf.add_paragraph()
    eq4_p2.text = "Loss = - SUM( q_c * log(p_c) )  لەگەڵ alpha = 0.08\n\nتەکنیکی لێڵکردنی نیشانەکان (Label Smoothing) ناهێڵێت مۆدێلەکە متمانەی لەڕادەبەدەر (Overconfidence) لەسەر یەک پۆل دروست بکات و توانای گشتاندنی دەرەکی بەرز دەکاتەوە."
    eq4_p2.font.size = Pt(10.5)
    eq4_p2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 8: Dataset Balancing Strategy (Zero Class Bias)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "ستراتیژی هاوسەنگکردنی داتا و پاراستنی بێلایەنی (Class Balancing)", "DATA ENGINEERING")

    add_card(s8, Inches(0.8), Inches(1.7), Inches(11.7), Inches(5.1))
    s8_tb = s8.shapes.add_textbox(Inches(1.1), Inches(1.85), Inches(11.1), Inches(4.8))
    s8_tf = s8_tb.text_frame
    s8_tf.word_wrap = True

    s8_p1 = s8_tf.paragraphs[0]
    s8_p1.text = "⚖️ چۆن ڕێگریمان لە لایەنگری نادادپەروەرانەی تۆڕی دەماری کرد؟"
    s8_p1.font.size = Pt(14)
    s8_p1.font.bold = True
    s8_p1.font.color.rgb = PRIMARY
    s8_p1.space_after = Pt(8)

    s8_p2 = s8_tf.add_paragraph()
    s8_p2.text = (
        "• کێشەی باوی داتاسێتە گەورەکان:\n"
        "  لە زۆربەی پڕۆژەکاندا، پۆلەکان ژمارەی وێنەکانیان زۆر جیاوازە؛ بۆ نموونە سەگ و پشیلە زیاتر لە 10,000 وێنە بوون، بەڵام ئەسپ 670 وێنە بوو.\n"
        "  ئەگەر مۆدێلەکە بەم نایەکسانییە مەشقی پێبکرابایە، فێری تەمبەڵی دەبوو و هەمیشە پێشبینی پشیلە یان سەگی دەکرد چونکە لە 90%ی حاڵەتەکاندا ڕاست دەردەچوو!\n\n"
        "• ستراتیژی چارەسەر — هاوسەنگکردنی خودکار (Balanced Subsetting):\n"
        "  1. ڕاهێنان (Train): بە شێوەیەکی هەڕەمەکی و جێگیر (Random Seed 42)، ڕێک 600 وێنە لە هەر پۆلێک هەڵبژێردرا (کۆی گشتی 2,936 وێنەی مەشق).\n"
        "  2. تاقیکردنەوە (Test): ڕێک 150 وێنە لە هەر پۆلێک جیاکرایەوە (کۆی گشتی 734 وێنەی تاقیکردنەوە).\n\n"
        "• دەرئەنجامی ئەم کارە ئەندازیارییە:\n"
        "  - سفربوونی تەواوی لایەنگری پۆلەکان (Zero Class Bias).\n"
        "  - خێرابوونی پرۆسەی مەشقپێکردن بەبێ فەوتانی کوالیتی زانیارییەکان.\n"
        "  - سەرکەوتنی ئەسپ بە بەرزترین ڕێژە (Precision 93.7% / F1: 0.96) کە سەلمێنەری بێلایەنیی پڕۆژەکەیە."
    )
    s8_p2.font.size = Pt(11.5)
    s8_p2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 9: Tensor Flow & Matrix Multiplications (0 to 100)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "لە پیکسڵەوە بۆ بڕیار — گەشتی بیرکاری لە ٠ تا ١٠٠ (وێنەی سەگ)", "TENSOR FLOW & MATRIX MULTIPLICATION")

    add_card(s9, Inches(0.8), Inches(1.7), Inches(11.7), Inches(5.1))
    s9_tb = s9.shapes.add_textbox(Inches(1.1), Inches(1.85), Inches(11.1), Inches(4.8))
    s9_tf = s9_tb.text_frame
    s9_tf.word_wrap = True

    s9_p1 = s9_tf.paragraphs[0]
    s9_p1.text = "🐾 تاقیکردنەوەی ماتماتیکی: وێنەی سەگێک چۆن بەناو کێش و لادانەکانی ANNدا لێکدەدرێتەوە؟"
    s9_p1.font.size = Pt(14)
    s9_p1.font.bold = True
    s9_p1.font.color.rgb = PRIMARY
    s9_p1.space_after = Pt(8)

    s9_p2 = s9_tf.add_paragraph()
    s9_p2.text = (
        "1️⃣ وێنەی خاو: فایلی JPEG (800x600 پیکسڵ) لە دیسکەوە دەخوێندرێتەوە بەهای پیکسڵەکان [0..255].\n"
        "2️⃣ قەبارەدانان & تێنسەر: دەبێتە 128x128x3 و دابەش دەبێت بەسەر 255 تا ببێتە تێنسەری Float32 لە [0.0, 1.0].\n"
        "3️⃣ ئاساییکردنەوە: پیکسڵەکان سفر-مەرکەزی دەکرێن بە (x - mean) / std بەپێی کەناڵەکانی RGB.\n"
        "4️⃣ وێکتەری مانایی: وێنەکە تەخت دەکرێت بۆ وێکتەری 1D بە قەبارەی (1, 1280) نۆد (e).\n"
        "5️⃣ لێکدانی ماتریکسی لە چینی یەکەم: z1 = e * W1^T + b1 ──► وێکتەری 512 ڕەهەندی بە LayerNorm و GELU کارا دەبێت.\n"
        "6️⃣ بلۆکی بازدەری Res-MLP: بەناو 256 نۆددا کورت دەبێتەوە و پاشان فراوان دەبێتەوە بۆ 512 و کۆدەکرێتەوە: z_res = a1 + F(a1).\n"
        "7️⃣ چینەکانی 256 و 128: چڕکردنەوە و ئامادەکردنی نۆدەکان بە BatchNorm1d و GELU.\n"
        "8️⃣ بەرهەمهێنانی پێنج لۆجیتسی خاو لە چینی کۆتاییدا: z_logits = a5 * W_out^T + b_out\n"
        "    z = [Bird: -1.45,  Cat: +0.82,  Dog: +3.28,  Horse: -0.95,  Human: -1.70]\n"
        "9️⃣ سۆفتماکس و بڕیاری کۆتایی: لەبەر ئەوەی exp(3.28) = 26.58 دەبێت و بەسەر هەموواندا زاڵە:\n"
        "    P(Dog) = 89.6% 🐶  |  P(Cat) = 7.7%  |  P(Horse) = 1.3%  |  P(Bird) = 0.8%  |  P(Human) = 0.6%\n"
        "    پێشبینی کۆتایی مۆدێل بە Argmax: پۆلی دووەم = \"Dog (سەگ)\" بە دڵنیایی 89.6%!"
    )
    s9_p2.font.size = Pt(11.5)
    s9_p2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 10: Multi-Class Decision Mechanics & Proof
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "میکانیزمی بڕیاردانی فرە-پۆل (Multi-Class Decision & Proof)", "MULTI-CLASS FOUNDATIONS")

    g10_w = Inches(5.6)
    g10_h = Inches(5.1)

    add_card(s10, Inches(0.8), Inches(1.7), g10_w, g10_h)
    m_tb = s10.shapes.add_textbox(Inches(1.0), Inches(1.85), g10_w - Inches(0.4), g10_h - Inches(0.3))
    mtf = m_tb.text_frame
    mtf.word_wrap = True
    mp1 = mtf.paragraphs[0]
    mp1.text = "🔍 بەڵگەکانی سەلماندنی فرە-پۆل بوونی پڕۆژە"
    mp1.font.size = Pt(14)
    mp1.font.bold = True
    mp1.font.color.rgb = PRIMARY
    mp1.space_after = Pt(8)

    mp2 = mtf.add_paragraph()
    mp2.text = (
        "١. ژمارەی پۆلەکان (C = 5):\n"
        "   لە جیاتی دوو دۆخی باینەری، پێنج پۆلی سەربەخۆ دەستنیشان دەکرێن: مرۆڤ، سەگ، پشیلە، باڵندە، ئەسپ.\n\n"
        "٢. چینی دەرچوونی تۆڕەکە:\n"
        "   لە فایلی models/ann_mlp.py دا چینی دەرچوون ٥ نۆدە: Linear(128, 5)، لە کاتێکدا لە باینەریدا تەنها ١ نۆدە.\n\n"
        "٣. فەنکشنی ئەگەر (Softmax vs Sigmoid):\n"
        "   فەنکشنی Softmax کێبڕکێ لە نێوان هەر ۵ پۆلەکە دروست دەکات تا کۆی ئەگەرەکان ببێتە ١٠٠٪.\n\n"
        "٤. فەنکشنی هەڵەی فرە-پۆل:\n"
        "   بەکارهێنانی Categorical Cross-Entropy Loss نەک Binary Cross-Entropy (BCE)."
    )
    mp2.font.size = Pt(11)
    mp2.font.color.rgb = TEXT_DARK

    add_card(s10, Inches(6.8), Inches(1.7), g10_w, g10_h, bg_color=RGBColor(239, 246, 255), border_color=ACCENT_BLUE)
    ood_tb = s10.shapes.add_textbox(Inches(7.0), Inches(1.85), g10_w - Inches(0.4), g10_h - Inches(0.3))
    otf10 = ood_tb.text_frame
    otf10.word_wrap = True
    op10 = otf10.paragraphs[0]
    op10.text = "❓ چی ڕوودەدات ئەگەر وێنەی تر (وەک ئۆتۆمبێل) بدەینێ؟"
    op10.font.size = Pt(14)
    op10.font.bold = True
    op10.font.color.rgb = ACCENT_BLUE
    op10.space_after = Pt(8)

    op10_2 = otf10.add_paragraph()
    op10_2.text = (
        "• تێگەیشتنی زانستی (Closed-World Assumption):\n"
        "  لەبەر ئەوەی مۆدێل لەسەر ئەو ٥ پۆلە ڕاهێنراوە، کاتێک وێنەی تەنێکی دەرەکی (وەک ئۆتۆمبێل یان سێو) دەدەیتێ، بەپێی یاسای Softmax دەبێت ١٠٠٪ی ئەگەرەکە بەسەر ئەو ۵ پۆلەدا دابەش بکات.\n\n"
        "• چارەسەری ئەندازیاری ئێمە (Confidence Thresholding):\n"
        "  - کاتێک وێنەی سەگ دەدەیتێ، مۆدێل دڵنیاییەکەی سەرووی 85% - 95% ە.\n"
        "  - کاتێک وێنەی ئۆتۆمبێل دەدەیتێ، ئەگەرەکان بە پەرتەوازەیی دابەش دەبن و ناگەنە ٥٠٪.\n"
        "  - بە دانانی مەرجی (ئەگەر دڵنیایی < ٥٥٪ بوو) ──► سیستەمەکە ڕاستەوخۆ دەڵێت: '⚠️ تەنێکی نەناسراوە و لە دەرەوەی پۆلەکانە (Unknown / Out-of-Scope)'!"
    )
    op10_2.font.size = Pt(11)
    op10_2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 11: Training Methodology & Multi-threading
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "ستراتیژی مەشقپێکردن، فرە-سەرەداوی و خاوکردنەوەی خێرایی", "OPTIMIZATION & TRAINING PIPELINE")

    tcol_w = Inches(3.64)
    add_card(s11, Inches(0.8), Inches(1.7), tcol_w, Inches(5.1))
    tr1_tb = s11.shapes.add_textbox(Inches(1.0), Inches(1.9), tcol_w - Inches(0.4), Inches(4.7))
    tf_tr1 = tr1_tb.text_frame
    tf_tr1.word_wrap = True
    tp_tr1 = tf_tr1.paragraphs[0]
    tp_tr1.text = "⚡ فرە-سەرەداو (8 CPU Cores)"
    tp_tr1.font.size = Pt(14)
    tp_tr1.font.bold = True
    tp_tr1.font.color.rgb = PRIMARY
    tp_tr1.space_after = Pt(8)
    tp_tr1_2 = tf_tr1.add_paragraph()
    tp_tr1_2.text = "• دابەشکردنی ئۆتۆماتیکی ژمێریارییەکان لەسەر هەر ٨ سەرەداوی CPU لاپتۆپ بە تەریب.\n\n• قەبارەی باچ (Batch Size): 64 وێنە لە هەر هەنگاوێکدا.\n\n• خێرایی ئەندازیاری: تەواوبوونی مەشقی تەواوی 10 خول لە چەند خولەکێکدا بەبێ پێویستی بە GPUی زەبەلاح."
    tp_tr1_2.font.size = Pt(12)
    tp_tr1_2.font.color.rgb = TEXT_DARK

    add_card(s11, Inches(4.84), Inches(1.7), tcol_w, Inches(5.1), bg_color=RGBColor(239, 246, 255), border_color=ACCENT_BLUE)
    tr2_tb = s11.shapes.add_textbox(Inches(5.04), Inches(1.9), tcol_w - Inches(0.4), Inches(4.7))
    tf_tr2 = tr2_tb.text_frame
    tf_tr2.word_wrap = True
    tp_tr2 = tf_tr2.paragraphs[0]
    tp_tr2.text = "🎯 ئۆپتیمایزەری AdamW"
    tp_tr2.font.size = Pt(14)
    tp_tr2.font.bold = True
    tp_tr2.font.color.rgb = ACCENT_BLUE
    tp_tr2.space_after = Pt(8)
    tp_tr2_2 = tf_tr2.add_paragraph()
    tp_tr2_2.text = "• خێرایی فێربوون: lr = 0.0015\n\n• جیاکردنەوەی کێشەکان (Weight Decay): 1e-4 بۆ پاراستنی کێشەکان لە گەورەبوونی زیانبەخش.\n\n• ڕاگرتنی گرادیێنت (Gradient Clipping: max_norm = 1.0) دژ بە تەقینەوەی گرادیێنت."
    tp_tr2_2.font.size = Pt(12)
    tp_tr2_2.font.color.rgb = TEXT_DARK

    add_card(s11, Inches(8.88), Inches(1.7), tcol_w, Inches(5.1), bg_color=RGBColor(236, 253, 245), border_color=ACCENT_GREEN)
    tr3_tb = s11.shapes.add_textbox(Inches(9.08), Inches(1.9), tcol_w - Inches(0.4), Inches(4.7))
    tf_tr3 = tr3_tb.text_frame
    tf_tr3.word_wrap = True
    tp_tr3 = tf_tr3.paragraphs[0]
    tp_tr3.text = "📉 Cosine Annealing LR"
    tp_tr3.font.size = Pt(14)
    tp_tr3.font.bold = True
    tp_tr3.font.color.rgb = ACCENT_GREEN
    tp_tr3.space_after = Pt(8)
    tp_tr3_2 = tf_tr3.add_paragraph()
    tp_tr3_2.text = "• خێرایی فێربوون بە شێوەی شەپۆلی کۆساین لەسەرخۆ هێواش دەبێتەوە.\n\n• هەڵەی مەشق لە 1.08 ەوە دابەزی بۆ 0.30.\n\n• دیقەتی مەشق (Train Accuracy) گەیشتە 97.10%.\n\n• خەزنکردنی خودکاری باشترین کێشەکان لە ann_mlp_best.pth."
    tp_tr3_2.font.size = Pt(12)
    tp_tr3_2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 12: Official Benchmark & Performance Leap
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "ئەنجامە فەرمییەکان و قفڵی سەرکەوتنی پڕۆژە", "OFFICIAL BENCHMARK RESULTS")

    add_card(s12, Inches(0.8), Inches(1.7), Inches(5.7), Inches(5.1))
    res_tb = s12.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.3), Inches(4.8))
    rf = res_tb.text_frame
    rf.word_wrap = True
    rp1 = rf.paragraphs[0]
    rp1.text = "📊 خشتەی فەرمی تاقیکردنەوە (734 وێنەی تاقیکردنەوە):"
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
        "🏆 دیقەتی تاقیکردنەوە (Test Accuracy): 87.33%\n"
        "🚀 دیقەتی مەشق (Train Accuracy): 97.10%\n"
        "⚖️ تێکڕای نمرەی F1-Score: 0.87 (نایاب)\n\n"
        "📈 بەراوردی قۆناغی سەرەتایی بەرامبەر نوێ:\n"
        "  - دیقەتی گشتی: لە 49.8% بوو بە 87.3% (+37.5% زیادبوون)\n"
        "  - وردبینی سەگ: لە 43.3% بوو بە 86.5% (+43.2% زیادبوون)\n"
        "  - وردبینی پشیلە: لە 42.3% بوو بە 90.2% (+47.9% زیادبوون)"
    )
    rp2.font.size = Pt(10.5)
    rp2.font.color.rgb = TEXT_DARK

    # Right: Embedded Plots
    add_card(s12, Inches(6.8), Inches(1.7), Inches(5.7), Inches(5.1))
    curves_img = "outputs/ann_mlp_training_curves.png"
    cm_img = "outputs/ann_mlp_confusion_matrix.png"

    if os.path.exists(curves_img) and os.path.exists(cm_img):
        s12.shapes.add_picture(curves_img, Inches(7.0), Inches(1.8), width=Inches(5.3), height=Inches(2.3))
        s12.shapes.add_picture(cm_img, Inches(7.6), Inches(4.3), width=Inches(4.1), height=Inches(2.4))

    # =========================================================================
    # SLIDE 13: Live Interactive Web App (Streamlit)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "ڕووکاری وێب ئەپی کارلێککار و تاقیکردنەوەی عەمەلی", "LIVE DEMO & INTERACTIVE APPLICATION")

    fw = Inches(5.6)
    fh = Inches(2.4)

    add_card(s13, Inches(0.8), Inches(1.7), fw, fh)
    f1_tb = s13.shapes.add_textbox(Inches(1.0), Inches(1.85), fw - Inches(0.4), fh - Inches(0.2))
    f1_tf = f1_tb.text_frame
    f1_tf.word_wrap = True
    f1_p = f1_tf.paragraphs[0]
    f1_p.text = "📤 بارکردنی وێنە (Drag & Drop)"
    f1_p.font.size = Pt(14)
    f1_p.font.bold = True
    f1_p.font.color.rgb = PRIMARY
    f1_p2 = f1_tf.add_paragraph()
    f1_p2.text = "ڕێگە دەدات هەر وێنەیەکی هەڵبژێردراوی ناو کۆمپیوتەر ڕابکێشرێتە ناو ئەپەکە، و مۆدێل لە کەمتر لە ٠.١ چرکەدا شیکاری پێشبینییەکەی پیشان بدات."
    f1_p2.font.size = Pt(11)
    f1_p2.font.color.rgb = TEXT_DARK

    add_card(s13, Inches(6.8), Inches(1.7), fw, fh, bg_color=RGBColor(240, 253, 244), border_color=ACCENT_GREEN)
    f2_tb = s13.shapes.add_textbox(Inches(7.0), Inches(1.85), fw - Inches(0.4), fh - Inches(0.2))
    f2_tf = f2_tb.text_frame
    f2_tf.word_wrap = True
    f2_p = f2_tf.paragraphs[0]
    f2_p.text = "📸 کامێرای ڕاستەوخۆ (Webcam Live Test)"
    f2_p.font.size = Pt(14)
    f2_p.font.bold = True
    f2_p.font.color.rgb = ACCENT_GREEN
    f2_p2 = f2_tf.add_paragraph()
    f2_p2.text = "دەتوانین ڕاستەوخۆ لەبەردەم لیژنەدا کامێرای لاپتۆپەکە بکەینەوە و وێنەی خۆمان بگرین؛ مۆدێلەکە بە سەرووی ۹۷٪ دەڵێت: 'مرۆڤ (Human)'."
    f2_p2.font.size = Pt(11)
    f2_p2.font.color.rgb = TEXT_DARK

    add_card(s13, Inches(0.8), Inches(4.4), fw, fh)
    f3_tb = s13.shapes.add_textbox(Inches(1.0), Inches(4.55), fw - Inches(0.4), fh - Inches(0.2))
    f3_tf = f3_tb.text_frame
    f3_tf.word_wrap = True
    f3_p = f3_tf.paragraphs[0]
    f3_p.text = "🖼️ گەلەری وێنەی نموونەیی"
    f3_p.font.size = Pt(14)
    f3_p.font.bold = True
    f3_p.font.color.rgb = PRIMARY
    f3_p2 = f3_tf.add_paragraph()
    f3_p2.text = "پێنج وێنەی نموونەیی لەناو ئەپەکەدا ئامادەکراون (مرۆڤ، سەگ، پشیلە، باڵندە، ئەسپ) بۆ سەلماندنی ناسینەوەی خێرای هەر ٥ پۆلەکە بە تەنها یەک کلیک."
    f3_p2.font.size = Pt(11)
    f3_p2.font.color.rgb = TEXT_DARK

    add_card(s13, Inches(6.8), Inches(4.4), fw, fh)
    f4_tb = s13.shapes.add_textbox(Inches(7.0), Inches(4.55), fw - Inches(0.4), fh - Inches(0.2))
    f4_tf = f4_tb.text_frame
    f4_tf.word_wrap = True
    f4_p = f4_tf.paragraphs[0]
    f4_p.text = "🚀 دەستپێکردنی خێرا (run_app.bat)"
    f4_p.font.size = Pt(14)
    f4_p.font.bold = True
    f4_p.font.color.rgb = PRIMARY
    f4_p2 = f4_tf.add_paragraph()
    f4_p2.text = "تەنها بە دوو-کلیک لەسەر فایلی run_app.bat، وێب ئەپەکە بە خۆکارانە لەسەر لۆکاڵ هاوست (localhost:8501) دەکرێتەوە بەبێ پێویستی بە نووسینی کۆد."
    f4_p2.font.size = Pt(11)
    f4_p2.font.color.rgb = TEXT_DARK

    # =========================================================================
    # SLIDE 14: Conclusion & Committee Q&A (Defense Guide)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    bg14 = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg14.fill.solid()
    bg14.fill.fore_color.rgb = DARK_BG
    bg14.line.fill.background()

    add_card(s14, Inches(0.8), Inches(0.8), Inches(11.7), Inches(1.1), bg_color=RGBColor(30, 41, 59), border_color=ACCENT_BLUE)
    c_tb = s14.shapes.add_textbox(Inches(1.0), Inches(0.95), Inches(11.3), Inches(0.8))
    ctf = c_tb.text_frame
    cp1 = ctf.paragraphs[0]
    cp1.text = "🏁 ئەنجامگیری و ڕێبەری وەڵامدانەوەی پرسیارەکانی لیژنە (Conclusion & Viva Defense)"
    cp1.font.size = Pt(19)
    cp1.font.bold = True
    cp1.font.color.rgb = RGBColor(255, 255, 255)

    qa_w = Inches(3.64)
    add_card(s14, Inches(0.8), Inches(2.2), qa_w, Inches(4.6), bg_color=RGBColor(30, 41, 59), border_color=ACCENT_GREEN)
    q1_tb = s14.shapes.add_textbox(Inches(1.0), Inches(2.35), qa_w - Inches(0.4), Inches(4.3))
    q1_tf = q1_tb.text_frame
    q1_tf.word_wrap = True
    qp1 = q1_tf.paragraphs[0]
    qp1.text = "پ١: بۆچی پڕۆژەکەتان فرە-پۆلە (Multi-Class)؟"
    qp1.font.size = Pt(13)
    qp1.font.bold = True
    qp1.font.color.rgb = ACCENT_GREEN
    qp1.space_after = Pt(6)
    qp2 = q1_tf.add_paragraph()
    qp2.text = "وەڵام: چونکە سیستەمەکە لە نێوان ٥ پۆلی جیاوازدا بڕیار دەدات. لە ڕووی کۆدەوە: چینی دەرچوون خاوەنی ٥ نۆدە، فەنکشنی Softmax بۆ گەیشتن بە ١٠٠٪ی ئەگەرەکان بەکارهاتووە، و فەنکشنی هەڵە Categorical Cross-Entropy یە نەک باینەری."
    qp2.font.size = Pt(11)
    qp2.font.color.rgb = RGBColor(226, 232, 240)

    add_card(s14, Inches(4.84), Inches(2.2), qa_w, Inches(4.6), bg_color=RGBColor(30, 41, 59), border_color=ACCENT_BLUE)
    q2_tb = s14.shapes.add_textbox(Inches(5.04), Inches(2.35), qa_w - Inches(0.4), Inches(4.3))
    q2_tf = q2_tb.text_frame
    q2_tf.word_wrap = True
    qp3 = q2_tf.paragraphs[0]
    qp3.text = "پ٢: گەورەترین دەستکەوتی ئەندازیاری پڕۆژە؟"
    qp3.font.size = Pt(13)
    qp3.font.bold = True
    qp3.font.color.rgb = ACCENT_BLUE
    qp3.space_after = Pt(6)
    qp4 = q2_tf.add_paragraph()
    qp4.text = "وەڵام: سەلماندنی ئەوەی کە تۆڕی دەماری فرەچین (ANN) تەنها بۆ داتای تەخت نییە؛ بەڵکو کاتێک بە تەلارسازی نوێی Res-MLP و بەستەری بازدەر (Skip Connection) دادەڕێژرێت، دەتوانێت بگاتە 87.33% دیقەت و کێشەی تێکەڵبوونی سەگ و پشیلە بە تەواوی چارەسەر بکات."
    qp4.font.size = Pt(11)
    qp4.font.color.rgb = RGBColor(226, 232, 240)

    add_card(s14, Inches(8.88), Inches(2.2), qa_w, Inches(4.6), bg_color=RGBColor(30, 41, 59), border_color=ACCENT_AMBER)
    q3_tb = s14.shapes.add_textbox(Inches(9.08), Inches(2.35), qa_w - Inches(0.4), Inches(4.3))
    q3_tf = q3_tb.text_frame
    q3_tf.word_wrap = True
    qp5 = q3_tf.paragraphs[0]
    qp5.text = "پ٣: ئەگەر وێنەی تەنێکی تر بدەینێ؟"
    qp5.font.size = Pt(13)
    qp5.font.bold = True
    qp5.font.color.rgb = ACCENT_AMBER
    qp5.space_after = Pt(6)
    qp6 = q3_tf.add_paragraph()
    qp6.text = "وەڵام: لەبەر بنەمای Closed-World مۆدێل ئەگەرەکان دابەش دەکات. بەڵام لەبەر ئەوەی دڵنیاییەکەی دەبێتە کەمتر لە ٥٠٪، بە دانانی Confidence Threshold دەتوانرێت بە ڕەنگی زەرد بڵێت '⚠️ تەنێکی نەناسراوە و لە دەرەوەی ۵ پۆلەکەیە (Unknown)'."
    qp6.font.size = Pt(11)
    qp6.font.color.rgb = RGBColor(226, 232, 240)

    # Save presentation
    out_dir = os.path.dirname(os.path.abspath(__file__))
    out_file = os.path.join(out_dir, "ANN_MultiClass_Presentation_14_Slides.pptx")
    prs.save(out_file)
    print(f"Generated 14-slide deck: {out_file}")

if __name__ == "__main__":
    create_14_slide_deck()
