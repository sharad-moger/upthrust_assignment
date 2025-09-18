from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests

app = Flask(__name__, static_folder="public", template_folder="public")
CORS(app, resources={r"/*": {"origins": "*"}})

history = []

# Serve index.html
@app.route("/")
def home():
    return send_from_directory("public", "index.html")

# Serve CSS
@app.route("/style.css")
def style():
    return send_from_directory("public", "style.css")

# Serve JS
@app.route("/script.js")
def script():
    return send_from_directory("public", "script.js")

# Run workflow
@app.route("/run-workflow", methods=["POST"])
def run_workflow():
    data = request.get_json()
    prompt = data.get("prompt", "No prompt")
    action = data.get("action", "none")

    # Mock AI response (short text)
    ai_response = f"{prompt} 🤖"

    # API response
    api_response = ""
    if action == "weather":
        city = "Delhi"
        api_response = f"Sunny in {city}, 32°C"  # Mock weather
    elif action == "news":
        api_response = "Breaking news headline here"  # Mock news
    elif action == "github":
        api_response = "Trending Repo: awesome-repo ⭐100k"  # Mock GitHub
    else:
        api_response = "No API selected."

    final_result = f"{ai_response} | {api_response} #{action}"

    # Store in history
    history.insert(0, {"prompt": prompt, "action": action, "ai_response": ai_response,
                        "api_response": api_response, "final_result": final_result})
    if len(history) > 10:
        history.pop()

    return jsonify({
        "ai_response": ai_response,
        "api_response": api_response,
        "final_result": final_result
    })

# Fetch history
@app.route("/history", methods=["GET"])
def get_history():
    return jsonify(history)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
