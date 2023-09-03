document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const search = document.getElementById('search-results').parentNode;
    const searchBlur = document.getElementById('search_blur');
    console.log(searchBlur);

    searchInput.addEventListener('input', function() {
        showResults();
    });

    searchInput.addEventListener('focus', function() {
        showResults();
    });

    searchBlur.addEventListener('mousedown', function() {
        console.log('я тут');
        hideResults();
    });

    function showResults() {
        console.log(search);
        search.classList.add('active');
        showSuggestions();
    }

    function hideResults() {
        search.classList.remove('active');
    }
});


// клик ответ на вопрос
const liElements = document.querySelectorAll('li.answer__choice');
liElements.forEach(function(li) {
    li.addEventListener('click', function() {
        const input = li.querySelector('input[type="radio"]');
        const ul = li.parentNode;

        // Deactivate all other li elements within the same ul
        const otherLiElements = ul.querySelectorAll('li.answer__choice');
        otherLiElements.forEach(function(otherLi) {
            if (otherLi !== li) {
                otherLi.classList.remove('active');
                otherLi.querySelector('input[type="radio"]').checked = false;
            }
        });

        // Activate the clicked li element
        li.classList.add('active');
        input.checked = true;
    });
});


function questionsCount() {
    let questions_count = document.querySelectorAll(".question__item").length;
    return questions_count;
}

function choicesCount(choices) {
    let choices_count = choices.querySelectorAll(".choice").length;
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

    var questionNum = document.createElement('div');
    questionNum.className = 'question__number';
    questionNum.innerHTML = `${++questionItemId}`;

    var questionWrapper = document.createElement('div');
    questionWrapper.className = 'question__wrapper';

    questionItem.appendChild(questionNum)
    questionItem.appendChild(questionWrapper)
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
    var choiceWrap = document.createElement('div');
    choiceWrap.className = 'choice__wrapper';
    var field_choice = document.createElement('div');
    field_choice.className = 'field';
    field_choice.innerHTML = `
    <label class="label" for="choice">1 Вариант ответа</label>
    <input autocomplete="off" class="input" id="choice" name="questions-${questionItemId}-answer_choice-0" required="" type="text" value="">
    `;

    choiceWrap.appendChild(field_choice);
    choice.appendChild(choiceWrap)
    let deleteChoice = `
    <div class="choice-delete">
    <button type="button" class="btn" id="delete_choice_button" onclick="deleteChoice()"><img src="../static/img/cancel.svg" alt="cancelErr"></button></div>`;
    field_choice.insertAdjacentHTML('afterend', deleteChoice);
    field_choices.appendChild(choice);

    choicesWrapper.appendChild(field_choices);

    var bottomBorder = document.createElement('div');
    bottomBorder.className = 'bottom-border';
    var field_right_answer = document.createElement('div');
    field_right_answer.className = 'field';
    field_right_answer.innerHTML = `
    <label class="label" for="right_choice">Правильный ответ</label>
    <input autocomplete="off" class="input" id="right_choice" name="questions-${questionItemId}-right_choice" required="" type="text" value="">
    `;



    questionWrapper.appendChild(field_question);
    questionWrapper.appendChild(choicesWrapper);
    questionWrapper.appendChild(bottomBorder);

    
    let add_choice_button = `<button type="button" class="add_choice" id="add_choice_button" onclick="addChoice()">
    вариант ответа
    </button>`;
    field_choices.insertAdjacentHTML('afterend', add_choice_button);

    bottomBorder.appendChild(field_right_answer);

    let deleteQuestion = `
    <div class="delete-btn-wrapper">
    <div class="delete_btn">
        <button type="button" class="btn tools_btn" id="delete_quastion_button" onclick="deleteQuestion()">Удалить</button>
    </div></div>`;
    field_right_answer.insertAdjacentHTML('afterend', deleteQuestion);
});



function deleteQuestion() {
    let questionItem = event.target.parentNode.parentNode.parentNode.parentNode.parentNode;
    let questionDeleteId = parseInt(questionItem.id);
    questionItem.remove();

    let questionItems = document.querySelectorAll('.question__item');
    questionItems.forEach((item, index) => {
        let itemId = parseInt(item.id);
        if (itemId != index) {
            item.id = index.toString();
            let itemNum = item.querySelector('.question__number');
            itemNum.textContent = index + 1;
        }
    });
}



