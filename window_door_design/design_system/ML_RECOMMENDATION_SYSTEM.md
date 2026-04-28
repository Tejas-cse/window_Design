# Window & Door Design - AI Recommendation System

Complete machine learning-based recommendation system for predicting optimal window and door designs based on room characteristics.

## Overview

This system uses a **Multi-Output RandomForest Classifier** to predict three design parameters simultaneously:
- **Window Type**: Sliding or Casement
- **Glass Type**: Single, Double, or Toughened
- **Material Type**: Aluminium Basic, Standard, or Premium

## System Architecture

```
┌─────────────────────────────────────────┐
│ dataset_generator.py                    │
│ - Generate 1000+ synthetic samples      │
│ - Rule-based relationships              │
│ - Save to CSV                           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ train_model.py                          │
│ - Load and preprocess dataset           │
│ - Encode categorical variables          │
│ - Train MultiOutput RandomForest        │
│ - Evaluate accuracy                     │
│ - Save model & encoders                 │
└──────────────┬──────────────────────────┘
               │
               ▼ (model.pkl, encoders.pkl)
┌─────────────────────────────────────────┐
│ predict.py                              │
│ - Load trained model                    │
│ - Encode user input                     │
│ - Make predictions                      │
│ - Decode predictions to labels          │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ Django Integration                      │
│ - views.py: get_design_recommendation   │
│ - recommendation.html: UI form          │
│ - urls.py: /recommendation/ route       │
└─────────────────────────────────────────┘
```

## Feature Inputs

| Feature | Values | Description |
|---------|--------|-------------|
| `room_size` | small, medium, large | Physical dimensions of the room |
| `budget` | low, medium, high | Budget allocation for windows/doors |
| `noise_level` | low, medium, high | Ambient noise in the area |
| `sunlight` | low, medium, high | Amount of direct sunlight |
| `room_type` | bedroom, kitchen, office, living | Purpose of the room |

## Target Outputs

### Window Type
- **Sliding**: Smooth operation, space-efficient, modern aesthetics
- **Casement**: Maximum ventilation, excellent seal, traditional look

### Glass Type
- **Single**: Basic insulation, cost-effective
- **Double**: Excellent thermal/noise insulation
- **Toughened**: Enhanced safety, UV protection

### Material Type
- **Aluminium Basic**: Cost-effective, standard quality
- **Aluminium Standard**: Good balance of quality and cost
- **Aluminium Premium**: Superior durability and aesthetics

## Model Performance

**Training Dataset**: 1000 samples

**Model Accuracy**:
- Window Type: 59%
- Glass Type: 69%
- Material Type: 71%

**Algorithm**: Multi-Output RandomForestClassifier (100 trees)
- Max Depth: 15
- Min Samples Split: 10
- Min Samples Leaf: 5

## File Structure

```
design_system/
├── dataset_generator.py      # Generate synthetic data
├── train_model.py            # Train ML model
├── predict.py                # Prediction engine
├── dataset.csv               # Generated training data
├── model.pkl                 # Trained model (joblib)
├── encoders.pkl              # Categorical encoders (joblib)
├── views.py                  # Django view (added function)
├── urls.py                   # Django URLs (added route)
└── templates/
    └── recommendation.html    # UI template
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install pandas numpy scikit-learn joblib
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

### 2. Generate Dataset

```bash
cd window_door_design/design_system
python dataset_generator.py
```

This creates `dataset.csv` with 1000 synthetic samples.

### 3. Train Model

```bash
python train_model.py
```

This creates:
- `model.pkl`: Trained RandomForest model
- `encoders.pkl`: LabelEncoders for features and targets

### 4. Access UI

Start Django server:
```bash
cd ..
python manage.py runserver
```

Visit: `http://localhost:8000/recommendation/`

## Usage Examples

### Example 1: Living Room with High Budget

**Input:**
```python
{
    'room_size': 'large',
    'budget': 'high',
    'noise_level': 'low',
    'sunlight': 'high',
    'room_type': 'living'
}
```

**Expected Output:**
```python
{
    'window_type': 'sliding',
    'glass_type': 'toughened',
    'material_type': 'aluminium_premium'
}
```

### Example 2: Small Bedroom, Budget Conscious

**Input:**
```python
{
    'room_size': 'small',
    'budget': 'low',
    'noise_level': 'low',
    'sunlight': 'medium',
    'room_type': 'bedroom'
}
```

**Expected Output:**
```python
{
    'window_type': 'casement',
    'glass_type': 'single',
    'material_type': 'aluminium_basic'
}
```

### Example 3: Noisy Kitchen, Medium Budget

**Input:**
```python
{
    'room_size': 'medium',
    'budget': 'medium',
    'noise_level': 'high',
    'sunlight': 'low',
    'room_type': 'kitchen'
}
```

