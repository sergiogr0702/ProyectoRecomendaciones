from flask import Blueprint, render_template, request

from forms.RecomendationByFilmForm import RecomendationByFilmForm

my_routes = Blueprint('my_routes', __name__)


@my_routes.route('/', methods=["GET", "POST"])
def index():
    form = RecomendationByFilmForm()
    response = []
    if form.is_submitted():
        title = request.form['title']  # Get the value of the 'title' field
        print(f"Submitted title: {title}")

        response.append({'title': 'Home', 'genres': ['genre1', 'genre2', 'genre3', 'genre3', 'genre3', 'genre3', 'genre3', 'genre3', 'genre3', 'genre3', 'genre3']})
        response.append({'title': 'About', 'genres': ['genre1', 'genre2']})
        response.append({'title': 'Pics', 'genres': ['genre1']})

    return render_template('pages/index.html', form=form, response=response)


@my_routes.route('/recommendation_by_user')
def recommendation_by_user():
    return render_template('pages/recommendation_by_user.html')


@my_routes.route('/search_users')
def search_users():
    return render_template('pages/search_users.html')


@my_routes.route('/search_movies')
def search_movies():
    return render_template('pages/search_movies.html')
