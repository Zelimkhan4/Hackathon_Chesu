import json

import requests
import bs4
import flask_login
from flask import Flask, render_template, url_for, redirect
from forms.register import RegisterForm
from forms.login import LoginForm
from data import db_session
from data.User import User
from flask import session
from flask_login import LoginManager, login_user, logout_user, login_required
import schedule
from flask import request
from PIL import Image
from io import BytesIO


app = Flask(__name__)
app.config["SECRET_KEY"] = "Hackathon_Chesu"
login_manager = LoginManager(app)
login_manager.init_app(app)
parsed_data = []
current_location = "50,50"
current_size = "650,450"


def parse_data():
    global parsed_data
    res = requests.get("https://chechnyatoday.com/content").text
    soup = bs4.BeautifulSoup(res, features="lxml")
    for div in soup.findAll("div", class_="row archive-item"):
        desc = div.find("a").text.strip()
        image_link = div.find("img")["src"].strip()
        parsed_data.append([desc, image_link])


@app.route("/geodata")
def trans_tracker():
    res = requests.get(f"https://static-maps.yandex.ru/1.x/?ll={current_location}&z=12&l=map,sat&size={current_size}")
    image = Image.open(BytesIO(res.content))
    image.save("./static/images/image.png")
    return render_template("geodata.html", image="./static/images/image.png")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
def index():
    global parsed_data
    return render_template("main.html", data=parsed_data)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        sess = db_session.create_session()
        user = sess.query(User).filter(User.email == form.email.data).first()
        if user.check_password(form.password.data):
            login_user(user)
            return redirect("/")
        return render_template("login.html", form=form, message="Пользователь с такими данными не найден")
    return render_template("login.html", form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("register.html", form=form, message="Пароли не совпадают")
        sess = db_session.create_session()
        if sess.query(User).filter(User.email == form.email.data).first():
            return render_template("register.html", form=form, message="Такой пользователь уже есть")
        # Такого пользователя нет, поэтому можем зарегать
        user = User(name=form.name.data, surname=form.surname.data, email=form.email.data,
                    passport_number=form.passport_number.data)
        user.set_password(form.password.data)
        sess.add(user)
        sess.commit()
        return redirect("/")
    return render_template("register.html", form=form)


if __name__ == "__main__":
    parse_data()
    db_session.global_init("db/database.sqlite")
    schedule.every(1).hours.do(lambda: parse_data())
    app.run(host="0.0.0.0", debug=True)
