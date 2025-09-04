from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
import numpy as np
import tensorflow as tf
from pathlib import Path

app = FastAPI(title="Plant Savior AI API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
MODEL_PATH = Path(__file__).parent / "models" / "best_plant_model_final.keras"
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    print(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Update these class names based on your model's output classes
CLASS_NAMES = ["Healthy Plant", "Leaf Spot Disease", "Powdery Mildew"]  # Adjust to match your model

def preprocess_image(img: Image.Image) -> np.ndarray:
    """Preprocess image for model prediction"""
    # Convert to RGB and resize (adjust size based on your model's input requirements)
    img = img.convert("RGB").resize((224, 224))  # Most models use 224x224
    
    # Convert to array and normalize
    img_array = np.array(img) / 255.0
    
    # Add batch dimension
    return np.expand_dims(img_array, 0)

@app.get("/")
async def root():
    return {"message": "Plant Savior AI API", "model_loaded": model is not None}

@app.post("/predict")
async def predict_disease(file: UploadFile = File(...)):
    """Predict plant disease from uploaded image"""
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read and process image
        image_bytes = await file.read()
        img = Image.open(io.BytesIO(image_bytes))
        
        # Preprocess for model
        processed_img = preprocess_image(img)
        
        # Make prediction
        predictions = model.predict(processed_img)
        probabilities = tf.nn.softmax(predictions[0]).numpy()
        
        # Get top prediction
        predicted_index = int(np.argmax(probabilities))
        confidence = float(probabilities[predicted_index])
        predicted_class = CLASS_NAMES[predicted_index] if predicted_index < len(CLASS_NAMES) else "Unknown"
        
        # Determine severity based on disease type and confidence
        severity = "low"
        if predicted_class != "Healthy Plant":
            if confidence > 0.8:
                severity = "high"
            elif confidence > 0.6:
                severity = "medium"
        
        # Generate treatment and prevention recommendations
        treatment_recommendations = get_treatment_recommendations(predicted_class)
        prevention_recommendations = get_prevention_recommendations(predicted_class)
        
        return {
            "predicted_class": predicted_class,
            "confidence": confidence,
            "severity": severity,
            "description": get_disease_description(predicted_class),
            "treatment": treatment_recommendations,
            "prevention": prevention_recommendations,
            "all_predictions": {
                CLASS_NAMES[i]: float(probabilities[i]) 
                for i in range(len(CLASS_NAMES))
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

def get_disease_description(disease_name: str) -> str:
    """Get description for detected disease"""
    descriptions = {
        "Healthy Plant": "No disease detected. Your plant appears to be in excellent health!",
        "Powdery Mildew": "A fungal disease that appears as white powdery spots on leaves and stems.",
        "Leaf Spot Disease": "Bacterial or fungal infection causing dark spots on leaf surfaces.",
    }
    return descriptions.get(disease_name, f"Detected: {disease_name}")

def get_treatment_recommendations(disease_name: str) -> list:
    """Get treatment recommendations for detected disease"""
    treatments = {
        "Healthy Plant": [
            "Continue current care routine",
            "Monitor plant regularly for changes",
            "Maintain consistent watering schedule",
            "Ensure adequate lighting conditions",
            "Check for pests monthly"
        ],
        "Powdery Mildew": [
            "Remove affected leaves and dispose of them away from healthy plants",
            "Improve air circulation around the plant",
            "Apply fungicidal soap or neem oil spray every 7-10 days",
            "Reduce humidity levels around the plant",
            "Water at soil level to avoid wetting leaves"
        ],
        "Leaf Spot Disease": [
            "Remove infected leaves immediately",
            "Apply copper-based fungicide spray",
            "Increase spacing between plants",
            "Water plants at soil level only",
            "Disinfect gardening tools between uses"
        ]
    }
    return treatments.get(disease_name, [
        "Consult with a plant specialist for detailed treatment",
        "Monitor plant closely for changes",
        "Ensure proper plant care conditions"
    ])

def get_prevention_recommendations(disease_name: str) -> list:
    """Get prevention recommendations for detected disease"""
    prevention = {
        "Healthy Plant": [
            "Maintain proper watering schedule",
            "Provide adequate sunlight exposure",
            "Use well-draining soil",
            "Fertilize appropriately for plant type",
            "Inspect plants regularly for early detection"
        ],
        "Powdery Mildew": [
            "Ensure proper spacing between plants for air circulation",
            "Avoid overhead watering",
            "Monitor humidity levels regularly",
            "Apply preventive fungicide during humid seasons",
            "Remove debris and fallen leaves promptly"
        ],
        "Leaf Spot Disease": [
            "Avoid watering leaves directly",
            "Ensure good drainage in soil",
            "Rotate crops annually",
            "Use drip irrigation systems",
            "Apply mulch to prevent soil splashing"
        ]
    }
    return prevention.get(disease_name, [
        "Maintain good plant hygiene",
        "Provide optimal growing conditions",
        "Regular monitoring and inspection"
    ])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8501)