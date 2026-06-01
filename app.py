import streamlit as st
import numpy as np
from PIL import Image
import time
import os
import urllib.request
import json

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Plant Leaf Disease Detector",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS Styling ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

    * {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], .stApp, p, span, div, td, th, button, input {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    h1, h2, h3 {
        font-weight: 700 !important;
        letter-spacing: -0.3px !important;
        color: #1B5E20;
    }

    /* Main background */
    .stApp { background-color: #f0f7f0; }

    /* Sidebar background mapping */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 60%, #388E3C 100%);
    }
    [data-testid="stSidebar"] * { color: #fff !important; }
    [data-testid="stSidebar"] .stSelectbox label { color: #C8E6C9 !important; }

    /* Dashboard Cards */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.4rem 1.6rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        border-left: 5px solid #2E7D32;
    }
    .card-red   { border-left-color: #c62828; }
    .card-blue  { border-left-color: #1565C0; }
    .card-amber { border-left-color: #E65100; }

    /* Result Badges */
    .badge-healthy  { background:#E8F5E9; color:#1B5E20; border:1.5px solid #2E7D32; border-radius:8px; padding:6px 18px; font-weight:700; font-size:1.1rem; }
    .badge-disease  { background:#FFEBEE; color:#B71C1C; border:1.5px solid #c62828; border-radius:8px; padding:6px 18px; font-weight:700; font-size:1.1rem; }

    /* Top Stats Counters */
    .stat-box {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    }
    .stat-num { 
        font-size: 2.2rem; 
        font-weight: 800; 
        color: #2E7D32; 
        letter-spacing: -0.5px;
    }
    .stat-lbl { font-size: 0.82rem; color: #666; margin-top: 2px; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 500; }

    /* ── COMPLETE FILE UPLOADER VISUAL REPAIRS ── */
    [data-testid="stFileUploader"] {
        border: 2px dashed #4CAF50 !important;
        border-radius: 14px !important;
        background-color: #F1F8E9 !important;
        padding: 16px !important;
    }
    [data-testid="stFileUploader"] label, 
    [data-testid="stFileUploader"] p, 
    [data-testid="stFileUploader"] span, 
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] div {
        color: #1B5E20 !important;
    }
    [data-testid="stFileUploader"] button {
        background-color: #2E7D32 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 6px 16px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1) !important;
    }
    [data-testid="stFileUploader"] button:hover {
        background-color: #1B5E20 !important;
    }

    /* Core Action Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #2E7D32, #4CAF50);
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s;
    }
    .stButton>button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(46,125,50,0.4); }

    .top-bar {
        background: linear-gradient(135deg, #1B5E20, #2E7D32);
        color: white;
        padding: 1.2rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Class Labels & Info mappings ──────────────────────────────────────────────
CLASS_LABELS = [
    "Apple — Scab", "Apple — Black Rot", "Apple — Cedar Apple Rust", "Apple — Healthy",
    "Background (No Leaf)", "Blueberry — Healthy", "Cherry — Powdery Mildew", "Cherry — Healthy",
    "Corn — Gray Leaf Spot", "Corn — Common Rust", "Corn — Northern Leaf Blight", "Corn — Healthy",
    "Grape — Black Rot", "Grape — Black Measles", "Grape — Leaf Blight", "Grape — Healthy",
    "Orange — Huanglongbing", "Peach — Bacterial Spot", "Peach — Healthy", "Pepper — Bacterial Spot",
    "Pepper — Healthy", "Potato — Early Blight", "Potato — Healthy", "Potato — Late Blight",
    "Raspberry — Healthy", "Soybean — Healthy", "Squash — Powdery Mildew", "Strawberry — Healthy",
    "Strawberry — Leaf Scorch", "Tomato — Bacterial Spot", "Tomato — Early Blight", "Tomato — Healthy",
    "Tomato — Late Blight", "Tomato — Leaf Mold", "Tomato — Septoria Leaf Spot", "Tomato — Spider Mites",
    "Tomato — Target Spot", "Tomato — Mosaic Virus", "Tomato — Yellow Leaf Curl Virus"
]

HEALTHY_KEYWORDS = ["Healthy", "Background"]
DISEASE_INFO = {
    "Scab": {"cause": "Fungal", "severity": "Moderate", "treatment": "Fungicides; remove infected leaves"},
    "Black Rot": {"cause": "Fungal", "severity": "High", "treatment": "Copper fungicides; prune infected branches"},
    "Early Blight": {"cause": "Fungal", "severity": "Moderate", "treatment": "Chlorothalonil sprays; clear lower leaves"},
    "Late Blight": {"cause": "Oomycete", "severity": "Critical", "treatment": "Destroy infected plants instantly; treat surrounding ones"},
    "Bacterial Spot": {"cause": "Bacterial", "severity": "High", "treatment": "Copper bactericides; avoid top-watering"}
}

# ── Cloud Repository Configs ──────────────────────────────────────────────────
MODEL_DIR = "models"
MODEL_FILENAME = "final_progression_model.h5" 
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)
METADATA_FILENAME = "metadata.json"
METADATA_PATH = os.path.join(MODEL_DIR, METADATA_FILENAME)

MODEL_URL = f"https://huggingface.co/Sharmistha-catalyst/sick-greens-plant-disease/resolve/main/{MODEL_FILENAME}"
METADATA_URL = f"https://huggingface.co/Sharmistha-catalyst/sick-greens-plant-disease/resolve/main/{METADATA_FILENAME}"

# ── Safe Infrastructure Sync Engine ───────────────────────────────────────────
@st.cache_resource
def load_assets():
    """Download weights and metadata files safely from Hugging Face."""
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Sync Metadata
    if not os.path.exists(METADATA_PATH):
        try:
            urllib.request.urlretrieve(METADATA_URL, METADATA_PATH)
        except Exception:
            pass
            
    # Sync Weights
    if not os.path.exists(MODEL_PATH):
        try:
            with st.spinner("📥 Downloading deep learning model weights from Hugging Face..."):
                urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        except Exception as e:
            st.sidebar.error(f"Download failed: {e}")
            return None, "demo"

    try:
        import tensorflow as tf
        if os.path.exists(MODEL_PATH):
            return tf.keras.models.load_model(MODEL_PATH), "tensorflow"
    except Exception:
        pass
    return None, "demo"

# Load backend assets
model, framework = load_assets()

# Read Meta-Metrics
metadata = {}
if os.path.exists(METADATA_PATH):
    try:
        with open(METADATA_PATH, "r") as f:
            metadata = json.load(f)
    except Exception:
        pass

def predict(model, framework, image: Image.Image):
    img = image.convert("RGB").resize((224, 224))
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, axis=0)
    
    if framework == "tensorflow":
        probs = model.predict(arr, verbose=0)[0]
    else:
        np.random.seed(42)
        probs = np.random.dirichlet(np.ones(len(CLASS_LABELS)) * 0.1)
        
    top5_idx = np.argsort(probs)[::-1][:5]
    return top5_idx, probs[top5_idx], probs

# ── Session State Management ──────────────────────────────────────────────────
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "current_file_name" not in st.session_state:
    st.session_state.current_file_name = None

# ── Interface Rendering ───────────────────────────────────────────────────────
st.markdown("""
<div class="top-bar">
    <h1 style="color:white;margin:0;font-size:1.8rem;">🌿 Sick-greens Dashboard</h1>
    <p style="color:#C8E6C9;margin:4px 0 0 0;font-size:0.95rem;">Plant Disease Diagnostics & Progression Tracker</p>
</div>
""", unsafe_allow_html=True)

# Stats Metrics Section
c1, c2, c3, c4 = st.columns(4)
metrics = [
    (metadata.get("total_samples", "61,486"), "Dataset Images"),
    (metadata.get("model_architecture", "MobileNetV2"), "Architecture"),
    (f"{metadata.get('disease_acc', 0.942)*100:.1f}%" if "disease_acc" in metadata else "94.2%", "Model Accuracy"),
    ("Deployed", "Status")
]
for col, (num, lbl) in zip([c1, c2, c3, c4], metrics):
    with col:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{num}</div><div class="stat-lbl">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
left, right = st.columns([1, 1.2], gap="large")

with left:
    st.markdown("<h3 style='color: #2E7D32; margin-top: 0;'>📸 Scan Leaf</h3>", unsafe_allow_html=True)
    
    uploaded = st.file_uploader("Upload leaf sample", type=["jpg", "png", "jpeg", "webp"], label_visibility="collapsed")
    
    if uploaded:
        if st.session_state.current_file_name != uploaded.name:
            st.session_state.current_file_name = uploaded.name
            st.session_state.analysis_done = False
            
        img = Image.open(uploaded)
        st.image(img, width='stretch')
        
        if st.button("Analyze Diagnostics", width='stretch'):
            st.session_state.analysis_done = True
    else:
        st.session_state.current_file_name = None
        st.session_state.analysis_done = False

with right:
    st.markdown("<h3 style='color: #2E7D32; margin-top: 0;'>🔬 System Insights</h3>", unsafe_allow_html=True)
    
    if not uploaded:
        st.info("Awaiting input sample. Drop a leaf crop profile into the scanner area to run live neural inference.")
    
    elif st.session_state.analysis_done:
        if framework == "demo":
            st.warning("Running in simulated mode. Verify that your model name matches your Hugging Face storage precisely.")
            
        top5_idx, top5_prob, all_probs = predict(model, framework, img)
        top_label = CLASS_LABELS[top5_idx[0]]
        top_conf = top5_prob[0]
        is_healthy = any(k in top_label for k in HEALTHY_KEYWORDS)
        
        badge = "badge-healthy" if is_healthy else "badge-disease"
        card_theme = "" if is_healthy else "card-red"
        
        st.markdown(f"""
        <div class="card {card_theme}">
            <p style="font-size:0.85rem;color:#888;margin:0;">DIAGNOSIS MATRIX</p>
            <p style="font-size:1.4rem;font-weight:800;margin:6px 0;">{top_label}</p>
            <span class="{badge}">{top_conf:.1%} Match Confidence</span>
        </div>
        """, unsafe_allow_html=True)
        
        if not is_healthy:
            matched = next((k for k in DISEASE_INFO if k.lower() in top_label.lower()), None)
            if matched:
                info = DISEASE_INFO[matched]
                st.markdown(f"""
                <div class="card card-amber">
                    <strong>📋 Clinical Protocol:</strong><br>
                    • <b>Pathogen Class:</b> {info['cause']}<br>
                    • <b>Threat Profile:</b> {info['severity']}<br>
                    • <b>Remediation Strategy:</b> {info['treatment']}
                </div>
                """, unsafe_allow_html=True)

        # Bar Charts Breakdown
        st.markdown("**⚡ Class Confidence Distribution**")
        import pandas as pd
        df = pd.DataFrame({"Classification": [CLASS_LABELS[i] for i in top5_idx], "Confidence": top5_prob})
        st.bar_chart(df.set_index("Classification"))
