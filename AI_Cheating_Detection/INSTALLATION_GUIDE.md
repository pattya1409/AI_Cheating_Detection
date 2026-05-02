# AI Cheating Detection System - Installation & Usage Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Webcam/Camera
- Windows/Linux/Mac OS

### Installation Steps

1. **Install Required Packages**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python run_app.py
   ```
   
   Or use the original:
   ```bash
   python app.py
   ```

3. **Access the System**
   - Open your browser and go to: `http://localhost:5000`
   - Default admin credentials: 
     - Username: `admin`
     - Password: `admin`

## 📋 Features

### ✅ Live Detection System
- Real-time face detection and tracking
- Head movement detection (looking left/right)
- Talking/mouth movement detection
- Mobile phone detection
- Multiple person detection
- Automatic evidence capture (screenshots)

### ✅ User Management
- User registration with role assignment
- Secure password hashing
- Admin and Examiner roles
- User profile management
- Session management

### ✅ Dashboard Features
- **Live Statistics**: Real-time detection counting
- **Active Days Tracking**: Monitors system usage
- **Recent Alerts**: View latest detection events
- **Evidence Gallery**: Access captured screenshots
- **Auto-refresh**: Updates every 3 seconds

### ✅ Admin Panel
- User management (create, view, delete)
- System monitoring
- Detection logs and reports
- Evidence management

## 🎯 How to Use

### For First-Time Users

1. **Register an Account**
   - Click "Create New Account" on login page
   - Fill in username, email, and password
   - Select role (Examiner or Administrator)
   - Submit registration

2. **Login**
   - Enter your credentials
   - Click "Login"

3. **Start Monitoring**
   - Navigate to "Live Monitor"
   - Click "Start Detection"
   - System will begin monitoring for suspicious behavior

4. **View Results**
   - Go to "Dashboard" to see live statistics
   - Check "Recent Alerts" for detection events
   - Click "View" to see evidence screenshots

### For Administrators

1. **Access Admin Panel**
   - Login with admin credentials
   - Click "Admin Panel" in navigation

2. **Manage Users**
   - View all registered users
   - Create new users
   - Delete users (except yourself)
   - Monitor user activity

3. **Monitor System**
   - View total detections
   - Track active days
   - Review detection logs
   - Access evidence files

## 🔧 Configuration

### Camera Settings
- Default camera index: 0 (built-in webcam)
- To change camera, modify `detection_service.py`:
  ```python
  self.cap = cv2.VideoCapture(0)  # Change 0 to your camera index
  ```

### Detection Sensitivity
- Adjust confidence threshold in `detection_service.py`:
  ```python
  if conf < 0.5:  # Change 0.5 to adjust sensitivity
  ```

### Database Location
- Default: `cheating_detection.db` in project root
- To change, modify `DATABASE` variable in `database.py`

## 📊 Detection Behaviors

The system detects the following suspicious behaviors:

1. **Looking Left/Right**: Head turned away from screen
2. **Talking**: Mouth movement detected
3. **Mobile Phone**: Phone detected in frame
4. **Multiple People**: More than one person detected

## 🔒 Security Features

- Secure password hashing (Werkzeug)
- Session management
- Role-based access control
- CSRF protection ready
- Input validation
- SQL injection prevention

## 📁 Project Structure

```
AI_Cheating_Detection/
├── app.py                  # Main Flask application
├── run_app.py             # Enhanced startup script
├── database.py            # Database operations
├── detection_service.py   # AI detection logic
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── admin.html
│   └── live_monitor.html
├── static/                # Static files
│   └── evidence/          # Detection evidence
│       └── screenshots/
└── cheating_detection.db  # SQLite database

```

## 🐛 Troubleshooting

### Camera Not Working
- Check if camera is connected
- Close other applications using the camera
- Try different camera index (0, 1, 2, etc.)
- Run camera test: Navigate to Live Monitor and check status

### Database Errors
- Delete `cheating_detection.db` and restart
- Check file permissions
- Ensure SQLite is installed

### Detection Not Working
- Ensure good lighting conditions
- Position face clearly in frame
- Check camera permissions
- Verify YOLO model file exists (`yolov8n.pt`)

### Login Issues
- Use default credentials: admin/admin
- Clear browser cookies
- Check database initialization
- Create new account via registration

## 📝 Default Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin`

**Note:** Change default password after first login for security!

## 🔄 Updates & Maintenance

### Backup Database
```bash
cp cheating_detection.db cheating_detection_backup.db
```

### Clear Old Evidence
```bash
# Delete screenshots older than 30 days
find static/evidence/screenshots/ -mtime +30 -delete
```

### Reset System
```bash
# Delete database and restart
rm cheating_detection.db
python run_app.py
```

## 📞 Support

For issues or questions:
1. Check this guide first
2. Review error messages in console
3. Check browser console for JavaScript errors
4. Verify all dependencies are installed

## 🎓 Best Practices

1. **Regular Monitoring**: Check dashboard frequently during exams
2. **Evidence Review**: Review captured screenshots for verification
3. **User Management**: Remove inactive users regularly
4. **System Updates**: Keep dependencies updated
5. **Backup Data**: Regular database backups recommended

## ⚠️ Important Notes

- This system is for educational/monitoring purposes
- Ensure proper consent and privacy compliance
- Test system before actual exam use
- Maintain good lighting for best detection
- Keep camera lens clean
- Stable internet connection recommended

## 🚀 Production Deployment

For production use:
1. Change secret key in `app.py`
2. Use production WSGI server (Gunicorn/uWSGI)
3. Enable HTTPS
4. Set up proper logging
5. Configure firewall rules
6. Regular security audits

---

**Version:** 2.0  
**Last Updated:** December 2025  
**License:** Educational Use
