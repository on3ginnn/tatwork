import json
import time

from flask import Flask, render_template, redirect, abort, request # работа с сервером
from werkzeug.datastructures import MultiDict
from werkzeug.utils import secure_filename
import os
from wtforms import RadioField, FieldList, SubmitField
from wtforms.validators import DataRequired

from data import db_session # создание и подключение к БД
from data.users import User # модель таблицы
from data.students import Student
from data.teachers import Teacher
from data.topic import Topic
from data.task import Task
from data.questions import Questions
from data.answers import Answers
import datetime

from forms.answers import TestAnswersForm
from forms.task import TaskForm
from forms.topic import TopicForm
# from forms.task import TaskForm # формы для обработки HTML
# from forms.topic import TopicForm
# from forms.questions import QuestionsForm
from forms.user import RegisterForm, LoginForm, ProfileEdit
from flask_login import LoginManager, login_user, login_required, logout_user, current_user # вход, выход, и тд,
# для взаимодействия с БД
from sqlalchemy.orm import scoped_session # закрывают бд для других процессов при обращении к ней
from flask import make_response, jsonify # преобразование данных
from flask_restful import reqparse, abort, Api, Resource # работа с HTTP
from flask import current_app


app = Flask(__name__)
api = Api(app)
app.config['IMG_FOLDER'] = 'static/img'
app.config['JSON_FOLDER'] = 'static/json'
# js тоже надо указывать в статистических данных
app.config['JS_FOLDER'] = 'static/scripts/script.js'
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
# создаем сессию(должна быть только одна, чтобы не е***а мозги)
db_sess = scoped_session(db_session.create_session)


@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(User).get(user_id)


# Выход
@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect("/")


# создание искусственных записей в БД
def artificialEngine():

    # создаем объект пользователя User
    user = User(name='Зульфия', surname='Ахатовна', status='Преподаватель')
    user.set_password('admin')
    # создаем объект студента и связываем его с пользователем
    teacher = Teacher(user=user)
    # добавляем пользователя и студента в базу данных
    db_sess.add(user)
    db_sess.add(teacher)
    db_sess.commit()


    # создаем объект пользователя User
    user = User(name='Тимур', surname='Фархутдинов')
    user.set_password('on3gin')
    # создаем объект студента и связываем его с пользователем
    student = Student(group='ИС-222б', user=user)
    # добавляем пользователя и студента в базу данных
    db_sess.add(user)
    db_sess.add(student)
    db_sess.commit()


    # создаем объект темы Topic и связываем его с пользователем User
    topic_author = db_sess.query(User).filter(User.name == 'Тимур', User.surname == 'Фархутдинов').first()
    topic = Topic(title='Испытание судьбы 1 часть', topic_lang='РУС', author=topic_author)
    # добавляем тему в базу данных
    db_sess.add(topic)
    db_sess.commit()


    # создаем объект задания Task и связываем его с темой Topic
    topic = db_sess.query(Topic).filter(Topic.id == 1).first()
    task = Task(title='Испытание судьбы', task_type='ТЕСТ', topic=topic)
    # добавляем задание в базу данных
    db_sess.add(task)
    db_sess.commit()


    # создаем объект вопросов и связываем его с заданием
    task = db_sess.query(Task).filter(Task.id == 1).first()
    questions = Questions(
        question=[
            {'question': 'Как называется столица Франции?',
             'answer_choice': ['Татарстан', 'Сиэтл', 'Пхеньян', 'Париж'],
             'right_choice': 'Париж'},
            {'question': 'Как называется столица Великобритании?',
             'answer_choice': ['Осака', 'Лондон', 'Пекин', 'Амстердам'],
             'right_choice': 'Лондон'}],
        task=task
    )
    # добавляем вопросы в базу данных
    db_sess.add(questions)
    db_sess.commit()


    # создаем объект ответов и связываем его с заданием и пользователем
    current_user_feic = db_sess.query(User).filter(User.name == 'Тимур', User.surname == 'Фархутдинов').first()
    task = db_sess.query(Task).filter(Task.id == 1).first()
    answers_item = [
        {'question': 'Как называется столица Франции?', 'answer': 'Париж', 'right': True},
        {'question': 'Как называется столица Великобритании?', 'answer': 'Лондон', 'right': True}
    ]
    answers = Answers(
        user=current_user_feic,
        task=task,
        status='Зачтено',
        score='2 / 2',
        answers=answers_item
    )

    # добавляем ответы в базу данных
    db_sess.add(answers)
    db_sess.commit()


