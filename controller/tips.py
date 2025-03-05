from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity, create_access_token
from datetime import datetime
from models import db
from models.tips import Tip, tips_schema
from controller import app
from models.user import User


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

@app.route("/tip/<int:tip_id>/upvote", methods=["POST"])
def upvote_tip(tip_id):
    tip = Tip.query.get(tip_id)
    if not tip:
        return jsonify({"error": "Tip not found"}), 404

    tip.upvotes += 1
    db.session.commit()

    return jsonify({"message": "Upvoted successfully", "upvotes": tip.upvotes, "downvotes": tip.downvotes})


@app.route("/tip/<int:tip_id>/downvote", methods=["POST"])
def downvote_tip(tip_id):
    tip = Tip.query.get(tip_id)
    if not tip:
        return jsonify({"error": "Tip not found"}), 404

    tip.downvotes += 1
    db.session.commit()

    return jsonify({"message": "Downvoted successfully", "upvotes": tip.upvotes, "downvotes": tip.downvotes})