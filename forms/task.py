from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, RadioField, FieldList, FormField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional


# class TaskForm(FlaskForm):
#     title = StringField("Название", validators=[DataRequired()])
#     # task_type = SelectField("Тип задания", choices=[('ТЕСТ', 'ТЕСТ'), ('КРОССВОРД', 'КРОССВОРД'),
#     #                                                 ('СООТНЕСТИ', 'СООТНЕСТИ'), ('ХРОНОЛОГИЯ', 'ХРОНОЛОГИЯ')])
#
#     questions = RadioField('Варианты ответа', validators=[DataRequired()], choices=[])
#
#     def add_choice(self):
#         num_choices = len(self.questions.choices)
#         letter = chr(ord('A') + num_choices)
#         choice = (letter, '')
#         self.questions.choices.append(choice)
#
#     submit = SubmitField('Применить')


# class TaskForm(FlaskForm):
#     title = StringField("Название", validators=[DataRequired()])
#
#     # questions = FieldList(FormField(QuestionForm), min_entries=1)
#
#     submit = SubmitField('Применить')
#
# class QuestionForm(FlaskForm):
#     question = StringField('Question')
#     answer_choice = FieldList(StringField('Answer Choice'))
#     right_choice = StringField('Right Choice')
#
# class QuestionsForm(FlaskForm):
#     questions = FieldList(FormField(QuestionForm))
#     submit = SubmitField('Submit')
#
#
#

# class QuestionForm(FlaskForm):
#     question = StringField('Вопрос', validators=[Optional()])
#     answer_choice = FieldList(StringField('Варианты ответа', validators=[Optional()]), min_entries=2, max_entries=2)
#     right_choice = StringField('Правильный ответ', validators=[Optional()])


# class TaskForm(FlaskForm):
#     title = StringField('Название задания', validators=[Optional()])
#     questions = FieldList(FormField(QuestionForm), min_entries=1, max_entries=1)
#     submit = SubmitField('Создать задание')
#
#     def create_questions(self):
#         questions = []
#         for question_form in self.questions:
#             if question_form.question.data:
#                 question = {'question': question_form.question.data,
#                             'answer_choice': question_form.answer_choice.data,
#                             'right_choice': question_form.right_choice.data}
#
#                 questions.append(question)
#         return questions

class AddAnswerForm(FlaskForm):
    add_answer_choice = StringField('1 Вариант ответа', validators=[DataRequired()])


class QuestionForm(FlaskForm):
    question = StringField('Вопрос', validators=[DataRequired()])
    answer_choice = FieldList(StringField('1 Вариант ответа', validators=[DataRequired()]), min_entries=1)
    right_choice = StringField('Правильный ответ', validators=[DataRequired()])


class TaskForm(FlaskForm):
    title = StringField('Название задания', validators=[DataRequired()])
    questions = FieldList(FormField(QuestionForm), min_entries=1)
    submit = SubmitField('Создать задание')


# class TaskForm(FlaskForm):
#     title = StringField('Название задания', validators=[DataRequired()])
#     questions = FieldList(FormField(QuestionForm))
#     submit = SubmitField('Создать задание')
#
#     # def create_questions(self):
#     #     questions = []
#     #     for question_form in self.questions:
#     #         question = {'question': question_form.question.data,
#     #                     'answer_choice': question_form.answer_choice.data,
#     #                     'right_choice': question_form.right_choice.data
#     #                     }
#     #         questions.append(question)
#     #     return questions
#
#
#     # изменить количество вопросов, нажав на кнопку
#     # def name(self):
#     #     self.questions.choices.append(choice)
#
#     def create_questions(self):
#         questions = []
#         for question_form in self.questions:
#             if question_form.question.data:
#                 question = {'question': question_form.question.data,
#                             'answer_choice': question_form.answer_choice.data,
#                             'right_choice': question_form.right_choice.data}
#                 print(question)
#                 del question['csrf_token']
#                 print(question)
#
#                 questions.append(question)
#         return questions


