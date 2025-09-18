// Получает дату рождения из поля ввода и запускает процесс расчета через API
async function calculateViaApi() {
    const dobInput = document.getElementById('dob-api');
    const resultDisplay = document.getElementById('result-display');
    const dobValue = dobInput.value;

    clearResult(resultDisplay);

    if (!dobValue) {
        displayError(resultDisplay, 'Пожалуйста, введите дату рождения.');
        return;
    }

    console.log(`Отправка даты '${dobValue}' на API /api/calculate`);

    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ dob: dobValue }),
        });

        const data = await response.json();

        if (response.ok) {
            console.log("API ответило успешно:", data);
            displaySuccess(resultDisplay, data.destiny_number, dobValue);
        } else {
            console.error("API вернуло ошибку:", data);
            displayError(resultDisplay, `Ошибка: ${data.error}` || 'Неизвестная ошибка API');
        }
    } catch (error) {
        console.error('Ошибка при вызове API:', error);
        displayError(resultDisplay, 'Не удалось связаться с сервером или обработать ответ.');
    }
}

// Очищает область отображения результата
function clearResult(element) {
    element.innerHTML = '';
}

// Отображает сообщение об ошибке
function displayError(element, message) {
    console.error('Ошибка:', error);
    element.innerHTML = `<p class="error">Ошибка: ${message}</p>`;
}

// Отображает успешный результат расчета
function displaySuccess(element, destinyNumber, dob) {
    element.innerHTML = `
        <div class="result">
            <h2>Ваше Число Судьбы: ${destinyNumber}</h2>
            <p>(Рассчитано для даты: ${dob} через API)</p>
        </div>
    `;
}