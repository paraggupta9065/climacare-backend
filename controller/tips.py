from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity, create_access_token
from datetime import datetime
from models import db, User, Tip
from controller import app


@app.route("/add_tip", methods=["POST"])
def add_tip():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    data = request.json
    
    new_tip = Tip(
        user_id=user_id,
        title=data.get("title"),
        weather_type=data.get("weather_type"),
        details=data.get("details")
    )
    db.session.add(new_tip)
    db.session.commit()
    
    return jsonify({"msg": "Tip added successfully!"}), 201

@app.route("/get_tips", methods=["GET"])
def get_tips():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    tips = Tip.query.filter_by(user_id=user_id).all()
    tips_list = [{
        "title": tip.title,
        "weather_type": tip.weather_type,
        "details": tip.details,
        "created_at": tip.created_at.isoformat()
    } for tip in tips]
    return jsonify(tips_list)
