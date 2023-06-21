

// let addTestButton = document.querySelector("#add_test_button");
// addTestButton.addEventListener("click", function() {
//     let tests = document.querySelector(".tests");

//     var field = document.createElement('div');
//     field.className = 'field';
//     field.innerHTML = `
//     <label class="label" for="test_item">Тест</label>
//     <input autocomplete="off" class="input" id="test_item" name="test" required="" type="text" value="">
//     `;

//     tests.appendChild(field);

// });

let questionItems = [0];

function questionsCount() {
    let questions_count = document.querySelectorAll(".question__item").length;
    if (!questionItems.includes(questions_count)) {

        questionItems.push(questions_count);
    } else {
        while (questionItems.includes(questions_count)) {
            questions_count++;
        }
        questionItems.push(questions_count);
    }    
    return questions_count;
}

let choiceItems = [0];

function choicesCount(choices) {
    let choices_count = choices.querySelectorAll(".choice").length;
    if (!choiceItems.includes(choices_count)) {
        choiceItems.push(choices_count);
    } else {
        while (choiceItems.includes(choices_count)) {
            choices_count++;
        }
        choiceItems.push(choices_count);
    }
    return choices_count;
}

let addQuestionButton = document.querySelector("#add_question_button");
addQuestionButton.addEventListener("click", function() {

    let questions_count = questionsCount();

    let questionBlock = document.querySelector(".question-block");

    var questionItem = document.createElement('div');
    questionItem.className = 'question__item';
    questionItem.id = questions_count;
    let questionItemId = questionItem.id;
    console.log('questionItemId');

    console.log(questionItemId);

    questionBlock.appendChild(questionItem);

    var field_question = document.createElement('div');
    field_question.className = 'field';
    field_question.innerHTML = `
    <label class="label" for="question">Вопрос</label>
    <input autocomplete="off" class="input" id="question" name="questions-${questionItemId}-question" required="" type="text" value="">
    `;


    var choicesWrapper = document.createElement('div');
    choicesWrapper.className = 'choices-wrapper';
    var field_choices = document.createElement('div');
    field_choices.className = 'choices';
    var choice = document.createElement('div');
    choice.className = 'choice';
    choice.id = 0;
    var field_choice = document.createElement('div');
    field_choice.className = 'field';
    field_choice.innerHTML = `
    <label class="label" for="choice">Варианты ответа</label>
    <input autocomplete="off" class="input" id="choice" name="questions-${questionItemId}-answer_choice-0" required="" type="text" value="">
    `;
    choice.appendChild(field_choice);
    let deleteChoice = '<button type="button" class="btn btn-primary" id="delete_choice_button" onclick="deleteChoice()">Удалить вариант ответа</button>';
    field_choice.insertAdjacentHTML('afterend', deleteChoice);
    field_choices.appendChild(choice);

    choicesWrapper.appendChild(field_choices);



    var field_right_answer = document.createElement('div');
    field_right_answer.className = 'field';
    field_right_answer.innerHTML = `
    <label class="label" for="right_choice">Правильный ответ</label>
    <input autocomplete="off" class="input" id="right_choice" name="questions-${questionItemId}-right_choice" required="" type="text" value="">
    `;



    questionItem.appendChild(field_question);
    questionItem.appendChild(choicesWrapper);

    let add_choice_button = '<button type="button" class="btn" id="add_choice_button" onclick="addChoice()">Добавить вариант ответа</button>';
    choicesWrapper.insertAdjacentHTML('afterend', add_choice_button);

    questionItem.appendChild(field_right_answer);

    let deleteQuestion = '<button type="button" class="btn" id="delete_quastion_button" onclick="deleteQuestion()">Удалить вопрос</button>';
    field_right_answer.insertAdjacentHTML('afterend', deleteQuestion);
});

function deleteQuestion() {
    let questionItem = event.target.parentNode;

    questionDeleteId = questionItem.id;
    questionItem.remove();

    questionItems = questionItems.filter(item => item != questionDeleteId);
}

function deleteChoice() {
    let choiceItem = event.target.parentNode;
    choiceDeleteId = choiceItem.id;

    choiceItem.remove();
    choiceItems = choiceItems.filter(item => item != choiceDeleteId);

}

