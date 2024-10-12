import os
from dotenv import load_dotenv
from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   flash)
from page_analyzer.utils import validate_url, get_url_data
from page_analyzer.db_manager import (get_urls,
                                      add_url,
                                      get_urls_by_name,
                                      get_urls_by_id,
                                      add_url_check,
                                      get_checks_by_url_id)


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/urls')
def urls_list():
    urls = get_urls()
    return render_template('/urls.html', urls=urls)


@app.post('/urls')
def add_site():
    url_name = request.form.get('url')
    error = validate_url(url_name).get('error')
    url = validate_url(url_name).get('url')

    if error:
        flash(error, 'danger')
        return redirect(url_for('index'))

    add_url(url)
    flash('Страница успешно добавлена', 'success')

    url_id = get_urls_by_name(url).get('id')

    return redirect(url_for('url_show', id=url_id))


@app.get('/urls/<int:id>')
def url_show(id):
    url = get_urls_by_id(id)
    checks = get_checks_by_url_id(id)
    return render_template('url_id.html', url=url, checks=checks,  id=id)


@app.post('/urls/<int:id>/checks')
def url_check(id):
    url = get_urls_by_id(id)['name']
    if not url:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('index'))
    try:
        check = get_url_data(url)
        check['url_id'] = id
        add_url_check(check)
        flash('Страница успешно проверена', 'success')
        return redirect(url_for('url_show', id=id))
    except Exception:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('url_show', id=id))
