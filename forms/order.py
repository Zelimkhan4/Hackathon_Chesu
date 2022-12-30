from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired
import flask_login
from parser_f import parse_hospitals


class OrderForm(FlaskForm):
    name = StringField("Имя")
    surname = StringField("Фамилия")
    email = EmailField("Почта")
    medical_card = StringField("Медицинская карта")
    medical_institutions = SelectField("Выберите больницу", choices=parse_hospitals("groznyiy"))
    submit = SubmitField("Отправить")
