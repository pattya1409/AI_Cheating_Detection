#!/usr/bin/env python3
"""
Production-Ready AI Cheating Detection System
Enhanced with proper error handling, security, and user management
"""

import os
import sys
from app import app
from database import init_db

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'cv2', 'mediapipe', 'flask', 'werkzeug', 
        'ultralytics', 'numpy', 'PIL'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            elif package == 'PIL':
                from PIL import Image
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for pkg in missing_packages:
            print(f"   - {pkg}")
        print("\n📦 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def check_camera():
    """Check if camera is available"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            cap.release()
            return True
        return False
    except:
        return False

def setup_directories():
    """Create necessary directories"""
    directories = [
        'static/evidence/screenshots',
        'static/evidence/videos',
        'static/css',
        'static/js'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def main():
    print("🚀 AI Cheating Detection System v2.0")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    
    print("✅ Python version check passed")
    
    # Check dependencies
    print("📦 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ All dependencies installed")
    
    # Setup directories
    print("📁 Setting up directories...")
    setup_directories()
    print("✅ Directories created")
    
    # Initialize database
    print("📊 Initializing database...")
    try:
        init_db()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)
    
    # Check camera
    print("📷 Checking camera availability...")
    if check_camera():
        print("✅ Camera is available")
    else:
        print("⚠️  Camera not detected (you can still access the system)")
    
    print("\n🌐 Starting web server...")
    print("📱 Access URLs:")
    print("   - Local:   http://localhost:5000")
    print("   - Network: http://0.0.0.0:5000")
    
    print("\n🔐 Login Information:")
    print("   Default Admin:")
    print("     Username: admin")
    print("     Password: admin")
    print("   Or create new account via registration")
    
    print("\n🎯 System Features:")
    print("   ✓ Real-time cheating detection")
    print("   ✓ Live statistics dashboard")
    print("   ✓ User registration & management")
    print("   ✓ Evidence capture & storage")
    print("   ✓ Admin panel with user controls")
    print("   ✓ Secure authentication system")
    
    print("\n📋 Detection Capabilities:")
    print("   • Head movement (looking left/right)")
    print("   • Talking/mouth movement")
    print("   • Mobile phone detection")
    print("   • Multiple person detection")
    print("   • Automatic evidence capture")
    
    print("\n⚠️  Important Notes:")
    print("   • Ensure good lighting for best detection")
    print("   • Keep camera lens clean")
    print("   • Test camera before exam sessions")
    print("   • Review captured evidence regularly")
    
    print("\n" + "=" * 50)
    print("🎓 System ready for exam monitoring!")
    print("=" * 50)
    
    # Set environment variables for production
    os.environ.setdefault('FLASK_ENV', 'production')
    
    try:
        # Start the Flask application
        app.run(
            debug=False,  # Disable debug in production
            host='0.0.0.0',
            port=5000,
            threaded=True,  # Enable threading for better performance
            use_reloader=False  # Disable auto-reloader in production
        )
    except KeyboardInterrupt:
        print("\n\n🛑 System shutdown requested")
        print("✅ AI Cheating Detection System stopped safely")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        print("💡 Try restarting the system or check the logs")
        sys.exit(1)

if __name__ == "__main__":
    main()