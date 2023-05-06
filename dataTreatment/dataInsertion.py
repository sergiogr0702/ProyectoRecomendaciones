def dataInsertion(client, moviesDf, ratingDf, usersDf):
    if not client.command('SELECT FROM ( SELECT expand(classes) FROM metadata:schema ) WHERE name = "Movie"'):
        print("-----Inserting Movies------")
        for index, row in moviesDf.iterrows():
            genres = row['Genres'].split("|")
            genres_str = ", ".join(["'{}'".format(genre) for genre in genres])
            query = "INSERT INTO Movie SET MovieID={}, Title='{}', genres=[{}]".format(row['MovieID'], row['Title'],
                                                                                       genres_str)
            print(index, " : ", query)
            client.command(query)

    if not client.command('SELECT FROM ( SELECT expand(classes) FROM metadata:schema ) WHERE name = "User"'):
        print("-----Inserting Users------")
        for index, row in usersDf.iterrows():
            query = "INSERT INTO User SET UserID={}, Gender='{}', Age={}, Occupation={}, ZipCode='{}'" \
                .format(row['UserID'], row['Gender'], row['Age'], row['Occupation'], row['ZipCode'])

            print(index, " : ", query)
            client.command(query)

    if not client.command('SELECT FROM ( SELECT expand(classes) FROM metadata:schema ) WHERE name = "Rating"'):
        print("-----Inserting Ratings------")
        for index, row in ratingDf.iterrows():
            # Check if the User and Movie nodes exist
            userExists = client.command("SELECT COUNT(*) FROM User WHERE UserID = {}".format(row['UserID']))[0].oRecordData[
                'COUNT']
            movieExists = \
                client.command("SELECT COUNT(*) FROM Movie WHERE MovieID = {}".format(row['MovieID']))[0].oRecordData[
                    'COUNT']

            if userExists > 0 and movieExists > 0:
                query = "CREATE EDGE Rating FROM (SELECT FROM User WHERE UserID={}) TO (SELECT FROM Movie WHERE MovieID={}) " \
                        "SET UserID={}, MovieID={}, Rating={}, Timestamp='{}'" \
                    .format(row['UserID'], row['MovieID'], row['UserID'], row['MovieID'], row['Rating'], row['Timestamp'])

                # Execute the query
                print(index, " : ", query)
                client.command(query)
            else:
                print(index, " : ", "User with ID {} or Movie with ID {} does not exist".format(row['UserID'], row['MovieID']))
