import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import io
from pathlib import Path
import base64

# Page configuration
st.set_page_config(
    page_title="Plant Savior AI - Disease Detection",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling (mimics the React app design)
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #0f766e, #059669);
        color: white;
        margin-bottom: 2rem;
        border-radius: 10px;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-bottom: 1rem;
    }
    
    .section-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
        border: 1px solid #e5e7eb;
    }
    
    .upload-area {
        border: 2px dashed #0d9488;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background: #f0fdfa;
        margin: 1rem 0;
    }
    
    .result-card {
        background: #f0fdfa;
        border-left: 4px solid #0d9488;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .confidence-bar {
        background: #e5e7eb;
        border-radius: 10px;
        overflow: hidden;
        margin: 0.5rem 0;
    }
    
    .confidence-fill {
        background: linear-gradient(90deg, #0d9488, #059669);
        height: 8px;
        border-radius: 10px;
    }
    
    .step-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .step-number {
        background: #0d9488;
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        border: 1px solid #f3f4f6;
        text-align: center;
    }
    
    .btn-primary {
        background: #0d9488;
        color: white;
        padding: 0.75rem 2rem;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        text-decoration: none;
        display: inline-block;
        cursor: pointer;
    }
    
    .btn-primary:hover {
        background: #0f766e;
    }
    
    .stButton > button {
        background: #0d9488 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background: #0f766e !important;
    }
    
    .stSelectbox > div > div {
        background: white;
        border-radius: 8px;
    }
    
    .stTextArea > div > div > textarea {
        background: white;
        border-radius: 8px;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #0d9488;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'model' not in st.session_state:
    st.session_state.model = None
    st.session_state.model_loaded = False
    st.session_state.analysis_results = None
    st.session_state.uploaded_image = None

# Load model function
@st.cache_resource
def load_model():
    """Load the Keras model"""
    model_paths = [
        Path("backend/models/best_plant_model_final.keras"),
        Path("best_plant_model_final.keras"),
        Path("models/best_plant_model_final.keras")
    ]
    
    for model_path in model_paths:
        if model_path.exists():
            try:
                model = tf.keras.models.load_model(model_path)
                return model, f"✅ Model loaded successfully from {model_path}"
            except Exception as e:
                continue
    
    return None, "❌ Model file not found. Please ensure 'best_plant_model_final.keras' is in the correct directory."

# Class names and descriptions
CLASS_NAMES = ["Healthy Plant", "Leaf Spot Disease", "Powdery Mildew"]

def get_disease_info(disease_name):
    """Get comprehensive disease information"""
    disease_info = {
        "Healthy Plant": {
            "description": "Excellent news! No disease detected. Your plant appears to be in perfect health with vibrant, disease-free foliage.",
            "severity": "None",
            "color": "#059669"
        },
        "Powdery Mildew": {
            "description": "A fungal disease characterized by white, powdery spots on leaves and stems. Thrives in warm, humid conditions with poor air circulation.",
            "severity": "Moderate to High",
            "color": "#f59e0b"
        },
        "Leaf Spot Disease": {
            "description": "A bacterial or fungal infection causing dark, circular spots on leaf surfaces. Can lead to yellowing and premature leaf drop if untreated.",
            "severity": "Moderate",
            "color": "#dc2626"
        }
    }
    return disease_info.get(disease_name, {
        "description": f"Condition detected: {disease_name}",
        "severity": "Unknown",
        "color": "#6b7280"
    })

def get_treatment_recommendations(disease_name):
    """Get treatment recommendations"""
    treatments = {
        "Healthy Plant": [
            "Continue your excellent care routine",
            "Monitor plant regularly for changes",
            "Maintain consistent watering schedule",
            "Ensure adequate lighting conditions",
            "Check monthly for pests and early signs"
        ],
        "Powdery Mildew": [
            "Remove affected leaves immediately",
            "Improve air circulation around plant",
            "Apply fungicidal soap or neem oil every 7-10 days",
            "Reduce humidity levels around plant",
            "Water at soil level only - avoid wetting leaves"
        ],
        "Leaf Spot Disease": [
            "Remove infected leaves with sterilized tools",
            "Apply copper-based fungicide spray",
            "Increase spacing between plants",
            "Water plants at soil level only",
            "Disinfect gardening tools between uses"
        ]
    }
    return treatments.get(disease_name, ["Consult with a plant specialist", "Monitor plant closely"])

def get_prevention_tips(disease_name):
    """Get prevention recommendations"""
    prevention = {
        "Healthy Plant": [
            "Maintain proper watering schedule",
            "Provide adequate sunlight exposure",
            "Use well-draining soil",
            "Fertilize appropriately for plant type",
            "Inspect plants weekly for early detection"
        ],
        "Powdery Mildew": [
            "Ensure proper spacing for air circulation",
            "Avoid overhead watering",
            "Monitor humidity levels regularly",
            "Apply preventive fungicide during humid seasons",
            "Remove debris and fallen leaves promptly"
        ],
        "Leaf Spot Disease": [
            "Always water at soil level",
            "Ensure excellent drainage",
            "Practice crop rotation in gardens",
            "Use drip irrigation systems",
            "Apply organic mulch to prevent soil splash"
        ]
    }
    return prevention.get(disease_name, ["Maintain good plant hygiene", "Provide optimal growing conditions"])

def preprocess_image(img):
    """Preprocess image for model prediction"""
    img = img.convert("RGB").resize((224, 224))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, 0)

def analyze_plant_disease(image, model):
    """Analyze plant disease from image"""
    if model is None:
        return None
    
    try:
        processed_img = preprocess_image(image)
        predictions = model.predict(processed_img, verbose=0)
        probabilities = tf.nn.softmax(predictions[0]).numpy()
        
        predicted_index = int(np.argmax(probabilities))
        confidence = float(probabilities[predicted_index])
        predicted_class = CLASS_NAMES[predicted_index] if predicted_index < len(CLASS_NAMES) else "Unknown"
        
        # Determine severity
        severity_level = "Low"
        if predicted_class != "Healthy Plant":
            if confidence > 0.8:
                severity_level = "High"
            elif confidence > 0.6:
                severity_level = "Medium"
        
        return {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "severity": severity_level,
            "probabilities": probabilities,
            "all_predictions": {CLASS_NAMES[i]: float(probabilities[i]) for i in range(len(CLASS_NAMES))}
        }
    except Exception as e:
        st.error(f"Analysis failed: {e}")
        return None

# Load model
model, model_status = load_model()
st.session_state.model = model
st.session_state.model_loaded = model is not None

# Header Section
st.markdown("""
<div class="main-header">
    <div class="hero-title">🌱 Plant Savior AI</div>
    <div class="hero-subtitle">AI-Powered Plant Disease Detection & Treatment Recommendations</div>
    <div style="font-size: 0.9rem; margin-top: 0.5rem;">""" + model_status + """</div>
</div>
""", unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📸 Upload Plant Image")
    
    # Upload area
    st.markdown('<div class="upload-area">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Choose a plant leaf image",
        type=['jpg', 'jpeg', 'png'],
        help="Supported formats: JPG, JPEG, PNG"
    )
    st.markdown("📱 Take a clear photo of the affected plant leaf for best results", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.session_state.uploaded_image = image
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Analyze button
        if st.button("🔬 Analyze Plant Disease", key="analyze_btn"):
            if st.session_state.model_loaded:
                with st.spinner("🔍 Analyzing plant condition..."):
                    results = analyze_plant_disease(image, st.session_state.model)
                    st.session_state.analysis_results = results
            else:
                st.error("❌ Model not loaded. Please check model file.")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Analysis Results")
    
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results
        disease_info = get_disease_info(results["predicted_class"])
        
        # Main result
        st.markdown(f"""
        <div class="result-card">
            <h4 style="margin: 0 0 1rem 0; color: {disease_info['color']};">
                🎯 Diagnosis: {results['predicted_class']}
            </h4>
            <p><strong>Confidence:</strong> {results['confidence']*100:.1f}%</p>
            <p><strong>Severity:</strong> {results['severity']}</p>
            <p style="margin-bottom: 0;"><strong>Description:</strong> {disease_info['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Confidence bars for all predictions
        st.markdown("**Detailed Analysis:**")
        for class_name, probability in results['all_predictions'].items():
            percentage = probability * 100
            st.markdown(f"""
            <div style="margin: 0.5rem 0;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                    <span>{class_name}</span>
                    <span>{percentage:.1f}%</span>
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {percentage}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Treatment and Prevention tabs
        tab1, tab2 = st.tabs(["💊 Treatment", "🛡️ Prevention"])
        
        with tab1:
            st.markdown("**Recommended Actions:**")
            treatments = get_treatment_recommendations(results["predicted_class"])
            for i, treatment in enumerate(treatments, 1):
                st.markdown(f"{i}. {treatment}")
        
        with tab2:
            st.markdown("**Prevention Strategies:**")
            prevention_tips = get_prevention_tips(results["predicted_class"])
            for i, tip in enumerate(prevention_tips, 1):
                st.markdown(f"{i}. {tip}")
    
    else:
        st.info("🔄 Upload an image and click 'Analyze' to see results here.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Features section
st.markdown("---")
st.markdown("## ✨ Key Features")

feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
        <h4>AI-Powered Detection</h4>
        <p>Advanced machine learning models trained on thousands of plant images for accurate disease identification.</p>
    </div>
    """, unsafe_allow_html=True)

with feature_col2:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
        <h4>Instant Analysis</h4>
        <p>Get results in seconds with confidence scores and detailed explanations for each diagnosis.</p>
    </div>
    """, unsafe_allow_html=True)

with feature_col3:
    st.markdown("""
    <div class="feature-card">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🌿</div>
        <h4>Treatment Guidance</h4>
        <p>Receive comprehensive treatment and prevention recommendations tailored to the detected condition.</p>
    </div>
    """, unsafe_allow_html=True)

# How it works section
st.markdown("---")
st.markdown("## 🔄 How It Works")

step_col1, step_col2, step_col3 = st.columns(3)

with step_col1:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">1</div>
        <h4>📸 Upload Image</h4>
        <p>Take a clear photo of your plant leaf and upload it to our system.</p>
    </div>
    """, unsafe_allow_html=True)

with step_col2:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">2</div>
        <h4>🔬 AI Analysis</h4>
        <p>Our trained model analyzes the image to detect diseases and assess plant health.</p>
    </div>
    """, unsafe_allow_html=True)

with step_col3:
    st.markdown("""
    <div class="step-card">
        <div class="step-number">3</div>
        <h4>📋 Get Results</h4>
        <p>Receive detailed diagnosis with treatment recommendations and prevention tips.</p>
    </div>
    """, unsafe_allow_html=True)

# About section
st.markdown("---")
st.markdown("## 🌱 About Plant Savior AI")

about_col1, about_col2 = st.columns([2, 1])

with about_col1:
    st.markdown("""
    Plant Savior AI leverages cutting-edge artificial intelligence to help gardeners, farmers, and plant enthusiasts 
    identify and treat plant diseases quickly and accurately. Our system is trained on a comprehensive dataset of 
    plant images, enabling precise detection of common diseases that affect plant health.
    
    **Why Choose Plant Savior AI?**
    - 🎯 **High Accuracy**: Advanced deep learning models with proven results
    - ⚡ **Fast Results**: Instant analysis and recommendations
    - 🌿 **Expert Guidance**: Treatment plans based on agricultural best practices
    - 📱 **Easy to Use**: Simple upload and analyze workflow
    - 🔒 **Secure**: Your images are processed securely and not stored
    """)

with about_col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0f766e, #059669); color: white; padding: 2rem; border-radius: 15px; text-align: center;">
        <h4 style="margin: 0 0 1rem 0;">Ready to Save Your Plants? 🌿</h4>
        <p style="margin: 0 0 1rem 0;">Upload your first plant image now and get instant AI-powered diagnosis!</p>
        <div style="font-size: 2rem;">🌱➡️🔬➡️💚</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #6b7280;">
    <p>🌱 Plant Savior AI - Keeping Your Plants Healthy with AI Technology</p>
    <p style="font-size: 0.9rem;">Powered by TensorFlow & Streamlit | Made with ❤️ for plant lovers</p>
</div>
""", unsafe_allow_html=True)