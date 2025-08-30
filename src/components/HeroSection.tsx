import { Upload, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import heroImage from "@/assets/hero-plants.jpg";

interface HeroSectionProps {
  onStartDiagnosis: () => void;
}

export const HeroSection = ({ onStartDiagnosis }: HeroSectionProps) => {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background Image with Overlay */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: `url(${heroImage})` }}
      >
        <div className="absolute inset-0 bg-gradient-to-r from-background/95 via-background/80 to-transparent" />
      </div>

      {/* Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="text-left animate-slide-up">
            <div className="mb-6">
              <span className="inline-flex items-center px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium mb-4">
                🌱 AI-Powered Plant Health
              </span>
            </div>
            
            <h1 className="text-h1 text-foreground mb-6 leading-tight">
              Plant Savior AI
              <span className="block text-gradient mt-2">
                Instant Plant Disease Detection
              </span>
            </h1>
            
            <p className="text-body text-muted-foreground mb-8 max-w-xl">
              Upload an image of your plant's leaves and receive instant AI-powered disease diagnosis 
              with personalized treatment recommendations. Help your plants thrive with cutting-edge 
              artificial intelligence technology.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 mb-12">
              <Button 
                onClick={onStartDiagnosis}
                className="btn-cta flex items-center gap-2 text-lg px-8 py-4 h-auto"
              >
                <Upload className="w-5 h-5" />
                Start Diagnosis
                <ArrowRight className="w-5 h-5" />
              </Button>
              
              <Button 
                variant="outline" 
                className="btn-outline text-lg px-8 py-4 h-auto"
              >
                Learn More
              </Button>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-6">
              <div className="text-center">
                <div className="text-h3 text-primary font-bold">95%</div>
                <div className="text-small text-muted-foreground">Accuracy Rate</div>
              </div>
              <div className="text-center">
                <div className="text-h3 text-primary font-bold">50+</div>
                <div className="text-small text-muted-foreground">Plant Diseases</div>
              </div>
              <div className="text-center">
                <div className="text-h3 text-primary font-bold">24/7</div>
                <div className="text-small text-muted-foreground">Available</div>
              </div>
            </div>
          </div>

          {/* Right Content - Floating Elements */}
          <div className="relative hidden lg:block">
            <div className="absolute inset-0 animate-float">
              <div className="w-64 h-64 bg-gradient-to-br from-primary/20 to-cta/20 rounded-full blur-3xl" />
            </div>
            <div className="relative z-10 animate-pulse-gentle">
              <div className="w-72 h-72 bg-gradient-to-br from-primary/10 to-primary-light/10 rounded-2xl backdrop-blur-sm border border-primary/20" />
            </div>
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div className="w-6 h-10 border-2 border-primary/30 rounded-full flex justify-center">
          <div className="w-1 h-3 bg-primary rounded-full mt-2 animate-pulse" />
        </div>
      </div>
    </section>
  );
};