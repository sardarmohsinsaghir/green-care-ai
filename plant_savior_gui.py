import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
from pathlib import Path
import threading

class PlantSaviorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌱 Plant Savior AI - Disease Detection")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f9ff')
        
        # Model and class names
        self.model = None
        self.class_names = ["Healthy Plant", "Leaf Spot Disease", "Powdery Mildew"]
        self.current_image = None
        
        # Load model on startup
        self.load_model()
        
        # Create GUI
        self.create_widgets()
        
    def load_model(self):
        """Load the Keras model"""
        model_path = Path("backend/models/best_plant_model_final.keras")
        if not model_path.exists():
            model_path = Path("best_plant_model_final.keras")
        
        try:
            self.model = tf.keras.models.load_model(model_path)
            self.model_status = "✅ Model loaded successfully!"
        except Exception as e:
            self.model_status = f"❌ Error loading model: {e}"
            self.model = None
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Title
        title_frame = tk.Frame(self.root, bg='#f0f9ff')
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame, 
            text="🌱 Plant Savior AI", 
            font=("Helvetica", 24, "bold"),
            bg='#f0f9ff',
            fg='#0f766e'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame, 
            text="AI-Powered Plant Disease Detection & Treatment Recommendations", 
            font=("Helvetica", 12),
            bg='#f0f9ff',
            fg='#374151'
        )
        subtitle_label.pack()
        
        # Model status
        status_label = tk.Label(
            title_frame, 
            text=self.model_status, 
            font=("Helvetica", 10),
            bg='#f0f9ff',
            fg='#059669' if self.model else '#dc2626'
        )
        status_label.pack(pady=5)
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='#f0f9ff')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Image upload and display
        left_frame = tk.LabelFrame(
            main_frame, 
            text="Upload Plant Image", 
            font=("Helvetica", 14, "bold"),
            bg='#ffffff',
            fg='#374151',
            bd=2,
            relief='ridge'
        )
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Upload button
        upload_btn = tk.Button(
            left_frame,
            text="📁 Select Image",
            font=("Helvetica", 12, "bold"),
            bg='#0d9488',
            fg='white',
            activebackground='#0f766e',
            activeforeground='white',
            command=self.upload_image,
            pady=10,
            cursor='hand2'
        )
        upload_btn.pack(pady=20)
        
        # Image display
        self.image_frame = tk.Frame(left_frame, bg='#f8fafc', relief='sunken', bd=2)
        self.image_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        self.image_label = tk.Label(
            self.image_frame,
            text="No image selected\n\nSupported formats: JPG, JPEG, PNG",
            font=("Helvetica", 12),
            bg='#f8fafc',
            fg='#64748b'
        )
        self.image_label.pack(expand=True)
        
        # Analyze button
        self.analyze_btn = tk.Button(
            left_frame,
            text="🔍 Analyze Plant",
            font=("Helvetica", 12, "bold"),
            bg='#059669',
            fg='white',
            activebackground='#047857',
            activeforeground='white',
            command=self.analyze_image,
            state=tk.DISABLED,
            pady=10,
            cursor='hand2'
        )
        self.analyze_btn.pack(pady=20)
        
        # Right panel - Results
        right_frame = tk.LabelFrame(
            main_frame, 
            text="Analysis Results", 
            font=("Helvetica", 14, "bold"),
            bg='#ffffff',
            fg='#374151',
            bd=2,
            relief='ridge'
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        # Results notebook (tabs)
        self.notebook = ttk.Notebook(right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Prediction tab
        self.prediction_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.prediction_frame, text="🎯 Prediction")
        
        # Treatment tab
        self.treatment_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.treatment_frame, text="💊 Treatment")
        
        # Prevention tab
        self.prevention_frame = tk.Frame(self.notebook, bg='#ffffff')
        self.notebook.add(self.prevention_frame, text="🛡️ Prevention")
        
        # Initialize result displays
        self.init_result_displays()
    
    def init_result_displays(self):
        """Initialize result display areas"""
        # Prediction results
        self.prediction_text = tk.Text(
            self.prediction_frame,
            wrap=tk.WORD,
            font=("Helvetica", 11),
            bg='#f8fafc',
            fg='#374151',
            height=15,
            padx=10,
            pady=10
        )
        self.prediction_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treatment recommendations
        self.treatment_text = tk.Text(
            self.treatment_frame,
            wrap=tk.WORD,
            font=("Helvetica", 11),
            bg='#f8fafc',
            fg='#374151',
            height=15,
            padx=10,
            pady=10
        )
        self.treatment_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Prevention recommendations
        self.prevention_text = tk.Text(
            self.prevention_frame,
            wrap=tk.WORD,
            font=("Helvetica", 11),
            bg='#f8fafc',
            fg='#374151',
            height=15,
            padx=10,
            pady=10
        )
        self.prevention_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initial placeholder text
        self.clear_results()
    
    def clear_results(self):
        """Clear all result displays"""
        placeholder = "Upload and analyze an image to see results here..."
        
        for text_widget in [self.prediction_text, self.treatment_text, self.prevention_text]:
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, placeholder)
            text_widget.config(state=tk.DISABLED)
    
    def upload_image(self):
        """Handle image upload"""
        file_path = filedialog.askopenfilename(
            title="Select Plant Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Load and display image
                img = Image.open(file_path)
                self.current_image = img.copy()
                
                # Resize for display (maintain aspect ratio)
                display_size = (300, 300)
                img.thumbnail(display_size, Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(img)
                
                # Update display
                self.image_label.config(image=photo, text="")
                self.image_label.image = photo  # Keep a reference
                
                # Enable analyze button
                if self.model:
                    self.analyze_btn.config(state=tk.NORMAL)
                
                # Clear previous results
                self.clear_results()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")
    
    def preprocess_image(self, img):
        """Preprocess image for model prediction"""
        # Convert to RGB and resize
        img = img.convert("RGB").resize((224, 224))
        
        # Convert to array and normalize
        img_array = np.array(img) / 255.0
        
        # Add batch dimension
        return np.expand_dims(img_array, 0)
    
    def analyze_image(self):
        """Analyze the uploaded image"""
        if not self.current_image or not self.model:
            return
        
        # Disable button and show progress
        self.analyze_btn.config(state=tk.DISABLED, text="🔄 Analyzing...")
        self.root.config(cursor="wait")
        
        # Run analysis in thread to prevent GUI freezing
        thread = threading.Thread(target=self._run_analysis)
        thread.daemon = True
        thread.start()
    
    def _run_analysis(self):
        """Run the actual analysis (in thread)"""
        try:
            # Preprocess image
            processed_img = self.preprocess_image(self.current_image)
            
            # Make prediction
            predictions = self.model.predict(processed_img, verbose=0)
            probabilities = tf.nn.softmax(predictions[0]).numpy()
            
            # Get results
            predicted_index = int(np.argmax(probabilities))
            confidence = float(probabilities[predicted_index])
            predicted_class = self.class_names[predicted_index] if predicted_index < len(self.class_names) else "Unknown"
            
            # Determine severity
            severity = "Low"
            if predicted_class != "Healthy Plant":
                if confidence > 0.8:
                    severity = "High"
                elif confidence > 0.6:
                    severity = "Medium"
            
            # Update GUI in main thread
            self.root.after(0, self._update_results, predicted_class, confidence, severity, probabilities)
            
        except Exception as e:
            self.root.after(0, self._show_error, f"Analysis failed: {e}")
    
    def _update_results(self, predicted_class, confidence, severity, probabilities):
        """Update results in GUI (main thread)"""
        # Prediction results
        self.prediction_text.config(state=tk.NORMAL)
        self.prediction_text.delete(1.0, tk.END)
        
        prediction_text = f"""🎯 DIAGNOSIS RESULTS

🏥 Detected Condition: {predicted_class}
📊 Confidence Level: {confidence*100:.1f}%
⚠️ Severity: {severity}

📈 DETAILED ANALYSIS:
"""
        
        for i, (class_name, prob) in enumerate(zip(self.class_names, probabilities)):
            percentage = prob * 100
            bar = "█" * int(percentage / 5) + "░" * (20 - int(percentage / 5))
            prediction_text += f"\n{class_name}:\n{bar} {percentage:.1f}%\n"
        
        prediction_text += f"\n\n📝 DESCRIPTION:\n{self.get_disease_description(predicted_class)}"
        
        self.prediction_text.insert(tk.END, prediction_text)
        self.prediction_text.config(state=tk.DISABLED)
        
        # Treatment recommendations
        self.treatment_text.config(state=tk.NORMAL)
        self.treatment_text.delete(1.0, tk.END)
        
        treatment_recommendations = self.get_treatment_recommendations(predicted_class)
        treatment_text = "💊 TREATMENT RECOMMENDATIONS:\n\n"
        for i, rec in enumerate(treatment_recommendations, 1):
            treatment_text += f"{i}. {rec}\n\n"
        
        self.treatment_text.insert(tk.END, treatment_text)
        self.treatment_text.config(state=tk.DISABLED)
        
        # Prevention recommendations
        self.prevention_text.config(state=tk.NORMAL)
        self.prevention_text.delete(1.0, tk.END)
        
        prevention_recommendations = self.get_prevention_recommendations(predicted_class)
        prevention_text = "🛡️ PREVENTION STRATEGIES:\n\n"
        for i, rec in enumerate(prevention_recommendations, 1):
            prevention_text += f"{i}. {rec}\n\n"
        
        self.prevention_text.insert(tk.END, prevention_text)
        self.prevention_text.config(state=tk.DISABLED)
        
        # Reset button and cursor
        self.analyze_btn.config(state=tk.NORMAL, text="🔍 Analyze Plant")
        self.root.config(cursor="")
    
    def _show_error(self, error_msg):
        """Show error message (main thread)"""
        messagebox.showerror("Analysis Error", error_msg)
        self.analyze_btn.config(state=tk.NORMAL, text="🔍 Analyze Plant")
        self.root.config(cursor="")
    
    def get_disease_description(self, disease_name):
        """Get description for detected disease"""
        descriptions = {
            "Healthy Plant": "Excellent news! No disease detected. Your plant appears to be in perfect health with vibrant, disease-free foliage.",
            "Powdery Mildew": "A common fungal disease characterized by white, powdery spots that appear on leaves and stems. This fungus thrives in warm, humid conditions with poor air circulation.",
            "Leaf Spot Disease": "A bacterial or fungal infection that causes dark, circular or irregular spots to develop on leaf surfaces. Can lead to yellowing and premature leaf drop if untreated.",
        }
        return descriptions.get(disease_name, f"Condition detected: {disease_name}. Consult a plant specialist for detailed information.")
    
    def get_treatment_recommendations(self, disease_name):
        """Get treatment recommendations"""
        treatments = {
            "Healthy Plant": [
                "Continue your excellent care routine - you're doing great!",
                "Monitor plant regularly for any changes in appearance",
                "Maintain consistent watering schedule based on plant needs",
                "Ensure adequate lighting conditions for optimal growth",
                "Check monthly for pests and early signs of stress",
                "Consider periodic fertilization during growing season"
            ],
            "Powdery Mildew": [
                "Remove all affected leaves immediately and dispose away from healthy plants",
                "Improve air circulation around the plant by spacing or using fans",
                "Apply fungicidal soap or neem oil spray every 7-10 days until resolved",
                "Reduce humidity levels around the plant (use dehumidifier if needed)",
                "Water at soil level only - avoid wetting leaves completely",
                "Consider applying baking soda solution (1 tsp per quart water) as natural treatment"
            ],
            "Leaf Spot Disease": [
                "Remove infected leaves immediately using sterilized pruning shears",
                "Apply copper-based fungicide spray according to package directions",
                "Increase spacing between plants to improve air circulation",
                "Water plants at soil level only - never water from above",
                "Disinfect all gardening tools between uses with rubbing alcohol",
                "Consider applying compost tea to boost plant immunity"
            ]
        }
        return treatments.get(disease_name, [
            "Consult with a plant specialist for detailed treatment plan",
            "Monitor plant closely for changes over the next week",
            "Ensure proper plant care conditions (water, light, nutrients)",
            "Consider isolating plant to prevent spread to other plants"
        ])
    
    def get_prevention_recommendations(self, disease_name):
        """Get prevention recommendations"""
        prevention = {
            "Healthy Plant": [
                "Maintain proper watering schedule - check soil moisture regularly",
                "Provide adequate sunlight exposure appropriate for plant type",
                "Use well-draining soil to prevent root rot and fungal issues",
                "Fertilize appropriately during growing seasons",
                "Inspect plants weekly for early detection of problems",
                "Quarantine new plants before introducing to collection"
            ],
            "Powdery Mildew": [
                "Ensure proper spacing between plants for optimal air circulation",
                "Avoid overhead watering - use drip irrigation or water at base",
                "Monitor and control humidity levels (keep below 70%)",
                "Apply preventive fungicide during humid seasons",
                "Remove debris and fallen leaves promptly to reduce fungal spores",
                "Choose resistant plant varieties when possible"
            ],
            "Leaf Spot Disease": [
                "Always water at soil level - never wet the foliage",
                "Ensure excellent drainage in soil and containers",
                "Practice crop rotation if growing in garden beds",
                "Use drip irrigation systems instead of sprinklers",
                "Apply organic mulch to prevent soil splashing onto leaves",
                "Maintain good garden hygiene by cleaning up plant debris"
            ]
        }
        return prevention.get(disease_name, [
            "Maintain excellent plant hygiene practices",
            "Provide optimal growing conditions for plant health",
            "Perform regular monitoring and early intervention",
            "Research specific care requirements for your plant species"
        ])

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = PlantSaviorGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()