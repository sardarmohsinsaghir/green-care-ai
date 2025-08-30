import { Brain, Shield, Zap, Users } from "lucide-react";

export const AboutSection = () => {
  const features = [
    {
      icon: Brain,
      title: "Advanced AI Technology",
      description: "Our machine learning model is trained on over 100,000 plant disease images, ensuring high accuracy in disease detection and classification."
    },
    {
      icon: Zap,
      title: "Instant Results",
      description: "Get comprehensive plant health analysis in seconds, not days. Our optimized algorithms deliver fast, reliable diagnoses when you need them most."
    },
    {
      icon: Shield,
      title: "Proven Accuracy",
      description: "With a 95% accuracy rate validated by agricultural experts, our AI provides reliable diagnoses you can trust for your plant care decisions."
    },
    {
      icon: Users,
      title: "For Everyone",
      description: "Whether you're a professional farmer, passionate gardener, or plant enthusiast, our tool is designed to be accessible and easy to use for all skill levels."
    }
  ];

  return (
    <section className="py-24 bg-gradient-to-b from-secondary/20 to-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center mb-20">
          <h2 className="text-h2 text-foreground mb-6">
            About Plant Savior AI
          </h2>
          <p className="text-body text-muted-foreground max-w-3xl mx-auto leading-relaxed">
            Plant Savior AI is revolutionizing plant health management through cutting-edge artificial intelligence. 
            Our mission is to make plant disease detection accessible to everyone, helping farmers, gardeners, and 
            plant enthusiasts maintain healthier plants and improve crop yields worldwide.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16">
          {features.map((feature, index) => {
            const IconComponent = feature.icon;
            
            return (
              <div key={index} className="card-feature text-center group">
                <div className="w-16 h-16 bg-gradient-to-br from-primary to-primary-light text-primary-foreground rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-nature group-hover:scale-110 transition-transform duration-300">
                  <IconComponent className="w-8 h-8" />
                </div>
                
                <h3 className="text-h3 text-foreground mb-4">{feature.title}</h3>
                <p className="text-body text-muted-foreground">{feature.description}</p>
              </div>
            );
          })}
        </div>

        {/* Mission Statement */}
        <div className="card-nature">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <div>
              <h3 className="text-h2 text-foreground mb-6">Our Mission</h3>
              <p className="text-body text-muted-foreground mb-6">
                We believe that healthy plants are essential for a sustainable future. By democratizing 
                access to advanced plant disease detection technology, we're empowering individuals and 
                communities to take better care of their plants and contribute to global food security.
              </p>
              <p className="text-body text-muted-foreground">
                Our AI technology combines computer vision, machine learning, and agricultural expertise 
                to provide accurate, actionable insights that help plants thrive and ecosystems flourish.
              </p>
            </div>
            
            <div className="relative">
              <div className="aspect-square bg-gradient-to-br from-primary/10 to-cta/10 rounded-3xl flex items-center justify-center">
                <div className="text-center">
                  <Brain className="w-20 h-20 text-primary mx-auto mb-4 animate-pulse-gentle" />
                  <p className="text-h3 text-primary font-bold">AI-Powered</p>
                  <p className="text-body text-muted-foreground">Plant Health Intelligence</p>
                </div>
              </div>
              
              {/* Floating elements */}
              <div className="absolute -top-4 -right-4 w-20 h-20 bg-cta/20 rounded-full animate-float" />
              <div className="absolute -bottom-6 -left-6 w-16 h-16 bg-primary/20 rounded-full animate-float" style={{ animationDelay: '2s' }} />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};