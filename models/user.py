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
    tips = db.relationship('Tip', backref='user', lazy=True)

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
    upvotes = db.Column(db.Integer, default=0, nullable=False)
    downvotes = db.Column(db.Integer, default=0, nullable=False)
    
class TipSchema(ma.SQLAlchemyAutoSchema):
    user = fields.Nested(UserSchema) 
    
    class Meta:
        model = Tip
        include_fk = True 
        load_instance = True

tip_schema = TipSchema()
tips_schema = TipSchema(many=True)

class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    questions = db.Column(db.JSON, nullable=False)  # JSON: List of 5 text-based questions
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    responses = db.Column(db.JSON, nullable=False)  # JSON: Dict with question index & answer
    submitted_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class SurveySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Survey
        load_instance = True

class SurveyResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SurveyResponse
        load_instance = True

survey_schema = SurveySchema(many=True)
survey_response_schema = SurveyResponseSchema(many=True)

