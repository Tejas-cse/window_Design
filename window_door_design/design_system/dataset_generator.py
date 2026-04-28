"""
Synthetic Dataset Generator for Window & Door Design Recommendation System
Generates 1000+ rows with rule-based relationships between features and targets
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

# Define categorical values
ROOM_SIZES = ['small', 'medium', 'large']
BUDGETS = ['low', 'medium', 'high']
NOISE_LEVELS = ['low', 'medium', 'high']
SUNLIGHT_LEVELS = ['low', 'medium', 'high']
ROOM_TYPES = ['bedroom', 'kitchen', 'office', 'living']

# Target variables
WINDOW_TYPES = ['sliding', 'casement']
GLASS_TYPES = ['single', 'double', 'toughened']
MATERIAL_TYPES = ['aluminium_basic', 'aluminium_standard', 'aluminium_premium']


def get_window_type(room_size, budget, room_type):
    """
    Predict window type based on features
    Rule: Large rooms and high budget → sliding windows
    """
    if room_size == 'large' or budget == 'high':
        return np.random.choice(['sliding', 'casement'], p=[0.7, 0.3])
    elif room_size == 'medium':
        return np.random.choice(['sliding', 'casement'], p=[0.5, 0.5])
    else:
        return np.random.choice(['sliding', 'casement'], p=[0.3, 0.7])


def get_glass_type(noise_level, sunlight, budget):
    """
    Predict glass type based on features
    Rule: High noise → double/toughened
          High sunlight → toughened
          High budget → double/toughened
    """
    if noise_level == 'high':
        return np.random.choice(['double', 'toughened'], p=[0.6, 0.4])
    elif sunlight == 'high':
        return np.random.choice(['toughened', 'double', 'single'], p=[0.6, 0.3, 0.1]) if budget == 'high' else np.random.choice(['toughened', 'double'], p=[0.7, 0.3])
    elif budget == 'high':
        return np.random.choice(['double', 'toughened'], p=[0.7, 0.3])
    elif budget == 'medium':
        return np.random.choice(['single', 'double'], p=[0.4, 0.6])
    else:
        return 'single'


def get_material_type(budget, room_size, room_type):
    """
    Predict material type based on budget and room characteristics
    Rule: High budget → premium
          Kitchen/Living → standard+
          Small rooms → basic
    """
    if budget == 'high':
        return np.random.choice(['aluminium_premium', 'aluminium_standard'], p=[0.7, 0.3])
    elif budget == 'medium':
        if room_type in ['kitchen', 'living']:
            return np.random.choice(['aluminium_standard', 'aluminium_basic'], p=[0.7, 0.3])
        else:
            return np.random.choice(['aluminium_standard', 'aluminium_basic'], p=[0.5, 0.5])
    else:
        if room_size == 'small':
            return 'aluminium_basic'
        else:
            return np.random.choice(['aluminium_basic', 'aluminium_standard'], p=[0.7, 0.3])


def generate_synthetic_dataset(num_samples=1000, random_seed=42):
    """
    Generate synthetic dataset with rule-based relationships
    
    Args:
        num_samples: Number of records to generate (default: 1000)
        random_seed: Random seed for reproducibility
    
    Returns:
        DataFrame with features and targets
    """
    np.random.seed(random_seed)
    
    data = {
        'room_size': np.random.choice(ROOM_SIZES, num_samples),
        'budget': np.random.choice(BUDGETS, num_samples),
        'noise_level': np.random.choice(NOISE_LEVELS, num_samples),
        'sunlight': np.random.choice(SUNLIGHT_LEVELS, num_samples),
        'room_type': np.random.choice(ROOM_TYPES, num_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Generate target variables using rule-based logic
    df['window_type'] = df.apply(
        lambda row: get_window_type(row['room_size'], row['budget'], row['room_type']),
        axis=1
    )
    
    df['glass_type'] = df.apply(
        lambda row: get_glass_type(row['noise_level'], row['sunlight'], row['budget']),
        axis=1
    )
    
    df['material_type'] = df.apply(
        lambda row: get_material_type(row['budget'], row['room_size'], row['room_type']),
        axis=1
    )
    
    return df


def save_dataset(df, filename='dataset.csv'):
    """
    Save dataset to CSV file
    
    Args:
        df: DataFrame to save
        filename: Output filename
    """
    # Get the design_system directory path
    current_dir = Path(__file__).parent
    filepath = current_dir / filename
    
    df.to_csv(filepath, index=False)
    print(f"Dataset saved to: {filepath}")
    print(f"Shape: {df.shape}")
    print(f"\nDataset Preview:")
    print(df.head(10))
    print(f"\nTarget Distribution:")
    print(f"Window Types:\n{df['window_type'].value_counts()}")
    print(f"\nGlass Types:\n{df['glass_type'].value_counts()}")
    print(f"\nMaterial Types:\n{df['material_type'].value_counts()}")
    
    return filepath


def main():
    """Main function to generate and save dataset"""
    print("Generating synthetic dataset...")
    df = generate_synthetic_dataset(num_samples=1000)
    save_dataset(df)


if __name__ == '__main__':
    main()
