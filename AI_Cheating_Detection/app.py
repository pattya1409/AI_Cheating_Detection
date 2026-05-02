from flask import Flask, render_template, Response, jsonify, request, session, redirect, url_for, flash
from detection_service import DetectionService
from database import init_db, get_dashboard_stats, authenticate_user, create_user, get_all_users, delete_user
from datetime import datetime
import cv2
import secrets
import os

app = Flask(__name__)
# Generate a secure secret key
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Initialize database
init_db()

detector = DetectionService()

# Helper function to check if user is logged in
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Please log in to access this page.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# Helper function to check if user is admin
def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in") or session.get("role") != "admin":
            flash("Access denied. Administrator privileges required.", "error")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return decorated_function

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # Try database authentication first
        user = authenticate_user(username, password)
        if user:
            session["logged_in"] = True
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            return redirect(url_for("dashboard"))
        
        # Fallback to hardcoded admin
        elif username == "admin" and password == "admin":
            session["logged_in"] = True
            session["user_id"] = 0
            session["username"] = "admin"
            session["role"] = "admin"
            return redirect(url_for("dashboard"))
        
        flash("Invalid credentials", "error")
        return render_template("login.html")
    
    return render_template("login.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        role = request.form.get("role", "examiner")
        
        # Validation
        if not all([username, email, password, confirm_password]):
            flash("All fields are required.", "error")
            return render_template("register.html")
        
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register.html")
        
        success, message = create_user(username, email, password, role)
        if success:
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        else:
            flash(message, "error")
            return render_template("register.html")
    
    return render_template("register.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
@login_required
def dashboard():
    try:
        # Get real statistics from database
        stats = get_dashboard_stats()
        
        return render_template(
            "dashboard.html",
            stats=stats,
            monitoring_status=detector.running,
            alerts=stats['recent_alerts']
        )
    except Exception as e:
        flash(f"Error loading dashboard: {str(e)}", "error")
        return render_template("dashboard.html", stats={"total_detections": 0, "active_days": 0}, monitoring_status=False, alerts=[])

# ---------------- ADMIN PANEL ----------------
@app.route("/admin")
@admin_required
def admin():
    try:
        # Get real statistics from database
        stats = get_dashboard_stats()
        users = get_all_users()
        
        return render_template(
            "admin.html",
            stats=stats,
            monitoring_status=detector.running,
            alerts=stats['recent_alerts'],
            users=users
        )
    except Exception as e:
        flash(f"Error loading admin panel: {str(e)}", "error")
        return redirect(url_for("dashboard"))

# ---------------- DELETE USER ----------------
@app.route("/admin/delete_user/<int:user_id>", methods=["POST"])
@admin_required
def delete_user_route(user_id):
    try:
        if user_id == session.get("user_id"):
            return jsonify({"status": "error", "message": "Cannot delete your own account"}), 400
        
        delete_user(user_id)
        return jsonify({"status": "success", "message": "User deleted successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ---------------- LIVE MONITOR ----------------
@app.route("/live_monitor")
@login_required
def live_monitor():
    return render_template("live_monitor.html")

# ---------------- TEST CAMERA ----------------
@app.route("/api/test_camera")
@login_required
def test_camera():
    try:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if cap.isOpened():
            cap.release()
            return jsonify({"status": "success", "message": "Camera is working properly"})
        return jsonify({"status": "error", "message": "Camera not accessible"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": f"Camera test failed: {str(e)}"}), 500

# ---------------- START DETECTION ----------------
@app.route("/api/start_detection", methods=["POST"])
@login_required
def start_detection():
    try:
        user_id = session.get("user_id", 1)
        detector.start_detection(session_id=1, examiner_id=user_id)
        return jsonify({"status": "success", "message": "Detection started successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to start detection: {str(e)}"}), 500

# ---------------- STOP DETECTION ----------------
@app.route("/api/stop_detection", methods=["POST"])
@login_required
def stop_detection():
    try:
        detector.stop_detection()
        return jsonify({"status": "success", "message": "Detection stopped successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to stop detection: {str(e)}"}), 500

# ---------------- VIDEO FEED ----------------
@app.route("/video_feed")
@login_required
def video_feed():
    try:
        return Response(
            detector.generate_frames(),
            mimetype="multipart/x-mixed-replace; boundary=frame"
        )
    except Exception as e:
        print(f"Video feed error: {e}")
        return Response("", mimetype="text/plain"), 500

# ---------------- STATUS ----------------
@app.route("/api/detection_status")
@login_required
def detection_status():
    try:
        return jsonify({
            "active": detector.running,
            "latest_alert": detector.latest_alert,
            "timestamp": detector.latest_alert.get("timestamp") if detector.latest_alert else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- LIVE STATS API ----------------
@app.route("/api/stats")
@login_required
def get_stats():
    """API endpoint to get real-time statistics"""
    try:
        stats = get_dashboard_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- SYSTEM STATUS ----------------
@app.route("/system_status")
@admin_required
def system_status():
    """System status and diagnostics page"""
    return render_template("system_status.html")

# ---------------- VIDEO UPLOAD PAGE ----------------
@app.route("/video_upload")
@login_required
def video_upload():
    """Video upload page"""
    return render_template("video_upload.html")

# ---------------- UPLOAD VIDEO API ----------------
@app.route("/api/upload_video", methods=["POST"])
@login_required
def upload_video():
    """Handle video file upload and processing"""
    try:
        if 'video' not in request.files:
            return jsonify({"status": "error", "message": "No video file provided"}), 400
        
        video_file = request.files['video']
        
        if video_file.filename == '':
            return jsonify({"status": "error", "message": "No file selected"}), 400
        
        # Validate file extension
        allowed_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'}
        file_ext = os.path.splitext(video_file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            return jsonify({"status": "error", "message": f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"}), 400
        
        # Create uploads directory
        upload_dir = "static/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save video file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"video_{timestamp}{file_ext}"
        video_path = os.path.join(upload_dir, filename)
        video_file.save(video_path)
        
        # Process video in background (for now, process synchronously)
        user_id = session.get("user_id", 1)
        results = detector.process_video(video_path, session_id=1, examiner_id=user_id)
        
        return jsonify({
            "status": "success",
            "message": "Video processed successfully",
            "results": results,
            "video_path": video_path
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": f"Upload failed: {str(e)}"}), 500

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    detector.stop_detection()
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
