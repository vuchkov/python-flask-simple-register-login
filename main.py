from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from threading import Thread
import re
import time

app = Flask(__name__)

# Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Initialize the database
#@app.before_first_request
@app.before_request
def create_tables():
    db.create_all() # Check if the DB is not overwrite on each first request?

# Helper function: input validation
def validate_input(username, password):
    if not username or not password:
        return False, "Username and password are required"
    if len(password) < 8 or not re.search(r"\d", password):  # Basic password validation
        return False, "Password must be at least 8 characters long and include a number"
    # Please check if the user already exists (username) in the BD?
    return True, None

# Register endpoint
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    is_valid, error = validate_input(username, password)
    if not is_valid:
        return jsonify({"error": error}), 400

    hashed_password = generate_password_hash(password)  # Hash the password for security
    user = User(username=username, password=hashed_password)

    # Use a thread to handle database insertion in the background
    def add_user_to_db(user):
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            app.logger.error(f"Failed to insert user: {e}")

    thread = Thread(target=add_user_to_db, args=(user,))
    thread.start()

    # Simulate delay to demonstrate concurrency
    time.sleep(1)

    return jsonify({"message": "User registered successfully"}), 201 # It is better to use 200 as a code!

# Login endpoint
@app.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": "Login successful"}), 200

# Security middleware
@app.after_request
def set_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    response.headers['X-Content-Type-Options'] = "nosniff"
    response.headers['X-Frame-Options'] = "DENY"
    response.headers['X-XSS-Protection'] = "1; mode=block"
    return response

if __name__ == '__main__':
    app.run(debug=True)

