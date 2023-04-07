from pyorient import OrientDB
from data.PySocket import PySocket


def dbConectar(DATABASE_NAME: str, DB_USER: str, DB_PWD: str):
    HOST = "localhost"
    PORT = 2424

    socket = PySocket(HOST, PORT)
    socket.connect()
    client = OrientDB(socket)
    token = client.get_session_token()
    client.set_session_token(token)

    client.db_open(DATABASE_NAME, DB_USER, DB_PWD)

    print("CONEXIÓN REALIZADA")

    return client
