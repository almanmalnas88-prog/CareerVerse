let questions = [];

let currentQuestion = 0;

let selectedOption = null;

let answers = [];


// =====================================
// START ASSESSMENT
// =====================================

function startAssessment() {

    document.getElementById("home")
        .style.display = "none";

    document.getElementById("profile")
        .style.display = "block";

    window.scrollTo(0, 0);
}


// =====================================
// LOAD QUESTIONS FROM MYSQL
// =====================================

async function loadQuestions() {

    const name =
        document.getElementById(
            "studentName"
        ).value.trim();

    if (!name) {

        alert(
            "Please enter your name."
        );

        return;
    }


    try {

        const response =
            await fetch(
                "/api/questions"
            );


        if (!response.ok) {

            throw new Error(
                "Could not load questions"
            );
        }


        questions =
            await response.json();


        if (questions.length === 0) {

            alert(
                "No questions found in database."
            );

            return;
        }


        document.getElementById(
            "profile"
        ).style.display = "none";


        document.getElementById(
            "assessment"
        ).style.display = "block";


        currentQuestion = 0;

        answers = [];

        showQuestion();

        window.scrollTo(0, 0);

    }

    catch (error) {

        console.error(error);

        alert(
            "Database connection problem. " +
            "Check your Python server."
        );
    }
}


// =====================================
// SHOW CURRENT QUESTION
// =====================================

function showQuestion() {

    const question =
        questions[currentQuestion];


    selectedOption = null;


    document.getElementById(
        "questionNumber"
    ).textContent =
        `Question ${currentQuestion + 1} of ${questions.length}`;


    document.getElementById(
        "questionText"
    ).textContent =
        question.question_text;


    const optionsContainer =
        document.getElementById(
            "options"
        );


    optionsContainer.innerHTML = "";


    question.options.forEach(
        function(option) {

            const button =
                document.createElement(
                    "button"
                );


            button.className =
                "option";


            button.textContent =
                option.option_text;


            button.onclick =
                function() {

                    selectOption(
                        button,
                        option
                    );

                };


            optionsContainer.appendChild(
                button
            );

        }
    );


    const progress =
        ((currentQuestion) /
        questions.length) * 100;


    document.getElementById(
        "progress"
    ).style.width =
        `${progress}%`;


    document.getElementById(
        "nextButton"
    ).textContent =
        currentQuestion ===
        questions.length - 1
            ? "See My Career →"
            : "Next →";
}


// =====================================
// SELECT OPTION
// =====================================

function selectOption(
    button,
    option
) {

    document
        .querySelectorAll(".option")
        .forEach(
            function(item) {

                item.classList.remove(
                    "selected"
                );

            }
        );


    button.classList.add(
        "selected"
    );


    selectedOption = option;
}


// =====================================
// NEXT QUESTION
// =====================================

function nextQuestion() {

    if (!selectedOption) {

        alert(
            "Please select an option first."
        );

        return;
    }


    answers[currentQuestion] = {

        question_id:
            questions[currentQuestion].id,

        option_id:
            selectedOption.id,

        category:
            selectedOption.category
    };


    if (
        currentQuestion <
        questions.length - 1
    ) {

        currentQuestion++;

        showQuestion();

    }

    else {

        getRecommendation();

    }
}


// =====================================
// GET CAREER RECOMMENDATION
// =====================================

async function getRecommendation() {

    try {

        const response =
            await fetch(
                "/api/recommend",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        answers: answers
                    })

                }
            );


        const result =
            await response.json();


        if (!response.ok) {

            throw new Error(
                result.error ||
                "Recommendation failed"
            );
        }


        showResults(result);

    }

    catch (error) {

        console.error(error);

        alert(
            "Could not calculate your career recommendation."
        );
    }
}


// =====================================
// SHOW RESULTS
// =====================================

function showResults(result) {

    document.getElementById(
        "assessment"
    ).style.display = "none";


    document.getElementById(
        "result"
    ).style.display = "block";


    const intro =
        document.getElementById(
            "resultIntro"
        );


    intro.textContent =
        `Based on your answers, your strongest
        career area is ${result.category}.
        Here are some careers you can explore.`;


    const container =
        document.getElementById(
            "careerResults"
        );


    container.innerHTML = "";


    result.careers.forEach(
        function(career) {

            const div =
                document.createElement(
                    "div"
                );


            div.className =
                "career";


            div.innerHTML = `

                <h3>
                    ${career.name}
                </h3>

                <p>
                    ${career.description}
                </p>

                <p>
                    <strong>
                        Education:
                    </strong>
                    ${career.education_required}
                </p>

                <p>
                    <strong>
                        Important Skills:
                    </strong>
                    ${career.skills_required}
                </p>

            `;


            container.appendChild(
                div
            );

        }
    );


    window.scrollTo(0, 0);
}


// =====================================
// REGISTER SERVICE WORKER
// =====================================

if ("serviceWorker" in navigator) {

    window.addEventListener("load", function () {

        navigator.serviceWorker
            .register("/service-worker.js")

            .then(function (registration) {

                console.log(
                    "CareerVerse Service Worker registered:",
                    registration
                );

            })

            .catch(function (error) {

                console.error(
                    "Service Worker registration failed:",
                    error
                );

            });

    });

}
