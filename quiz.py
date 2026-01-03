from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

questions = [
    # General Knowledge
    {
        "category": "General Knowledge",
        "question": "What is the capital of France?",
        "options": ["Paris", "London", "Berlin", "Madrid"],
        "answer": "Paris"
    },
    {
        "category": "General Knowledge",
        "question": "Which country hosted the 2020 Summer Olympics?",
        "options": ["China", "Japan", "USA", "Brazil"],
        "answer": "Japan"
    },
    {
        "category": "General Knowledge",
        "question": "Who invented the telephone?",
        "options": ["Thomas Edison", "Alexander Graham Bell", "Newton", "Einstein"],
        "answer": "Alexander Graham Bell"
    },
    {
        "category": "General Knowledge",
        "question": "What is the capital of Australia?",
        "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"],
        "answer": "Canberra"
    },
    {
        "category": "General Knowledge",
        "question": "Which Indian state is known as the 'Spice Garden of India'?",
        "options": ["Kerala", "Assam", "Goa", "Tamil Nadu"],
        "answer": "Kerala"
    },

    # Math
    {
        "category": "Math",
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "22"],
        "answer": "4"
    },
    {
        "category": "Math",
        "question": "What is 7 × 8?",
        "options": ["56", "54", "64", "58"],
        "answer": "56"
    },
    {
        "category": "Math",
        "question": "What is the next prime number after 7?",
        "options": ["9", "11", "13", "17"],
        "answer": "11"
    },
    {
        "category": "Math",
        "question": "What is the value of 3² + 4²?",
        "options": ["25", "7", "12", "5"],
        "answer": "25"
    },
    {
        "category": "Math",
        "question": "What is the cube of 2?",
        "options": ["4", "6", "8", "12"],
        "answer": "8"
    },

    # Science
    {
        "category": "Science",
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Saturn"],
        "answer": "Mars"
    },
    {
        "category": "Science",
        "question": "What gas do humans exhale?",
        "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Helium"],
        "answer": "Carbon Dioxide"
    },
    {
        "category": "Science",
        "question": "Which organ purifies our blood?",
        "options": ["Heart", "Lungs", "Kidney", "Liver"],
        "answer": "Kidney"
    },
    {
        "category": "Science",
        "question": "The hardest substance in the human body is?",
        "options": ["Bone", "Skull", "Tooth enamel", "Cartilage"],
        "answer": "Tooth enamel"
    },
    {
        "category": "Science",
        "question": "Which vitamin is provided by sunlight?",
        "options": ["Vitamin A", "Vitamin B", "Vitamin C", "Vitamin D"],
        "answer": "Vitamin D"
    },
    {
        "category": "Science",
        "question": "What is the chemical symbol for water?",
        "options": ["O2", "H2O", "CO2", "NaCl"],
        "answer": "H2O"
    },

    # English
    {
        "category": "English",
        "question": "Who wrote 'Romeo and Juliet'?",
        "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
        "answer": "William Shakespeare"
    },
    {
        "category": "English",
        "question": "Identify the adjective: 'She wore a beautiful dress.'",
        "options": ["She", "Wore", "Beautiful", "Dress"],
        "answer": "Beautiful"
    },
    {
        "category": "English",
        "question": "Choose the correct spelling:",
        "options": ["Recieve", "Receive", "Recive", "Receeve"],
        "answer": "Receive"
    },
    {
        "category": "English",
        "question": "Which word is a preposition?",
        "options": ["Quickly", "On", "Jumped", "They"],
        "answer": "On"
    },
    {
        "category": "English",
        "question": "Fill in the blank: He ______ to school every day.",
        "options": ["go", "goes", "gone", "going"],
        "answer": "goes"
    }
]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get-questions')
def get_questions():
    category = request.args.get('category', '')
    filtered = [q for q in questions if q['category'] == category]
    return jsonify([{ "question": q["question"], "options": q["options"] } for q in filtered])


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    username = data.get('username', 'Unknown')
    category = data.get('category', '')
    answers = data['answers']

    filtered_questions = [q for q in questions if q['category'] == category]
    correct_answers = [q['answer'] for q in filtered_questions]

    score = 0
    for i, ans in enumerate(answers):
        if ans == correct_answers[i]:
            score += 1

    with open("scores.txt", "a") as f:
        f.write(f"{username} ({category}): {score}/{len(correct_answers)}\n")

    return jsonify({"score": score, "correct_answers": correct_answers})


@app.route('/scoreboard')
def scoreboard():
    try:
        with open("scores.txt", "r") as f:
            lines = f.readlines()
            scores = [line.strip() for line in lines if line.strip()]
    except FileNotFoundError:
        scores = []
    return render_template("scoreboard.html", scores=scores)


if __name__ == '__main__':
    app.run(debug=True)
