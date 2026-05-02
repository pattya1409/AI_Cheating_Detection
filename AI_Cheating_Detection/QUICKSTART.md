# Quick Start Guide

## First Time Setup

1. **Activate Virtual Environment**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   ⚠️ This may take 5-10 minutes as it downloads PyTorch and YOLOv8.

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Access the Application**
   - Open browser: http://localhost:5000
   - Login with default credentials:
     - **Admin:** `admin` / `admin123`
     - **Examiner:** `examiner` / `examiner123`

## Using the System

### Step 1: Login
- Use admin or examiner credentials
- You'll be redirected to the dashboard

### Step 2: Start Monitoring
1. Click **"Live Monitor"** in the navigation
2. Click **"Start Monitoring"** button
3. Allow camera access when prompted
4. The system will begin detecting cheating behaviors

### Step 3: View Results
- **Dashboard:** See statistics and recent alerts
- **Reports:** View all detection logs with evidence
- **Admin Panel:** Manage users and view activity (admin only)

## Default Credentials

⚠️ **IMPORTANT:** Change these passwords before production use!

- **Admin Account:**
  - Username: `admin`
  - Password: `admin123`
  - Email: `admin@example.com`

- **Examiner Account:**
  - Username: `examiner`
  - Password: `examiner123`
  - Email: `examiner@example.com`

## Email Alerts (Optional)

To enable email alerts for high-risk cheating:

1. Create a `.env` file in the project root
2. Add your SMTP credentials:
   ```
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   ```
3. For Gmail, use an [App Password](https://myaccount.google.com/apppasswords)

## Troubleshooting

### Camera Not Working
- Check if another application is using the camera
- Verify camera permissions in system settings
- Try restarting the application

### Import Errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Database Errors
- Delete `cheating_detection.db` and restart (will recreate database)
- Check file permissions in the project directory

### Detection Not Starting
- Verify `yolov8n.pt` file exists in the project root
- Check console for error messages
- Ensure camera is connected and working

## Next Steps

- Review the full [README.md](README.md) for detailed documentation
- Customize detection thresholds in `detection_service.py`
- Configure email alerts for production use
- Change default passwords immediately

