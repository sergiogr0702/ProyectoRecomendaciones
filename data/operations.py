from sortedcontainers import SortedDict
import itertools


# TODO Añadir filtro para comprobar que la pelicula existe
def findSimilarMovies(client, movie_title):
    usersIDList = []

    recommendedMovies = SortedDict()

    movieQuery = "SELECT MovieID FROM Movie WHERE Title LIKE '%{}%' LIMIT 1".format(movie_title)

    movieID = client.command(movieQuery)[0].oRecordData['MovieID']

    usersQuery = "SELECT FROM (TRAVERSE in('Rating') FROM (SELECT FROM Movie WHERE Title LIKE '%{}%') " \
                 "MAXDEPTH 1) WHERE @class = 'User'".format(movie_title)

    results = client.command(usersQuery)

    for item in results:
        user_props = item.oRecordData
        userID = user_props['UserID']

        ratingsQuery1 = "SELECT FROM Rating WHERE UserID={} AND MovieID={} LIMIT 1".format(userID, movieID)

        ratingResult = client.command(ratingsQuery1)

        if ratingResult:
            rating = ratingResult[0].oRecordData

            if rating['Rating'] == 5:
                usersIDList.append(userID)

    for UId in usersIDList:
        moviesQuery = "SELECT FROM (TRAVERSE out('Rating') FROM (SELECT FROM User WHERE UserID = '{}') " \
                      "MAXDEPTH 1) WHERE @class = 'Movie' AND MovieID != {}".format(UId, movieID)

        movies = client.command(moviesQuery)

        for movie in movies:
            movie_props = movie.oRecordData

            ratingsQuery2 = "SELECT FROM Rating WHERE UserID={} AND MovieID={} LIMIT 1".format(UId,
                                                                                               movie_props['MovieID'])

            rating = client.command(ratingsQuery2)[0].oRecordData

            if rating['Rating'] == 5:
                if movie_props['Title'] not in recommendedMovies:
                    recommendedMovies[movie_props['Title']] = 1
                else:
                    recommendedMovies[movie_props['Title']] += 1

    # Convert the TreeMap items to a list of tuples
    tree_map_items = list(recommendedMovies.items())

    # Sort the list by the second element of each tuple in descending order
    sorted_tree_map_items = sorted(tree_map_items, key=lambda x: x[1], reverse=True)

    # Print the TreeMap in descending order
    # It returs a diccionary with the title and the number of 5 star votes
    # TODO CAMBIAR POR RETURN AL IMPLEMENTAR
    for key, value in sorted_tree_map_items:
        print(key, " : ", value)


def compute_similarity_score(user1_props, user2_props, target_user_ratings, other_user_ratings):
    gender_weight = 5
    age_weight = 10
    occupation_weight = 1
    zipcode_weight = 1
    rating_weight = 20

    gender_similarity = int(user1_props['Gender'] == user2_props['Gender']) * gender_weight
    age_similarity = int(user1_props['Age'] == user2_props['Age']) * age_weight
    occupation_similarity = int(user1_props['Occupation'] == user2_props['Occupation']) * occupation_weight
    zipcode_similarity = int(user1_props['ZipCode'] == user2_props['ZipCode']) * zipcode_weight

    user1_movies = set(target_user_ratings.keys())
    user2_movies = set(other_user_ratings.keys())
    common_movies = user1_movies.intersection(user2_movies)
    rating_diff = 0
    for movie_id in common_movies:
        rating_diff += abs(target_user_ratings[movie_id] - other_user_ratings[movie_id])
    rating_diff *= rating_weight

    total_similarity = gender_similarity + age_similarity + occupation_similarity + zipcode_similarity
    total_movies = len(user1_movies.union(user2_movies))
    if total_movies == 0:
        movie_similarity = 0
    else:
        movie_similarity = len(common_movies) / total_movies

    similarity_score = (total_similarity + rating_diff) * movie_similarity
    return similarity_score


def recommendMoviesGivenUser(client, target_user_id):
    # Step 1: Retrieve the info of the target user
    query = "SELECT UserID, Age, Gender, Occupation, ZipCode FROM User WHERE UserID = {} LIMIT 1"
    target_user_props = client.command(query.format(target_user_id))[0].oRecordData

    # Step 2: Retrieve the info  of all other users
    other_users_props = {}
    query = "SELECT UserID, Age, Gender, Occupation, ZipCode FROM User WHERE NOT (UserID = {}) ORDER BY UserID"
    results = client.command(query.format(target_user_id))
    for item in results:
        user_props = item.oRecordData
        if user_props['UserID'] != target_user_id:
            other_users_props[user_props['UserID']] = user_props

    # Step 3: Retrieve the ratings of the target user
    target_user_ratings = {}
    query = "SELECT MovieID, Rating FROM Rating WHERE UserID = {}"
    results = client.command(query.format(target_user_id))
    for item in results:
        movie_id = item.MovieID
        rating = item.Rating
        target_user_ratings[movie_id] = rating

    # Step 4: Retrieve the ratings of all other users
    other_users_ratings = {}
    query = "SELECT UserID, MovieID, Rating FROM Rating WHERE NOT (UserID = {}) ORDER BY UserID"
    results = client.command(query.format(target_user_id))
    for user_id, group in itertools.groupby(results, key=lambda x: x.UserID):
        if user_id != target_user_id:
            ratings = {}
            for item in group:
                movie_id = item.MovieID
                rating = item.Rating
                ratings[movie_id] = rating
            other_users_ratings[user_id] = ratings

    # Step 5: Compute the similarity between the target user and each other user based on their ratings
    similarity_scores = {}
    for user_id, ratings in other_users_ratings.items():
        similarity = compute_similarity_score(target_user_props, other_users_props[user_id], target_user_ratings, ratings)
        similarity_scores[user_id] = similarity

    # Step 6: Find the most similar user(s) to the target user
    most_similar_users = sorted(similarity_scores, key=similarity_scores.get, reverse=True)[
                         :20]  # Replace 5 with the number of most similar users you want to find

    # Step 7: Retrieve the movies ids that the most similar user(s) rated highly but the target user has not rated
    recommended_movies = []
    for user_id in most_similar_users:
        query = "SELECT MovieID, Rating FROM Rating WHERE UserID = {} AND MovieID NOT IN [{}]"
        rated_movie_ids = ','.join(str(movie_id) for movie_id in target_user_ratings.keys())
        results = client.command(query.format(user_id, rated_movie_ids))
        for item in results:
            movie_id = item.MovieID
            rating = item.Rating
            if rating >= 4:  # Replace 4 with the minimum rating required for a movie to be recommended
                recommended_movies.append(movie_id)
    recommended_movies = list(set(recommended_movies))  # Remove duplicates

    # Step 8: Retrieve the movies titles of the obtained ids
    query = "SELECT Title FROM Movie WHERE MovieID IN [{}]"
    movie_ids = ','.join(str(movie_id) for movie_id in recommended_movies)
    results = client.command(query.format(movie_ids))

    # Extract the titles from the result list
    titles = [result.Title for result in results]

    # TODO CAMBIAR POR RETURN AL IMPLEMENTAR
    print(titles)