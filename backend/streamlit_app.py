import streamlit as st
from pathlib import Path
import tensorflow as tf
import numpy as np
from PIL import Image

# Page config
st.set_page_config(
    page_title="Plant Savior AI - Model Tester",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Plant Savior AI - Direct Model Testing")
st.markdown("Upload a plant image to test your trained Keras model")

# Model path - adjust this based on where you upload your model
MODEL_PATH = "best_plant_model_final.keras"

@st.cache_resource
def load_model():
    """Load the model with caching"""
    try:
        # Try different loading methods
        try:
            # Method 1: Standard loading
            model = tf.keras.models.load_model(MODEL_PATH)
            return model, "Standard loading successful"
        except Exception as e1:
            st.warning(f"Standard loading failed: {str(e1)[:100]}...")
            try:
                # Method 2: Load without compilation
                model = tf.keras.models.load_model(MODEL_PATH, compile=False)
                model.compile(
                    optimizer='adam',
                    loss='categorical_crossentropy',
                    metrics=['accuracy']
                )
                return model, "Loaded without compilation, then recompiled"
            except Exception as e2:
                return None, f"All loading methods failed. Last error: {str(e2)[:100]}..."
    except Exception as e:
        return None, f"Critical error: {str(e)[:100]}..."

# Load model
with st.spinner("Loading model..."):
    model, load_message = load_model()

if model is not None:
    st.success(f"✅ Model loaded successfully! ({load_message})")
    
    # Model information
    st.subheader("📊 Model Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Input Shape", str(model.input_shape))
    with col2:
        st.metric("Output Shape", str(model.output_shape))
    with col3:
        st.metric("Parameters", f"{model.count_params():,}")
    
    # Class names - UPDATE THESE BASED ON YOUR MODEL
    CLASS_NAMES = [
        "Apple Scab",
        "Apple Black Rot", 
        "Apple Cedar Apple Rust",
        "Apple Healthy",
        "Cherry Powdery Mildew",
        "Cherry Healthy",
        "Corn Cercospora Leaf Spot",
        "Corn Common Rust",
        "Corn Northern Leaf Blight",
        "Corn Healthy",
        "Grape Black Rot",
        "Grape Esca",
        "Grape Leaf Blight",
        "Grape Healthy",
        "Potato Early Blight",
        "Potato Late Blight",
        "Potato Healthy",
        "Strawberry Leaf Scorch",
        "Strawberry Healthy",
        "Tomato Bacterial Spot",
        "Tomato Early Blight",
        "Tomato Late Blight",
        "Tomato Leaf Mold",
        "Tomato Septoria Leaf Spot",
        "Tomato Spider Mites",
        "Tomato Target Spot",
        "Tomato Yellow Leaf Curl Virus",
        "Tomato Mosaic Virus",
        "Tomato Healthy"
    ]
    
    with st.expander("🏷️ Model Classes"):
        for i, class_name in enumerate(CLASS_NAMES):
            st.write(f"{i}: {class_name}")
    
    st.markdown("---")
    
    # File upload section
    st.subheader("📤 Upload Plant Image")
    uploaded_file = st.file_uploader(
        "Choose a plant leaf image...",
        type=["jpg", "jpeg", "png"],
        help="Upload a clear image of a plant leaf for disease detection"
    )
    
    if uploaded_file is not None:
        # Create columns for layout
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🖼️ Uploaded Image")
            try:
                image = Image.open(uploaded_file)
                st.image(image, caption="Original Image", use_container_width=True)
                
                # Image info
                st.write(f"**Size:** {image.size}")
                st.write(f"**Mode:** {image.mode}")
                
            except Exception as e:
                st.error(f"Error loading image: {e}")
                image = None
        
        with col2:
            st.subheader("🔬 Analysis Results")
            
            if image is not None:
                # Preprocess image
                def preprocess_image(img):
                    """Preprocess image for model prediction"""
                    try:
                        # Convert to RGB if needed
                        if img.mode != "RGB":
                            img = img.convert("RGB")
                        
                        # Resize to model's expected input size
                        # Most plant disease models use 224x224
                        target_size = (224, 224)
                        img = img.resize(target_size, Image.Resampling.LANCZOS)
                        
                        # Convert to array and normalize to [0,1]
                        img_array = np.array(img, dtype=np.float32)
                        img_array = img_array / 255.0
                        
                        # Add batch dimension
                        img_array = np.expand_dims(img_array, axis=0)
                        
                        return img_array
                    
                    except Exception as e:
                        st.error(f"Preprocessing error: {e}")
                        return None
                
                # Make prediction button
                if st.button("🔍 Analyze Plant", type="primary", use_container_width=True):
                    try:
                        with st.spinner("🤖 AI is analyzing your plant..."):
                            # Preprocess
                            processed_img = preprocess_image(image)
                            
                            if processed_img is not None:
                                # Get prediction
                                predictions = model.predict(processed_img, verbose=0)
                                
                                # Handle different output formats
                                if isinstance(predictions, (list, tuple)):
                                    predictions = predictions[0]
                                
                                # Apply softmax to get probabilities
                                if len(predictions.shape) > 1:
                                    probabilities = tf.nn.softmax(predictions[0]).numpy()
                                else:
                                    probabilities = tf.nn.softmax(predictions).numpy()
                                
                                # Get top prediction
                                predicted_idx = int(np.argmax(probabilities))
                                confidence = float(probabilities[predicted_idx])
                                
                                # Display main result
                                if predicted_idx < len(CLASS_NAMES):
                                    predicted_class = CLASS_NAMES[predicted_idx]
                                else:
                                    predicted_class = f"Unknown Class {predicted_idx}"
                                
                                # Color-coded result based on confidence
                                if confidence >= 0.8:
                                    st.success(f"🎯 **{predicted_class}**")
                                elif confidence >= 0.6:
                                    st.warning(f"⚠️ **{predicted_class}**")
                                else:
                                    st.info(f"🤔 **{predicted_class}** (Low confidence)")
                                
                                # Confidence meter
                                st.metric(
                                    label="Confidence Level",
                                    value=f"{confidence*100:.1f}%",
                                    delta=f"{'High' if confidence > 0.7 else 'Medium' if confidence > 0.5 else 'Low'} confidence"
                                )
                                
                                # Health status
                                is_healthy = "healthy" in predicted_class.lower()
                                if is_healthy:
                                    st.success("🌿 Your plant appears healthy!")
                                else:
                                    st.warning("🚨 Disease detected - consider treatment")
                                
                                # Top 3 predictions
                                st.subheader("📈 Top 3 Predictions")
                                top_3_indices = np.argsort(probabilities)[-3:][::-1]
                                
                                for i, idx in enumerate(top_3_indices):
                                    prob = probabilities[idx]
                                    class_name = CLASS_NAMES[idx] if idx < len(CLASS_NAMES) else f"Class {idx}"
                                    
                                    # Create progress bar for each prediction
                                    st.write(f"**{i+1}. {class_name}**")
                                    st.progress(float(prob))
                                    st.write(f"{prob*100:.2f}%")
                                    st.write("")
                                
                                # Detailed probabilities in expander
                                with st.expander("🔍 View All Predictions"):
                                    # Sort by probability
                                    sorted_indices = np.argsort(probabilities)[::-1]
                                    
                                    for idx in sorted_indices:
                                        prob = probabilities[idx]
                                        class_name = CLASS_NAMES[idx] if idx < len(CLASS_NAMES) else f"Class {idx}"
                                        
                                        # Only show if probability > 0.1%
                                        if prob > 0.001:
                                            st.write(f"**{class_name}:** {prob*100:.3f}%")
                    
                    except Exception as e:
                        st.error(f"❌ Prediction failed: {e}")
                        
                        # Debugging information
                        with st.expander("🔧 Debug Information"):
                            st.write(f"**Error Type:** {type(e).__name__}")
                            st.write(f"**Error Details:** {str(e)}")
                            st.write(f"**Image Shape:** {image.size if image else 'N/A'}")
                            st.write(f"**Model Input Shape:** {model.input_shape}")
                            st.write(f"**Model Output Shape:** {model.output_shape}")

else:
    st.error(f"❌ {load_message}")
    
    # Detailed troubleshooting
    st.subheader("🔧 Model Compatibility Issues")
    
    st.error("**Batch Normalization Error Detected**")
    st.markdown("""
    This error occurs when your model was trained with an older TensorFlow version. 
    The batch normalization layer implementation changed between versions.
    """)
    
    st.subheader("💡 Solutions")
    
    # Solution tabs
    sol_tab1, sol_tab2, sol_tab3 = st.tabs(["Quick Fix", "Model Reconstruction", "Upload New Model"])
    
    with sol_tab1:
        st.markdown("""
        **Try these commands in your training environment:**
        
        ```python
        # Option 1: Re-save your model
        import tensorflow as tf
        model = tf.keras.models.load_model('your_model.h5', compile=False)
        model.save('best_plant_model_final.keras', save_format='tf')
        
        # Option 2: Save only weights
        model.save_weights('model_weights.h5')
        ```
        """)
    
    with sol_tab2:
        st.markdown("""
        **If you have the original training code, retrain with:**
        
        ```python
        # Use latest TensorFlow
        pip install tensorflow --upgrade
        
        # When building model, ensure proper batch norm usage
        base_model = tf.keras.applications.MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(224, 224, 3)
        )
        
        model = tf.keras.Sequential([
            base_model,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(num_classes, activation='softmax')
        ])
        
        # Save in new format
        model.save('best_plant_model_final.keras')
        ```
        """)
    
    with sol_tab3:
        # File upload for model
        st.markdown("Upload a compatible model file:")
        model_file = st.file_uploader(
            "Upload your .keras or .h5 model file",
            type=["keras", "h5"],
            help="Upload a model trained with TensorFlow 2.13+"
        )
        
        if model_file is not None:
            # Save uploaded model temporarily and try to load
            temp_path = "temp_uploaded_model.keras"
            
            try:
                with open(temp_path, "wb") as f:
                    f.write(model_file.getbuffer())
                
                with st.spinner("Testing uploaded model..."):
                    # Try to load the uploaded model
                    test_model = tf.keras.models.load_model(temp_path, compile=False)
                    test_model.compile(
                        optimizer='adam',
                        loss='categorical_crossentropy', 
                        metrics=['accuracy']
                    )
                
                st.success("✅ Uploaded model works! You can use this one.")
                
                # Show model info
                st.write(f"**Input Shape:** {test_model.input_shape}")
                st.write(f"**Output Shape:** {test_model.output_shape}")
                st.write(f"**Parameters:** {test_model.count_params():,}")
                
                # Option to use this model for testing
                if st.button("Use This Model for Testing"):
                    st.session_state.use_uploaded_model = True
                    st.session_state.uploaded_model = test_model
                    st.rerun()
                
            except Exception as e:
                st.error(f"❌ Uploaded model also failed: {e}")
                st.info("This model has the same compatibility issues.")
    
    # Show current TensorFlow version
    st.subheader("🔍 Environment Info")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Current TensorFlow:** {tf.__version__}")
        st.write(f"**Expected Model Format:** .keras (TF 2.13+)")
    with col2:
        st.write(f"**Python Version:** {'.'.join(map(str, __import__('sys').version_info[:3]))}")
        st.write(f"**Model Path:** {MODEL_PATH}")

# Check if we should use uploaded model
if hasattr(st.session_state, 'use_uploaded_model') and st.session_state.use_uploaded_model:
    model = st.session_state.uploaded_model
    load_message = "Using uploaded model"

# Footer
st.markdown("---")
st.markdown("### 💡 Tips")
st.markdown("""
- Use clear, well-lit images of plant leaves
- Ensure the leaf takes up most of the image frame
- Avoid blurry or heavily shadowed images
- Different lighting conditions may affect results
""")

# Debug info in sidebar
st.sidebar.markdown("### 🔧 System Info")
st.sidebar.write(f"**TensorFlow:** {tf.__version__}")
st.sidebar.write(f"**Python:** {'.'.join(map(str, __import__('sys').version_info[:3]))}")
st.sidebar.write(f"**Streamlit:** {st.__version__}")

# Model status indicator
if Path(MODEL_PATH).exists():
    st.sidebar.success("✅ Model file found")
else:
    st.sidebar.error("❌ Model file missing")
    st.sidebar.write(f"Expected: `{MODEL_PATH}`")
