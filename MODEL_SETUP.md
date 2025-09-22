# Model Setup Instructions

## Required Files

You need to place these files in the `public` folder to replace the placeholders:

1. **best_plant_model_final.keras** - Your trained plant disease detection model
2. **treatment_dict_complete.json** - Your complete treatment dictionary (already partially set up)

## Steps to Setup

1. Copy your `best_plant_model_final.keras` file to `public/best_plant_model_final.keras`
2. Update `public/treatment_dict_complete.json` with your complete treatment data matching your model's classes

## Model Format

The app expects:
- A Keras model (.keras format) that outputs predictions for plant disease classes
- Input image size of 224x224 pixels (will be automatically resized)
- The model should output probabilities for each class

## Treatment Dictionary Format

The JSON should contain:
- `classes`: Array of class names matching your model's output
- `treatments`: Object mapping class names to treatment information

Your model integration is now ready! Just replace the placeholder files with your actual model and treatment data.