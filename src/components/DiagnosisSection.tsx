import { useState, useEffect } from "react";
import * as tf from '@tensorflow/tfjs';
import { FileUpload } from "./FileUpload";
import { DiagnosisResults } from "./DiagnosisResults";

// Load treatment dictionary
let treatmentDict: any = null;
let model: tf.LayersModel | null = null;

const loadTreatmentDict = async () => {
  if (!treatmentDict) {
    const response = await fetch('/treatment_dict_complete.json');
    treatmentDict = await response.json();
  }
  return treatmentDict;
};

const loadModel = async () => {
  if (!model) {
    try {
      // Try to load from public folder first
      model = await tf.loadLayersModel('/best_plant_model_final.keras');
    } catch (error) {
      console.error('Error loading model:', error);
      throw new Error('Failed to load plant disease detection model');
    }
  }
  return model;
};

const preprocessImage = async (file: File): Promise<tf.Tensor> => {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d')!;
      
      // Resize to model input size (assuming 224x224)
      canvas.width = 224;
      canvas.height = 224;
      ctx.drawImage(img, 0, 0, 224, 224);
      
      // Convert to tensor and normalize
      const tensor = tf.browser.fromPixels(canvas)
        .expandDims(0)
        .cast('float32')
        .div(255.0);
      
      resolve(tensor);
    };
    img.src = URL.createObjectURL(file);
  });
};

const realDiagnosis = async (file: File) => {
  try {
    // Load model and treatment dictionary
    const [loadedModel, treatments] = await Promise.all([
      loadModel(),
      loadTreatmentDict()
    ]);

    // Preprocess the image
    const processedImage = await preprocessImage(file);

    // Make prediction
    const prediction = loadedModel.predict(processedImage) as tf.Tensor;
    const predictionData = await prediction.data();
    
    // Get the class with highest probability
    const maxIndex = predictionData.indexOf(Math.max(...Array.from(predictionData)));
    const confidence = Math.round(predictionData[maxIndex] * 100);
    
    // Get class name and treatment info
    const className = treatments.classes[maxIndex];
    const treatmentInfo = treatments.treatments[className];
    
    // Clean up tensors
    processedImage.dispose();
    prediction.dispose();
    
    if (!treatmentInfo) {
      throw new Error('Treatment information not found for detected disease');
    }

    // Determine severity based on disease type
    let severity: 'low' | 'medium' | 'high' = 'medium';
    if (className.includes('healthy')) {
      severity = 'low';
    } else if (className.includes('blight') || className.includes('rot')) {
      severity = 'high';
    }

    return {
      disease: treatmentInfo.disease,
      confidence,
      severity,
      description: treatmentInfo.description,
      treatment: treatmentInfo.treatment,
      prevention: treatmentInfo.prevention
    };

  } catch (error) {
    console.error('Diagnosis error:', error);
    throw error;
  }
};

const saveDiagnosis = (file: File, result: any) => {
  const diagnosis = {
    id: Date.now().toString(),
    date: new Date().toISOString(),
    disease: result.disease,
    confidence: result.confidence,
    severity: result.severity,
    fileName: file.name
  };

  const existing = JSON.parse(localStorage.getItem('plant-diagnoses') || '[]');
  const updated = [diagnosis, ...existing].slice(0, 10); // Keep only last 10
  localStorage.setItem('plant-diagnoses', JSON.stringify(updated));
};

export const DiagnosisSection = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [diagnosisResult, setDiagnosisResult] = useState<any>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [modelLoading, setModelLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Initialize TensorFlow.js and load model on component mount
  useEffect(() => {
    const initializeTensorFlow = async () => {
      setModelLoading(true);
      try {
        // Set backend to webgl for better performance
        await tf.setBackend('webgl');
        await tf.ready();
        
        // Preload model and treatment dictionary
        await Promise.all([loadModel(), loadTreatmentDict()]);
        
        console.log('Model and treatment dictionary loaded successfully');
      } catch (error) {
        console.error('Failed to initialize TensorFlow or load model:', error);
        setError('Failed to load AI model. Please refresh the page.');
      } finally {
        setModelLoading(false);
      }
    };

    initializeTensorFlow();
  }, []);

  const handleFileSelect = async (file: File) => {
    setSelectedFile(file);
    setDiagnosisResult(null);
    setError(null);
    
    // Start analysis
    setIsAnalyzing(true);
    try {
      const result = await realDiagnosis(file);
      setDiagnosisResult(result);
      saveDiagnosis(file, result);
    } catch (error) {
      console.error('Analysis failed:', error);
      setError('Failed to analyze the image. Please try again with a clear plant leaf image.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleClearFile = () => {
    setSelectedFile(null);
    setDiagnosisResult(null);
    setIsAnalyzing(false);
    setError(null);
  };

  const handleNewDiagnosis = () => {
    handleClearFile();
  };

  return (
    <section className="py-24 bg-gradient-to-b from-background to-secondary/20">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-12">
          <h2 className="text-h2 text-foreground mb-4">
            Plant Disease Diagnosis
          </h2>
          <p className="text-body text-muted-foreground max-w-2xl mx-auto">
            Upload a clear image of your plant's leaves to get instant AI-powered disease detection 
            and treatment recommendations.
          </p>
          {modelLoading && (
            <div className="mt-4 p-4 bg-primary/10 rounded-lg">
              <p className="text-sm text-primary">Loading AI model, please wait...</p>
            </div>
          )}
          {error && (
            <div className="mt-4 p-4 bg-destructive/10 text-destructive rounded-lg">
              <p className="text-sm">{error}</p>
            </div>
          )}
        </div>

        <div className="grid lg:grid-cols-2 gap-8 items-start">
          {/* Upload Section */}
          <div className="space-y-6">
            <FileUpload
              onFileSelect={handleFileSelect}
              selectedFile={selectedFile}
              onClearFile={handleClearFile}
              disabled={modelLoading || isAnalyzing}
            />

            {/* Image Preview */}
            {selectedFile && (
              <div className="card-nature">
                <h4 className="text-h3 text-foreground mb-4">Image Preview</h4>
                <div className="aspect-square w-full bg-muted rounded-xl overflow-hidden">
                  <img
                    src={URL.createObjectURL(selectedFile)}
                    alt="Plant leaf for analysis"
                    className="w-full h-full object-cover"
                  />
                </div>
                
                {diagnosisResult && !isAnalyzing && (
                  <div className="mt-4 pt-4 border-t border-border">
                    <button
                      onClick={handleNewDiagnosis}
                      className="btn-outline w-full"
                    >
                      Analyze New Image
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Results Section */}
          <div>
            {(isAnalyzing || diagnosisResult) && (
              <DiagnosisResults
                result={diagnosisResult}
                isLoading={isAnalyzing}
              />
            )}

            {!selectedFile && !isAnalyzing && !diagnosisResult && (
              <div className="card-nature text-center py-12">
                <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6">
                  <div className="w-8 h-8 border-2 border-primary/30 border-t-primary rounded-full" />
                </div>
                <h4 className="text-h3 text-foreground mb-2">Ready for Analysis</h4>
                <p className="text-body text-muted-foreground">
                  Upload an image to get started with AI-powered plant disease detection.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
};