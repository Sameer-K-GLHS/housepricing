let currentQuestion = 1;
let totalQuestions = document.getElementsByClassName("question").length;

function showQuestion(questionNumber) {
  let questions = document.getElementsByClassName("question");
  for (let i = 0; i < questions.length; i++) {
    questions[i].style.display = "none";
  }
  
  let question = document.getElementById("question" + questionNumber);
  if (question) {
    question.style.display = "block";
  }
}

function nextQuestion() {
  if (currentQuestion < totalQuestions) {
    currentQuestion++;
    showQuestion(currentQuestion);
  }
}

function previousQuestion() {
  if (currentQuestion > 1) {
    currentQuestion--;
    showQuestion(currentQuestion);
  }
}

document.getElementById("formSlideshow").addEventListener("submit", function(event) {
  event.preventDefault();
  
  let unansweredQuestions = false;
  let questions = document.getElementsByClassName("question");
  for (let i = 0; i < questions.length; i++) {
    let input = questions[i].querySelector("input, select");
    if (!input.value) {
      unansweredQuestions = true;
      questions[i].querySelector("input, select").value = 1;
      break;
    }
  }

  let errorDropdown = document.getElementById("errorDropdown");

 if (unansweredQuestions) {
    errorDropdown.style.display = "block";
  } else {
    errorDropdown.style.transform = "none";
    predictHousePrice();
  }
});

showQuestion(currentQuestion);

function predictHousePrice() {
  let responses = [];
  let questions = document.getElementsByClassName("question");
  for (let i = 0; i < questions.length; i++) {
    let input = questions[i].querySelector("input, select");
    responses.push(input.value.toString());
  }
  console.log(responses);

const url = 'https://skhan15.pythonanywhere.com/predict';
const body = {
  values: responses
};
const headers = { 'Content-Type': 'application/json' };

fetch(url, {
  method: 'POST',
  headers: headers,
  body: JSON.stringify(body)
})
  .then(response => response.json())
  .then(data => {
    const prediction = data['predictions'];
    const predictionElement = document.getElementsByClassName("prediction")[0];
    predictionElement.innerText = "";
    predictionElement.innerText = "$" + prediction[0].toFixed(2);
  })
  .catch(error => console.error(error));
}

