const express = require('express');
const multer = require('multer');
const tf = require('@tensorflow/tfjs-node');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Configure multer for file uploads
const upload = multer({
  dest: 'uploads/',
  limits: {
    fileSize: 5 * 1024 * 1024 // 5MB limit
  }
});

// Load model and treatment data
let model = null;
let treatmentData = null;

// Load the model and treatment data on server start
async function loadModelAndData() {
  try {
    // Load the Keras model
    console.log('Loading plant disease detection model...');
    model = await tf.loadLayersModel('file://./models/best_plant_model_final.keras');
    console.log('Model loaded successfully');

    // Load treatment data
    console.log('Loading treatment data...');
    const treatmentDataPath = path.join(__dirname, 'data', 'treatment_dict_complete.json');
    treatmentData = JSON.parse(fs.readFileSync(treatmentDataPath, 'utf8'));
    console.log('Treatment data loaded successfully');
  } catch (error) {
    console.error('Error loading model or data:', error);
    process.exit(1);
  }
}

// Preprocess image for model
function preprocessImage(imagePath) {
  return new Promise((resolve, reject) => {
    try {
      const imageBuffer = fs.readFileSync(imagePath);
      const tfImage = tf.node.decodeImage(imageBuffer);
      
      // Resize to model input size (assuming 224x224, adjust if different)
      const resized = tf.image.resizeBilinear(tfImage, [224, 224]);
      
      // Normalize pixel values to [0,1]
      const normalized = resized.div(255.0);
      
      // Add batch dimension
      const batched = normalized.expandDims(0);
      
      resolve(batched);
    } catch (error) {
      reject(error);
    }
  });
}

// Main diagnosis endpoint
app.post('/api/diagnose', upload.single('image'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No image file provided' });
    }

    if (!model || !treatmentData) {
      return res.status(500).json({ error: 'Model or treatment data not loaded' });
    }

    // Preprocess the uploaded image
    const preprocessedImage = await preprocessImage(req.file.path);
    
    // Make prediction
    const prediction = model.predict(preprocessedImage);
    const scores = await prediction.data();
    
    // Get the predicted class (highest probability)
    const predictedClassIndex = scores.indexOf(Math.max(...scores));
    const confidence = Math.round(Math.max(...scores) * 100);
    
    // Map class index to disease name (you may need to adjust this based on your model's class mapping)
    const classNames = Object.keys(treatmentData);
    const predictedDisease = classNames[predictedClassIndex] || 'Unknown';
    
    // Get treatment information
    const diseaseInfo = treatmentData[predictedDisease] || {
      description: 'Disease information not available',
      treatment: ['Consult with a plant specialist for proper diagnosis'],
      prevention: ['Regular plant health monitoring recommended']
    };

    // Determine severity based on confidence and disease type
    let severity = 'low';
    if (predictedDisease !== 'Healthy' && confidence > 80) {
      severity = 'high';
    } else if (predictedDisease !== 'Healthy' && confidence > 60) {
      severity = 'medium';
    }

    // Clean up uploaded file
    fs.unlinkSync(req.file.path);

    // Return diagnosis result
    res.json({
      disease: predictedDisease,
      confidence: confidence,
      severity: severity,
      description: diseaseInfo.description || 'No description available',
      treatment: diseaseInfo.treatment || [],
      prevention: diseaseInfo.prevention || []
    });

  } catch (error) {
    console.error('Diagnosis error:', error);
    
    // Clean up uploaded file on error
    if (req.file && fs.existsSync(req.file.path)) {
      fs.unlinkSync(req.file.path);
    }
    
    res.status(500).json({ error: 'Analysis failed. Please try again.' });
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    model_loaded: !!model,
    treatment_data_loaded: !!treatmentData 
  });
});

// Start server
async function startServer() {
  await loadModelAndData();
  app.listen(PORT, () => {
    console.log(`Plant diagnosis server running on port ${PORT}`);
  });
}

startServer().catch(console.error);