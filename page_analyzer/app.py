import os
from dotenv import load_dotenv
from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for,
                   flash)
from page_analyzer.utils import validate_url
from page_analyzer.db_manager import (get_urls,
                                      add_url,
                                      get_urls_by_name,
                                      get_urls_by_id)


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

    return redirect(url_for('show_url', id=url_id))


@app.get('/urls/<int:id>')
def show_url(id):
    url = get_urls_by_id(id)
    return render_template('url_id.html', url=url, id=id)
