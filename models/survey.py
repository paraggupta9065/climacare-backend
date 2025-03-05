from models import db
from marshmallow import ValidationError, fields
from flask_marshmallow import Marshmallow
from controller import app
from datetime import datetime
ma = Marshmallow(app)


class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    responses = db.Column(db.JSON, nullable=False)
    submitted_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class SurveyResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SurveyResponse
        load_instance = True

survey_response_schema = SurveyResponseSchema(many=True)

