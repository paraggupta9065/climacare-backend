from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.user import User, db, Survey, SurveyResponse, survey_schema, survey_response_schema
from controller import app

@app.route("/create_survey", methods=["POST"])
def create_survey():
    verify_jwt_in_request()
    data = request.json

    new_survey = Survey(
        title=data.get("title"),
        description=data.get("description")
    )
    db.session.add(new_survey)
    db.session.commit()

    return jsonify({"message": "Survey created successfully!"}), 201

@app.route("/get_surveys", methods=["GET"])
def get_surveys():
    surveys = Survey.query.all()
    return survey_schema.jsonify(surveys)

@app.route("/get_survey/<int:survey_id>", methods=["GET"])
def get_survey(survey_id):
    survey = Survey.query.get(survey_id)
    if not survey:
        return jsonify({"error": "Survey not found"}), 404

    responses = SurveyResponse.query.filter_by(survey_id=survey_id).all()
    return jsonify({
        "survey": {
            "id": survey.id,
            "title": survey.title,
            "description": survey.description,
            "created_at": survey.created_at.isoformat()
        },
        "responses": survey_response_schema.dump(responses)
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

    new_response = SurveyResponse(
        survey_id=survey.id,
        user_id=user.id,
        response_data=data.get("response_data")
    )
    db.session.add(new_response)
    db.session.commit()

    return jsonify({"message": "Survey response submitted successfully!"}), 201
