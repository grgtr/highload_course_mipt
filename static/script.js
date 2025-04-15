async function calculateViaApi() {
    const dobInput = document.getElementById('dob-api');
    const resultDisplay = document.getElementById('result-display');
    const dobValue = dobInput.value; // Получаем значение ГГГГ-ММ-ДД

    resultDisplay.innerHTML = ''; // Очищаем предыдущий результат/ошибку

    if (!dobValue) {
        resultDisplay.innerHTML = '<p style="color: red;">Пожалуйста, введите дату рождения.</p>';
        return;
    }

    console.log(`Отправка даты '${dobValue}' на API /api/calculate`);

    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ dob: dobValue }), // Отправляем в нужном формате
        });

        const data = await response.json(); // Пытаемся распарсить JSON ответ

        if (response.ok) { // Статус 200-299
            console.log("API ответило успешно:", data);
            resultDisplay.innerHTML = `
                <div class="result">
                    <h2>Ваше Число Судьбы: ${data.destiny_number}</h2>
                     <p>(Рассчитано для даты: ${dobValue} через API)</p>
                </div>`;
        } else {
            // Ошибка от API (статус 400, 500 и т.д.)
            console.error("API вернуло ошибку:", data);
            resultDisplay.innerHTML = `<p class="error">Ошибка: ${data.error || 'Неизвестная ошибка API'}</p>`;
        }
    } catch (error) {
        // Ошибка сети или ошибка парсинга JSON
        console.error('Ошибка при вызове API:', error);
        resultDisplay.innerHTML = `<p class="error">Не удалось связаться с сервером или обработать ответ.</p>`;
    }
}