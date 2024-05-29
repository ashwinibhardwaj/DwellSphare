from flask import Flask,flash,jsonify, render_template, redirect, url_for, request, session, flash, send_from_directory, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, current_user
import secrets
from datetime import timedelta
from flask import render_template, request
from sqlalchemy import and_
from twilio.rest import Client
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_mail import Mail, Message
import mysql.connector
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ash96808@localhost/dwellsphare'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = '/uploads'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(50), nullable=False)
    room_size = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.String(50), nullable=False)
    rent = db.Column(db.String(50), nullable=False)
    facilities = db.Column(db.String(50), nullable=False)
    security_fee = db.Column(db.String(50), nullable=False)
    water_fee = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    image_path = db.Column(db.String(255), nullable=True)
    user = db.Column(db.String(255), nullable=False)
    ph_no = db.Column(db.String(20), nullable=False)

# Folder to store uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create 'uploads' directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    address = db.Column(db.String(255))
    ph_no = db.Column(db.INTEGER)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_name = db.Column(db.String(255), nullable=False)
    user_message = db.Column(db.Text, nullable=False)



# MySQL connector setup
db_connector = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ash96808",
    database="dwellsphare"
)

cursor = db_connector.cursor()

# Twilio credentials
account_sid = 'AC4a72ac87bcdca9eaa81a34907965ba0b'
auth_token = '121c86cbb1ffa30517aef34b9cdc1434'
twilio_phone_number = '+19283251086'

client = Client(account_sid, auth_token)


@app.route('/')
def index():
    current_users_count = count_users()
    current_properties_count = count_rooms()
    return render_template('index.html', current_users_count=current_users_count, current_properties_count=current_properties_count)



def count_users():
    return User.query.count()

def count_rooms():
    return Room.query.count()




app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'ashwini.10521@gmail.com'
app.config['MAIL_PASSWORD'] = 'Ash26707'
app.config['MAIL_DEFAULT_SENDER'] = 'ashwini.10521@gmail.com'

mail = Mail(app)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    
    return render_template('contact.html')


