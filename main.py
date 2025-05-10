import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, current_user

from flask_login import login_required, login_user


from flask_login import login_required
from datetime import datetime
from flask import flash
from flask import send_file
import io
from bs4 import BeautifulSoup


login_manager = LoginManager()

local_server = True
app = Flask(__name__)
app.secret_key = 'sunvi'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sut'  # Replace with your actual DB URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager.init_app(app)

# Set the upload folder for videos. Make sure the folder exists.
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads', 'videos')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# -----------------------------
# Models
# -----------------------------
class CourseProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    week = db.Column(db.Integer, nullable=False)  # 1, 2, or 3
    is_completed = db.Column(db.Boolean, default=False)

    user = db.relationship('users', backref='course_progress')
    course = db.relationship('Course', backref='progress')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    videos = db.relationship('CourseVideo', backref='course', lazy=True)
    user = db.relationship('users', backref='courses')
class CourseVideo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer, nullable=False)  # Week number (1, 2, 3)
    title = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

class notes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(100), nullable=False)
    des = db.Column(db.String(258))
    tags = db.Column(db.String(50))
    categories = db.Column(db.String(50))
    ispublic = db.Column(db.Boolean)
    note = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    starred_by = db.relationship('StarredNote', backref='note', lazy=True)

class StarredNote(db.Model):
    __tablename__ = 'starred_note'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'), nullable=False)

class users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)  # True for admin, False for regular user
    is_subscribed = db.Column(db.Boolean, default=False)  # Track subscription status
    starred_notes = db.relationship('StarredNote', backref='user', lazy=True)
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'), nullable=True)
    video_id = db.Column(db.Integer, nullable=True)
    course_id = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship('users', backref='comments')
    note = db.relationship('notes', backref='comments')

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    timestamp = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship('users', backref='notifications')


class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_type = db.Column(db.String(100), nullable=False)  # e.g., 'opened_note'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'), nullable=True)
    course_id = db.Column(db.Integer, nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    user = db.relationship('users', backref='activity_logs')
    note = db.relationship('notes', backref='activity_logs')
# New model for storing uploaded videos
class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    course_id = db.Column(db.Integer, nullable=True)  # Optional: assign course if needed

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    card_name = db.Column(db.String(100), nullable=False)
    card_number = db.Column(db.String(16), nullable=False)  # ideally masked/stored securely
    amount = db.Column(db.Float, nullable=False)
    expiry = db.Column(db.String(5), nullable=False)  # Format: MM/YY
    cvv = db.Column(db.String(3), nullable=False)     # never store in production
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))
# -----------------------------
# Routes
# -----------------------------
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = users.query.get(user_id)

    # Redirect to admin dashboard if the user is an admin
    if user.is_admin:
        all_users = users.query.all()
        all_courses = Course.query.all()
        return render_template('admin_dash.html', users=all_users, courses=all_courses)
    
    # Fetch recent notes
    recent_notes = notes.query.filter_by(user_id=user_id).order_by(notes.id.desc()).limit(5).all()

    # Fetch starred notes
    starred_note_ids = [star.note_id for star in StarredNote.query.filter_by(user_id=user_id).all()]
    starred_notes = notes.query.filter(notes.id.in_(starred_note_ids)).all()

    # Fetch recent courses (e.g., created or enrolled by the user)
    recent_courses = Course.query.filter_by(user_id=user_id).order_by(Course.id.desc()).limit(5).all()

    return render_template('index.html', recent_notes=recent_notes, starred_notes=starred_notes, recent_courses=recent_courses)

@app.route('/create_note', methods=["GET", "POST"])
def create_note():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        tags = request.form['tags']
        categories = request.form['categories']
        ispublic = request.form.get('ispublic') == 'on'
        note_content = request.form['note']

        new_note = notes(
            Title=title,
            des=description,
            tags=tags,
            categories=categories,
            ispublic=ispublic,
            note=note_content,
            user_id=user_id
        )

        try:
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('notepad', note_id=new_note.id))
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

    return render_template('create_note.html')

@app.route('/profile')
@login_required
def profile():
    user_id = session['user_id']
    user = users.query.get(user_id)
    return render_template('profile.html', user=user)

@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    user_id = session['user_id']
    user = users.query.get(user_id)

    if request.method == 'POST':
        user.username = request.form['username']
        #user.email = request.form['email']
        db.session.commit()
        return redirect(url_for('profile'))

    return render_template('update_profile.html', user=user)

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    user_id = session['user_id']
    user = users.query.get(user_id)

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']

        if user.password == current_password:  # Replace with hashed password check
            user.password = new_password  # Hash the new password before saving
            db.session.commit()
            return redirect(url_for('profile'))
        else:
            return render_template('change_password.html', error="Incorrect current password")

    return render_template('change_password.html')

