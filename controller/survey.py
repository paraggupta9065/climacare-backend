from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.survey import db, Survey, SurveyResponse, survey_schema, survey_response_schema
from models.user import User
from controller import app

@app.route("/create_survey", methods=["POST"])
def create_survey():
    verify_jwt_in_request()
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    data = request.json
    

    if "questions" not in data or len(data["questions"]) != 5:
        return jsonify({"error": "Exactly 5 text-based questions are required"}), 400

    new_survey = SurveyResponse(
        user_id=user.id,
        responses=data.get("responses"),
    )
    db.session.add(new_survey)
    db.session.commit()

    return jsonify({"message": "Survey filled!", "survey": survey_schema.dump([new_survey])[0]}), 201
