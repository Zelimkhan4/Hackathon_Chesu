import requests
from flask import Flask, render_template, url_for, redirect
from forms.register import RegisterForm
from forms.login import LoginForm
from data import db_session
from data.User import User
from flask_login import LoginManager, login_user, logout_user, login_required
from forms.order import OrderForm
from data.Estate import Estate

from parser_f import parse_news, parse_hospitals


app = Flask(__name__)
app.config["SECRET_KEY"] = "Hackathon_Chesu"
login_manager = LoginManager(app)
login_manager.init_app(app)
data_cache = []


def get_coords_from_address(data):
    global data_cache
    if not data_cache:
        if data:
            for est in data:
                base_url = "http://geocode-maps.yandex.ru/1.x/"
                params = {
                    "apikey": "9425a070-3065-43f1-be4f-8cfea45435ce",
                    "geocode": est.address,
                    "format": "json"
                 }
                req = requests.get(base_url, params=params)
                json_response = req.json()
                print(json_response)

                if req.status_code in (200, 300) and json_response["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]["found"] != "0":
                    toponym = json_response["response"]["GeoObjectCollection"][
                        "featureMember"][0]["GeoObject"]
                    toponym_coordinates = list(map(float, toponym["Point"]["pos"].split()))[::-1]

                    if not est.about is None:
                        r = est.about.strip()
                        data_cache.append([est.name.strip(), *toponym_coordinates, r.replace("\n", "")[:161]])
                    else:
                        data_cache.append([est.name.strip(), *toponym_coordinates, None])


@app.route("/map")
def map_():
    global data_cache
    db_sess = db_session.create_session()
    get_coords_from_address(db_sess.query(Estate).all())

    return render_template("map.html", data=data_cache)


@app.route("/hospitals", methods=["POST", "GET"])
def hospitals():
    db_sess = db_session.create_session()
    hosp = parse_hospitals("groznyiy")
    form = OrderForm()
    if form.validate_on_submit():
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template("/", message="Услуга успешно заказана")
    return render_template("order.html", form=form)


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
    data = parse_news()
    return render_template("map.html", data=data)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        sess = db_session.create_session()
        user = sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
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


@app.route("/3d_sample")
def around_view():
    link = None
    return render_template("around_view.html", link=link)


if __name__ == "__main__":
    db_session.global_init("db/database.sqlite")
    app.run(host="0.0.0.0", debug=True)
