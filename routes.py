from data.operations import operations
from dataTreatment.createStructure import createStructure
from dataTreatment.dataCleanup import readCSV
from dataTreatment.dataInsertion import dataInsertion
from flask import Blueprint, render_template, request
from data.orient_setup import dbConectar
from forms.RecomendationByFilmForm import RecomendationByFilmForm
from forms.RecomendationByUserForm import RecomendationByUserForm
from forms.SearchMoviesForm import SearchMoviesForm
from forms.SearchUsersForm import SearchUsersForm
from utils.dataConverter import discretize_ocupacion, discretize_age

my_routes = Blueprint('my_routes', __name__)

# Conexion con las base de datos
print("---Conectando a la base de datos---")
client = dbConectar("Pruebas", "root", "123456")

# TODO Solo descomentar esto cuando se tenga que entregar el proyecto

# Lectura y preparacion de los datos leidos desde los csv
print("---Preparando datos para la insercion---")
[moviesDf, ratingDf, usersDf] = readCSV("ml-1m")

print("---Creando estructura de la base de datos con indices---")
createStructure(client)

# La insercion tiene como 20000 tuplas que no valen porque se han borrado mas de 800000 registros del archivo
# original de Ratings (tenia 1000000 y explotaba). Asi que el tamaño practico de la base de datos es el siguiente:
# 3883 peliculas
# 4500 usuarios
# 80853 ratings
# Aviso importante, tarda en ejecutar unos 3 min porque OrientDB es un poco lento al insertar datos ya que
# los replica en varios clusters internos

print("---Insertando datos en OrientDB---")
dataInsertion(client, moviesDf, ratingDf, usersDf)
print("---Datos insertados correctamente =)---")

dao = operations(client)

print("---Aplicacion iniciada---")


@my_routes.route('/', methods=["GET", "POST"])
def index():
    form = RecomendationByFilmForm()
    response = []
    if form.is_submitted():
        title = request.form['title']
        number = request.form['number']
        response = dao.findSimilarMovies(title, number)

    return render_template('pages/index.html', form=form, response=response)


@my_routes.route('/recommendation_by_user', methods=["GET", "POST"])
def recommendation_by_user():
    form = RecomendationByUserForm()
    response = []
    if form.is_submitted():
        userId = request.form['userId']
        number = request.form['number']

        response = dao.recommendMoviesGivenUserV2(userId, number)

    return render_template('pages/recommendation_by_user.html', form=form, response=response)


@my_routes.route('/search_users', methods=["GET", "POST"])
def search_users():
    form = SearchUsersForm()
    response = []
    if form.is_submitted():
        ocupation = request.form['ocupation']
        age = request.form['age']
        gender = request.form['gender']
        number = request.form['number']

        ocupation = discretize_ocupacion(ocupation)
        age = discretize_age(int(age))

        response = dao.searchUsers(ocupation, age, gender, number)

    return render_template('pages/search_users.html', form=form, response=response)


@my_routes.route('/search_movies', methods=["GET", "POST"])
def search_movies():
    form = SearchMoviesForm()
    response = []
    if form.is_submitted():
        categories = request.form.getlist('categories')
        number = request.form['number']

        response = dao.searchMovies(categories, number)

    return render_template('pages/search_movies.html', form=form, response=response)
