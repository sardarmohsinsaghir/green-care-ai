import { useState } from "react";
import { FileUpload } from "./FileUpload";
import { DiagnosisResults } from "./DiagnosisResults";

// Streamlit API configuration
const STREAMLIT_API_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-streamlit-app.streamlit.app' // Replace with your deployed Streamlit URL
  : 'http://localhost:8501'; // Local Streamlit development URL

// AI diagnosis function that calls Streamlit backend
const callStreamlitDiagnosis = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${STREAMLIT_API_URL}/predict`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`API call failed: ${response.status} ${response.statusText}`);
    }

    const result = await response.json();
    
    // Transform Streamlit response to match our expected format
    return {
      disease: result.predicted_class || result.disease || 'Unknown Disease',
      confidence: Math.round((result.confidence || result.probability || 0) * 100),
      severity: result.severity || 'medium',
      description: result.description || `Detected: ${result.predicted_class || 'Unknown condition'}`,
      treatment: result.treatment || [
        "Consult with a plant specialist for detailed treatment",
        "Monitor plant closely for changes",
        "Ensure proper plant care conditions"
      ],
      prevention: result.prevention || [
        "Maintain good plant hygiene",
        "Provide optimal growing conditions",
        "Regular monitoring and inspection"
      ]
    };
  } catch (error) {
    console.error('Streamlit API Error:', error);
    
    // Fallback error response
    throw new Error(
      error instanceof Error 
        ? `Analysis failed: ${error.message}` 
        : 'Unable to connect to analysis service. Please try again later.'
    );
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

  const handleFileSelect = async (file: File) => {
    setSelectedFile(file);
    setDiagnosisResult(null);
    
    // Start analysis
    setIsAnalyzing(true);
    try {
      const result = await callStreamlitDiagnosis(file);
      setDiagnosisResult(result);
      saveDiagnosis(file, result);
    } catch (error) {
      console.error('Analysis failed:', error);
      // Handle error state
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleClearFile = () => {
    setSelectedFile(null);
    setDiagnosisResult(null);
    setIsAnalyzing(false);
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
        </div>

        <div className="grid lg:grid-cols-2 gap-8 items-start">
          {/* Upload Section */}
          <div className="space-y-6">
            <FileUpload
              onFileSelect={handleFileSelect}
              selectedFile={selectedFile}
              onClearFile={handleClearFile}
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