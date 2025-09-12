# MLOps Grades Classifier

## Overview  
Classifier for student grades using machine learning. The project includes modular pipelines for training, evaluation, and deployment via a REST API.

## Structure  

- `src/`: training, prediction, utility functions  
- `notebook/`: EDA and prototyping  
- `app.py` + `templates/`: Flask app for inference  
- `artifacts/`: serialized models and outputs  
- `Dockerfile`: containerization setup  
- `.github/workflows/`: CI/CD automation  
- `catboost_info/`: logs from CatBoost model training  

## Setup  

```bash
git clone https://github.com/SA-Duran/MLOps_grades_classifier.git
cd MLOps_grades_classifier
pip install -r requirements.txt
```

## Training  

Prepare your dataset and run:

```bash
python src/train_pipeline.py
```

This stores the model in `artifacts/model.pkl`.

## Inference API  

```bash
python app.py
```

Then send a POST request to `/predict`:

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"feature1": value1, "feature2": value2, ...}'
```

## Docker  

```bash
docker build -t grades-classifier .
docker run -p 5000:5000 grades-classifier
```

## Tools  

- CatBoost  
- Flask  
- Docker  
- GitHub Actions  
- Jupyter + pandas + scikit-learn  

## Next Steps  

- Add SHAP explainability  
- Extend to multi-class prediction  
- Improve input validation  

## License  
MIT (add `LICENSE` file if missing)
