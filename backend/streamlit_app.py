import streamlit as st
from pathlib import Path
import tensorflow as tf
import numpy as np
from PIL import Image
import requests
import json

# Page config
st.set_page_config(
    page_title="Plant Savior AI - Model Tester",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Plant Savior AI - Model Tester")
st.markdown("Test your Keras model directly or via the FastAPI endpoint")

# Model path
MODEL_PATH = Path(__file__).parent / "models" / "best_plant_model_final.keras"

# Tabs for different testing methods
tab1, tab2 = st.tabs(["Direct Model Testing", "API Testing"])

with tab1:
    st.header("Direct Model Testing")
    
    # Check if model exists
    if MODEL_PATH.exists():
        try:
            # Load model
            with st.spinner("Loading model..."):
                model = tf.keras.models.load_model(MODEL_PATH)
            
            st.success("✅ Model loaded successfully!")
            
            # Model info
            st.subheader("Model Information")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Input Shape:** {model.input_shape}")
            with col2:
                st.write(f"**Output Shape:** {model.output_shape}")
            
            # Class names (update these based on your model)
            CLASS_NAMES = ["Healthy Plant", "Leaf Spot Disease", "Powdery Mildew"]
            st.write(f"**Classes:** {', '.join(CLASS_NAMES)}")
            
            # File upload
            uploaded_file = st.file_uploader(
                "Upload plant leaf image", 
                type=["jpg", "jpeg", "png"],
                key="direct_test"
            )
            
            if uploaded_file is not None:
                # Display image
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Uploaded Image")
                    image = Image.open(uploaded_file)
                    st.image(image, caption="Original Image", use_container_width=True)
                
                with col2:
                    st.subheader("Prediction Results")
                    
                    # Preprocess image
                    def preprocess_image(img):
                        img = img.convert("RGB").resize((224, 224))
                        img_array = np.array(img) / 255.0
                        return np.expand_dims(img_array, 0)
                    
                    # Make prediction
                    with st.spinner("Analyzing image..."):
                        processed_img = preprocess_image(image)
                        predictions = model.predict(processed_img)
                        probabilities = tf.nn.softmax(predictions[0]).numpy()
                    
                    # Display results
                    predicted_index = int(np.argmax(probabilities))
                    confidence = float(probabilities[predicted_index])
                    predicted_class = CLASS_NAMES[predicted_index] if predicted_index < len(CLASS_NAMES) else "Unknown"
                    
                    st.success(f"**Prediction:** {predicted_class}")
                    st.info(f"**Confidence:** {confidence*100:.1f}%")
                    
                    # Show all class probabilities
                    st.subheader("All Class Probabilities")
                    for i, (class_name, prob) in enumerate(zip(CLASS_NAMES, probabilities)):
                        st.write(f"**{class_name}:** {prob*100:.2f}%")
                        st.progress(float(prob))
                        
        except Exception as e:
            st.error(f"❌ Error loading model: {e}")
            st.info("Make sure your model file is compatible with the current TensorFlow version.")
    else:
        st.error(f"❌ Model file not found at: {MODEL_PATH}")
        st.info("Please place your `best_plant_model_final.keras` file in the `backend/models/` directory.")

with tab2:
    st.header("API Testing")
    st.markdown("Test the FastAPI endpoint that your React app will use")
    
    # API URL input
    api_url = st.text_input(
        "API URL", 
        value="http://localhost:8501",
        help="URL where your FastAPI server is running"
    )
    
    # Test API connection
    if st.button("Test API Connection"):
        try:
            response = requests.get(f"{api_url}/")
            if response.status_code == 200:
                data = response.json()
                st.success("✅ API is running!")
                st.json(data)
            else:
                st.error(f"❌ API returned status code: {response.status_code}")
        except Exception as e:
            st.error(f"❌ Cannot connect to API: {e}")
            st.info("Make sure your FastAPI server is running: `uvicorn api:app --reload --port 8501`")
    
    # File upload for API testing
    uploaded_file_api = st.file_uploader(
        "Upload plant leaf image for API testing", 
        type=["jpg", "jpeg", "png"],
        key="api_test"
    )
    
    if uploaded_file_api is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Uploaded Image")
            image = Image.open(uploaded_file_api)
            st.image(image, caption="Image for API Testing", use_container_width=True)
        
        with col2:
            st.subheader("API Response")
            
            if st.button("Send to API"):
                try:
                    with st.spinner("Sending to API..."):
                        # Reset file pointer
                        uploaded_file_api.seek(0)
                        files = {"file": uploaded_file_api}
                        response = requests.post(f"{api_url}/predict", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ API Response Received!")
                        
                        # Display main results
                        st.write(f"**Predicted Class:** {result.get('predicted_class', 'N/A')}")
                        st.write(f"**Confidence:** {result.get('confidence', 0)*100:.1f}%")
                        st.write(f"**Severity:** {result.get('severity', 'N/A')}")
                        
                        # Show full JSON response
                        with st.expander("Full API Response"):
                            st.json(result)
                    else:
                        st.error(f"❌ API Error: {response.status_code}")
                        st.text(response.text)
                        
                except Exception as e:
                    st.error(f"❌ Request failed: {e}")

# Instructions
st.sidebar.markdown("""
## 🚀 Quick Start

### 1. Setup Backend
```bash
cd backend
pip install -r requirements.txt
```

### 2. Place Model File
Put `best_plant_model_final.keras` in:
```
backend/models/best_plant_model_final.keras
```

### 3. Run FastAPI Server
```bash
uvicorn api:app --reload --port 8501
```

### 4. Run Streamlit (Optional)
```bash
streamlit run streamlit_app.py --server.port 8502
```

### 5. Update React App
Set `STREAMLIT_API_URL` to your API URL
""")