"""
Model Training for Window & Door Design Recommendation System
Trains multi-output RandomForestClassifier on synthetic dataset
"""

import pandas as pd
import numpy as np
import sys
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
from pathlib import Path

try:
    from dataset_generator import generate_synthetic_dataset
except ImportError:
    # If relative import fails, try to import directly
    import dataset_generator as dg
    generate_synthetic_dataset = dg.generate_synthetic_dataset


class ModelTrainer:
    """Train multi-output recommendation model"""
    
    def __init__(self, dataset_path=None):
        self.dataset_path = dataset_path
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.model = None
        self.encoders = {}
        self.target_encoders = {}
        
    def load_dataset(self, create_if_missing=True):
        """
        Load dataset from CSV or generate if missing
        
        Args:
            create_if_missing: Generate synthetic data if file not found
        """
        if self.dataset_path and Path(self.dataset_path).exists():
            self.df = pd.read_csv(self.dataset_path)
            print(f"Loaded dataset from {self.dataset_path}")
        else:
            if create_if_missing:
                print("Dataset not found. Generating synthetic dataset...")
                self.df = generate_synthetic_dataset(num_samples=1000)
                if self.dataset_path:
                    self.df.to_csv(self.dataset_path, index=False)
                    print(f"Generated dataset saved to {self.dataset_path}")
            else:
                raise FileNotFoundError(f"Dataset not found at {self.dataset_path}")
        
        print(f"Dataset shape: {self.df.shape}")
        return self.df
    
    def preprocess_data(self):
        """
        Encode categorical features and targets
        """
        print("\nPreprocessing data...")
        
        # Separate features and targets
        feature_cols = ['room_size', 'budget', 'noise_level', 'sunlight', 'room_type']
        target_cols = ['window_type', 'glass_type', 'material_type']
        
        X = self.df[feature_cols].copy()
        y = self.df[target_cols].copy()
        
        # Encode input features
        for col in feature_cols:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            self.encoders[col] = le
        
        # Encode target variables
        for col in target_cols:
            le = LabelEncoder()
            y[col] = le.fit_transform(y[col])
            self.target_encoders[col] = le
        
        print("Encoding complete")
        print(f"Feature encoders: {list(self.encoders.keys())}")
        print(f"Target encoders: {list(self.target_encoders.keys())}")
        
        return X, y
    
    def split_data(self, X, y, test_size=0.2, random_state=42):
        """
        Split data into train and test sets
        """
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        print(f"\nData split - Train: {self.X_train.shape}, Test: {self.X_test.shape}")
        
    def train_model(self, n_estimators=100, random_state=42):
        """
        Train multi-output RandomForestClassifier
        
        Args:
            n_estimators: Number of trees in the forest
            random_state: Random seed for reproducibility
        """
        print(f"\nTraining MultiOutput RandomForestClassifier ({n_estimators} estimators)...")
        
        # Create and train model
        base_model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=random_state,
            n_jobs=-1,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=5
        )
        
        self.model = MultiOutputClassifier(base_model)
        self.model.fit(self.X_train, self.y_train)
        
        print("Training complete!")
        
    def evaluate_model(self):
        """
        Evaluate model performance on test set
        """
        print("\nEvaluating model...")
        
        # Predictions
        y_pred = self.model.predict(self.X_test)
        
        # Calculate accuracy for each output
        for idx, col in enumerate(['window_type', 'glass_type', 'material_type']):
            accuracy = accuracy_score(self.y_test.iloc[:, idx], y_pred[:, idx])
            print(f"\n{col.upper()} Accuracy: {accuracy:.4f}")
            
            # Classification report
            print(f"Classification Report for {col}:")
            print(classification_report(
                self.y_test.iloc[:, idx],
                y_pred[:, idx],
                target_names=self.target_encoders[col].classes_,
                zero_division=0
            ))
    
    def save_model(self, model_path='model.pkl', encoders_path='encoders.pkl'):
        """
        Save trained model and encoders using joblib
        
        Args:
            model_path: Path to save model
            encoders_path: Path to save encoders
        """
        current_dir = Path(__file__).parent
        model_file = current_dir / model_path
        encoders_file = current_dir / encoders_path
        
        # Save model
        joblib.dump(self.model, model_file)
        print(f"\nModel saved to: {model_file}")
        
        # Save encoders
        encoders_dict = {
            'input_encoders': self.encoders,
            'target_encoders': self.target_encoders
        }
        joblib.dump(encoders_dict, encoders_file)
        print(f"Encoders saved to: {encoders_file}")
        
        return model_file, encoders_file
    
    def full_training_pipeline(self, dataset_path='dataset.csv'):
        """
        Run complete training pipeline
        """
        print("="*60)
        print("STARTING MODEL TRAINING PIPELINE")
        print("="*60)
        
        self.dataset_path = Path(__file__).parent / dataset_path
        
        # Step 1: Load data
        self.load_dataset()
        
        # Step 2: Preprocess
        X, y = self.preprocess_data()
        
        # Step 3: Split
        self.split_data(X, y)
        
        # Step 4: Train
        self.train_model()
        
        # Step 5: Evaluate
        self.evaluate_model()
        
        # Step 6: Save
        self.save_model()
        
        print("\n" + "="*60)
        print("TRAINING PIPELINE COMPLETE")
        print("="*60)


def main():
    """Main training script"""
    trainer = ModelTrainer()
    trainer.full_training_pipeline()


if __name__ == '__main__':
    main()