# создание JSON файла со всеми пользователями
def usersJson():
    users = db_sess.query(User).all()

    js_users = []
    for user in users:
        js_user = {
            'id': user.id,
            'name': user.name,
            'surname': user.surname,
            'status': user.status
        }
        js_users.append(js_user)
    usersJsonLst = json.dumps(js_users)

    json_path = os.path.join(app.config['JSON_FOLDER'], 'users.json')
    if os.path.exists(json_path):
        os.remove(json_path)
    print(json_path)

    with open(json_path, 'w') as ujson:
        ujson.write(usersJsonLst)


# создание JSON файла со всеми темами
def topicsJson():
    topics = db_sess.query(Topic).all()

    js_topics = []
    for topic in topics:
        js_topic = {
            'id': topic.id,
            'title': topic.title,
            'topic_lang': topic.topic_lang
        }
        js_topics.append(js_topic)
    topicsJsonLst = json.dumps(js_topics)

    json_path = os.path.join(app.config['JSON_FOLDER'], 'topics.json')
    if os.path.exists(json_path):
        os.remove(json_path)
    print(json_path)

    with open(json_path, 'w') as tjson:
        tjson.write(topicsJsonLst)


def main():
    db_session.global_init('db/tatwork.db')

    # создать тест-записи в БД
    # artificialEngine()

    # создание JSON файла со всеми пользователями
    usersJson()
    # создание JSON файла со всеми темами
    topicsJson()

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


# перевод из студента в препод
# удаление студента по id (нужно для работы magic func)
def deleteStudentById(id):
    student = db_sess.query(Student).filter_by(user_id=id).first()
    db_sess.delete(student)
    db_sess.commit()


# добавление препода по id (нужно для работы magic func)
def addTeacherById(user):
    teacher = Teacher(user=user)
    db_sess.add(teacher)
    user.status = 'Преподаватель'
    db_sess.commit()


# удаление препода по id (нужно для работы magic func)
def deleteTeachertById(id):
    teacher = db_sess.query(Teacher).filter_by(user_id=id).first()
    db_sess.delete(teacher)
    db_sess.commit()


# добавление студента по id (нужно для работы magic func)
def addStudentById(user):
    student = Student(user=user)
    db_sess.add(student)
    user.status = 'Студент'
    db_sess.commit()


# Изменение статуса со студента на препода
@app.route("/magic", methods=['GET', 'POST'])
def magic():
    if current_user.status == 'Студент':
        deleteStudentById(current_user.id)
        addTeacherById(current_user)
    else:
        deleteTeachertById(current_user.id)
        addStudentById(current_user)
    return redirect("/profile")


@app.route("/magic/<int:id>", methods=['GET', 'POST'])
def magic_for(id):
    user_magic = db_sess.query(User).filter_by(id=id).first()
    if user_magic.status == 'Студент':
        deleteStudentById(id)
        addTeacherById(user_magic)
    else:
        deleteTeachertById(id)
        addStudentById(user_magic)

    return redirect(f"/profile/{id}")


# Главная страница
@app.route("/", methods=['GET', 'POST'])
def index():
    topics = db_sess.query(Topic).all()

    return render_template("index.html", topics=topics)


# Новое задание(создание), сразу же создаются вопросы и задания
@app.route('/task/<int:topic_id>', methods=['GET', 'POST'])
def new_task(topic_id):
    form = TaskForm()

    # создать другую проверку валидации, form.validate_on_submit() не работает, хз поч, проверять все то, что нужно

    if request.method == "POST":
        print(form.questions.data)
        questions = []
        for question in form.questions.data:
            try:
                print(question['answer_choice'])
                question_item = {'question': question['question'],
                                 'answer_choice': question['answer_choice'],
                                 'right_choice': question['right_choice']}
                questions.append(question_item)
            except Exception as error:
                pass

        topic = db_sess.query(Topic).filter_by(id=topic_id).first()
        task = Task(topic=topic, title=form.title.data)
        db_sess.add(task)
        db_sess.commit()
        # создаем объект вопросов и связываем его с заданием
        questions = Questions(
            question=questions,
            task=task
        )
        db_sess.add(questions)
        db_sess.commit()
        return redirect(f'/topic_view/{topic_id}')
    return render_template('task.html', form=form, task_mode='Новое задание')


