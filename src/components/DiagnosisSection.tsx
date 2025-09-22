import { useState } from "react";
import { FileUpload } from "./FileUpload";
import { DiagnosisResults } from "./DiagnosisResults";

// Mock AI diagnosis function
const mockDiagnosis = async (file: File) => {
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 3000));

  // Mock results based on filename or random selection
  const mockDiseases = [
    {
      disease: "Powdery Mildew",
      confidence: 92,
      severity: 'medium' as const,
      description: "A fungal disease that appears as white powdery spots on leaves and stems.",
      treatment: [
        "Remove affected leaves and dispose of them away from healthy plants",
        "Improve air circulation around the plant",
        "Apply fungicidal soap or neem oil spray every 7-10 days",
        "Reduce humidity levels around the plant",
        "Water at soil level to avoid wetting leaves"
      ],
      prevention: [
        "Ensure proper spacing between plants for air circulation",
        "Avoid overhead watering",
        "Monitor humidity levels regularly",
        "Apply preventive fungicide during humid seasons",
        "Remove debris and fallen leaves promptly"
      ]
    },
    {
      disease: "Leaf Spot Disease",
      confidence: 87,
      severity: 'low' as const,
      description: "Bacterial or fungal infection causing dark spots on leaf surfaces.",
      treatment: [
        "Remove infected leaves immediately",
        "Apply copper-based fungicide spray",
        "Increase spacing between plants",
        "Water plants at soil level only",
        "Disinfect gardening tools between uses"
      ],
      prevention: [
        "Avoid watering leaves directly",
        "Ensure good drainage in soil",
        "Rotate crops annually",
        "Use drip irrigation systems",
        "Apply mulch to prevent soil splashing"
      ]
    },
    {
      disease: "Healthy Plant",
      confidence: 96,
      severity: 'low' as const,
      description: "No disease detected. Your plant appears to be in excellent health!",
      treatment: [
        "Continue current care routine",
        "Monitor plant regularly for changes",
        "Maintain consistent watering schedule",
        "Ensure adequate lighting conditions",
        "Check for pests monthly"
      ],
      prevention: [
        "Maintain proper watering schedule",
        "Provide adequate sunlight exposure",
        "Use well-draining soil",
        "Fertilize appropriately for plant type",
        "Inspect plants regularly for early detection"
      ]
    }
  ];

  // Return random result for demonstration
  return mockDiseases[Math.floor(Math.random() * mockDiseases.length)];
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
      const result = await mockDiagnosis(file);
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