from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import db, Survey, SurveyResponse, survey_schema, survey_response_schema
from models.user import User
from controller import app

@app.route("/create_survey", methods=["POST"])
def create_survey():
    verify_jwt_in_request()
    data = request.json

    if "questions" not in data or len(data["questions"]) != 5:
        return jsonify({"error": "Exactly 5 text-based questions are required"}), 400

    new_survey = Survey(
        title=data.get("title"),
        description=data.get("description"),
        questions=data.get("questions")
    )
    db.session.add(new_survey)
    db.session.commit()

    return jsonify({"message": "Survey created!", "survey": survey_schema.dump([new_survey])[0]}), 201

@app.route("/get_surveys", methods=["GET"])
def get_surveys():
    surveys = Survey.query.all()
    return jsonify(survey_schema.dump(surveys))

@app.route("/get_survey/<int:survey_id>", methods=["GET"])
def get_survey(survey_id):
    survey = Survey.query.get(survey_id)
    if not survey:
        return jsonify({"error": "Survey not found"}), 404

    return jsonify({
        "survey": survey_schema.dump([survey])[0]
    })

@app.route("/submit_survey_response/<int:survey_id>", methods=["POST"])
def submit_survey_response(survey_id):
    verify_jwt_in_request()
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    survey = Survey.query.get(survey_id)
    if not survey:
        return jsonify({"error": "Survey not found"}), 404

    data = request.json
    if "responses" not in data or len(data["responses"]) != 5:
        return jsonify({"error": "Exactly 5 responses are required"}), 400

    new_response = SurveyResponse(
        survey_id=survey.id,
        user_id=user.id,
        responses=data["responses"]  # Dict with 5 text responses
    )
    db.session.add(new_response)
    db.session.commit()

    return jsonify({"message": "Survey response submitted!", "response": survey_response_schema.dump([new_response])[0]}), 201
