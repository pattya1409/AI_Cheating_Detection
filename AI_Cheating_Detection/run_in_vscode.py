#!/usr/bin/env python3
"""
VS Code Runner for AI Cheating Detection System
This script helps set up and run the project in VS Code
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major != 3 or version.minor < 8:
        print("❌ Python 3.8+ is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    if not os.path.exists("venv"):
        print("📦 Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print("✓ Virtual environment created successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to create virtual environment")
            return False
    else:
        print("✓ Virtual environment already exists")
    return True

def get_python_executable():
    """Get the correct Python executable path for the platform"""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "python.exe")
    else:
        return os.path.join("venv", "bin", "python")

def get_pip_executable():
    """Get the correct pip executable path for the platform"""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "pip.exe")
    else:
        return os.path.join("venv", "bin", "pip")

def install_dependencies():
    """Install required dependencies"""
    print("📚 Installing dependencies...")
    
    pip_exe = get_pip_executable()
    
    # Upgrade pip first
    try:
        subprocess.run([pip_exe, "install", "--upgrade", "pip"], check=True)
        print("✓ Pip upgraded successfully")
    except subprocess.CalledProcessError:
        print("⚠️ Warning: Could not upgrade pip")
    
    # Install specific versions to avoid compatibility issues
    dependencies = [
        "numpy==1.24.3",
        "opencv-python==4.8.1.78", 
        "mediapipe==0.10.7",
        "flask==2.3.3",
        "werkzeug==2.3.7"
    ]
    
    for dep in dependencies:
        try:
            print(f"Installing {dep}...")
            subprocess.run([pip_exe, "install", dep], check=True)
            print(f"✓ {dep} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {dep}")
            return False
    
    return True

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    python_exe = get_python_executable()
    
    test_script = """
try:
    import flask
    import cv2
    import mediapipe
    print("✓ All imports successful!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)
"""
    
    try:
        result = subprocess.run([python_exe, "-c", test_script], 
                              capture_output=True, text=True, check=True)
        print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Import test failed: {e.stderr}")
        return False

def run_application():
    """Run the Flask application"""
    print("\n🚀 Starting AI Cheating Detection System...")
    print("=" * 50)
    print("Application URL: http://localhost:5000")
    print("\nDefault Login Credentials:")
    print("  Admin: admin / admin123")
    print("  Examiner: examiner / examiner123")
    print("\nPress Ctrl+C to stop the application")
    print("=" * 50)
    
    python_exe = get_python_executable()
    
    try:
        subprocess.run([python_exe, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Application failed to start: {e}")
        return False
    
    return True

def main():
    """Main function to set up and run the project"""
    print("🎯 AI Cheating Detection System - VS Code Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Test imports
    if not test_imports():
        return False
    
    # Run application
    return run_application()

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
    else:
        print("\n✅ Setup completed successfully!")