@app.route('/allProperty')
def allProperty():
    sql = "SELECT * FROM room"
    cursor.execute(sql)
    columns = [column[0] for column in cursor.description]
    results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    room_ids = get_ids_based_on_context(results)
    session['room_ids'] = room_ids
    session['search_results'] = results

    return render_template('searchresults.html', results=results, room_ids=room_ids)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_address = request.form['search_address']
        min_capacity = int(request.form['min_capacity'])
        max_rent = int(request.form['max_rent'])

        sql = "SELECT * FROM room WHERE address LIKE %s AND capacity >= %s AND rent <= %s"
        values = ('%' + search_address + '%', min_capacity, max_rent)
        
        cursor.execute(sql, values)
        columns = [column[0] for column in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

        room_ids = get_ids_based_on_context(results)
        session['room_ids'] = room_ids
        session['search_results'] = results

        return render_template('searchresults.html', results=results, room_ids=room_ids)

account_sid = 'AC4a72ac87bcdca9eaa81a34907965ba0b'
auth_token = '121c86cbb1ffa30517aef34b9cdc1434'
twilio_phone_number = '+19283251086'
my_phone_number = '+919680826707'

client = Client(account_sid, auth_token)  

@app.route('/send_message/<int:room_id>', methods=['POST'])
def send_message(room_id):
    try:
        room = Room.query.get(room_id)

        if room:
            message = client.messages.create(
                body="Hello from ashwini",
                from_=twilio_phone_number,
                to=room.ph_no  # Assuming there is a 'phone_number' field in the Room model
            )

            return jsonify({"message": "Message sent successfully", "sid": message.sid})
        else:
            return jsonify({"error": "Room not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/preview/<int:room_id>')
def preview(room_id):
    # Fetch the room details
    room = Room.query.get(room_id)

    # Fetch ratings for the specified room from the database
    ratings = Review.query.filter_by(room_id=room_id).all()

    # Calculate average rating and star counts
    total_reviews = len(ratings)
    average_rating = 0.0  # Default value if there are no reviews

    if total_reviews > 0:
        average_rating = round(sum([rating.rating for rating in ratings]) / total_reviews, 1)

    star_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for rating in ratings:
        star_counts[rating.rating] += 1

    # Calculate other rating statistics
    total_reviews_percentage = total_reviews * 20

    # Calculate percentages only if total_reviews is not zero
    if total_reviews > 0:
        rating_data = {
            'average_rating': average_rating,
            'total_reviews': total_reviews,
            'five_star_reviews': star_counts[5],
            'four_star_reviews': star_counts[4],
            'three_star_reviews': star_counts[3],
            'two_star_reviews': star_counts[2],
            'one_star_reviews': star_counts[1],
            'five_star_percentage': (star_counts[5] / total_reviews) * total_reviews_percentage,
            'four_star_percentage': (star_counts[4] / total_reviews) * total_reviews_percentage,
            'three_star_percentage': (star_counts[3] / total_reviews) * total_reviews_percentage,
            'two_star_percentage': (star_counts[2] / total_reviews) * total_reviews_percentage,
            'one_star_percentage': (star_counts[1] / total_reviews) * total_reviews_percentage,
            'reviews': [{'name': rating.user_name, 'message': rating.user_message} for rating in ratings]
        }
    else:
        # Set percentages to zero or any default value
        rating_data = {
            'average_rating': average_rating,
            'total_reviews': total_reviews,
            'five_star_reviews': 0,
            'four_star_reviews': 0,
            'three_star_reviews': 0,
            'two_star_reviews': 0,
            'one_star_reviews': 0,
            'five_star_percentage': 0,
            'four_star_percentage': 0,
            'three_star_percentage': 0,
            'two_star_percentage': 0,
            'one_star_percentage': 0,
            'reviews': []
        }

    # Render the preview HTML page with room details and rating data
    return render_template('preview.html', room=room, rating_data=rating_data, room_id=room_id)


def get_ids_based_on_context(results):
    
    if results:
        return [room.get('id') for room in results]
    else:
        return []


@app.route('/submit_review/<int:room_id>', methods=['POST'])
def submit_review(room_id):
    # Check if the room_id exists in the room table
    room = Room.query.get(room_id)
    if room is None:
        abort(400, "Invalid room_id. Room not found.")

    rating = request.form.get('rating')
    user_name = request.form.get('userName')
    user_message = request.form.get('userMessage')

    # Get the id value from the Room model
    room_id_from_db = room.id

    # Assign the room_id_from_db value to the hostel_id column in the Review model
    new_review = Review(room_id=room_id_from_db, rating=rating, user_name=user_name, user_message=user_message)
    db.session.add(new_review)
    db.session.commit()

    # Return a JSON response indicating success
    return jsonify({"success": True, "message": "Review submitted successfully!"})

@app.route('/get_ratings/<int:room_id>', methods=['GET'])
def get_ratings(room_id):
    # Fetch ratings for the specified room from the database
    ratings = Review.query.filter_by(room_id=room_id).all()

    # Calculate average rating
    total_reviews = len(ratings)
    average_rating = 0.0  # Default value if there are no reviews
    if total_reviews > 0:
        average_rating = sum([rating.rating for rating in ratings]) / total_reviews

    # Calculate the number of reviews for each star level
    five_star_reviews = len([rating for rating in ratings if rating.rating == 5])
    four_star_reviews = len([rating for rating in ratings if rating.rating == 4])
    three_star_reviews = len([rating for rating in ratings if rating.rating == 3])
    two_star_reviews = len([rating for rating in ratings if rating.rating == 2])
    one_star_reviews = len([rating for rating in ratings if rating.rating == 1])

    # Calculate the percentage of each star level
    total_reviews_percentage = total_reviews * 20  # Each star represents 20%

    # Calculate percentages only if total_reviews is not zero
    if total_reviews > 0:
        response = {
            'average_rating': average_rating,
            'total_reviews': total_reviews,
            'five_star_reviews': five_star_reviews,
            'four_star_reviews': four_star_reviews,
            'three_star_reviews': three_star_reviews,
            'two_star_reviews': two_star_reviews,
            'one_star_reviews': one_star_reviews,
            'five_star_percentage': (five_star_reviews / total_reviews) * total_reviews_percentage,
            'four_star_percentage': (four_star_reviews / total_reviews) * total_reviews_percentage,
            'three_star_percentage': (three_star_reviews / total_reviews) * total_reviews_percentage,
            'two_star_percentage': (two_star_reviews / total_reviews) * total_reviews_percentage,
            'one_star_percentage': (one_star_reviews / total_reviews) * total_reviews_percentage,
            'reviews': [{'name': rating.user_name, 'message': rating.user_message} for rating in ratings]
        }
    else:
        # Set percentages to zero or any default value
        response = {
            'average_rating': average_rating,
            'total_reviews': total_reviews,
            'five_star_reviews': five_star_reviews,
            'four_star_reviews': four_star_reviews,
            'three_star_reviews': three_star_reviews,
            'two_star_reviews': two_star_reviews,
            'one_star_reviews': one_star_reviews,
            'five_star_percentage': 0,
            'four_star_percentage': 0,
            'three_star_percentage': 0,
            'two_star_percentage': 0,
            'one_star_percentage': 0,
            'reviews': []
        }

    return jsonify(response)


       
    
@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        existing_user_query = "SELECT * FROM user WHERE username = %s"
        cursor.execute(existing_user_query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username already exists. Please choose a different one.', category='error')
        else:
            new_user_query = "INSERT INTO user (username, password) VALUES (%s, %s)"
            cursor.execute(new_user_query, (username, hashed_password))
            db_connector.commit()

            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)

            # Set the username in the session
            session['username'] = user.username

            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Please check your username and password.', 'error')

    return render_template('login.html', error_message='Login failed. Please check your username and password.')


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        # User is not logged in, redirect to login page
        return redirect(url_for('login'))

    # User is logged in, show the dashboard
    username = session['username']

    # Retrieve entries for the logged-in user
    entries = Room.query.filter_by(user=username).with_entities(Room.room_type, Room.room_size, Room.capacity, Room.rent, Room.security_fee, Room.water_fee).all()
    print(entries)

    return render_template('dashboard.html', username=username, entries=entries)
    
@app.route('/profile')
def profile():
    if 'username' in session:
        username = session['username']
        user = UserProfile.query.filter_by(username=username).first()
        if user:
            return render_template('profile.html',
                                   username=user.username,
                                   full_name=user.full_name,
                                   email=user.email,
                                   address=user.address,
                                   ph_no=user.ph_no)
        else:
            flash('User not found', 'error')
            return redirect(url_for('dashboard'))
    else:
        flash('You need to log in first', 'error')
        return redirect(url_for('login'))




# Folder to store uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create 'uploads' directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/addform')
def addform():
    return render_template('addform.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        # Check if the user is logged in
        if 'username' not in session:
            flash('You need to log in first', 'error')
            return redirect(url_for('login'))

        room_type = request.form['roomType']
        room_size = request.form['roomSize']
        capacity = request.form['capacity']
        rent = request.form['rent']
        facilities = request.form['facilities']
        security_fee = request.form['securityFee']
        water_fee = request.form['waterFee']
        address = request.form['address']
        user = session['username']
        # country_code = request.form['countryCode']
        # phone_number = request.form['phoneNumber']
        # combined_number = country_code + phone_number
        ph_no = request.form['phoneNumber']
        message = "Property added successfully"

        # Handle file upload
        if 'image' in request.files:
            image = request.files['image']
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                image_path = os.path.join('static', app.config['UPLOAD_FOLDER'], filename).replace('\\', '/')
                image.save(image_path)
            else:
                image_path = None

            # Insert form data and image path into the MySQL database using SQLAlchemy
            new_room = Room(
                room_type=room_type,
                room_size=room_size,
                capacity=capacity,
                rent=rent,
                facilities=facilities,
                security_fee=security_fee,
                water_fee=water_fee,
                address=address,
                image_path=image_path,
                user=user,
                ph_no = ph_no
            )
            db.session.add(new_room)
            db.session.commit()



        return render_template('submission_result.html', message=message)
    except Exception as e:
        db.session.rollback()
        error_message = f"Error: {str(e)}"
        return render_template('submission_result.html', message=error_message)
    

def get_user_profile():
    username = session['username']
    user_profile = UserProfile.query.filter_by(username=username).first()
    return user_profile

@app.route('/profile')
def profile_info():
    user_profile = get_user_profile()
    print(user_profile)

    if user_profile:
        # Check if the user has filled the profile
        profile_filled = all([user_profile.full_name, user_profile.email, user_profile.address])

        return render_template('profile.html', full_name=user_profile.full_name, email=user_profile.email, address=user_profile.address, profile_filled=profile_filled)

    else:
        flash('Session time out. You need to log in first', 'error')
        return redirect(url_for('login'))
    
@app.route('/check_profile')
def check_profile():
    if 'username' in session:
        username = session['username']
        user_profile = UserProfile.query.filter_by(username=username).first()

        if user_profile:
            # Check if the user has filled the profile
            profile_exists = True
        else:
            profile_exists = False

        return jsonify({'exists': profile_exists})
    else:
        return jsonify({'error': 'User not logged in'}), 401 
    

@app.route('/fill_profile', methods=['GET', 'POST'])
def fill_profile():
    if request.method == 'POST':
        # Get data from the filled form
        full_name = request.form['full_name']
        email = request.form['email']
        address = request.form['address']

        # Check if 'username' is present in the session
        if 'username' in session:
            user = session['username']

            try:
                # Save the data to the database
                new_profile = UserProfile(username=user, full_name=full_name, email=email, address=address)
                db.session.add(new_profile)
                db.session.commit()

                flash('Profile filled successfully!', 'success')  # Flash success message

                return redirect(url_for('profile'))

            except IntegrityError as e:
                db.session.rollback()  # Rollback the transaction
                flash('Profile already filled.', 'error')  # Flash error message

                # If the profile exists, redirect to the profile page
                existing_profile = UserProfile.query.filter_by(username=user).first()
                if existing_profile:
                    return redirect(url_for('profile'))

        else:
            return redirect(url_for('login'))  # Redirect to the login page

    return render_template('fill_profile.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
