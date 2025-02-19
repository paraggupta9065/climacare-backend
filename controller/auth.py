from controller import app
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User
from models import db
from marshmallow import ValidationError, fields
from models.user import user_schema

bcrypt = Bcrypt(app)

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already exists'}), 400
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(
        full_name=data['full_name'],
        email=data['email'],
        password=hashed_password,
        age=data['age'],
        gender=data['gender'],
        location=data['location'],
        health_preferences=data.get('health_preferences', ''),
        daily_routine=data['daily_routine'],
        course_schedule=data['course_schedule'],
        accommodation_type=data['accommodation_type'],
        activity_level=data['activity_level']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not bcrypt.check_password_hash(user.password, data.get('password')):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.email)
    return jsonify({'data': {"access_token":access_token}}), 200


@app.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    user_data = {
        'full_name': user.full_name,
        'email': user.email,
        'age': user.age,
        'gender': user.gender,
        'location': user.location,
        'health_preferences': user.health_preferences,
        'daily_routine': user.daily_routine,
        'course_schedule': user.course_schedule,
        'accommodation_type': user.accommodation_type,
        'activity_level': user.activity_level
    }
    return jsonify({'data': {"user":user_data}}), 200