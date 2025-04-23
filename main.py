import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename

local_server = True
app = Flask(__name__)
app.secret_key = 'sunvi'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/suh'  # Replace with your actual DB URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set the upload folder for videos. Make sure the folder exists.
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads', 'videos')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# -----------------------------
# Models
# -----------------------------
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    videos = db.relationship('CourseVideo', backref='course', lazy=True)

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

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
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

# -----------------------------
# Routes
# -----------------------------

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    # Fetch the 5 most recent notes
    recent_notes = notes.query.filter_by(user_id=user_id).order_by(notes.id.desc()).limit(5).all()

    # Fetch the starred notes
    starred_note_ids = [star.note_id for star in StarredNote.query.filter_by(user_id=user_id).all()]
    starred_notes = notes.query.filter(notes.id.in_(starred_note_ids)).all()

    return render_template('index.html', recent_notes=recent_notes, starred_notes=starred_notes)

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

@app.route('/notepad/<int:note_id>')
def notepad(note_id):
    note = notes.query.get_or_404(note_id)
    return render_template('notepad.html', note=note)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = users.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = username
            session['user_id'] = user.id 
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
        existing_user = users.query.filter_by(username=uname).first()

        if existing_user:
            return render_template('signup.html', error='Username already exists')

        new_user = users(username=uname, password=pwd)
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
    logs = ActivityLog.query.filter_by(user_id=user_id).order_by(ActivityLog.timestamp.desc()).all()

    # Mark all notifications as read
    Notification.query.filter_by(user_id=user_id, is_read=False).update({'is_read': True})
    db.session.commit()

    return render_template('activity.html', activities=logs)

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
    course = Course.query.get_or_404(course_id)
    videos = CourseVideo.query.filter_by(course_id=course_id).order_by(CourseVideo.week.asc()).all()

    # Group videos by week
    week_videos = {1: [], 2: [], 3: []}
    for video in videos:
        week_videos.setdefault(video.week, []).append(video)

    return render_template('view_course.html', course=course, week_videos=week_videos)

@app.route('/courses')
def courses():
    all_courses = Course.query.all()
    return render_template('courses.html', courses=all_courses)

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


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