function deleteChoice() {
    let choiceItem = event.target.parentNode.parentNode.parentNode.parentNode;
    console.log(choiceItem);

    let choiceItems = choiceItem.parentNode.children;
    console.log(choiceItems);

    choiceItem.remove();
    console.log(choiceItems);

    Array.from(choiceItems).forEach((item, index) => {
        console.log(item, index, item.id);
        item.id = index.toString();
        let itemNum = item.querySelector('.label');
        itemNum.textContent = `${++index} Вариант ответа`;
    });
}




function addChoice() {
    let choices = event.target.parentNode.querySelector('.choices');
    let choice_count = choicesCount(choices);
    console.log(choices.parentNode.parentNode.parentNode);
    let questionItemId = choices.parentNode.parentNode.parentNode.id;

    let choices_count = choices.querySelectorAll(".choice").length;

    var choice = document.createElement('div');
    choice.className = 'choice';
    let choiceId = choice_count
    choice.id = choiceId

    var choiceWrapper = document.createElement('div');
    choiceWrapper.className = 'choice__wrapper';

    choice.appendChild(choiceWrapper)
    choices.appendChild(choice);


    var field_choice = document.createElement('div');
    field_choice.className = 'field';
    field_choice.innerHTML = `
    <label class="label" for="choice">${++choiceId} Вариант ответа</label>
    <input autocomplete="off" class="input" id="choice" name="questions-${questionItemId}-answer_choice-${choices_count}" required="" type="text" value="">
    `;
    choiceWrapper.appendChild(field_choice);

    let deleteChoice = `
    <div class="choice-delete">
    <button type="button" class="btn" id="delete_choice_button" onclick="deleteChoice()"><img src="../static/img/cancel.svg" alt="cancelErr"></button></div>`;
    field_choice.insertAdjacentHTML('afterend', deleteChoice);
    

}



    
// Обработчик события ввода текста в строку поиска
function showSuggestions() {
    // Находим элементы формы и результата поиска
    var searchInput = document.getElementById('search-input');
    var searchResultsUsers = document.getElementById('search-results__users-wrapper');
    var searchResultsTopics = document.getElementById('search-results__topics-wrapper');
    var users = null;
    var topics = null;
    // возможно не будет работать при загрузки на сервер
    const files = [
        "http://127.0.0.1:5000/static/json/users.json",
        "http://127.0.0.1:5000/static/json/topics.json"
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
            searchResultsUsers.innerHTML = `<div class="empty-wrapper search_empty">
            <div class="empty__content">
                <div class="empty">
                    Здесь ничего нет
                </div>
            </div>
        </div>`;
            searchResultsTopics.innerHTML = `<div class="empty-wrapper search_empty">
            <div class="empty__content">
                <div class="empty">
                    Здесь ничего нет
                </div>
            </div>
        </div>`;
            // Получаем текущий текст из строки поиска
            var searchText = searchInput.value;
            console.log(searchText);
            if (searchText) {
                // Фильтруем пользователей, оставляя только тех, у которых имя или фамилия начинается с текущего текста
                var matchingUsers = users.filter(function(user) {
                    return user.surname.toLowerCase().startsWith(searchText.toLowerCase()) || user.name.toLowerCase().startsWith(searchText.toLowerCase());
                });
                var matchingTopics = topics.filter(function(topic) {
                    return topic.title.toLowerCase().startsWith(searchText.toLowerCase());
                });
                console.log(matchingUsers);
                console.log(matchingTopics);

                // Добавляем подсказки в список результатов
                // темы
                var ul = document.createElement('ul');
                ul.className = 'search-topics';
                matchingTopics.forEach(function(topic) {
                    
                    const li = document.createElement('li');
                    li.className = 'search__topic';
                    li.innerHTML = `<a href="/topic_view/${topic.id}">${topic.title}</a>`;
                    
                    ul.appendChild(li);

                });
                console.log(ul);
                if (ul.childElementCount === 0) {
                    searchResultsTopics.innerHTML = `<div class="empty-wrapper search_empty">
                    <div class="empty__content">
                        <div class="empty">
                            Здесь ничего нет
                        </div>
                    </div>
                </div>`
                } else {
                    searchResultsTopics.innerHTML = '';
                    searchResultsTopics.appendChild(ul);
                }
                // пользователи
                var ul = document.createElement('ul');
                ul.className = 'search-users';
                matchingUsers.forEach(function(user) {
                                            
                    const li = document.createElement('li');
                    li.className = 'search-user';
                    li.innerHTML = `<a href="/profile/${user.id}">${user.surname} ${user.name}</a>`;
                    
                    ul.appendChild(li);
                });
                console.log(ul);
                if (ul.childElementCount === 0) {
                    searchResultsUsers.innerHTML = `<div class="empty-wrapper search_empty">
                    <div class="empty__content">
                        <div class="empty">
                            Здесь ничего нет
                        </div>
                    </div>
                </div>`
                } else {
                    searchResultsUsers.innerHTML = '';
                    searchResultsUsers.appendChild(ul);
                }

            }
        })
        .catch(error => console.error(error))
}


