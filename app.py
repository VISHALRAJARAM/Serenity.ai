from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai
import traceback

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Use a supported model name
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

app = Flask(__name__)

COUNT_FILE = "count.txt"

def read_count():
    """Reads the count from the file."""
    if not os.path.exists(COUNT_FILE):
        with open(COUNT_FILE, "w") as f:
            f.write("0")
    with open(COUNT_FILE, "r") as f:
        return int(f.read())

def write_count(count):
    """Writes the updated count to the file."""
    with open(COUNT_FILE, "w") as f:
        f.write(str(count))

@app.route("/")
def home():
    count = read_count()
    count += 1
    write_count(count)
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_response():
    user_input = request.json.get("message", "")
    try:
        prompt = f"""
You are a compassionate and emotionally intelligent mental wellness counselor who speaks gently and supportively.

When a user shares something personal or painful:
- First, validate and acknowledge their emotions in a warm, understanding tone.
- Then ask an open-ended question to gently guide them toward reflecting more.
- Don’t give a full solution or long answer up front. Focus on listening and understanding first.
- Only after a few back-and-forths should you start suggesting gentle practices (like breathing exercises, journaling, mindfulness, etc.)
- Your tone should always be warm, soft, non-judgmental, and human — like a close, caring therapist.

Begin responding to this message from the user:
\"{user_input}\"
"""
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        print("⚠️ Gemini Error:", e)
        traceback.print_exc()
        return jsonify({"response": "I'm here for you, even if something went wrong 🌻 Let’s take a deep breath together."})

@app.route("/increment", methods=["POST"])
def increment_count():
    count = read_count()
    count += 1
    write_count(count)
    return jsonify({"count": count})

@app.route("/get-count", methods=["GET"])
def get_count():
    count = read_count()
    return jsonify({"count": count})

if __name__ == "__main__":
    app.run(debug=True)