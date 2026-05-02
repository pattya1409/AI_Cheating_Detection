# Quick Reference Guide

## 🚀 Start Application

```bash
cd AI_Cheating_Detection
python app.py
```

**Access**: http://localhost:5000

---

## 🔐 Login Credentials

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Administrator |
| examiner | examiner123 | Examiner |

---

## 📋 Main Features

### 1. Dashboard
- **URL**: `/dashboard`
- **Features**: Statistics, charts, recent alerts
- **Design**: 3D glassmorphism cards with animations

### 2. Live Monitor
- **URL**: `/live_monitor`
- **Features**: Real-time camera monitoring, AI detection
- **Actions**: Test Camera → Start → Monitor → Stop
- **Design**: 3D video card, animated controls, live alerts

### 3. Video Upload (NEW)
- **URL**: `/video_upload`
- **Features**: Upload pre-recorded videos for analysis
- **Formats**: MP4, AVI, MOV, MKV, FLV, WMV
- **Results**: Statistics, behaviors, timeline, evidence
- **Design**: 3D upload zone, progress bar, results cards

### 4. Admin Panel
- **URL**: `/admin` (admin only)
- **Features**: User management, system stats

---

## 🎯 Quick Actions

### Upload & Analyze Video
1. Click **Upload Video** in navigation
2. Drag & drop video or click **Browse Files**
3. Wait for processing (progress bar shows status)
4. Review results:
   - Total frames processed
   - Suspicious frames detected
   - Risk level percentage
   - Behaviors summary
   - Detection timeline

### Start Live Monitoring
1. Click **Monitor** in navigation
2. Click **Test Camera** (optional)
3. Click **Start** button
4. Watch live feed with AI detection
5. View alerts in real-time
6. Click **Stop** when done

---

## 🔍 Detection Types

The system detects:
- 👀 **Looking Left/Right**: Head direction tracking
- 💬 **Talking**: Mouth movement detection
- 📱 **Mobile Phone**: Object detection via YOLO
- 👥 **Multiple People**: Person count detection
- 😊 **Multiple Faces**: Face count detection

---

## 📁 Important Directories

```
AI_Cheating_Detection/
├── static/
│   ├── uploads/          # Uploaded videos
│   └── evidence/
│       └── screenshots/  # Detection evidence
├── templates/            # HTML pages
├── app.py               # Main application
├── detection_service.py # AI detection logic
└── database.py          # Database operations
```

---

## 🎨 Design Features

All pages feature:
- ✨ 3D glassmorphism cards
- 🌈 Purple/pink gradient backgrounds
- 🎭 Animated icons and buttons
- 💫 Hover tilt effects
- 🔄 Smooth transitions
- 📱 Responsive design

---

## ⚡ Keyboard Shortcuts

- **F5**: Refresh page
- **Ctrl+C**: Stop application (in terminal)
- **Esc**: Close modals/alerts

---

## 🛠️ Troubleshooting

### Camera Not Working
1. Check camera connection
2. Close other apps using camera
3. Click "Test Camera" button
4. Restart application if needed

### Video Upload Failed
1. Check file format (MP4, AVI, MOV, etc.)
2. Ensure file size is reasonable (< 500MB)
3. Check available disk space
4. Try a different video file

### Application Won't Start
1. Check Python is installed: `python --version`
2. Install dependencies: `pip install -r requirements.txt`
3. Check port 5000 is available
4. Review error messages in terminal

---

## 📊 Performance Tips

- **Video Upload**: Use videos < 5 minutes for faster processing
- **Live Monitor**: Ensure good lighting for better detection
- **Browser**: Use Chrome/Edge for best performance
- **Camera**: 720p or higher recommended

---

## 🔒 Security Notes

- Change default passwords in production
- Use HTTPS in production
- Keep dependencies updated
- Review evidence files regularly
- Backup database periodically

---

## 📞 Support

For issues or questions:
1. Check documentation files:
   - `README.md`
   - `NEW_FEATURES.md`
   - `INSTALLATION_GUIDE.md`
2. Review error messages in terminal
3. Check browser console (F12)

---

## 🎓 Best Practices

### For Examiners
- Test camera before exam starts
- Monitor continuously during exam
- Review alerts immediately
- Save evidence screenshots
- Document suspicious behavior

### For Administrators
- Create user accounts before exams
- Monitor system status regularly
- Review detection statistics
- Backup database weekly
- Update system regularly

---

**Quick Start**: Login → Choose Monitor or Upload → Start Detection → Review Results

**Application Status**: ✅ Running on http://localhost:5000
