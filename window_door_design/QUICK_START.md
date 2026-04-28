# Quick Start Guide - AI Recommendation System

## 🚀 5-Minute Setup

### Prerequisites
```bash
# Ensure you're in the project directory
cd /Users/tejassantoshdhembe/Downloads/Design/window_door_design

# Activate virtual environment
source /Users/tejassantoshdhembe/Downloads/Design/.venv/bin/activate
```

### Step 1: Generate Dataset
```bash
cd design_system
python dataset_generator.py
```
Output: Creates `dataset.csv` with 1000 samples

### Step 2: Train Model
```bash
python train_model.py
```
Output: Creates `model.pkl` and `encoders.pkl`

### Step 3: Start Django Server
```bash
cd ..
python manage.py runserver
```
Server starts at: `http://localhost:8000/`

### Step 4: Access Recommendation System
Open browser: `http://localhost:8000/recommendation/`

---

## 💡 Quick Examples

### Example 1: Living Room (High Budget)
**Input**:
- Room Size: Large
- Budget: High
- Noise Level: Low
- Sunlight: High
- Room Type: Living

**Expected Result**: Sliding + Toughened + Premium

### Example 2: Bedroom (Budget Conscious)
**Input**:
- Room Size: Small
- Budget: Low
- Noise Level: Low
- Sunlight: Medium
- Room Type: Bedroom

**Expected Result**: Casement + Single + Basic

### Example 3: Noisy Kitchen
**Input**:
- Room Size: Medium
- Budget: Medium
- Noise Level: High
- Sunlight: Low
- Room Type: Kitchen

**Expected Result**: Sliding + Double + Standard

---

## 🐍 Python API Quick Reference

### Import Predictor
```python
from design_system.predict import DesignPredictor, predict_design
```

### Quick Prediction
```python
result = predict_design({
    'room_size': 'large',
    'budget': 'high',
    'noise_level': 'low',
    'sunlight': 'high',
    'room_type': 'living'
})
print(result)
# {'window_type': 'sliding', 'glass_type': 'toughened', 'material_type': 'aluminium_premium'}
```

### Full Details
```python
from design_system.predict import get_recommendation_details

predictor = DesignPredictor()
prediction = predictor.predict(user_input)
details = get_recommendation_details(prediction)
print(details['advantages'])
```

### Get Valid Values
```python
valid = predictor.get_valid_values()
# {
#     'room_size': ['small', 'medium', 'large'],
#     'budget': ['low', 'medium', 'high'],
#     ...
# }
```

---

## 🌐 Web Interface

### Location
```
http://localhost:8000/recommendation/
```

### Form Fields
1. **Room Size**: small, medium, large
2. **Budget**: low, medium, high
3. **Noise Level**: low, medium, high
4. **Sunlight**: low, medium, high
5. **Room Type**: bedroom, kitchen, office, living

### Actions
- Click "Get Recommendation" → See predictions
- Click "Create Design Based on Recommendation" → Create design

---

## 📊 Model Info

| Metric | Value |
|--------|-------|
| Training Samples | 1000 |
| Features | 5 |
| Targets | 3 (multi-output) |
| Algorithm | RandomForest (100 trees) |
| Train/Test Split | 80/20 |
| **Average Accuracy** | **66.3%** |
| Window Type Accuracy | 59% |
| Glass Type Accuracy | 69% |
| Material Type Accuracy | 71% |

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `dataset_generator.py` | Generate training data |
| `train_model.py` | Train ML model |
| `predict.py` | Make predictions |
| `dataset.csv` | Training dataset |
| `model.pkl` | Trained model |
| `encoders.pkl` | LabelEncoders |
| `recommendation.html` | Web UI |
| `views.py` | Django view |
| `urls.py` | URL routing |

---

## 🔧 Troubleshooting

### "Model not found" Error
```bash
# Solution: Run training
python design_system/train_model.py
```

### "Dataset not found" Error
```bash
# Solution: Generate dataset
python design_system/dataset_generator.py
```

### Server won't start
```bash
# Kill any existing process
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Start fresh
python manage.py runserver
```

### Module import errors
```bash
# Ensure virtual environment is activated
source /Users/tejassantoshdhembe/Downloads/Design/.venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 📈 Performance Expectations

**Prediction Speed**: <100ms per prediction

**Accuracy by Feature**:
- Window Type: 59% (room size dependent)
- Glass Type: 69% (noise level dependent)
- Material Type: 71% (budget dependent)

**Use Case**: Best for general recommendations, not critical applications

---

## 🎯 Common Tasks

### View Model Performance
```bash
cd design_system
python train_model.py  # Shows accuracy metrics
```

### Test Prediction
```bash
cd design_system
python predict.py  # Runs test prediction
```

### Regenerate Everything
```bash
cd design_system
python dataset_generator.py  # 1. Create data
python train_model.py         # 2. Train model
# Server automatically loads new model
```

---

## 📚 Full Documentation

For detailed information, see:
- `ML_RECOMMENDATION_SYSTEM.md` (Comprehensive guide)
- `ML_SYSTEM_IMPLEMENTATION_SUMMARY.md` (Implementation details)
- Docstrings in Python files (Code documentation)

---

## 🚦 Status Check

### Verify Installation
```bash
# Check packages installed
pip list | grep -E "pandas|numpy|scikit"

# Check files exist
ls design_system/{dataset.csv,model.pkl,encoders.pkl}

# Check server
curl http://localhost:8000/recommendation/ | head -10
```

---

## ⚡ Performance Tips

1. **Batch Predictions**: Make multiple predictions in one session
2. **Cache Predictor**: Load once, reuse multiple times
3. **Monitor**: Track prediction accuracy over time
4. **Feedback**: Collect user validation for model improvement

---

## 🎓 Learning Path

1. **Beginner**: Use web interface at `/recommendation/`
2. **Intermediate**: Run Python scripts directly
3. **Advanced**: Modify rule-based logic in `dataset_generator.py`
4. **Expert**: Retrain model with custom hyperparameters

---

## 📞 Support

### Check Logs
```bash
python manage.py runserver  # Shows Django logs
```

### Debug Prediction
```python
from design_system.predict import DesignPredictor
predictor = DesignPredictor()
# Check valid values
print(predictor.get_valid_values())
```

### View Dataset
```bash
head -20 design_system/dataset.csv
```

---

## ✅ Ready to Go!

Your ML recommendation system is ready. Start with:

```bash
cd /Users/tejassantoshdhembe/Downloads/Design/window_door_design
source /Users/tejassantoshdhembe/Downloads/Design/.venv/bin/activate
python manage.py runserver
# Visit: http://localhost:8000/recommendation/
```

Enjoy! 🎉

---

**Last Updated**: April 17, 2026  
**Version**: 1.0  
**Status**: Ready for Production ✅
