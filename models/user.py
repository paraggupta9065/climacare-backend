from models import db
from marshmallow import ValidationError, fields
from flask_marshmallow import Marshmallow
from controller import app
from datetime import datetime
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)  # 'Male' or 'Female'
    location = db.Column(db.String(255), nullable=False)
    health_preferences = db.Column(db.Text, nullable=True)
    daily_routine = db.Column(db.String(10), nullable=False)  # 'Early' or 'Late'
    course_schedule = db.Column(db.String(100), nullable=False)
    accommodation_type = db.Column(db.String(100), nullable=False)
    activity_level = db.Column(db.Float, nullable=False)  # Store slider value

    def __repr__(self):
        return f"<User {self.email}>"

class UserSchema(ma.Schema):
    full_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    age = fields.Integer(required=True)
    gender = fields.String(required=True)
    location = fields.String(required=True)
    health_preferences = fields.String(missing='')
    daily_routine = fields.String(required=True)
    course_schedule = fields.String(required=True)
    accommodation_type = fields.String(required=True)
    activity_level = fields.Float(required=True)

user_schema = UserSchema()


class Tip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    title = db.Column(db.String(255), nullable=False)
    weather_type = db.Column(db.String(50), nullable=False)
    details = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)