# Смотреть задание(прохождение)
@app.route('/task_answer/<string:topic_task_id>', methods=['GET', 'POST'])
def task_answer(topic_task_id):
    topic_id = topic_task_id.split('-')[0]
    task_id = topic_task_id.split('-')[1]
    if current_user.is_authenticated:
        form = TestAnswersForm()
        task = db_sess.query(Task).filter_by(id=task_id).first()
        questions = db_sess.query(Questions).filter_by(task_id=task_id).first()
        if request.method == 'POST':
            form_answers = form.test_answers.data
            answers_items = []
            question_right_count = 0
            for num in range(len(form_answers)):
                right = form_answers[num] == questions.question[num]['right_choice']
                question_right_count += 1 if right else 0
                answers_items.append({'question': questions.question[num]['question'], 'answer': form_answers[num],
                                      'right': right})

            score = f'{question_right_count} / {len(form_answers)}'

            answers = Answers(
                answers=answers_items,
                user=current_user,
                task=task,
                status='На проверке',
                score=score
            )

            db_sess.add(answers)
            db_sess.commit()

            return redirect(f'/topic_view/{topic_id}')
        return render_template('answers.html', form=form, task=task, questions=questions.question)
    else:
        return redirect('/register')


# Редактировать задание(для преподов)
@app.route('/task_edit/<string:topic_task_id>', methods=['GET', 'POST'])
def task_edit(topic_task_id):
    topic_id = topic_task_id.split('-')[0]
    task_id = topic_task_id.split('-')[1]
    if current_user.is_authenticated:
        form = TaskForm()
        task = db_sess.query(Task).filter_by(id=task_id).first()
        questions = db_sess.query(Questions).filter_by(task_id=task_id).first()
        topic = db_sess.query(Topic).filter_by(id=topic_id).first()

        if request.method == 'POST':
            questions_edit = []
            for question in form.questions.data:
                try:
                    question_item = {'question': question['question'],
                                     'answer_choice': question['answer_choice'],
                                     'right_choice': question['right_choice']}
                    questions_edit.append(question_item)
                except Exception as error:
                    pass
            print(questions_edit)
            task.title = form.title.data
            questions.question = questions_edit
            questions.task = task

            db_sess.commit()
            return redirect(f'/topic_view/{topic_id}')
        return render_template('task-edit.html', form=form, task=task, questions=questions.question)
    else:
        return redirect('/register')


# редактирование ответов
@app.route('/answer_edit/<int:answer_id>', methods=['GET', 'POST'])
def answer_edit(answer_id):
    if current_user.is_authenticated:
        form = TestAnswersForm()
        answers = db_sess.query(Answers).filter_by(id=answer_id).first()
        task = db_sess.query(Task).filter(Task.answer.contains(answers)).first()
        questions = db_sess.query(Questions).filter_by(task=task).first()
        if request.method == 'GET':
            questions_by_user = []
            for num in range(len(answers.answers)):
                print(questions.question[num])
                print(answers.answers[num])
                questions_by_user.append(
                    {'question': questions.question[num]['question'],
                     'answer_choice': questions.question[num]['answer_choice'],
                     'right_choice': questions.question[num]['right_choice'],
                     'user_answer_index_for_choices':
                         questions.question[num]['answer_choice'].index(answers.answers[num]['answer'])
                     }
                )
            print(questions_by_user)
        if request.method == 'POST':
            form_answers_edit = form.test_answers.data
            for i in range(len(form_answers_edit)):

                print(form_answers_edit[i])
            answers_items = []
            question_right_count = 0
            for num in range(len(form_answers_edit)):
                right = form_answers_edit[num] == questions.question[num]['right_choice']
                question_right_count += 1 if right else 0
                answers_items.append({'question': questions.question[num]['question'], 'answer': form_answers_edit[num],
                                      'right': right})

            score = f'{question_right_count} / {len(form_answers_edit)}'

            answers.answers = answers_items
            answers.status = 'На проверке'
            answers.score = score
            answers.modified_date = datetime.datetime.now()

            db_sess.commit()

            return redirect(f'/answers_my')
        return render_template('answers-edit.html', form=form, task=task, questions_by_user=questions_by_user)
    else:
        return redirect('/register')


