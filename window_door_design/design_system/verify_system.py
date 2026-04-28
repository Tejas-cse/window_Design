#!/usr/bin/env python
"""
ML Recommendation System - Verification Script
Checks all components are properly installed and working
"""

import sys
import os
from pathlib import Path

def check_files():
    """Verify all required files exist"""
    print("\n" + "="*60)
    print("CHECKING ML SYSTEM FILES")
    print("="*60)
    
    design_system = Path(__file__).parent
    required_files = {
        'Python Files': [
            'dataset_generator.py',
            'train_model.py',
            'predict.py',
            'views.py',
            'urls.py'
        ],
        'ML Artifacts': [
            'dataset.csv',
            'model.pkl',
            'encoders.pkl'
        ],
        'Documentation': [
            'ML_RECOMMENDATION_SYSTEM.md'
        ]
    }
    
    all_good = True
    for category, files in required_files.items():
        print(f"\n{category}:")
        for fname in files:
            filepath = design_system / fname
            if filepath.exists():
                size = filepath.stat().st_size
                size_str = f"{size / 1024:.1f}K" if size > 1024 else f"{size}B"
                print(f"  ✅ {fname:<30} ({size_str})")
            else:
                print(f"  ❌ {fname:<30} (MISSING)")
                all_good = False
    
    return all_good


def check_packages():
    """Verify all required packages are installed"""
    print("\n" + "="*60)
    print("CHECKING DEPENDENCIES")
    print("="*60)
    
    packages = {
        'pandas': '2.0+',
        'numpy': '1.24+',
        'scikit-learn': '1.3+',
        'joblib': '1.3+',
        'Django': '4.2+'
    }
    
    all_good = True
    for package, version_req in packages.items():
        try:
            mod = __import__(package)
            version = getattr(mod, '__version__', 'unknown')
            print(f"  ✅ {package:<20} (v{version})")
        except ImportError:
            print(f"  ❌ {package:<20} (NOT INSTALLED)")
            all_good = False
    
    return all_good


def check_model():
    """Test loading and using the model"""
    print("\n" + "="*60)
    print("TESTING ML MODEL")
    print("="*60)
    
    try:
        # Change to design_system directory
        design_system = Path(__file__).parent
        os.chdir(design_system)
        sys.path.insert(0, str(design_system))
        
        from predict import DesignPredictor, predict_design
        
        # Test model loading
        print("\n  Loading model...")
        predictor = DesignPredictor()
        print("  ✅ Model loaded successfully")
        
        # Test prediction
        print("\n  Testing prediction...")
        test_input = {
            'room_size': 'large',
            'budget': 'high',
            'noise_level': 'low',
            'sunlight': 'high',
            'room_type': 'living'
        }
        
        result = predictor.predict(test_input)
        print(f"  ✅ Prediction successful")
        print(f"     Window Type: {result['window_type']}")
        print(f"     Glass Type: {result['glass_type']}")
        print(f"     Material Type: {result['material_type']}")
        
        # Test convenience function
        print("\n  Testing convenience function...")
        result2 = predict_design(test_input)
        print("  ✅ Convenience function working")
        
        # Test valid values
        print("\n  Testing valid values lookup...")
        valid = predictor.get_valid_values()
        print(f"  ✅ Found valid values for {len(valid)} features")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_django():
    """Test Django integration"""
    print("\n" + "="*60)
    print("TESTING DJANGO INTEGRATION")
    print("="*60)
    
    try:
        print("\n  Checking Django imports...")
        from django.conf import settings
        if not settings.configured:
            import django
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
            django.setup()
        
        print("  ✅ Django configured")
        
        print("\n  Checking recommendation view...")
        from design_system.views import get_design_recommendation
        print("  ✅ Recommendation view imported")
        
        print("\n  Checking URL routing...")
        from design_system.urls import urlpatterns
        has_recommendation = any('recommendation' in str(p) for p in urlpatterns)
        if has_recommendation:
            print("  ✅ Recommendation URL found")
        else:
            print("  ⚠️  Recommendation URL not found in urlpatterns")
        
        print("\n  Checking templates...")
        template_path = Path(__file__).parent.parent / 'templates' / 'recommendation.html'
        if template_path.exists():
            print(f"  ✅ recommendation.html found ({template_path.stat().st_size / 1024:.1f}K)")
        else:
            print(f"  ❌ recommendation.html not found at {template_path}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def print_summary(results):
    """Print verification summary"""
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    
    checks = [
        ("Files", results['files']),
        ("Packages", results['packages']),
        ("ML Model", results['model']),
        ("Django", results['django'])
    ]
    
    for name, status in checks:
        status_str = "✅ PASS" if status else "❌ FAIL"
        print(f"{name:<20} {status_str}")
    
    all_pass = all(results.values())
    print("\n" + "="*60)
    if all_pass:
        print("✅ ALL CHECKS PASSED - System Ready!")
    else:
        print("❌ SOME CHECKS FAILED - Please fix issues above")
    print("="*60 + "\n")
    
    return all_pass


def main():
    """Run all verification checks"""
    print("\n🤖 ML RECOMMENDATION SYSTEM - VERIFICATION")
    print("=" * 60)
    
    results = {
        'files': check_files(),
        'packages': check_packages(),
        'model': check_model(),
        'django': check_django()
    }
    
    success = print_summary(results)
    
    print("\n📚 DOCUMENTATION:")
    print("  - ML_RECOMMENDATION_SYSTEM.md (Comprehensive guide)")
    print("  - ML_SYSTEM_IMPLEMENTATION_SUMMARY.md (Implementation details)")
    print("  - QUICK_START.md (Quick reference)")
    
    print("\n🌐 WEB INTERFACE:")
    print("  - Visit: http://localhost:8000/recommendation/")
    print("  - Start: python manage.py runserver")
    
    print("\n🐍 PYTHON API:")
    print("  - from design_system.predict import predict_design")
    print("  - result = predict_design(user_input)")
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
