import { Upload, Brain, FileText } from "lucide-react";

export const ProcessSteps = () => {
  const steps = [
    {
      icon: Upload,
      number: "01",
      title: "Upload Image",
      description: "Take or upload a clear photo of your plant's leaves showing any visible symptoms or concerns."
    },
    {
      icon: Brain,
      number: "02", 
      title: "AI Analysis",
      description: "Our advanced AI model analyzes the image using machine learning trained on thousands of plant diseases."
    },
    {
      icon: FileText,
      number: "03",
      title: "Get Results",
      description: "Receive instant diagnosis with confidence score and personalized treatment recommendations."
    }
  ];

  return (
    <section className="py-24 bg-gradient-to-b from-background to-secondary/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-20">
          <h2 className="text-h2 text-foreground mb-4">
            How It Works
          </h2>
          <p className="text-body text-muted-foreground max-w-2xl mx-auto">
            Get instant plant disease diagnosis in three simple steps. Our AI-powered system 
            makes plant health monitoring accessible to everyone.
          </p>
        </div>

        {/* Steps Grid */}
        <div className="grid md:grid-cols-3 gap-8 lg:gap-12">
          {steps.map((step, index) => {
            const IconComponent = step.icon;
            
            return (
              <div key={index} className="relative group">
                {/* Connector Line */}
                {index < steps.length - 1 && (
                  <div className="hidden md:block absolute top-16 left-full w-full h-0.5 bg-gradient-to-r from-primary/50 to-transparent transform translate-x-4 lg:translate-x-8" />
                )}
                
                <div className="card-feature text-center relative z-10">
                  {/* Step Number */}
                  <div className="absolute -top-4 -right-4 w-12 h-12 bg-cta text-cta-foreground rounded-full flex items-center justify-center font-bold text-sm">
                    {step.number}
                  </div>
                  
                  {/* Icon */}
                  <div className="w-16 h-16 bg-gradient-to-br from-primary to-primary-light text-primary-foreground rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-nature">
                    <IconComponent className="w-8 h-8" />
                  </div>
                  
                  {/* Content */}
                  <h3 className="text-h3 text-foreground mb-4">{step.title}</h3>
                  <p className="text-body text-muted-foreground leading-relaxed">{step.description}</p>
                </div>
              </div>
            );
          })}
        </div>

        {/* Bottom CTA */}
        <div className="text-center mt-16">
          <div className="inline-flex items-center gap-2 px-6 py-3 bg-primary/10 text-primary rounded-full">
            <Brain className="w-4 h-4" />
            <span className="text-sm font-medium">Powered by Advanced Machine Learning</span>
          </div>
        </div>
      </div>
    </section>
  );
};