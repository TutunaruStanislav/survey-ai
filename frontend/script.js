const API_BASE_URL = 'http://127.0.0.1:9000';

let questions = [];

async function loadQuestions() {
    const loadingDiv = document.getElementById('loading');
    loadingDiv.textContent = 'Загрузка вопросов...';

    try {
        const response = await fetch(`${API_BASE_URL}/questions`);
        if (!response.ok) {
            throw new Error('Failed to load questions');
        }
        questions = await response.json();
        renderForm();
        loadingDiv.style.display = 'none';
    } catch (error) {
        loadingDiv.innerHTML = `<div class="error">Ошибка загрузки: ${error.message}</div>`;
        console.error('Error:', error);
    }
}

function renderForm() {
    const formDiv = document.getElementById('form');
    formDiv.innerHTML = '';

    questions.forEach(question => {
        const groupDiv = document.createElement('div');
        groupDiv.className = 'form-group';

        const labelElement = document.createElement('label');
        labelElement.textContent = question.text;
        groupDiv.appendChild(labelElement);

        if (question.type === 'text') {
            const input = document.createElement('input');
            input.type = 'text';
            input.id = `q_${question.id}`;
            input.name = question.id;
            input.required = true;
            groupDiv.appendChild(input);
        } else if (question.type === 'radio') {
            const radioGroup = document.createElement('div');
            radioGroup.className = 'radio-group';

            question.options.forEach(option => {
                const optionDiv = document.createElement('div');
                optionDiv.className = 'radio-option';

                const radio = document.createElement('input');
                radio.type = 'radio';
                radio.id = `q_${question.id}_${option}`;
                radio.name = question.id;
                radio.value = option;
                radio.required = true;

                const optionLabel = document.createElement('label');
                optionLabel.htmlFor = `q_${question.id}_${option}`;
                optionLabel.textContent = option;

                optionDiv.appendChild(radio);
                optionDiv.appendChild(optionLabel);
                radioGroup.appendChild(optionDiv);
            });

            groupDiv.appendChild(radioGroup);
        }

        formDiv.appendChild(groupDiv);
    });

    const submitButton = document.createElement('button');
    submitButton.type = 'submit';
    submitButton.textContent = 'Отправить';
    submitButton.onclick = submitForm;
    formDiv.appendChild(submitButton);
}

async function submitForm(e) {
    e.preventDefault();

    const answers = {};
    questions.forEach(question => {
        if (question.type === 'text') {
            answers[question.id] = document.getElementById(`q_${question.id}`).value;
        } else if (question.type === 'radio') {
            const selected = document.querySelector(`input[name="${question.id}"]:checked`);
            answers[question.id] = selected ? selected.value : '';
        }
    });

    try {
        const response = await fetch(`${API_BASE_URL}/answers`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(answers),
        });

        if (!response.ok) {
            throw new Error('Failed to submit answers');
        }

        const result = await response.json();

        document.getElementById('form').innerHTML = '';
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.textContent = '✓ ' + result.message;
        document.getElementById('form').appendChild(successDiv);
    } catch (error) {
        alert('Ошибка при отправке: ' + error.message);
        console.error('Error:', error);
    }
}

document.addEventListener('DOMContentLoaded', loadQuestions);
