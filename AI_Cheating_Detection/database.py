import sqlite3
import os
from werkzeug.security import generate_password_hash
from datetime import datetime

DATABASE = 'cheating_detection.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with all required tables"""
    conn = get_db_connection()
    
    # Users table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'examiner',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Exam sessions table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS exam_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            examiner_id INTEGER NOT NULL,
            start_time TIMESTAMP NOT NULL,
            end_time TIMESTAMP,
            status TEXT DEFAULT 'active',
            FOREIGN KEY (examiner_id) REFERENCES users (id)
        )
    ''')
    
    # Detection logs table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS detection_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            timestamp TIMESTAMP NOT NULL,
            behaviors TEXT NOT NULL,
            evidence_path TEXT,
            person_count INTEGER DEFAULT 0,
            face_count INTEGER DEFAULT 0,
            FOREIGN KEY (session_id) REFERENCES exam_sessions (id)
        )
    ''')
    
    # Try to remove risk_score column if it exists (for existing databases)
    try:
        conn.execute('ALTER TABLE detection_logs DROP COLUMN risk_score')
    except:
        pass  # Column doesn't exist or can't be dropped (SQLite limitation)
    
    # Evidence table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS evidence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            detection_log_id INTEGER,
            file_path TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_size INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (detection_log_id) REFERENCES detection_logs (id)
        )
    ''')
    
    # Activity logs table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            activity_type TEXT NOT NULL,
            description TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    
    # Create default admin user if it doesn't exist
    admin_exists = conn.execute('SELECT COUNT(*) as count FROM users WHERE role = ?', ('admin',)).fetchone()['count']
    if admin_exists == 0:
        admin_password = generate_password_hash('admin123')
        conn.execute('''
            INSERT INTO users (username, email, password, role)
            VALUES (?, ?, ?, ?)
        ''', ('admin', 'admin@example.com', admin_password, 'admin'))
        
        # Create default examiner user
        examiner_password = generate_password_hash('examiner123')
        conn.execute('''
            INSERT INTO users (username, email, password, role)
            VALUES (?, ?, ?, ?)
        ''', ('examiner', 'examiner@example.com', examiner_password, 'examiner'))
        
        conn.commit()
    
    conn.close()
    print("Database initialized successfully!")

def save_detection(session_id, behaviors, evidence_path=None, person_count=0, face_count=0):
    """Save a detection event to the database with error handling"""
    try:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO detection_logs (session_id, timestamp, behaviors, evidence_path, person_count, face_count)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (session_id, datetime.now(), ', '.join(behaviors), evidence_path, person_count, face_count))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving detection: {e}")
        return False

def get_dashboard_stats():
    """Get statistics for the admin dashboard"""
    conn = get_db_connection()
    
    # Total detections
    total_detections = conn.execute('SELECT COUNT(*) as count FROM detection_logs').fetchone()['count']
    
    # Active days (distinct dates with detections)
    active_days = conn.execute('''
        SELECT COUNT(DISTINCT DATE(timestamp)) as count 
        FROM detection_logs
    ''').fetchone()['count']
    
    # Recent alerts (last 10)
    recent_alerts = conn.execute('''
        SELECT timestamp, behaviors, evidence_path 
        FROM detection_logs 
        ORDER BY timestamp DESC 
        LIMIT 10
    ''').fetchall()
    
    conn.close()
    
    return {
        'total_detections': total_detections,
        'active_days': active_days,
        'recent_alerts': [dict(alert) for alert in recent_alerts]
    }

def create_user(username, email, password, role='examiner'):
    """Create a new user with proper validation"""
    # Input validation
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters long"
    
    if not email or '@' not in email:
        return False, "Please enter a valid email address"
    
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    if role not in ['admin', 'examiner']:
        return False, "Invalid role specified"
    
    conn = get_db_connection()
    try:
        hashed_password = generate_password_hash(password)
        conn.execute('''
            INSERT INTO users (username, email, password, role)
            VALUES (?, ?, ?, ?)
        ''', (username.strip(), email.strip().lower(), hashed_password, role))
        conn.commit()
        conn.close()
        return True, "User created successfully"
    except sqlite3.IntegrityError as e:
        conn.close()
        if 'username' in str(e):
            return False, "Username already exists"
        elif 'email' in str(e):
            return False, "Email already exists"
        else:
            return False, "User creation failed"
    except Exception as e:
        conn.close()
        return False, f"Database error: {str(e)}"

def authenticate_user(username, password):
    """Authenticate user login with proper error handling"""
    from werkzeug.security import check_password_hash
    
    if not username or not password:
        return None
    
    try:
        conn = get_db_connection()
        user = conn.execute('''
            SELECT id, username, email, password, role 
            FROM users 
            WHERE username = ?
        ''', (username.strip(),)).fetchone()
        
        if user and check_password_hash(user['password'], password):
            # Update last login
            conn.execute('''
                UPDATE users SET last_login = ? WHERE id = ?
            ''', (datetime.now(), user['id']))
            conn.commit()
            conn.close()
            return dict(user)
        
        conn.close()
        return None
    except Exception as e:
        print(f"Authentication error: {e}")
        return None

def get_all_users():
    """Get all users for admin management"""
    conn = get_db_connection()
    users = conn.execute('''
        SELECT id, username, email, role, created_at, last_login 
        FROM users 
        ORDER BY created_at DESC
    ''').fetchall()
    conn.close()
    return [dict(user) for user in users]

def delete_user(user_id):
    """Delete a user"""
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return True

