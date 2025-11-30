#!/usr/bin/env python3
"""
System Test Script

Quick validation that all components are working.
Run this to verify your installation.
"""

import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported"""
    print("\n" + "="*60)
    print("TEST 1: Module Imports")
    print("="*60)

    try:
        from app import InvoiceOCR, HSNMatcher, GSTR3BGenerator, InvoiceProcessor
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_dependencies():
    """Test that external dependencies are installed"""
    print("\n" + "="*60)
    print("TEST 2: External Dependencies")
    print("="*60)

    errors = []

    # Test pytesseract
    try:
        import pytesseract
        print("✅ pytesseract installed")
    except ImportError:
        errors.append("pytesseract not installed. Run: pip install pytesseract")

    # Test PIL
    try:
        from PIL import Image
        print("✅ Pillow (PIL) installed")
    except ImportError:
        errors.append("Pillow not installed. Run: pip install Pillow")

    # Test pdf2image
    try:
        import pdf2image
        print("✅ pdf2image installed")
    except ImportError:
        errors.append("pdf2image not installed. Run: pip install pdf2image")

    # Test fuzzywuzzy
    try:
        from fuzzywuzzy import fuzz
        print("✅ fuzzywuzzy installed")
    except ImportError:
        print("⚠️  fuzzywuzzy not installed (optional). Run: pip install fuzzywuzzy")
        print("   System will use basic string matching as fallback")

    if errors:
        print("\n❌ Missing dependencies:")
        for error in errors:
            print(f"   - {error}")
        return False

    return True

def test_hsn_database():
    """Test that HSN database exists and is valid"""
    print("\n" + "="*60)
    print("TEST 3: HSN Database")
    print("="*60)

    hsn_db_path = Path(__file__).parent / 'data' / 'hsn_master.json'

    if not hsn_db_path.exists():
        print(f"❌ HSN database not found at: {hsn_db_path}")
        return False

    try:
        import json
        with open(hsn_db_path, 'r') as f:
            hsn_data = json.load(f)

        print(f"✅ HSN database loaded: {len(hsn_data)} codes")

        # Validate structure
        if hsn_data and 'hsn' in hsn_data[0] and 'gst_rate' in hsn_data[0]:
            print(f"✅ HSN database structure valid")
            return True
        else:
            print("❌ HSN database structure invalid")
            return False

    except Exception as e:
        print(f"❌ Error loading HSN database: {e}")
        return False

def test_hsn_matching():
    """Test HSN matching functionality"""
    print("\n" + "="*60)
    print("TEST 4: HSN Matching")
    print("="*60)

    try:
        from app.hsn_matcher import HSNMatcher

        matcher = HSNMatcher()

        # Test common items
        test_items = [
            ("Laptop", "8471", 18),
            ("Software Development", "998314", 18),
            ("Rice", "1006", 0),
        ]

        all_passed = True
        for item_desc, expected_hsn, expected_rate in test_items:
            result = matcher.suggest_hsn(item_desc)

            if result['hsn_code'] == expected_hsn and result['gst_rate'] == expected_rate:
                print(f"✅ {item_desc}: HSN {result['hsn_code']} ({result['gst_rate']}%) - Confidence: {result['confidence']}%")
            else:
                print(f"⚠️  {item_desc}: Got HSN {result['hsn_code']} ({result['gst_rate']}%), expected {expected_hsn} ({expected_rate}%)")
                all_passed = False

        return all_passed

    except Exception as e:
        print(f"❌ HSN matching test failed: {e}")
        return False

def test_directories():
    """Test that required directories exist"""
    print("\n" + "="*60)
    print("TEST 5: Directory Structure")
    print("="*60)

    base_dir = Path(__file__).parent

    required_dirs = [
        'data',
        'test_invoices',
        'uploads',
        'app',
    ]

    all_exist = True
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print(f"✅ {dir_name}/ exists")
        else:
            print(f"⚠️  {dir_name}/ missing (will be auto-created)")
            # Create missing directories
            dir_path.mkdir(exist_ok=True)

    return True

def test_tesseract():
    """Test that Tesseract OCR is installed"""
    print("\n" + "="*60)
    print("TEST 6: Tesseract OCR")
    print("="*60)

    try:
        import pytesseract
        from PIL import Image
        import subprocess

        # Test Tesseract command
        result = subprocess.run(['tesseract', '--version'],
                              capture_output=True, text=True)

        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✅ Tesseract installed: {version}")
            return True
        else:
            print("❌ Tesseract not found")
            print("   Install with:")
            print("   macOS: brew install tesseract")
            print("   Ubuntu: sudo apt-get install tesseract-ocr")
            return False

    except FileNotFoundError:
        print("❌ Tesseract not found in system PATH")
        print("   Install with:")
        print("   macOS: brew install tesseract")
        print("   Ubuntu: sudo apt-get install tesseract-ocr")
        return False
    except Exception as e:
        print(f"⚠️  Error testing Tesseract: {e}")
        return False

def print_summary(results):
    """Print test summary"""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    total_tests = len(results)
    passed_tests = sum(results.values())

    print(f"\nTests Passed: {passed_tests}/{total_tests}")

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")

    if passed_tests == total_tests:
        print("\n🎉 All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("1. Create a test invoice (see test_invoices/SAMPLE_INVOICE_TEMPLATE.md)")
        print("2. Run: python -m app.processor process test_invoices/sample1.pdf --type purchase")
        print("3. Run: python -m app.processor gstr3b YOUR_GSTIN 12 2024")
        return True
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above before proceeding.")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("GST AUTOMATION MVP - SYSTEM TEST")
    print("="*60)
    print("\nThis will verify that all components are installed correctly.\n")

    results = {
        "Module Imports": test_imports(),
        "Dependencies": test_dependencies(),
        "HSN Database": test_hsn_database(),
        "HSN Matching": test_hsn_matching(),
        "Directory Structure": test_directories(),
        "Tesseract OCR": test_tesseract(),
    }

    success = print_summary(results)

    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()
