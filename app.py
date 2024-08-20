from flask import Flask, render_template, redirect, url_for, flash, request,session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from config import Config
from models import db, User, Brief,BriefHistory
from brief_generator import generate_brief
from datetime import datetime, timedelta
import pytz
from forms import UpdateProfileForm
from flask_migrate import Migrate
from flask import jsonify

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'salman_faizi'

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db = SQLAlchemy(app)
migrate = Migrate(app, db)

import os
import secrets
from PIL import Image

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    return None


def render_generator():
    content = ""
    if request.method == 'POST':
        if 'modified_content' in request.form:
            content = request.form['modified_content']
            brief_type = "Custom"
            domain = "Custom"
        else:
            brief_type = request.form.get('brief_type') or request.form.get('custom_brief_type')
            domain = request.form.get('domain') or request.form.get('custom_domain')
            content = generate_brief(brief_type, domain)
    
    return render_template('index.html', content=content)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# @app.route('/')
# def index():
#     return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('introduction.html')

# @app.route('/login_redirect')
# def login_redirect():
#     return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if username or email already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        
        if existing_user:
            flash('Username or Email already exists! Please try logging in or use a different username/email.', 'warning')
            return redirect(url_for('signup'))
        
        # Create new user if no conflict
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = authenticate_user(email, password)
        
        if user:
            login_user(user)
            # render_generator

            return redirect(url_for('home'))  # Redirect to the dashboard or another page
        else:
            flash('Invalid email or password. Please try again.', 'error')
    
    return render_template('login.html')

    
    # return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('start_time', None)  # Clear guest session data
    logout_user()
    return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    content = ""
    if request.method == 'POST':
        if 'modified_content' in request.form:
            content = request.form['modified_content']
            brief_type = "Custom"
            domain = "Custom"
        else:
            brief_type = request.form.get('brief_type') or request.form.get('custom_brief_type')
            domain = request.form.get('domain') or request.form.get('custom_domain')
            content = generate_brief(brief_type, domain)
            brief = Brief(type=brief_type, domain=domain, content=content, author=current_user)
            db.session.add(brief)
            db.session.commit()
            generate_brief_history(BriefHistory=BriefHistory,content=content)
    return render_template('index.html', content=content)





@app.route('/guest_home', methods=['GET', 'POST'])
def guest_home():
    # Initialize session start time if not set
    if 'start_time' not in session:
        session['start_time'] = datetime.utcnow().isoformat()
    
    start_time_str = session.get('start_time')
    start_time = datetime.fromisoformat(start_time_str)
    
    # Check if 30 minutes have passed
    time_elapsed = datetime.utcnow() - start_time
    
    if time_elapsed > timedelta(minutes=30):
        # Session expired, either redirect to session_expired page
        session.pop('start_time', None)  # Clear session start time
        flash("Your guest session has expired. Please sign up to continue.", "warning")
        return redirect(url_for('session_expired'))  # Redirect to session_expired page
    
    content = ""
    if request.method == 'POST':
        if 'modified_content' in request.form:
            content = request.form['modified_content']
            brief_type = "Custom"
            domain = "Custom"
        else:
            brief_type = request.form.get('brief_type') or request.form.get('custom_brief_type')
            domain = request.form.get('domain') or request.form.get('custom_domain')
            content = generate_brief(brief_type, domain)
    
    return render_template('index.html', content=content)




@app.route('/session_expired')
def session_expired():
    return render_template('session_expired.html')


# @app.route('/generate', methods=['POST'])
# @login_required
def generate_brief_history(BriefHistory,content):
    # Brief generation logic here
    # ...
    new_history = BriefHistory(
        user_id=current_user.id,
        brief_type=request.form['brief_type'],
        domain=request.form['domain'],
        generated_brief=content
    )
    db.session.add(new_history)
    db.session.commit()
    # return render_template('index.html', content=generated_brief_content)


@app.route('/history', methods=['GET'])
@login_required
def get_history():
    user_id = current_user.id
    history_records = BriefHistory.query.filter_by(user_id=user_id).all()
    history_list = [{
        'type': record.brief_type,
        'domain': record.domain,
        'brief': record.generated_brief,
        'timestamp': record.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for record in history_records]
    return jsonify(history_list)

# Additional routes and application code here

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    
    # Handling the POST request (update profile)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data  # Update username
        current_user.name = form.name.data          # Update name
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('profile'))

    # Handling the GET request (view profile)
    elif request.method == 'GET':
        form.username.data = current_user.username  # Display username
        form.name.data = current_user.name          # Display name
        form.bio.data = current_user.bio
        form.email.data = current_user.email        # Display email, but read-only

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) if current_user.image_file else url_for('static', filename='profile_pics/default.jpg')

    return render_template('profile.html', title='Account', image_file=image_file, form=form, on_profile_page=True)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
