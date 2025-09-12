# MLOps Grade Classifier

## 🧠 Overview  
This project implements an end-to-end MLOps pipeline to predict **student math scores** based on demographic and academic features. It includes data ingestion, preprocessing, model training with hyperparameter tuning, and a production-ready Flask app for real-time prediction.

---

## ⚙️ Architecture & Components

### 1. `data_ingestion.py`  
- Loads the dataset (`stud.csv`)  
- Splits into train/test sets and saves them under `artifacts/`:contentReference[oaicite:0]{index=0}

### 2. `data_transformation.py`  
- Preprocesses numeric and categorical features:
  - Imputation (median, most frequent)
  - One-hot encoding
  - Standard scaling
- Saves a `preprocessor.pkl` file for inference reuse:contentReference[oaicite:1]{index=1}

### 3. `model_trainer.py`  
- Trains and evaluates multiple regressors (Random Forest, CatBoost, XGBoost, etc.)  
- Uses `GridSearchCV`-like parameter grids for tuning  
- Saves the best model to `model.pkl` based on R² score:contentReference[oaicite:2]{index=2}

### 4. `train_pipeline.py`  
- Orchestrates the full pipeline: ingestion → transformation → training  
- Saves metrics and artifacts for tracking model performance:contentReference[oaicite:3]{index=3}

### 5. `predict_pipeline.py`  
- Loads saved preprocessor and model  
- Accepts user input via `CustomData`, transforms and predicts the math score:contentReference[oaicite:4]{index=4}

### 6. `app.py`  
- Flask web server with:
  - `/` for homepage  
  - `/predictdata` for form submission and model inference  
- Renders prediction results via HTML templates:contentReference[oaicite:5]{index=5}

---

## 🧰 Tech Stack

| Layer            | Tools / Libraries                      |
|------------------|-----------------------------------------|
| ML Models        | CatBoost, XGBoost, RandomForest, etc.   |
| Preprocessing    | Scikit-learn pipelines + transformers   |
| Web Interface    | Flask + Jinja templates                 |
| Packaging        | `pyproject.toml`, `setuptools`          |
| Logging & Errors | Python `logging`, custom exception class|
| Deployment-ready | Modular pipelines, reusable artifacts   |

---

## 📦 Installation

```bash
git clone https://github.com/SA-Duran/MLOps_grade_classifier.git
cd MLOps_grade_classifier
pip install -r requirements.txt
```

Or if you're using PEP 621-style packaging:

```bash
pip install .
```

Set your Python version to 3.10+ as specified in `pyproject.toml`:contentReference[oaicite:6]{index=6}

---

## 🚀 Run the Training Pipeline

```bash
python train_pipeline.py
```

This will:
- Ingest and split data
- Preprocess features
- Train multiple models with tuning
- Save best model and metrics in `artifacts/`

---

## 🧪 Make Predictions via Web App

```bash
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) and input values like:

- Gender
- Race/Ethnicity
- Parental Education Level
- Lunch type
- Test Preparation Course
- Reading and Writing Scores

It will return the predicted **Math Score**.

---

## 📁 Output Artifacts

- `model.pkl`: trained regression model  
- `preprocessor.pkl`: Scikit-learn transformation pipeline  
- `train.csv`, `test.csv`: split datasets  
- `metrics.json`: training performance (R², MAE, etc.)

---

## 📄 License

MIT
