from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity, create_access_token
from datetime import datetime
from models import db
from models.user import Tip, User, tips_schema
from controller import app


@app.route("/add_tip", methods=["POST"])
def add_tip():
    verify_jwt_in_request()
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    data = request.json

    new_tip = Tip(
        user_id=user.id,
        title=data.get("title"),
        weather_type=data.get("weather_type"),
        details=data.get("details")
    )
    db.session.add(new_tip)
    db.session.commit()
    
    return jsonify({"msg": "Tip added successfully!"}), 201

@app.route("/get_tips", methods=["GET"])
def get_tips():
    tips = Tip.query.all()
    return tips_schema.jsonify(tips)  # Use Marshmallow to serialize


