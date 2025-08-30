import { useState } from "react";
import { AlertTriangle, CheckCircle, Info, ChevronDown, ChevronUp } from "lucide-react";
import { Button } from "@/components/ui/button";

interface DiagnosisResult {
  disease: string;
  confidence: number;
  severity: 'low' | 'medium' | 'high';
  description: string;
  treatment: string[];
  prevention: string[];
}

interface DiagnosisResultsProps {
  result: DiagnosisResult;
  isLoading?: boolean;
}

export const DiagnosisResults = ({ result, isLoading = false }: DiagnosisResultsProps) => {
  const [showDetails, setShowDetails] = useState(false);

  if (isLoading) {
    return (
      <div className="card-nature">
        <div className="text-center py-12">
          <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6 animate-pulse-gentle">
            <div className="w-8 h-8 bg-primary/20 rounded-full animate-spin" />
          </div>
          <h3 className="text-h3 text-foreground mb-2">Analyzing Your Plant...</h3>
          <p className="text-body text-muted-foreground">
            Our AI is examining the image for disease indicators
          </p>
          <div className="progress-nature w-64 h-2 mx-auto mt-6">
            <div className="progress-bar w-3/4" />
          </div>
        </div>
      </div>
    );
  }

  const getSeverityIcon = () => {
    switch (result.severity) {
      case 'low':
        return <CheckCircle className="w-6 h-6 text-green-500" />;
      case 'medium':
        return <Info className="w-6 h-6 text-yellow-500" />;
      case 'high':
        return <AlertTriangle className="w-6 h-6 text-red-500" />;
    }
  };

  const getSeverityColor = () => {
    switch (result.severity) {
      case 'low':
        return 'text-green-600 bg-green-50 border-green-200';
      case 'medium':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'high':
        return 'text-red-600 bg-red-50 border-red-200';
    }
  };

  return (
    <div className="space-y-6">
      {/* Main Result Card */}
      <div className="card-nature">
        <div className="flex items-start gap-4 mb-6">
          {getSeverityIcon()}
          <div className="flex-1">
            <h3 className="text-h3 text-foreground mb-2">{result.disease}</h3>
            <p className="text-body text-muted-foreground">{result.description}</p>
          </div>
          <div className={`px-3 py-1 rounded-full border text-small font-medium ${getSeverityColor()}`}>
            {result.severity.toUpperCase()}
          </div>
        </div>

        {/* Confidence Score */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <span className="text-small font-medium text-foreground">Confidence Score</span>
            <span className="text-small font-bold text-primary">{result.confidence}%</span>
          </div>
          <div className="progress-nature h-3">
            <div 
              className="progress-bar" 
              style={{ width: `${result.confidence}%` }} 
            />
          </div>
        </div>

        {/* Quick Actions */}
        <div className="flex gap-3">
          <Button 
            className="btn-cta flex-1"
            onClick={() => setShowDetails(!showDetails)}
          >
            {showDetails ? (
              <>
                Hide Details <ChevronUp className="w-4 h-4 ml-2" />
              </>
            ) : (
              <>
                View Treatment <ChevronDown className="w-4 h-4 ml-2" />
              </>
            )}
          </Button>
          <Button variant="outline" className="btn-outline">
            Get Second Opinion
          </Button>
        </div>
      </div>

      {/* Detailed Treatment */}
      {showDetails && (
        <div className="grid md:grid-cols-2 gap-6 animate-slide-up">
          {/* Treatment */}
          <div className="card-feature">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center">
                <CheckCircle className="w-4 h-4 text-primary" />
              </div>
              <h4 className="text-h3 text-foreground">Treatment</h4>
            </div>
            <ul className="space-y-3">
              {result.treatment.map((step, index) => (
                <li key={index} className="flex items-start gap-3">
                  <div className="w-6 h-6 bg-cta/10 text-cta rounded-full flex items-center justify-center text-small font-bold flex-shrink-0 mt-0.5">
                    {index + 1}
                  </div>
                  <span className="text-small text-muted-foreground">{step}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Prevention */}
          <div className="card-feature">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center">
                <AlertTriangle className="w-4 h-4 text-primary" />
              </div>
              <h4 className="text-h3 text-foreground">Prevention</h4>
            </div>
            <ul className="space-y-3">
              {result.prevention.map((tip, index) => (
                <li key={index} className="flex items-start gap-3">
                  <div className="w-2 h-2 bg-primary rounded-full flex-shrink-0 mt-2" />
                  <span className="text-small text-muted-foreground">{tip}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};