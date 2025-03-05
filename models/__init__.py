from datetime import datetime
from controller import app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'


db = SQLAlchemy(app)

from models.user import User, user_schema
from models.tips import Tip, tip_schema

from models.survey import SurveyResponse, survey_response_schema