function showAvatar(input) {
    const reader = new FileReader();
  
    reader.onload = function(e) {
        const img = document.createElement("img");
        img.src = e.target.result;
        img.classList.add("avatar_preview");
    
        const oldImage = document.querySelector(".avatar_preview");
        if (oldImage) {
            oldImage.parentNode.replaceChild(img, oldImage);
        } else {
            document.querySelector(".avatar-container").appendChild(img);
        }
    };
  
    reader.readAsDataURL(input.files[0]);
}


function showPicture(input) {
    const reader = new FileReader();
  
    reader.onload = function(e) {
        const img = document.createElement("img");
        img.src = e.target.result;
        img.classList.add("picture_preview");
    
        const oldImage = document.querySelector(".picture_preview");
        if (oldImage) {
            oldImage.parentNode.replaceChild(img, oldImage);
        } else {
            document.querySelector(".picture-container").appendChild(img);
        }
    };
  
    reader.readAsDataURL(input.files[0]);
}

// Обработчик события ввода текста в строку поиска
// function showSuggestionsAuthor() {
//     // Находим элементы формы и результата поиска
//     var searchInput = document.getElementById('search-input-author');
//     var searchResults = document.getElementById('search-results-author');
//     var users = null;
//     // возможно не будет работать при загрузки на сервер
//     const files = [
//         "https://eager-beautiful-printer.glitch.me/static/json/users.json"
//     ];
//     Promise.all(files.map(file => fetch(file)))
//         .then(responses => Promise.all(responses.map(res => res.json())))
//         .then(json => {
//             users = json[0];
    
//             // Очищаем список результатов
//             searchResults.innerHTML = '';
//             // Получаем текущий текст из строки поиска
//             var searchText = searchInput.value;
//             console.log(searchText);
//             if (searchText) {
//                 // Фильтруем пользователей, оставляя только тех, у которых имя или фамилия начинается с текущего текста
//                 var matchingUsers = users.filter(function(user) {
//                     return user.name.toLowerCase().startsWith(searchText.toLowerCase()) || user.surname.toLowerCase().startsWith(searchText.toLowerCase());
//                 });
//                 console.log(matchingUsers);

//                 // Добавляем подсказки в список результатов
//                 // пользователи
//                 var ul = document.createElement('ul');
//                 ul.className = 'user-items-author';
//                 matchingUsers.forEach(function(user) {
//                     console.log(user);

//                     const li = document.createElement('li');
//                     li.className = 'user__item-author';
//                     li.textContent = `${user.name} ${user.surname}`;
                    
//                     li.addEventListener('click', function() {
//                         searchInput.value = this.textContent.trim();
//                         searchResults.innerHTML = '';
//                     });

//                     ul.appendChild(li);

//                 });
//                 searchResults.appendChild(ul);

//             }
//         })
//         .catch(error => console.error(error))
// }



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