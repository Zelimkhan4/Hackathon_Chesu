from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField('Имя')
    surname = StringField('Фамилия')
    email = EmailField('Почта')
    password = PasswordField('Пароль')
    password_again = PasswordField('Повторите пароль')
    passport_number = StringField("Серия и номер паспорта")
    submit = SubmitField('Войти')