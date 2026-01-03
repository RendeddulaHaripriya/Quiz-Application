let questions = [];
let userAnswers = [];

function loadQuestions(category) {
  fetch(`/get-questions?category=${encodeURIComponent(category)}`)
    .then((res) => res.json())
    .then((data) => {
      questions = data;
      userAnswers = new Array(questions.length).fill(null);
      displayQuestions();
      document.getElementById("login-box").style.display = "none";
      document.getElementById("quiz-section").style.display = "block";
    });
}

function displayQuestions() {
  const quizBox = document.getElementById("quiz-box");
  quizBox.innerHTML = "";

  questions.forEach((q, index) => {
    const questionEl = document.createElement("div");
    questionEl.classList.add("question");

    const questionText = document.createElement("p");
    questionText.textContent = `${index + 1}. ${q.question}`;
    questionEl.appendChild(questionText);

    q.options.forEach((opt) => {
      const label = document.createElement("label");
      label.innerHTML = `
        <input type="radio" name="q${index}" value="${opt}" onchange="userAnswers[${index}]='${opt}'">
        ${opt}
      `;
      questionEl.appendChild(label);
      questionEl.appendChild(document.createElement("br"));
    });

    quizBox.appendChild(questionEl);
  });
}

function submitQuiz() {
  const username = document.getElementById("username").value;
  const category = document.getElementById("category").value;

  fetch("/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username: username,
      category: category,
      answers: userAnswers
    })
  })
    .then((res) => res.json())
    .then((data) => {
      const resultDiv = document.getElementById("result");
      resultDiv.innerHTML = `<h3>Score: ${data.score}/${data.correct_answers.length}</h3>`;
      // Show correct answers
      questions.forEach((q, i) => {
        const correct = data.correct_answers[i];
        const user = userAnswers[i];
        resultDiv.innerHTML += `
          <p><strong>Q${i + 1}:</strong> ${q.question}<br>
          <span style="color: ${user === correct ? 'green' : 'red'}">
            Your answer: ${user || "Not answered"}
          </span><br>
          Correct answer: ${correct}</p>
        `;
      });

      clearInterval(countdownInterval);
      document.getElementById("play-again").style.display = "block";

    });
}
