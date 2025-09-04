# Plant Savior AI Backend

This backend provides API endpoints for plant disease detection using your trained Keras model.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Place your model:**
   - Put `best_plant_model_final.keras` in the `models/` directory
   - The file should be at: `backend/models/best_plant_model_final.keras`

3. **Update class names:**
   - Edit `CLASS_NAMES` in `api.py` to match your model's output classes
   - Default: `["Healthy Plant", "Leaf Spot Disease", "Powdery Mildew"]`

## Running

### FastAPI Server (for React frontend)
```bash
uvicorn api:app --reload --port 8501
```
- API will be available at: http://localhost:8501
- Interactive docs at: http://localhost:8501/docs

### Streamlit App (for testing)
```bash
streamlit run streamlit_app.py --server.port 8502
```
- Streamlit UI at: http://localhost:8502

## API Endpoints

### GET /
Health check endpoint

### POST /predict
Predict plant disease from uploaded image

**Request:**
- Form data with file upload
- Accepts: JPG, JPEG, PNG

**Response:**
```json
{
  "predicted_class": "Powdery Mildew",
  "confidence": 0.92,
  "severity": "medium",
  "description": "A fungal disease that appears as white powdery spots...",
  "treatment": ["Remove affected leaves...", "..."],
  "prevention": ["Ensure proper spacing...", "..."],
  "all_predictions": {
    "Healthy Plant": 0.03,
    "Leaf Spot Disease": 0.05,
    "Powdery Mildew": 0.92
  }
}
```

## Model Requirements

- Input shape: (224, 224, 3) - RGB images
- Output: Softmax probabilities for each class
- Supported formats: .keras, .h5

## Deployment

### Local Development
- FastAPI: `uvicorn api:app --reload --port 8501`
- Streamlit: `streamlit run streamlit_app.py --server.port 8502`

### Production
- Deploy FastAPI to platforms like Railway, Render, or Heroku
- Update `STREAMLIT_API_URL` in your React app to point to deployed API
- Consider using Docker for containerized deployment

## File Structure
```
backend/
├── models/
│   └── best_plant_model_final.keras  # Your trained model
├── api.py                            # FastAPI server
├── streamlit_app.py                  # Streamlit testing interface
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```