@app.route('/admin')
@login_required
def admin_dashboard():
    user_id = session['user_id']
    user = users.query.get(user_id)

    if not user.is_admin:
        return redirect(url_for('index'))
    all_users = users.query.all()
    all_notes = notes.query.all()
    all_courses = Course.query.all()
    all_comments = Comments.query.all()
    all_notifications = Notification.query.all()
    return render_template('admin_dash.html', all_users=all_users, all_notes=all_notes, all_courses=all_courses, all_comments=all_comments, all_notifications=all_notifications)

@app.route('/approve_course/<int:course_id>', methods=['POST'])
@login_required
def approve_course(course_id):
    user_id = session['user_id']
    user = users.query.get(user_id)

    if not user.role:
        return redirect(url_for('index'))

    course = Course.query.get(course_id)
    course.is_approved = True  # Add an `is_approved` field to the `Course` model
    db.session.commit()
    return redirect(url_for('admin_dashboard'))

@app.route('/remove_user/<int:user_id>', methods=['POST'])
@login_required
def remove_user(user_id):
    # Get the current logged-in user
    admin_id = session.get('user_id')
    admin = users.query.get(admin_id)

    # Check if the logged-in user is an admin
    if not admin or not admin.is_admin:
        return redirect(url_for('index', error="You are not authorized to perform this action."))

    # Fetch the user to be removed
    user = users.query.get(user_id)
    if not user:
        return redirect(url_for('admin_dashboard', error="User not found."))

    # Prevent admin users from being removed
    if user.is_admin:
        return redirect(url_for('admin_dashboard', error="Cannot remove an admin user."))

    # Remove the user
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('admin_dashboard', success="User removed successfully."))
    except Exception as e:
        return redirect(url_for('admin_dashboard', error=f"Error removing user: {str(e)}"))



@app.route('/notepad/<int:note_id>', methods=['GET', 'POST'])
def notepad(note_id):
    note = notes.query.get_or_404(note_id)
    
    # Check if the user is authorized to view/edit the note
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if note.user_id != session['user_id'] and not note.ispublic:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'POST':
        # Get the updated note content from the form
        note_content = request.form.get('note_content')
        if note_content:
            note.note = note_content  # Update the note's content
            try:
                db.session.commit()
                flash('Note saved successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error saving note: {str(e)}', 'error')
        return redirect(url_for('notepad', note_id=note_id))
    
    return render_template('notepad.html', note=note)
@app.route('/download_note/<int:note_id>')
def download_note(note_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    note = notes.query.get_or_404(note_id)
    # Check if the user owns the note or if it's public
    if note.user_id != session['user_id'] and not note.ispublic:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Strip HTML tags from note content for plain text
    soup = BeautifulSoup(note.note or '', 'html.parser')
    plain_text = soup.get_text()
    
    # Create the text content for the file
    content = f"Title: {note.Title}\n"
    if note.des:
        content += f"Description: {note.des}\n"
    if note.tags:
        content += f"Tags: {note.tags}\n"
    if note.categories:
        content += f"Category: {note.categories}\n"
    content += f"Public: {'Yes' if note.ispublic else 'No'}\n\n"
    content += f"Content:\n{plain_text}"
    
    # Create a BytesIO buffer to serve the file
    buffer = io.BytesIO(content.encode('utf-8'))
    buffer.seek(0)
    
    # Serve the file as a download
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"{note.Title}.txt",
        mimetype='text/plain'
    )
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = users.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            session['user_id'] = user.id
            login_user(user)  # Use Flask-Login to log in the user
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        is_admin = request.form.get('is_admin') == 'on'  # Checkbox for admin signup

        existing_user = users.query.filter_by(username=uname).first()
        if existing_user:
            return render_template('signup.html', error='Username already exists')

        # Hash the password before storing it
        hashed_pwd = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())

        new_user = users(username=uname, password=hashed_pwd.decode('utf-8'), is_admin=is_admin)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            return render_template('signup.html', error=str(e))

    return render_template('signup.html')

@app.route('/all_notes')
def all_notes():
    all_notes = notes.query.all()
    return render_template('all_notes.html', notes=all_notes)

