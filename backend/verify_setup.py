#!/usr/bin/env python3
"""
Paeon AI - Setup Verification Script
Verifies that all dependencies and configurations are correctly set up.
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version is 3.11+"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11+ required")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_required_packages():
    """Check if required packages are installed"""
    required = ['fastapi', 'uvicorn', 'google', 'pydantic']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package}")
    
    return len(missing) == 0

def check_env_file():
    """Check if .env file exists and has API key"""
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file not found")
        return False
    
    with open(env_path) as f:
        content = f.read()
        if "GEMINI_API_KEY=" not in content:
            print("❌ GEMINI_API_KEY not in .env")
            return False
        if "GEMINI_API_KEY=your-api-key-here" in content:
            print("⚠️  GEMINI_API_KEY is still set to default value")
            return False
    
    print("✓ .env file configured")
    return True

def check_app_imports():
    """Check if app can be imported without errors"""
    try:
        from app.main import app
        print("✓ App imports successfully")
        return True
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("PAEON AI - SETUP VERIFICATION")
    print("="*60 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages),
        ("Environment File", check_env_file),
        ("App Configuration", check_app_imports),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        print("-" * 40)
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    if all(results):
        print("✓ All checks passed! Ready to start the server.")
        print("\nRun: python -m uvicorn app.main:app --host 127.0.0.1 --port 8000")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("1. Python 3.11+: Download from https://python.org")
        print("2. Packages: Run 'pip install -r requirements.txt'")
        print("3. .env file: Create backend/.env with your Gemini API key")
        sys.exit(1)
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
