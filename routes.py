from data.operations import operations
from dataTreatment.createStructure import createStructure
from dataTreatment.dataCleanup import readCSV
from dataTreatment.dataInsertion import dataInsertion
from flask import Blueprint, render_template, request
from data.orient_setup import dbConectar
from forms.RecomendationByFilmForm import RecomendationByFilmForm
from forms.RecomendationByUserForm import RecomendationByUserForm

my_routes = Blueprint('my_routes', __name__)

# Conexion con las base de datos
print("---Conectando a la base de datos---")
client = dbConectar("Pruebas", "root", "123456")

# TODO Solo descomentar esto cuando se tenga que entregar el proyecto
""""
# Lectura y preparacion de los datos leidos desde los csv
print("---Preparando datos para la insercion---")
[moviesDf, ratingDf, usersDf] = readCSV("C:\\Users\\Usuario\\Desktop\\UNI\\2\\RIBW\\TrabajoRIBW\\ml-1m")

print("---Creando estructura de la base de datos con indices---")
createStructure(client)

# La insercion tiene como 20000 tuplas que no valen porque se han borrado mas de 800000 registros del archivo
# original de Ratings (tenia 1000000 y explotaba). Asi que el tamaño practico de la base de datos es el siguiente:
# 3883 peliculas
# 4500 usuarios
# 80853 ratings
# Aviso importante, tarda en ejecutar unos 5 min porque OrientDB es un poco lento al insertar datos ya que 
# los replica en varios clusters internos

print("---Insertando datos en OrientDB---")
dataInsertion(client, moviesDf, ratingDf, usersDf)
print("---Datos insertados correctamente =)---")
"""

dao = operations(client)


@my_routes.route('/', methods=["GET", "POST"])
def index():
    form = RecomendationByFilmForm()
    response = []
    if form.is_submitted():
        title = request.form['title']  # Get the value of the 'title' field
        response = dao.findSimilarMovies(title)

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


@my_routes.route('/search_users')
def search_users():
    return render_template('pages/search_users.html')


@my_routes.route('/search_movies')
def search_movies():
    return render_template('pages/search_movies.html')
