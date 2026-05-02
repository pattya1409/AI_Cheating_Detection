# VS Code Setup Guide for AI Cheating Detection System

## 🚀 Complete Setup Instructions for VS Code

This guide provides step-by-step instructions to run the AI Cheating Detection project in VS Code on Windows.

## Prerequisites

- **Python 3.8-3.10** (recommended: Python 3.10)
- **VS Code** with Python extension
- **Git** (optional, for version control)
- **Webcam** for testing detection features

## Step 1: Open Project in VS Code

1. Open VS Code
2. File → Open Folder
3. Navigate to and select the `AI_Cheating_Detection` folder
4. VS Code will open the project

## Step 2: Set Up Python Environment

### Option A: Using VS Code's Built-in Terminal

1. Open VS Code Terminal: `Ctrl + `` (backtick)
2. Create virtual environment:
   ```cmd
   python -m venv venv
   ```

3. Activate virtual environment:
   ```cmd
   venv\Scripts\activate
   ```

4. You should see `(venv)` in your terminal prompt

### Option B: Using VS Code Python Interpreter

1. Press `Ctrl + Shift + P`
2. Type "Python: Select Interpreter"
3. Choose "Create Virtual Environment"
4. Select "venv"
5. Choose your Python installation

## Step 3: Install Dependencies

With the virtual environment activated, install the required packages:

```cmd
# Upgrade pip first
python -m pip install --upgrade pip

# Install compatible versions
pip install numpy==1.24.3
pip install opencv-python==4.8.1.78
pip install mediapipe==0.10.7
pip install flask==2.3.3
pip install werkzeug==2.3.7
pip install ultralytics==8.0.196
```

## Step 4: Fix Common Issues

### Issue 1: MediaPipe Import Error
If you get `AttributeError: module 'mediapipe' has no attribute 'solutions'`:

```cmd
pip uninstall mediapipe
pip install mediapipe==0.10.7
```

### Issue 2: YOLO Model Loading Error
The project includes a fix for PyTorch security issues. If YOLO fails to load, it will continue with face detection only.

### Issue 3: NumPy Compatibility
If you get numpy errors:

```cmd
pip uninstall numpy opencv-python
pip install numpy==1.24.3 opencv-python==4.8.1.78
```

## Step 5: Configure VS Code Settings

Create `.vscode/settings.json` in your project root:

```json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

## Step 6: Create Launch Configuration

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run AI Cheating Detection",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/app.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}",
            "env": {
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "1"
            }
        }
    ]
}
```

## Step 7: Running the Application

### Method 1: Using VS Code Debugger
1. Press `F5` or go to Run → Start Debugging
2. Select "Run AI Cheating Detection"
3. The application will start in debug mode

### Method 2: Using Terminal
1. Open VS Code Terminal (`Ctrl + `` )
2. Ensure virtual environment is activated
3. Run:
   ```cmd
   python app.py
   ```

### Method 3: Using VS Code Tasks
Create `.vscode/tasks.json`:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run AI Cheating Detection",
            "type": "shell",
            "command": "${workspaceFolder}/venv/Scripts/python.exe",
            "args": ["app.py"],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "new"
            },
            "options": {
                "cwd": "${workspaceFolder}"
            }
        }
    ]
}
```

Then press `Ctrl + Shift + P` → "Tasks: Run Task" → "Run AI Cheating Detection"

## Step 8: Access the Application

1. Once running, open your browser
2. Navigate to: `http://localhost:5000`
3. Login with default credentials:
   - **Admin:** `admin` / `admin123`
   - **Examiner:** `examiner` / `examiner123`

## Troubleshooting

### Camera Access Issues
- Ensure no other applications are using the camera
- Check Windows camera privacy settings
- Try restarting VS Code and the application

### Port Already in Use
If port 5000 is busy:
1. Stop the running process: `Ctrl + C` in terminal
2. Or change the port in `app.py`:
   ```python
   if __name__ == '__main__':
       app.run(debug=True, port=5001)  # Change port here
   ```

### Import Errors
1. Verify virtual environment is activated
2. Check Python interpreter in VS Code status bar
3. Reinstall problematic packages:
   ```cmd
   pip uninstall [package_name]
   pip install [package_name]==version
   ```

### Performance Issues
- Close unnecessary VS Code extensions
- Ensure sufficient RAM (minimum 4GB recommended)
- Close other resource-intensive applications

## VS Code Extensions (Recommended)

Install these extensions for better development experience:

1. **Python** (Microsoft) - Essential for Python development
2. **Pylance** (Microsoft) - Advanced Python language support
3. **Python Docstring Generator** - Auto-generate docstrings
4. **GitLens** - Enhanced Git capabilities
5. **Bracket Pair Colorizer** - Better code readability
6. **Material Icon Theme** - Better file icons

## Project Structure in VS Code

```
AI_Cheating_Detection/
├── .vscode/                 # VS Code configuration
│   ├── settings.json
│   ├── launch.json
│   └── tasks.json
├── venv/                    # Virtual environment
├── static/                  # Static files (CSS, JS, images)
├── templates/               # HTML templates
├── app.py                   # Main Flask application
├── detection_service.py     # AI detection logic
├── database.py             # Database operations
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## Development Tips

### Debugging
- Set breakpoints by clicking left of line numbers
- Use `F5` to start debugging
- Use `F10` (step over) and `F11` (step into) for debugging

### Code Formatting
- Install `black` formatter: `pip install black`
- Format code: `Shift + Alt + F`

### Git Integration
- Initialize git: `git init`
- Stage changes: `Ctrl + Shift + G`
- Commit changes directly from VS Code

## Security Notes

⚠️ **Important Security Reminders:**

1. **Change default passwords** before production use
2. **Never commit sensitive data** to version control
3. **Use environment variables** for sensitive configuration
4. **Keep dependencies updated** regularly

## Performance Optimization

- **Camera Resolution:** Lower resolution improves performance
- **Detection Frequency:** Adjust detection intervals in code
- **Memory Management:** Monitor memory usage during long sessions

## Next Steps

1. Customize detection parameters in `detection_service.py`
2. Modify UI templates in `templates/` folder
3. Add custom CSS in `static/css/`
4. Implement additional features as needed

## Support

If you encounter issues:

1. Check this guide first
2. Review error messages in VS Code terminal
3. Check the main `README.md` for additional information
4. Verify all dependencies are correctly installed

---

**Happy Coding! 🎉**

The AI Cheating Detection system is now ready to run in VS Code with full debugging and development capabilities.