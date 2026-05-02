# AI-Based Cheating Detection System for Online Examinations

A comprehensive, industry-level cheating detection system that uses YOLOv8 and MediaPipe for real-time monitoring of online examinations.

## Features

### Backend & Architecture
- **Flask-based backend** with RESTful API
- **SQLite database** for users, logs, and evidence metadata
- **Secure session-based authentication** with role-based access control
- **Separated AI detection service** running in background threads

### Authentication & Roles
- **Login/Logout** functionality
- **Role-based access control:**
  - **Admin**: Full system access, user management, activity logs
  - **Examiner**: Monitoring, reports, and evidence access

### AI & Proctoring Enhancements
- **Multiple cheating behavior detection:**
  - Mobile phone usage (YOLOv8)
  - Multiple persons in frame
  - Frequent head movement
  - Talking (mouth open detection)
  - Book/object detection
- **Cheating Risk Score** calculation (0-100) based on detected behaviors
- **Real-time detection** with live camera feed

### Evidence & Alerts
- **Automatic evidence capture:**
  - Screenshots of suspicious activities
  - Timestamped logs of all detections
- **Email alerts** to examiners for high-risk cheating (risk score ≥ 70)

### Frontend (Responsive UI)
- **Bootstrap 5** responsive design
- **Professional pages:**
  - Login page
  - Dashboard with statistics and recent alerts
  - Live monitoring interface
  - Reports and logs viewer
  - Admin panel
- **Mobile, tablet, and desktop** compatible

### Reporting & Logging
- **Structured logs** for:
  - Detection events with risk scores
  - User activity tracking
  - Exam sessions
- **Admin dashboard** for system management

## Installation & Setup

### Prerequisites
- Python 3.8+ (3.10 recommended)
- Webcam/Camera access
- (Optional) SMTP credentials for email alerts

### Step 1: Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note:** The first installation may take several minutes as it downloads PyTorch and YOLOv8 models.

### Step 3: Initialize Database
The database will be automatically created on first run. Default credentials:
- **Admin:** username: `admin`, password: `admin123`
- **Examiner:** username: `examiner`, password: `examiner123`

**⚠️ Important:** Change these default passwords in production!

### Step 4: (Optional) Configure Email Alerts
Create a `.env` file in the project root:
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

For Gmail, use an [App Password](https://myaccount.google.com/apppasswords) instead of your regular password.

### Step 5: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## Usage

### Login
1. Open your browser and navigate to `http://localhost:5000`
2. Login with admin or examiner credentials
3. You'll be redirected to the dashboard

### Start Monitoring
1. Navigate to **Live Monitor** from the navigation menu
2. Click **Start Monitoring** to begin detection
3. The system will:
   - Access your webcam
   - Detect cheating behaviors in real-time
   - Capture evidence automatically
   - Log all detections to the database

### View Reports
1. Go to **Reports** to see all detection logs
2. Filter and view evidence (screenshots)
3. Check risk scores and detected behaviors

### Admin Panel
1. Login as admin to access the admin panel
2. View all users and their roles
3. Monitor system activity logs

## Project Structure

```
AI_Cheating_Detection/
├── app.py                 # Flask application and routes
├── database.py            # Database initialization and connection
├── detection_service.py   # YOLOv8 detection logic (preserved from main.py)
├── email_service.py       # Email alert functionality
├── mobile_detector.py     # MobileNet-SSD detector (optional backup)
├── main.py                # Original standalone script (preserved)
├── requirements.txt       # Python dependencies
├── templates/             # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── live_monitor.html
│   ├── reports.html
│   └── admin.html
├── static/                # Static files
│   ├── css/
│   ├── js/
│   └── evidence/          # Captured screenshots and videos
│       ├── screenshots/
│       └── videos/
├── yolov8n.pt            # YOLOv8 model file
└── cheating_detection.db  # SQLite database (created on first run)
```

## API Endpoints

- `GET /` - Redirects to login or dashboard
- `GET/POST /login` - User authentication
- `GET /logout` - User logout
- `GET /dashboard` - Main dashboard
- `GET /live_monitor` - Live monitoring interface
- `GET /reports` - Detection reports
- `GET /admin` - Admin panel (admin only)
- `POST /api/start_detection` - Start live monitoring
- `POST /api/stop_detection` - Stop live monitoring
- `GET /api/detection_status` - Get current detection status
- `GET /api/recent_alerts` - Get recent detection alerts
- `GET /api/evidence/<id>` - Download evidence file

## Detection Behaviors & Risk Scoring

The system calculates a risk score (0-100) based on detected behaviors:

| Behavior | Risk Points |
|----------|-------------|
| Mobile Phone Detected | 30 |
| Multiple Faces | 25 |
| Extra Person Detected | 25 |
| Book Detected | 20 |
| Talking | 15 |
| Frequent Head Movement | 10 |
| Looking Left/Right | 5 each |

**Risk Levels:**
- **High Risk (≥70):** Email alert sent to examiner
- **Medium Risk (40-69):** Logged with evidence
- **Low Risk (<40):** Logged for review

## Technical Details

### Preserved YOLO Detection Logic
The original YOLOv8 detection logic from `main.py` has been preserved in `detection_service.py`:
- Face detection using MediaPipe FaceMesh
- Head turn detection (left/right)
- Mouth open detection (talking)
- Object detection (person, cell phone, book) using YOLOv8
- Multiple person detection

### Database Schema
- **users**: User accounts with roles
- **exam_sessions**: Active exam monitoring sessions
- **detection_logs**: All cheating detection events
- **evidence**: Screenshots and video metadata
- **activity_logs**: User activity tracking

## Troubleshooting

### Camera Not Working
- Ensure your webcam is connected and not being used by another application
- Check camera permissions in your operating system

### Email Alerts Not Sending
- Verify SMTP credentials in `.env` file
- For Gmail, ensure you're using an App Password
- Check firewall settings for SMTP port 587

### Detection Not Starting
- Ensure YOLOv8 model file (`yolov8n.pt`) is present
- Check that all dependencies are installed correctly
- Review console output for error messages

## Security Notes

- **Change default passwords** before deploying to production
- Use strong passwords for admin accounts
- Configure HTTPS for production deployments
- Regularly backup the SQLite database
- Review and rotate SMTP credentials periodically

## Future Enhancements

- Video clip capture for suspicious activities
- Advanced audio detection
- Machine learning-based behavior analysis
- Multi-camera support
- Real-time video streaming to frontend
- Export reports to PDF/Excel

## License

This project is developed for academic/research purposes.

## Support

For issues or questions, please review the code comments and database schema for implementation details.
