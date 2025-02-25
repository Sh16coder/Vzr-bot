from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# OpenAI API key (store in Render's environment variables)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Doubt-clearing bot is running!"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_question = data.get("question")

        if not user_question:
            return jsonify({"error": "No question provided"}), 400

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_question}]
        )

        bot_reply = response["choices"][0]["message"]["content"]
        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Render allows custom ports
