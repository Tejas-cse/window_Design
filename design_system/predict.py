"""
Prediction Module for Window & Door Design Recommendation System
Loads trained model and encoders, provides prediction function
"""

import joblib
import numpy as np
from pathlib import Path
from typing import Dict, Tuple


class DesignPredictor:
    """Load model and make predictions"""
    
    def __init__(self, model_path='model.pkl', encoders_path='encoders.pkl'):
        """
        Initialize predictor by loading model and encoders
        
        Args:
            model_path: Path to trained model
            encoders_path: Path to encoders dictionary
        """
        current_dir = Path(__file__).parent
        self.model_path = current_dir / model_path
        self.encoders_path = current_dir / encoders_path
        
        self.model = None
        self.input_encoders = None
        self.target_encoders = None
        self.feature_cols = ['room_size', 'budget', 'noise_level', 'sunlight', 'room_type']
        self.target_cols = ['window_type', 'glass_type', 'material_type']
        
        self.load_model()
    
    def load_model(self):
        """Load trained model and encoders"""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        if not self.encoders_path.exists():
            raise FileNotFoundError(f"Encoders file not found: {self.encoders_path}")
        
        self.model = joblib.load(self.model_path)
        encoders_dict = joblib.load(self.encoders_path)
        
        self.input_encoders = encoders_dict['input_encoders']
        self.target_encoders = encoders_dict['target_encoders']
        
        print(f"Model loaded from: {self.model_path}")
        print(f"Encoders loaded from: {self.encoders_path}")
    
    def encode_input(self, input_data: Dict) -> np.ndarray:
        """
        Encode input features using trained encoders
        
        Args:
            input_data: Dictionary with feature values
            
        Returns:
            Encoded feature array
        """
        encoded = []
        for col in self.feature_cols:
            if col not in input_data:
                raise ValueError(f"Missing feature: {col}")
            
            value = input_data[col]
            try:
                encoded_value = self.input_encoders[col].transform([value])[0]
                encoded.append(encoded_value)
            except ValueError:
                raise ValueError(f"Invalid value for {col}: {value}")
        
        return np.array(encoded).reshape(1, -1)
    
    def decode_predictions(self, predictions: np.ndarray) -> Dict[str, str]:
        """
        Decode model predictions back to readable labels
        
        Args:
            predictions: Model predictions (encoded)
            
        Returns:
            Dictionary with readable predictions
        """
        decoded = {}
        for idx, col in enumerate(self.target_cols):
            pred_value = predictions[0][idx]
            decoded_value = self.target_encoders[col].inverse_transform([pred_value])[0]
            decoded[col] = decoded_value
        
        return decoded
    
    def predict(self, input_data: Dict) -> Dict[str, str]:
        """
        Make prediction for given input
        
        Args:
            input_data: Dictionary with user inputs
                       {
                           'room_size': 'small|medium|large',
                           'budget': 'low|medium|high',
                           'noise_level': 'low|medium|high',
                           'sunlight': 'low|medium|high',
                           'room_type': 'bedroom|kitchen|office|living'
                       }
        
        Returns:
            Dictionary with predictions
            {
                'window_type': 'sliding|casement',
                'glass_type': 'single|double|toughened',
                'material_type': 'aluminium_basic|aluminium_standard|aluminium_premium'
            }
        """
        if not self.model:
            raise RuntimeError("Model not loaded")
        
        # Encode input
        encoded_input = self.encode_input(input_data)
        
        # Make prediction
        predictions = self.model.predict(encoded_input)
        
        # Decode predictions
        decoded = self.decode_predictions(predictions)
        
        return decoded
    
    def get_valid_values(self) -> Dict[str, list]:
        """
        Get valid values for each feature
        
        Returns:
            Dictionary with lists of valid values
        """
        valid_values = {}
        for col in self.feature_cols:
            valid_values[col] = list(self.input_encoders[col].classes_)
        
        return valid_values


def predict_design(input_dict: Dict) -> Dict[str, str]:
    """
    Convenience function to make predictions
    
    Args:
        input_dict: User input dictionary
        
    Returns:
        Dictionary with predictions
    """
    try:
        predictor = DesignPredictor()
        return predictor.predict(input_dict)
    except FileNotFoundError as e:
        return {'error': f"Model not trained yet: {str(e)}"}
    except Exception as e:
        return {'error': str(e)}


def get_recommendation_details(prediction: Dict[str, str]) -> Dict:
    """
    Generate recommendation details based on predictions
    
    Args:
        prediction: Model predictions
        
    Returns:
        Dictionary with recommendation details and reasoning
    """
    recommendations = {
        'window_type': prediction.get('window_type', ''),
        'glass_type': prediction.get('glass_type', ''),
        'material_type': prediction.get('material_type', ''),
        'description': '',
        'advantages': [],
        'considerations': []
    }
    
    # Add descriptions and advantages
    window_type = prediction.get('window_type', '')
    if window_type == 'sliding':
        recommendations['description'] = 'Sliding window system provides smooth operation and modern aesthetics.'
        recommendations['advantages'] = [
            'Easy to operate and maintain',
            'Space-efficient design',
            'Contemporary look',
            'Better for modern interiors'
        ]
    elif window_type == 'casement':
        recommendations['description'] = 'Casement windows offer excellent ventilation and security.'
        recommendations['advantages'] = [
            'Maximum ventilation',
            'Excellent seal and insulation',
            'Enhanced security features',
            'Traditional elegance'
        ]
    
    glass_type = prediction.get('glass_type', '')
    if glass_type == 'single':
        recommendations['considerations'].append('Single glazing - suitable for moderate climates')
    elif glass_type == 'double':
        recommendations['considerations'].append('Double glazing - excellent thermal and noise insulation')
    elif glass_type == 'toughened':
        recommendations['considerations'].append('Toughened glass - enhanced safety and UV protection')
    
    material_type = prediction.get('material_type', '')
    if 'premium' in material_type:
        recommendations['considerations'].append('Premium finish - superior durability and aesthetics')
    elif 'standard' in material_type:
        recommendations['considerations'].append('Standard quality - good balance of quality and cost')
    else:
        recommendations['considerations'].append('Basic model - cost-effective solution')
    
    return recommendations


if __name__ == '__main__':
    # Test example
    test_input = {
        'room_size': 'large',
        'budget': 'high',
        'noise_level': 'low',
        'sunlight': 'high',
        'room_type': 'living'
    }
    
    try:
        result = predict_design(test_input)
        print(f"Input: {test_input}")
        print(f"Prediction: {result}")
        
        if 'error' not in result:
            details = get_recommendation_details(result)
            print(f"Details: {details}")
    except Exception as e:
        print(f"Error: {e}")