# отметить как проверенное(для преподов)
@app.route('/answer_verif/<int:answer_id>', methods=['GET', 'POST'])
@login_required
def answer_verif(answer_id):
    if current_user.is_authenticated:
        answers = db_sess.query(Answers).filter_by(id=answer_id).first()
        answers.status = 'Зачтено'

        db_sess.commit()

        return redirect('/answers_check')
    else:
        return redirect('/register')


# список непроверенных ответов(для преподов)
@app.route('/answers_check', methods=['GET', 'POST'])
@login_required
def answers():
    if current_user.is_authenticated:
        answers = db_sess.query(Answers).all()
        return render_template('answers-check.html', answers=answers)
    else:
        return redirect('/register')


# список моих ответов
@app.route('/answers_my', methods=['GET', 'POST'])
@login_required
def answers_my():
    if current_user.is_authenticated:
        answers = db_sess.query(Answers).filter_by(user=current_user).all()
        return render_template('answers-check-my.html', answers=answers)
    else:
        return redirect('/register')


# список пользователей
@app.route('/users_list', methods=['GET', 'POST'])
@login_required
def users_list():
    if current_user.is_authenticated:
        students = db_sess.query(Student).all()
        teachers = db_sess.query(Teacher).all()
        return render_template('users-list.html', students=students, teachers=teachers)
    else:
        return redirect('/register')


# Новая тема(создание)
@app.route('/topic', methods=['GET', 'POST'])
@login_required
def new_topic():
    global db_sess
    form = TopicForm()
    if form.validate_on_submit():
        if db_sess.query(Topic).filter_by(title=form.title.data).first():
            return render_template('topic-edit.html', form=form, topic_mode='Новая тема',
                                   message="Такая тема уже есть.")

        try:

            name, surname = str(form.author.data).split()

            user = db_sess.query(User).filter_by(name=name, surname=surname).first()
            if not user:
                return render_template('topic-edit.html', form=form, topic_mode='Новая тема',
                                       message="Пользователь, указанный автором, не найден.")
        except Exception:
            return render_template('topic-edit.html', form=form, topic_mode='Новая тема',
                                   message="Инициалы автора должны содержать Имя и Фамилию")


        topic = Topic(
            title=form.title.data,
            author_id=user.id,
            topic_lang=form.topic_lang.data,
        )
        picture = request.files['picture']
        if picture:
            filename = secure_filename(picture.filename)
            picture_path = os.path.join(app.config['IMG_FOLDER'], filename)
            picture.save(picture_path)
            topic.picture = filename
        db_sess.add(topic)
        db_sess.commit()

        # обновление JSON файла со всеми темами
        topicsJson()

        return redirect(f'/topic_view/{topic.id}')
    return render_template('topic-edit.html', form=form, topic_mode='Новая тема')