@app.route('/star_note/<int:note_id>', methods=['POST'])
def star_note(note_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    already_starred = StarredNote.query.filter_by(user_id=user_id, note_id=note_id).first()
    if not already_starred:
        star = StarredNote(user_id=user_id, note_id=note_id)
        db.session.add(star)
        db.session.commit()
    return redirect(request.referrer)

@app.route('/unstar_note/<int:note_id>', methods=['POST'])
def unstar_note(note_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    starred_note = StarredNote.query.filter_by(user_id=user_id, note_id=note_id).first()
    if starred_note:
        db.session.delete(starred_note)
        db.session.commit()

    return redirect(request.referrer)

@app.route('/starred_notes')
def starred_notes():
    user_id = session.get('user_id')
    starred = StarredNote.query.filter_by(user_id=user_id).all()
    note_ids = [s.note_id for s in starred]
    notes_list = notes.query.filter(notes.id.in_(note_ids)).all()
    return render_template('starred_notes.html', notes=notes_list)

@app.route('/add_comment/<int:note_id>', methods=['POST'])
def add_comment(note_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    comment_content = request.form['comment']

    new_comment = Comments(content=comment_content, user_id=user_id, note_id=note_id)
    try:
        db.session.add(new_comment)
        db.session.commit()
        return redirect(request.referrer)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# New route for uploading videos
@app.route('/upload_video', methods=['GET', 'POST'])
def upload_video():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        video_file = request.files.get('video')
        if video_file:
            # Generate the secure filename
            filename = secure_filename(video_file.filename)

            # Define the upload path, ensuring forward slashes for the URL
            upload_path = os.path.join('static', 'uploads', 'videos', filename)

            # Ensure the file path uses forward slashes
            upload_path = upload_path.replace(os.sep, '/')  # Replace system-dependent separator

            try:
                # Save the video file
                video_file.save(os.path.join('static', 'uploads', 'videos', filename))

                # Create a new video entry in the database with forward slashes in the file path
                new_video = Video(title=title, file_path=upload_path, course_id=None)
                db.session.add(new_video)
                db.session.commit()

                return redirect(url_for('index'))
            except Exception as e:
                return jsonify({"status": "error", "message": str(e)})

    return render_template('upload_video.html')


# New route to list all videos
@app.route('/videos')
def videos():
    all_videos = Video.query.all()
    return render_template('videos.html', videos=all_videos)

# New route for playing a video with note taking
@app.route('/course/<int:video_id>', methods=['GET', 'POST'])
def course(video_id):
    video_item = Video.query.get_or_404(video_id)
    if request.method == 'POST':
        note_content = request.form.get('note_content')
        # Here you could save the note content to a new model (like VideoNote)
        # For demonstration, we're just printing it.
        print("Note saved:", note_content)
        return redirect(url_for('course', video_id=video_id))
    return render_template('course_video.html', video=video_item)

@app.route('/notifications')
def notifications():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    notifs = Notification.query.filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()
    return render_template('notifications.html', notifications=notifs)
@app.route('/activity')
def activity():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    # Fetch activity logs
    logs = ActivityLog.query.filter_by(user_id=user_id).order_by(ActivityLog.timestamp.desc()).limit(10).all()

    # Fetch unread notifications
    notifications = Notification.query.filter_by(user_id=user_id, is_read=False).order_by(Notification.timestamp.desc()).all()

    # Mark all notifications as read
    for notification in notifications:
        notification.is_read = True
    db.session.commit()

    return render_template('activity.html', activities=logs, notifications=notifications)

@app.route('/upload_course', methods=['GET', 'POST'])
def upload_course():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        course_title = request.form['course_title']
        user_id = session['user_id']
        video_files = {
            1: request.files.get('week1_video'),
            2: request.files.get('week2_video'),
            3: request.files.get('week3_video')
        }

        new_course = Course(title=course_title, user_id=user_id)
        db.session.add(new_course)
        db.session.commit()

        for week, file in video_files.items():
            if file:
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                relative_path = path.replace(os.sep, '/')

                course_video = CourseVideo(
                    week=week,
                    title=f"Week {week} Video",
                    file_path=relative_path,
                    course_id=new_course.id
                )
                db.session.add(course_video)

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('upload_course.html')

@app.route('/view_course/<int:course_id>')
def view_course(course_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    course = Course.query.get_or_404(course_id)
    videos = CourseVideo.query.filter_by(course_id=course_id).order_by(CourseVideo.week.asc()).all()

    # Group videos by week
    week_videos = {1: [], 2: [], 3: []}
    for video in videos:
        week_videos.setdefault(video.week, []).append(video)

    # Get user's completed weeks
    completed_weeks = [
        progress.week for progress in CourseProgress.query.filter_by(user_id=user_id, course_id=course_id, is_completed=True)
    ]

    return render_template('view_course.html', course=course, week_videos=week_videos, completed_weeks=completed_weeks)

@app.route('/mark_week_complete/<int:course_id>/<int:week>', methods=['POST'])
def mark_week_complete(course_id, week):
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401  # Return error if not logged in

    user_id = session['user_id']

    # Check if progress already exists
    progress = CourseProgress.query.filter_by(user_id=user_id, course_id=course_id, week=week).first()

    try:
        if not progress:
            # If no progress exists, create a new one
            progress = CourseProgress(user_id=user_id, course_id=course_id, week=week, is_completed=True)
            db.session.add(progress)
            db.session.commit()  # Commit to save changes
        else:
            # If progress exists, just mark it as completed
            progress.is_completed = True
            db.session.commit()

        return jsonify({'message': f'Week {week} of Course {course_id} marked as completed.'}), 200

    except Exception as e:
        # Handle any potential errors
        print(f"Error: {e}")
        db.session.rollback()  # Rollback any changes if an error occurs
        return jsonify({'error': 'An error occurred while marking the week as complete.'}), 500


    db.session.commit()
    return redirect(url_for('view_course', course_id=course_id))
@app.route('/track_progress', methods=['POST'])
@login_required
def track_progress():
    data = request.get_json()
    course_id = data.get('course_id')
    week = data.get('week')
    
    # Check if entry exists
    progress = CourseProgress.query.filter_by(
        user_id=current_user.id,
        course_id=course_id,
        week=week
    ).first()

    if not progress:
        progress = CourseProgress(
            user_id=current_user.id,
            course_id=course_id,
            week=week,
            is_completed=True
        )
        db.session.add(progress)
    else:
        progress.is_completed = True

    db.session.commit()
    return jsonify({"status": "success"})

@app.route('/courses')
def courses():
    search_query = request.args.get('q', '').strip()
    category_filter = request.args.get('category', '').strip()

    query = Course.query

    if search_query:
        query = query.filter(Course.title.ilike(f"%{search_query}%"))

    if category_filter:
        query = query.filter_by(category=category_filter)

    filtered_courses = query.all()

    return render_template('courses.html', courses=filtered_courses)


@app.context_processor
def inject_notifications_count():
    if 'user_id' in session:
        user_id = session['user_id']
        notifications_count = Notification.query.filter_by(user_id=user_id, is_read=False).count()
        return {'notifications_count': notifications_count}
    return {'notifications_count': 0}

@app.route('/subscription_status')
def subscription_status():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = users.query.get(user_id)

    # Check if the user is subscribed
    if user.is_subscribed:
        subscription_message = "You are subscribed! Here is your personal session link."
        session_link = "https://example.com/your-personal-session-link"
    else:
        subscription_message = "You are not subscribed. Please subscribe to access one-on-one sessions."
        session_link = None

    return render_template('subscription_status.html', 
                           subscription_message=subscription_message, 
                           session_link=session_link)
@app.route('/course_progress/<int:course_id>', methods=['GET'])
def course_progress(course_id):
    # Fetch the course by its ID
    course = Course.query.get_or_404(course_id)
    
    # Fetch the progress data for the course
    progress_data = CourseProgress.query.filter_by(course_id=course_id).all()
    
    # Render the course progress page with course and progress data
    return render_template('course_progress.html', course=course, progress_data=progress_data)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        try:
            # Get and validate form data
            card_name = request.form.get('card_name', '').strip()
            card_number = request.form.get('card_number', '').replace(" ", "")
            amount = float(request.form.get('amount', '0'))
            expiry = request.form.get('expiry', '').strip()
            cvv = request.form.get('cvv', '').strip()

            # Enhanced validation
            if not all([card_name, card_number, expiry, cvv]):
                flash('All fields are required', 'error')
                return render_template('payment.html')
            
            if amount <= 0:
                flash('Amount must be positive', 'error')
                return render_template('payment.html')

            if not card_number.isdigit() or len(card_number) not in (13, 14, 15, 16):
                flash('Invalid card number', 'error')
                return render_template('payment.html')

            if not all(x.isdigit() for x in cvv) or len(cvv) not in (3, 4):
                flash('Invalid CVV', 'error')
                return render_template('payment.html')

            # Process payment (store only last 4 digits)
            payment = Payment(
                card_name=card_name,
                card_number=card_number[-4:],
                amount=amount,
                expiry=expiry,
                cvv='***',
                payment_date=datetime.utcnow()
            )

            db.session.add(payment)
            db.session.commit()
            if 'user_id' in session:
                   user = users.query.get(session['user_id'])
                   if user:
                       user.is_subscribed = True
                       db.session.commit()
            flash('Payment processed successfully!', 'success')
            return redirect(url_for('payment'))

        except ValueError:
            flash('Invalid amount format', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Payment failed: {str(e)}', 'error')

    return render_template('payment.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
