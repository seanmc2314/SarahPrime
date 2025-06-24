from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from dotenv import load_dotenv
import os
import ast
import subprocess
from guardian import Guardian
from code_generator import CodeGenerator

app = Flask(__name__)
CORS(app)

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize components
conversations = []
guardian = Guardian()
code_generator = CodeGenerator()

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    conversations.append({"role": "user", "content": user_message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversations
        )
        ai_message = response.choices[0].message.content
        conversations.append({"role": "assistant", "content": ai_message})
        return jsonify({"message": ai_message})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/propose_feature", methods=["POST"])
def propose_feature():
    data = request.json
    feature_description = data.get("feature")
    if not feature_description:
        return jsonify({"error": "No feature description provided"}), 400

    # Generate code for the feature
    try:
        code, filename = code_generator.generate_feature_code(feature_description)
        change_id = guardian.log_proposed_change(feature_description, code, filename)
        return jsonify({
            "status": "Feature proposed",
            "feature": feature_description,
            "change_id": change_id,
            "message": "Awaiting your approval to implement this feature."
        })
    except Exception as e:
        return jsonify({"error": f"Code generation failed: {str(e)}"}), 500

@app.route("/api/approve_feature", methods=["POST"])
def approve_feature():
    data = request.json
    change_id = data.get("change_id")
    if not change_id:
        return jsonify({"error": "No change ID provided"}), 400

    # Validate and apply the change
    try:
        if guardian.validate_change(change_id):
            code_generator.apply_change(change_id)
            guardian.log_applied_change(change_id)
            return jsonify({
                "status": "Feature approved",
                "change_id": change_id,
                "message": "Feature implemented successfully."
            })
        else:
            return jsonify({"error": "Change validation failed"}), 400
    except Exception as e:
        return jsonify({"error": f"Feature implementation failed: {str(e)}"}), 500

@app.route("/api/build_program", methods=["POST"])
def build_program():
    data = request.json
    program_description = data.get("program")
    if not program_description:
        return jsonify({"error": "No program description provided"}), 400

    # Generate and build a new program
    try:
        program_code, program_name = code_generator.generate_program_code(program_description)
        change_id = guardian.log_proposed_change(program_description, program_code, f"programs/{program_name}.py")
        return jsonify({
            "status": "Program proposed",
            "program": program_description,
            "change_id": change_id,
            "message": "Awaiting your approval to build and roll out this program."
        })
    except Exception as e:
        return jsonify({"error": f"Program generation failed: {str(e)}"}), 500

if __name__ == "__main__":
    os.makedirs("changes/pending", exist_ok=True)
    os.makedirs("changes/applied", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("programs", exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
