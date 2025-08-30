import { useState, useEffect } from "react";
import { History, Calendar, AlertTriangle, CheckCircle, Info, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";

interface DiagnosisHistoryItem {
  id: string;
  date: string;
  disease: string;
  confidence: number;
  severity: 'low' | 'medium' | 'high';
  fileName: string;
}

export const RecentDiagnoses = () => {
  const [diagnoses, setDiagnoses] = useState<DiagnosisHistoryItem[]>([]);

  useEffect(() => {
    // Load from localStorage on mount
    const saved = localStorage.getItem('plant-diagnoses');
    if (saved) {
      try {
        setDiagnoses(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to parse saved diagnoses:', e);
      }
    }
  }, []);

  const clearHistory = () => {
    setDiagnoses([]);
    localStorage.removeItem('plant-diagnoses');
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'low':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'medium':
        return <Info className="w-4 h-4 text-yellow-500" />;
      case 'high':
        return <AlertTriangle className="w-4 h-4 text-red-500" />;
      default:
        return <Info className="w-4 h-4 text-gray-500" />;
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'low':
        return 'text-green-600 bg-green-50 border-green-200';
      case 'medium':
        return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'high':
        return 'text-red-600 bg-red-50 border-red-200';
      default:
        return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  if (diagnoses.length === 0) {
    return (
      <section className="py-16 bg-gradient-to-b from-secondary/30 to-background">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="card-nature text-center py-12">
            <div className="w-16 h-16 bg-muted rounded-full flex items-center justify-center mx-auto mb-6">
              <History className="w-8 h-8 text-muted-foreground" />
            </div>
            <h3 className="text-h3 text-foreground mb-2">No Recent Diagnoses</h3>
            <p className="text-body text-muted-foreground">
              Your recent plant diagnoses will appear here after you start using the system.
            </p>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="py-16 bg-gradient-to-b from-secondary/30 to-background">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary/10 rounded-xl flex items-center justify-center">
              <History className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h2 className="text-h2 text-foreground">Recent Diagnoses</h2>
              <p className="text-small text-muted-foreground">{diagnoses.length} diagnoses stored</p>
            </div>
          </div>
          
          <Button
            variant="ghost"
            size="sm"
            onClick={clearHistory}
            className="text-muted-foreground hover:text-destructive"
          >
            <Trash2 className="w-4 h-4 mr-2" />
            Clear History
          </Button>
        </div>

        {/* Diagnoses List */}
        <div className="space-y-4">
          {diagnoses.map((diagnosis) => (
            <div key={diagnosis.id} className="card-feature">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4 flex-1 min-w-0">
                  {getSeverityIcon(diagnosis.severity)}
                  
                  <div className="flex-1 min-w-0">
                    <h4 className="text-h3 text-foreground truncate">{diagnosis.disease}</h4>
                    <div className="flex items-center gap-3 mt-1">
                      <div className="flex items-center gap-1 text-small text-muted-foreground">
                        <Calendar className="w-3 h-3" />
                        {new Date(diagnosis.date).toLocaleDateString()}
                      </div>
                      <span className="text-small text-muted-foreground truncate">
                        {diagnosis.fileName}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3 flex-shrink-0">
                  <div className="text-right">
                    <div className="text-small font-semibold text-primary">
                      {diagnosis.confidence}% confidence
                    </div>
                    <div className={`px-2 py-1 rounded-full border text-xs font-medium ${getSeverityColor(diagnosis.severity)}`}>
                      {diagnosis.severity.toUpperCase()}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};