**Expected Output:**
```python
{
    'window_type': 'sliding',
    'glass_type': 'double',
    'material_type': 'aluminium_standard'
}
```

## Python API

### Using DesignPredictor Class

```python
from design_system.predict import DesignPredictor, get_recommendation_details

# Initialize predictor
predictor = DesignPredictor()

# Get valid values
valid_values = predictor.get_valid_values()
# Returns: {'room_size': [...], 'budget': [...], ...}

# Make prediction
input_data = {
    'room_size': 'large',
    'budget': 'high',
    'noise_level': 'low',
    'sunlight': 'high',
    'room_type': 'living'
}

prediction = predictor.predict(input_data)
# Returns: {'window_type': '...', 'glass_type': '...', 'material_type': '...'}

# Get detailed recommendations
details = get_recommendation_details(prediction)
# Returns: {'description': '...', 'advantages': [...], 'considerations': [...]}
```

### Using Convenience Function

```python
from design_system.predict import predict_design

result = predict_design(input_data)
print(result)
```

## Django Integration

### View Function

```python
def get_design_recommendation(request):
    """Handles both GET (form display) and POST (predictions)"""
    # GET: Display recommendation form
    # POST: Process input and return predictions
```

### Template

Access at: `/recommendation/`

Features:
- Form with all required input fields
- Real-time prediction display
- Design advantages and considerations
- Link to create design based on recommendation

### URL Route

```python
path('recommendation/', views.get_design_recommendation, name='get_design_recommendation')
```

### Navigation

The "AI Recommendation" link is added to the main navigation bar.

## Extending the System

### Adding New Input Features

1. Update `dataset_generator.py`:
   - Add feature to `ROOM_SIZES`, `BUDGETS`, etc.
   - Update generation logic

2. Retrain model:
   ```bash
   python train_model.py
   ```

3. Update form in `recommendation.html`

### Improving Model Accuracy

1. **Increase Dataset Size**:
   ```python
   generate_synthetic_dataset(num_samples=5000)
   ```

2. **Tune Hyperparameters** in `train_model.py`:
   ```python
   RandomForestClassifier(
       n_estimators=200,  # Increase trees
       max_depth=20,      # Increase depth
       min_samples_split=5
   )
   ```

3. **Add More Features**: Collect real user data and retrain

### Custom Rule-Based Logic

Modify prediction functions in `dataset_generator.py`:

```python
def get_window_type(room_size, budget, room_type):
    # Add your custom rules here
    if specific_condition:
        return 'sliding'
    return 'casement'
```

## Troubleshooting

### Model Not Found Error

```
FileNotFoundError: Model file not found: model.pkl
```

**Solution**: Run `python train_model.py` to generate model files.

### Invalid Input Error

```
ValueError: Invalid value for room_size: invalid_value
```

**Solution**: Use only valid values from `predictor.get_valid_values()`

### Sklearn Warning

```
UserWarning: X does not have valid feature names
```

**Note**: This is a non-critical warning. Model predictions are still accurate.

## Performance Metrics

| Metric | Value |
|--------|-------|
| Training Samples | 1000 |
| Test Samples | 200 |
| Total Classes | 3 (multi-output) |
| Window Type Accuracy | 59% |
| Glass Type Accuracy | 69% |
| Material Type Accuracy | 71% |
| Average Accuracy | 66.3% |

## Future Enhancements

1. **User Feedback Loop**: Collect user validation to retrain model
2. **Deep Learning**: Migrate to neural networks for better accuracy
3. **Real-World Data**: Replace synthetic data with actual customer choices
4. **Advanced Features**: Add climate data, energy efficiency ratings
5. **Price Prediction**: Add cost estimation to recommendations
6. **Clustering**: Group similar designs for batch processing
7. **A/B Testing**: Test recommendation quality with users

## Technical Details

### Preprocessing Pipeline

1. **Input Encoding**: LabelEncoder for categorical features
2. **Train/Test Split**: 80/20 split
3. **No Scaling**: Tree-based models don't require feature scaling
4. **No Missing Values**: All synthetic data is complete

### Model Serialization

- **Format**: joblib pickles (binary)
- **Model File**: ~1-2 MB
- **Encoders File**: ~1 KB
- **Load Time**: <100ms

### Prediction Pipeline

1. User submits form input
2. Django view calls `predict_design()`
3. Input is encoded using stored LabelEncoders
4. Random Forest makes prediction
5. Output is decoded back to labels
6. Details are generated using recommendation rules
7. Results displayed in template

## License

Part of the Window & Door Design System
Django Application - 2026

## Support

For issues or questions:
1. Check troubleshooting section
2. Verify model files exist (model.pkl, encoders.pkl)
3. Ensure all dependencies installed
4. Check Django logs: `python manage.py runserver`

---

**Last Updated**: April 17, 2026
**Model Version**: v1.0
**Framework**: Django 4.2.11 + scikit-learn 1.8.0
