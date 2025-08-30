import { useState } from "react";
import { HeroSection } from "@/components/HeroSection";
import { ProcessSteps } from "@/components/ProcessSteps";
import { DiagnosisSection } from "@/components/DiagnosisSection";
import { AboutSection } from "@/components/AboutSection";
import { RecentDiagnoses } from "@/components/RecentDiagnoses";

const Index = () => {
  const [showDiagnosis, setShowDiagnosis] = useState(false);

  const handleStartDiagnosis = () => {
    setShowDiagnosis(true);
    // Smooth scroll to diagnosis section
    setTimeout(() => {
      const diagnosisSection = document.getElementById('diagnosis-section');
      if (diagnosisSection) {
        diagnosisSection.scrollIntoView({ behavior: 'smooth' });
      }
    }, 100);
  };

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <HeroSection onStartDiagnosis={handleStartDiagnosis} />

      {/* Process Steps */}
      <ProcessSteps />

      {/* Diagnosis Section */}
      <div id="diagnosis-section">
        <DiagnosisSection />
      </div>

      {/* Recent Diagnoses */}
      <RecentDiagnoses />

      {/* About Section */}
      <AboutSection />

      {/* Footer */}
      <footer className="bg-foreground text-background py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-h3 mb-4 text-primary-light">Plant Savior AI</h3>
              <p className="text-body opacity-80">
                AI-powered plant disease detection for healthier plants and better yields.
              </p>
            </div>
            
            <div>
              <h4 className="text-h3 mb-4">Quick Links</h4>
              <ul className="space-y-2 text-body opacity-80">
                <li><a href="#" className="hover:text-primary-light transition-colors">How It Works</a></li>
                <li><a href="#" className="hover:text-primary-light transition-colors">About Us</a></li>
                <li><a href="#" className="hover:text-primary-light transition-colors">Contact</a></li>
                <li><a href="#" className="hover:text-primary-light transition-colors">Privacy Policy</a></li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-h3 mb-4">Contact</h4>
              <div className="text-body opacity-80 space-y-2">
                <p>Email: support@plantsavior.ai</p>
                <p>Phone: +1 (555) 123-4567</p>
                <p>Available 24/7 for plant emergencies</p>
              </div>
            </div>
          </div>
          
          <div className="border-t border-background/20 mt-8 pt-8 text-center">
            <p className="text-body opacity-60">
              © 2024 Plant Savior AI. All rights reserved. Built with love for plants and technology.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
