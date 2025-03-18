from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from google import genai
import datetime
from controller import app
import requests

from models.tips import Tip
from models.user import User


@app.route("/gen_ai", methods=["POST"])
def gen_ai():
    verify_jwt_in_request()
    current_user_email = get_jwt_identity()

    data = request.get_json()
    user_message = data.get("message", "Hello Ai")
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    tips = Tip.query.filter_by(user_id=user.id).all()
    current_time = datetime.datetime.now()

    weather_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 23.077675,
        "longitude": 76.850713,
        "daily": "sunrise,sunset,daylight_duration,sunshine_duration,uv_index_max,uv_index_clear_sky_max",
        "timezone": "auto",
    }

    try:
        weather_response = requests.get(weather_url, params=params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
    except requests.exceptions.RequestException as e:
        return (
            jsonify({"error": "Failed to fetch weather data", "details": str(e)}),
            500,
        )

    context = {
        "weather_context": weather_data,
        "current_time": current_time,
        "location": "Vit Bhopal",
        "surrounding_info": {
            "campus": {
                "name": "VIT Bhopal University",
                "location": {
                    "address": "Bhopal-Indore Highway, Kothrikalan, Sehore, Bhopal - 466114, Madhya Pradesh, India",
                    "latitude": 23.0258,
                    "longitude": 77.4280,
                },
                "area_acres": 300,
                "features": {
                    "playgrounds": 2,
                    "ponds": 1,
                    "academic_blocks": 1,
                    "laboratory_complexes": 1,
                    "hostel_blocks": {"boys": 3, "girls": 1},
                    "under_construction": {
                        "academic_block_2": true,
                        "additional_hostel_blocks": true,
                    },
                },
            },
            "academic_buildings": [
                {
                    "name": "Academic Block 1",
                    "status": "operational",
                    "area_sqm": 31180,
                },
                {
                    "name": "Academic Block 2",
                    "status": "operational",
                },
                {
                    "name": "Laboratory Complex",
                    "status": "operational",
                    "area_sqm": 7875.7,
                    "features": ["advanced_laboratories"],
                },
                {"name": "Architecture Block", "status": "operational"},
            ],
        },
        "purpose": "Provide a concise 3-4 line response to the user's health-related question, incorporating their preferences and activity level while avoiding complex language.",
        "user_id": user.id,
        "user_info": {
            "name": user.full_name,
            "email": user.email,
            "age": user.age,
            "gender": user.gender,
            "location": user.location,
            "health_preferences": user.health_preferences,
            "daily_routine": user.daily_routine,
            "course_schedule": user.course_schedule,
            "accommodation_type": user.accommodation_type,
            "activity_level": user.activity_level,
        },
        "tips": [
            {
                "id": tip.id,
                "title": tip.title,
                "weather_type": tip.weather_type,
                "details": tip.details,
                "created_at": tip.created_at.isoformat(),
                "upvotes": tip.upvotes,
                "downvotes": tip.downvotes,
            }
            for tip in tips
        ],
    }

    client = genai.Client(api_key="AIzaSyCOmnmipcIJgaMes7dNp92j2lOR1mr-usc")

    input_contents = [user_message, str(context)]
    print(input_contents)

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=input_contents
    )

    return jsonify({"message": response.text})