# Редактировать тему
@app.route('/topic/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_topic(id):
    global db_sess
    form = TopicForm()

    if request.method == "GET":
        topic = db_sess.query(Topic).filter_by(id=id).first()
        if topic:
            form.title.data = topic.title
            if topic.author:
                author = f'{topic.author.name} {topic.author.surname}'
            else:
                author = 'Не найден'
            form.author.data = author
            form.topic_lang.data = topic.topic_lang

        else:
            abort(404)
    if form.validate_on_submit():
        full_name = str(form.author.data)
        name, surname = "", ""
        if len(full_name.split()) == 2:
            name, surname = full_name.split()
        else:
            return render_template('topic-edit.html', form=form, topic_mode='Редактирование темы',
                                   message="Неверное значение поля автора. Надо: <имя фамилия>")

        user = db_sess.query(User).filter_by(name=name, surname=surname).first()

        if not user:
            return render_template('topic-edit.html', form=form, topic_mode='Редактирование темы',
                                   message="Пользователь, указанный автором, не найден.")

        topic = db_sess.query(Topic).filter_by(id=id).first()

        if topic:
            try:
                # Редактирование картинки темы (без учета расширения)
                picture = request.files['picture']
                if picture:
                    filename = secure_filename(picture.filename)
                    picture_path = os.path.join(app.config['IMG_FOLDER'], filename)
                    print(picture_path)

                    picture.save(picture_path)
                    if topic.picture:
                        old_picture_path = os.path.join(app.config['IMG_FOLDER'], topic.picture)
                        os.remove(old_picture_path)
                    db_sess.query(Topic).filter_by(id=id).update({Topic.picture: filename})

                # Редактирование других данных темы
                db_sess.query(Topic).filter_by(id=id).update({Topic.title: form.title.data, Topic.author_id: user.id,
                                                              Topic.topic_lang: form.topic_lang.data})

                db_sess.commit()

                # обновление JSON файла со всеми темами
                topicsJson()

                return redirect(f'/topic_view/{topic.id}')
            except Exception as e:
                db_sess.rollback()
                print(e)
        else:
            abort(404)

    return render_template('topic-edit.html', form=form, topic_mode='Редактирование темы')


def task_delete_func(tasks):
    for task in tasks:
        print(tasks)
        print(task.title)
        task_question = db_sess.query(Questions).filter_by(task=task).first()
        task_answer = db_sess.query(Answers).filter_by(task=task).first()
        if task_question:
            db_sess.delete(task_question)
        if task_answer:
            db_sess.delete(task_answer)
        db_sess.delete(task)
    db_sess.commit()


# Удалить тему(нужно удалять все задания, привязанные к ней)
@app.route('/topic_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def topic_delete(id):
    topic = db_sess.query(Topic).filter_by(id=id).first()

    # удалить все задания, привязанные к теме
    task_delete_func(topic.tasks)


    db_sess.delete(topic)
    db_sess.commit()
    # обновление JSON файла со всеми темами
    topicsJson()
    return redirect('/')


# Удалить задание
@app.route('/task_delete/<string:topic_task_id>', methods=['GET', 'POST'])
@login_required
def task_delete(topic_task_id):
    topic_id = topic_task_id.split('-')[0]
    task_id = topic_task_id.split('-')[1]
    task = db_sess.query(Task).filter_by(id=int(task_id)).first()
    # удалить все задания, привязанные к теме
    task_delete_func([task])

    return redirect(f'/topic_view/{topic_id}')


# удаление непроверенных ответов(только для препода)
@app.route('/answer_delete/<int:answer_id>', methods=['GET', 'POST'])
@login_required
def answer_delete(answer_id):
    answer = db_sess.query(Answers).filter_by(id=answer_id).first()

    db_sess.delete(answer)
    db_sess.commit()
    return redirect(f'/users_list')


# Смотреть тему(содержание)
@app.route('/topic_view/<int:id>', methods=['GET', 'POST'])
def topic_view(id):
    if current_user.is_authenticated:
        topic = db_sess.query(Topic).filter_by(id=id).first()
        tasks = topic.tasks
        user_answers = list(map(lambda x: x.task_id, current_user.answer))

        return render_template('topic.html', topic=topic, tasks=tasks, user_answers=user_answers)
    else:
        return redirect('/register')


# Профиль личный
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    return render_template('profile.html', user=current_user)


# Удаление аккаунта
@app.route('/profile_delete/<int:id>', methods=['GET', 'POST'])
def profile_delete(id):
    user = db_sess.query(User).filter_by(id=id).first()
    if user:
        user_answers = db_sess.query(Answers).filter_by(user=user).all()
        if user_answers:
            for answer in user_answers:
                db_sess.delete(answer)
        if user.status == 'Студент':
            student = db_sess.query(Student).filter_by(user_id=user.id).first()
            if student:
                db_sess.delete(student)
        elif user.status == 'Преподаватель':
            teacher = db_sess.query(Teacher).filter_by(user_id=user.id).first()
            if teacher:
                db_sess.delete(teacher)

        # обновление JSON файла со всеми пользователями
        usersJson()

        db_sess.delete(user)
        db_sess.commit()

    return redirect('/')


# Профиль не личный
@app.route('/profile/<int:id>', methods=['GET', 'POST'])
def profileOther(id):
    user = db_sess.query(User).filter_by(id=id).first()

    return render_template('profile.html', user=user)


# Вход
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.name == form.name.data, User.surname == form.surname.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', message="Заполните все поля!", form=form)


# Регистрация для преподов
@app.route('/register_teacher', methods=['GET', 'POST'])
def register_teacher():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form, message="Пароли не совпадают")
        if db_sess.query(User).filter(User.name == form.name.data, User.surname == form.surname.data).first():
            return render_template('register.html', form=form, message="Такой пользователь уже есть")

        # создаем объект пользователя User
        user = User(
            name=form.name.data,
            surname=form.surname.data
        )

        avatar = request.files['avatar']
        if avatar:
            filename = secure_filename(avatar.filename)
            avatar_path = os.path.join(app.config['IMG_FOLDER'], filename)
            avatar.save(avatar_path)
            user.avatar = filename

        user.set_password(form.password.data)

        # создаем объект препода и связываем его с пользователем
        teacher = Teacher(user=user)

        # добавляем пользователя и препода в базу данных
        db_sess.add(user)
        db_sess.add(teacher)
        db_sess.commit()

        # обновление JSON файла со всеми пользователями
        usersJson()

        return redirect('/login')
    return render_template('register.html', form=form)


# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', form=form, message="Пароли не совпадают")
        if db_sess.query(User).filter(User.name == form.name.data, User.surname == form.surname.data).first():
            return render_template('register.html', form=form, message="Такой пользователь уже есть")

        # создаем объект пользователя User
        user = User(
            name=form.name.data,
            surname=form.surname.data
        )

        avatar = request.files['avatar']
        if avatar:
            filename = secure_filename(avatar.filename)
            avatar_path = os.path.join(app.config['IMG_FOLDER'], filename)
            avatar.save(avatar_path)
            user.avatar = filename

        user.set_password(form.password.data)

        # создаем объект студента и связываем его с пользователем
        student = Student(group=form.group.data, user=user)

        # добавляем пользователя и студента в базу данных
        db_sess.add(user)
        db_sess.add(student)
        db_sess.commit()

        # обновление JSON файла со всеми пользователями
        usersJson()

        return redirect('/login')
    return render_template('register.html', form=form)


# Редактирование своего профиля
@app.route('/profile_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    form = ProfileEdit()
    user = db_sess.query(User).filter_by(id=id).first()

    if request.method == "GET":
        if user:
            form.name.data = user.name
            form.surname.data = user.surname
            form.password.data = user.hashed_password
            if user.status == 'Студент':
                form.group.data = user.student[0].group
        else:
            abort(404)

    if form.validate_on_submit():
        if user:
            try:
                edit_user = db_sess.query(User).filter_by(name=form.name.data, surname=form.surname.data).first()
                if edit_user and edit_user.id != user.id:
                    return render_template('edit_profile.html', form=form, status=user.status,
                                           message="Пользователь с такими инициалами уже есть.")
                # Редактирование аватарки (без учета расширения)
                avatar = request.files['avatar']
                if avatar:
                    filename = secure_filename(avatar.filename)
                    avatar_path = os.path.join(app.config['IMG_FOLDER'], filename)
                    print(avatar_path)

                    avatar.save(avatar_path)
                    if user.avatar:
                        old_avatar_path = os.path.join(app.config['IMG_FOLDER'], user.avatar)
                        os.remove(old_avatar_path)
                    db_sess.query(User).filter(User.id == user.id).update({User.avatar: filename})

                # Редактирование других данных профиля пользователя
                # Обновляем имя пользователя и группу студента (нельзя 2 сессии одновремено, поэтому update)
                user.set_password(form.password.data)
                db_sess.query(User).filter_by(id=user.id).update({User.name: form.name.data,
                                                                  User.surname: form.surname.data})
                if user.status == 'Студент':
                    db_sess.query(Student).filter_by(user=user).update({Student.group: form.group.data})

                # Сохраняем изменения
                db_sess.commit()

                return redirect(f'/profile/{id}')
            except Exception as e:
                db_sess.rollback()
                print(e)
        else:
            abort(404)

    return render_template('edit_profile.html', form=form, status=user.status)

                # <!-- {% if current_user.student %}
                # <div class="field">
                #     {{ form.group.label(for="group", class="label") }}
                #     {{ form.group(class="input", id="group") }}
                #     {% for error in form.group.errors %}
                #     <p class="alert alert-danger" role="alert">
                #     {{ error }}
                #     </p>
                #     {% endfor %}
                # </div>
                # {% endif %} -->


                        # <!-- {% if current_user.student %}
                        # <div class="status__value">
                        #     Студент
                        # </div>
                        # <div class="group">
                        #     {{ current_user.student[0].group }}
                        # </div>
                        # {% else %}
                        # <div class="status__value">
                        #     Преподаватель
                        # </div>
                        # {% endif %} -->



if __name__ == '__main__':
    main()