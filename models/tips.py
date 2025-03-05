
from models import db
from marshmallow import ValidationError, fields
from flask_marshmallow import Marshmallow
from controller import app
from datetime import datetime

from models.user import UserSchema
ma = Marshmallow(app)

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