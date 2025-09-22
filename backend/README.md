# Plant Savior Backend

## Setup Instructions

1. **Install Dependencies:**
   ```bash
   cd backend
   npm install
   ```

2. **Add Model Files:**
   - Place `best_plant_model_final.keras` in `backend/models/` directory
   - Place `treatment_dict_complete.json` in `backend/data/` directory

3. **Directory Structure:**
   ```
   backend/
   ├── models/
   │   └── best_plant_model_final.keras
   ├── data/
   │   └── treatment_dict_complete.json
   ├── uploads/ (auto-created)
   ├── server.js
   └── package.json
   ```

4. **Run the Server:**
   ```bash
   npm start
   # or for development
   npm run dev
   ```

The API will be available at `http://localhost:3001`

## API Endpoints

- `POST /api/diagnose` - Upload image for disease detection
- `GET /api/health` - Check server and model status