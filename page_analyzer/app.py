from flask import Flask, render_template, request, redirect, url_for, flash
from page_analyzer.utils import validate_url, normalize_url, get_url_data
from page_analyzer.env_manager import get_secret_key
import page_analyzer.db_manager as db


app = Flask(__name__)
app.config["SECRET_KEY"] = get_secret_key()


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/urls")
def urls_list():
    urls = db.get_urls()
    return render_template("/urls.html", urls=urls)


@app.post("/urls")
def add_site():
    url_name = request.form.get("url")

    url_name = normalize_url(url_name)
    error = validate_url(url_name).get("error")
    url = validate_url(url_name).get("url")

    match error:
        case "exists":
            id = db.get_urls_by_name(url).get("id")
            flash("Страница уже существует", "info")
            return redirect(url_for("url_show", id=id))
        case "empty_url":
            flash("URL обязателен", "danger")
            return render_template("index.html", url=url), 422
        case "incorrect_url":
            flash("Некорректный URL", "danger")
            return render_template("index.html", url=url), 422
        case "size":
            flash("URL превышает 255 символов", "danger")
            return render_template("index.html", url=url), 422

    db.add_url(url)
    flash("Страница успешно добавлена", "success")

    url_id = db.get_urls_name(url).get("id")

    return redirect(url_for("url_show", id=url_id))


@app.get("/urls/<int:id>")
def url_show(id):
    url = db.get_urls_by_id(id)
    checks = db.get_checks_by_url_id(id)
    return render_template("url_id.html", url=url, checks=checks, id=id)


@app.post("/urls/<int:id>/checks")
def url_check(id):
    url = db.get_urls_by_id(id)["name"]
    if not url:
        flash("Страница не найдена", "danger")
        return redirect(url_for("index"))
    try:
        check = get_url_data(url)
        check["url_id"] = id
        db.add_url_check(check)
        flash("Страница успешно проверена", "success")
        return redirect(url_for("url_show", id=id))
    except Exception:
        flash("Произошла ошибка при проверке", "danger")
        return redirect(url_for("url_show", id=id))
