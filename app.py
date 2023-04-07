import os
import sys
from data.orient_setup import dbConectar
from dataTreatment.createStructure import createStructure
from dataTreatment.dataCleanup import readCSV
from dataTreatment.dataInsertion import dataInsertion
from flask import Flask

from routes import my_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)

app.register_blueprint(my_routes)

if __name__ == '__main__':
    if sys.argv.__len__() != 5:
        print("Error:El programa se necesita ejecutar de la siguiente manera: python app.py <directory_with_csv's> "
              "<database_name> <username_in_db> <password_of_db>")
        sys.exit(1)

    # Conexion con las base de datos
    print("---Conectando a la base de datos---")
    client = dbConectar(sys.argv[2], sys.argv[3], sys.argv[4])

    # TODO Solo descomentar esto cuando se tenga que entregar el proyecto
    """"
    # Lectura y preparacion de los datos leidos desde los csv
    print("---Preparando datos para la insercion---")
    [moviesDf, ratingDf, usersDf] = readCSV(sys.argv[1])
    
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

    print("---Lanzando aplicación---")
    app.run()

    client.close()
