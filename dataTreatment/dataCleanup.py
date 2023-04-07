import os
import pandas as pd

# Set the display options to show all columns
pd.set_option('display.max_columns', None)


def readCSV(dirPath):
    # Get the current working directory
    current_dir = os.getcwd()

    # Use the os module to change the current working directory to the directory you want to open
    os.chdir(dirPath)

    moviesDf = pd.read_csv(dirPath + "\\movies.dat", sep="::", engine="python", header=None,
                           names=["MovieID", "Title", "Genres"], encoding='ANSI')
    ratingsDf = pd.read_csv(dirPath + "\\ratings.dat", sep="::", engine="python", header=None,
                            names=["UserID", "MovieID", "Rating", "Timestamp"])
    usersDf = pd.read_csv(dirPath + "\\users.dat", sep="::", engine="python", header=None,
                          names=["UserID", "Gender", "Age", "Occupation", "ZipCode"])

    # Remove apostrophes from all string columns
    moviesDf = moviesDf.apply(lambda x: x.str.replace("'", "") if x.dtype == "object" else x)
    ratingsDf = ratingsDf.apply(lambda x: x.str.replace("'", "") if x.dtype == "object" else x)
    usersDf = usersDf.apply(lambda x: x.str.replace("'", "") if x.dtype == "object" else x)

    ratingsDf['Timestamp'] = pd.to_datetime(ratingsDf['Timestamp'], unit='s')

    # Sort dataframe by UserID and Timestamp in descending order
    ratingsDf = ratingsDf.sort_values(['UserID', 'Timestamp'], ascending=[True, False])

    # Create a new dataframe to hold the sampled rows
    sampledDf = pd.DataFrame()

    # Iterate over each group in the grouped dataframe
    for group_name, group_df in ratingsDf.groupby('UserID'):
        # Calculate the number of rows to keep
        num_rows_to_keep = max(1, int(len(group_df) * 0.11))

        # Select the first num_rows_to_keep rows and append to the sampled dataframe
        sampledDf = pd.concat([sampledDf, group_df.head(num_rows_to_keep)], ignore_index=True)

    # Use os.chdir() again to change the current working directory back to the previous directory
    os.chdir(current_dir)

    return [moviesDf, sampledDf, usersDf]
