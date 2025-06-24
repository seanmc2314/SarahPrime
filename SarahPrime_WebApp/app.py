from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("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")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Sarah, a helpful and evolving assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)