function addChoice() {
    let choices = event.target.parentNode.querySelector('.choices');
    let choice_count = choicesCount(choices);
    let questionItemId = choices.parentNode.parentNode.id;

    let choices_count = choices.querySelectorAll(".choice").length;
    var choice = document.createElement('div');
    choice.className = 'choice';
    choice.id = choice_count;
    var field_choice = document.createElement('div');
    field_choice.className = 'field';
    field_choice.innerHTML = `
    <label class="label" for="choice">Варианты ответа</label>
    <input autocomplete="off" class="input" id="choice" name="questions-${questionItemId}-answer_choice-${choices_count}" required="" type="text" value="">
    `;
    choice.appendChild(field_choice);
    let deleteChoice = '<button type="button" class="btn btn-primary" id="delete_choice_button" onclick="deleteChoice()">Удалить вариант ответа</button>';
    field_choice.insertAdjacentHTML('afterend', deleteChoice);
    choices.appendChild(choice);

}

    
// Обработчик события ввода текста в строку поиска
function showSuggestions() {
    // Находим элементы формы и результата поиска
    var searchInput = document.getElementById('search-input');
    var searchResults = document.getElementById('search-results');
    var users = null;
    var topics = null;
    // возможно не будет работать при загрузки на сервер
    const files = [
        "https://brazen-probable-orchestra.glitch.me/static/json/users.json",
        "https://brazen-probable-orchestra.glitch.me/static/json/topics.json"
    ];
        
    Promise.all(files.map(file => fetch(file)))
        .then(responses => Promise.all(responses.map(res => res.json())))
        .then(json => {
            users = json[0];
            topics = json[1];
            // console.log(users);
            // console.log(topics);
            // console.log('f');
    
            // Очищаем список результатов
            searchResults.innerHTML = '';
            // Получаем текущий текст из строки поиска
            var searchText = searchInput.value;
            console.log(searchText);
            if (searchText) {
                // Фильтруем пользователей, оставляя только тех, у которых имя или фамилия начинается с текущего текста
                var matchingUsers = users.filter(function(user) {
                    return user.name.toLowerCase().startsWith(searchText.toLowerCase()) || user.surname.toLowerCase().startsWith(searchText.toLowerCase());
                });
                var matchingTopics = topics.filter(function(topic) {
                    return topic.title.toLowerCase().startsWith(searchText.toLowerCase());
                });
                console.log(matchingUsers);
                console.log(matchingTopics);

                // Добавляем подсказки в список результатов
                // темы
                var ul = document.createElement('ul');
                ul.className = 'topic-items';
                matchingTopics.forEach(function(topic) {
                    
                    const li = document.createElement('li');
                    li.className = 'user__item';
                    li.innerHTML = `<a href="/topic_view/${topic.id}">${topic.title}</a>`;
                    
                    ul.appendChild(li);

                });
                console.log(ul);
                searchResults.appendChild(ul);
                // пользователи
                var ul = document.createElement('ul');
                ul.className = 'user-items';
                matchingUsers.forEach(function(user) {
                                            
                    const li = document.createElement('li');
                    li.className = 'user__item';
                    li.innerHTML = `<a href="/profile/${user.id}">${user.name} ${user.surname}</a>`;
                    
                    ul.appendChild(li);


                });
                console.log(ul);

                searchResults.appendChild(ul);

            }
        })
        .catch(error => console.error(error))
}


// Обработчик события ввода текста в строку поиска
function showSuggestionsAuthor() {
    // Находим элементы формы и результата поиска
    var searchInput = document.getElementById('search-input-author');
    var searchResults = document.getElementById('search-results-author');
    var users = null;
    // возможно не будет работать при загрузки на сервер
    const files = [
        "http://127.0.0.1:5000/static/json/users.json"
    ];
    Promise.all(files.map(file => fetch(file)))
        .then(responses => Promise.all(responses.map(res => res.json())))
        .then(json => {
            users = json[0];
    
            // Очищаем список результатов
            searchResults.innerHTML = '';
            // Получаем текущий текст из строки поиска
            var searchText = searchInput.value;
            console.log(searchText);
            if (searchText) {
                // Фильтруем пользователей, оставляя только тех, у которых имя или фамилия начинается с текущего текста
                var matchingUsers = users.filter(function(user) {
                    return user.name.toLowerCase().startsWith(searchText.toLowerCase()) || user.surname.toLowerCase().startsWith(searchText.toLowerCase());
                });
                console.log(matchingUsers);

                // Добавляем подсказки в список результатов
                // пользователи
                var ul = document.createElement('ul');
                ul.className = 'user-items-author';
                matchingUsers.forEach(function(user) {
                    console.log(user);

                    const li = document.createElement('li');
                    li.className = 'user__item-author';
                    li.textContent = `${user.name} ${user.surname}`;
                    
                    li.addEventListener('click', function() {
                        searchInput.value = this.textContent.trim();
                        searchResults.innerHTML = '';
                    });

                    ul.appendChild(li);

                });
                searchResults.appendChild(ul);

            }
        })
        .catch(error => console.error(error))
}



window.onload = function () {
    // const profileDropdown = document.querySelector(".profile_dropdown");
    // console.log(profileDropdown);

    // profileDropdown.addEventListener('click', function (e) {
    //     console.log(e.target);
    // });


    // // Используем объект XMLHttpRequest для загрузки содержимого файла
    // var xhttp = new XMLHttpRequest();
    // // Открываем файл, используя метод open()
    // // xhttp.open("GET", "../json/users.json", true);
    // // xhttp.open("GET", "static/json/users.json", true);
    // xhttp.open("GET", "../static/json/users.json", true);
    // console.log(xhttp);

    // // Определяем тип ответа, используя метод setRequestHeader()
    // xhttp.setRequestHeader("Content-type", "application/json");
    // console.log(xhttp);

    // var data = JSON.parse(users);
    // console.log(data);
    // // Обрабатываем полученный результат, используя метод onload()
    // xhttp.onload = function() {
    //     var data = JSON.parse(xhttp.responseText);
    //     console.log(data);

    //     if (xhttp.status == 200) {
    //         var data = JSON.parse(xhttp.responseText);
    //         // код для работы с полученными данными
    //         console.log(data);
    //     }
    // };




    // надо указать путь как в константе python
    // const url = "../static/json/users.json";
    // // const url = "users.json";

    // const fetchJson = async () => {
    //     try {
    //         const data = await fetch(url);
    //         console.log(data);

    //         const response = await data.json();  
    //     } catch (error) {
    //         console.log(error);
    //     }
    // };
    // fetchJson();



}