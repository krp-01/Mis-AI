from flask import Flask, request, jsonify
from flask_cors import CORS
from response_engine import generate_local_response
from ai_connector import generate_ai_response
from profile_manager import (
    save_profile,
    load_profile,
    user_exists,
    save_history,
    load_history
)

app = Flask(__name__)
CORS(app)


@app.route("/signup", methods=["POST"])
def signup():
    data = request.json

    username = data.get("username", "").strip().lower()
    display_name = data.get("display_name", "").strip()
    password = data.get("password", "").strip()

    if not username:
        return jsonify({"error": "Username lipsa"}), 400

    if not display_name:
        return jsonify({"error": "Nume afisat lipsa"}), 400

    if not password:
        return jsonify({"error": "Parola lipsa"}), 400

    if user_exists(username):
        return jsonify({"error": "User exista deja"}), 400

    profile = {
        "username": username,
        "display_name": display_name,
        "password": password,
        "risc": data.get("risc", "prudent"),
        "social": data.get("social", "rezervat"),
        "organizare": data.get("organizare", "organizat"),
        "emotie": data.get("emotie", "rational"),
        "rabdare": data.get("rabdare", "rabdator"),
        "adaptare": data.get("adaptare", "flexibil"),
        "disciplina": data.get("disciplina", "disciplinat"),
        "incredere": data.get("incredere", "increzator"),
        "avatar": data.get("avatar", "")
    }

    save_profile(username, profile)
    save_history(username, [])

    return jsonify({"message": "Cont creat cu succes"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username", "").strip().lower()
    password = data.get("password", "").strip()

    if not username:
        return jsonify({"error": "Username lipsa"}), 400

    if not password:
        return jsonify({"error": "Parola lipsa"}), 400

    profile = load_profile(username)

    if profile is None:
        return jsonify({"error": "User inexistent"}), 400

    if profile.get("password") != password:
        return jsonify({"error": "Parola gresita"}), 400

    history = load_history(username)

    return jsonify({
        "profile": profile,
        "history": history
    })


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json

    message = data.get("message", "").strip()
    profile = data.get("profile", {})
    mode = data.get("mode", "ai")

    if not message:
        return jsonify({"error": "Mesaj gol"}), 400

    username = profile.get("username", "").strip().lower()
    if not username:
        return jsonify({"error": "Username lipsa din profil"}), 400

    saved_profile = load_profile(username)
    if saved_profile is None:
        return jsonify({"error": "Utilizatorul nu exista"}), 400

    if mode == "ai":
        try:
            response = generate_ai_response(
                message,
                saved_profile,
                saved_profile.get("display_name", ""),
                saved_profile.get("username", "")
            )
        except Exception:
            response = generate_local_response(message, saved_profile)
    else:
        response = generate_local_response(message, saved_profile)

    history = load_history(username)
    history.append({"speaker": "Tu", "message": message})
    history.append({"speaker": "MIS", "message": response})
    save_history(username, history)

    return jsonify({"response": response})


@app.route("/history", methods=["POST"])
def history():
    data = request.json
    username = data.get("username", "").strip().lower()

    if not username:
        return jsonify({"error": "Username lipsa"}), 400

    if not user_exists(username):
        return jsonify({"error": "User inexistent"}), 400

    history_data = load_history(username)
    return jsonify({"history": history_data})


if __name__ == "__main__":
    app.run(debug=True)
