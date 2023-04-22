

def createStructure(client):
    if not client.command('SELECT FROM ( SELECT expand(classes) FROM metadata:schema ) WHERE name = "Movie"'):
        client.command("CREATE CLASS Movie EXTENDS V")
        client.command("CREATE PROPERTY Movie.MovieID INTEGER")
        client.command("CREATE PROPERTY Movie.Title STRING")
        client.command("CREATE PROPERTY Movie.Genres EMBEDDEDLIST STRING")

        client.command("CREATE INDEX Movie.MovieID ON Movie (MovieID) UNIQUE")
        client.command("CREATE INDEX Movie.Title ON Movie (Title) FULLTEXT ENGINE LUCENE")
        client.command("CREATE INDEX Movie.Genres ON Movie (Genres) NOTUNIQUE_HASH_INDEX")

    if not client.command('SELECT FROM ( SELECT expand(classes) FROM metadata:schema ) WHERE name = "User"'):
        client.command("CREATE CLASS User EXTENDS V")
        client.command("CREATE PROPERTY User.UserID INTEGER")
        client.command("CREATE PROPERTY User.Gender STRING")
        client.command("CREATE PROPERTY User.Age INTEGER")
        client.command("CREATE PROPERTY User.Occupation INTEGER")
        client.command("CREATE PROPERTY User.ZipCode STRING")

        client.command("CREATE INDEX User.UserID ON User (UserID) UNIQUE")

    if not client.command('SELECT FROM ( SELECT expand(classes) FROM metadata:schema ) WHERE name = "Rating"'):
        client.command("CREATE CLASS Rating EXTENDS E")
        client.command("CREATE PROPERTY Rating.UserID INTEGER")
        client.command("CREATE PROPERTY Rating.MovieID INTEGER")
        client.command("CREATE PROPERTY Rating.Rating INTEGER")
        client.command("CREATE PROPERTY Rating.Timestamp DATE")

        client.command("CREATE INDEX Rating.UserID.MovieID ON Rating(UserID, MovieID) UNIQUE")
