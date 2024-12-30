from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os
from groq import Groq

# Load environment variables from .env
load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# Initialize Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=GROQ_API_KEY)

# Resume context (Fine-tuned with structured prompts)
RESUME_CONTEXT = """
My name is Siddharth Gautam. I am a B.Tech graduate in Computer Science & Engineering from NIT Patna.

### Education
- B.Tech in CSE (2021–2025) | NIT Patna | GPA: 8.19
- High School: 96.4% (2019)
- Intermediate: 87.0% (2021)

### Skills
- Programming: C, C++, Python
- Frameworks: ReactJS, NodeJS, Express
- Databases: MySQL
- DevOps: Docker, Kubernetes, CI/CD
- Subjects: Operating Systems, Machine Learning, DBMS, Data Structures
- Soft Skills: Problem Solving, Leadership, Management

### Projects
- **SpamShield**: Email Spam Classifier using Naïve Bayes with TF-IDF vectorization.
- **PawDetect AI**: Image classifier for cats/dogs using CNNs with data augmentation.
- **Pixelkeeper**: React app with Firebase and Tailwind CSS for managing image collections.

### Achievements
- Winner at NITP Hackathon
- Solved 500+ coding problems, LeetCode rating: 1775
- Completed Udemy courses on DSA, Web Development, and Machine Learning

### Leadership
- Core Team Member: HackSlash Club, ML Team, GDSC Club
- President: Dance Club, NITP (2024–Present)
"""

# Route for serving the homepage
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")  # Ensure `index.html` is in the "templates" folder

# Route for serving the resume PDF file
@app.route("/files/resume.pdf", methods=["GET"])
def download_resume():
    try:
        # Serve the resume.pdf from the "files" folder
        return send_from_directory("files", "resume.pdf", as_attachment=True, download_name="Siddharth_Gautam_Resume.pdf")
    except Exception as e:
        print(f"Error serving resume: {e}")
        return jsonify({"error": "File not found."}), 404

# Route for chatbot API
@app.route("/chat", methods=["POST"])
def chat():
    try:
        # Get user input
        user_message = request.json.get("message", "")
        if not user_message:
            return jsonify({"reply": "Please ask a valid question."})

        # Structured prompt to respond as Siddharth Gautam
        prompt = f"""
        You are Siddharth Gautam, a B.Tech graduate in Computer Science & Engineering. You are asked to reply as yourself based on the following resume data:

        {RESUME_CONTEXT}

        User: {user_message}
        Siddharth:
        """

        # Groq chat completion request
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
        )

        # Get the chatbot's reply
        reply = chat_completion.choices[0].message.content.strip()
        return jsonify({"reply": reply})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "An error occurred while processing your request."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
