import json
import sqlite3

class BayesianSort():
    def __init__(self, data) -> None:
        self.data = data

    def bayesian_calculations(self):
        """
        calulates average rating and average number of votes for Bayesian calculation
        return: [average rating, average number of votes]
        """
        movie_data = self.data
        num_movies = len(movie_data)
        total_rating = 0
        total_num_votes = 0
        for movie in movie_data:
            rating_list = json.loads(movie[6])
            total_num_votes += rating_list[1]
            total_rating += rating_list[0]
        avg_rating = total_rating / num_movies
        avg_num_votes = total_num_votes / num_movies
        
        return [avg_rating, avg_num_votes]
        
    def bayesian_score(self, movie_rating, movie_num_votes):
        """
        sort movies by rating and number of votes
        return: [title, title_type, year]
        """
        bayesian_calculations = self.bayesian_calculations()

        avg_rating = bayesian_calculations[0]
        avg_num_votes = bayesian_calculations[1]
        smoothing_factor=5
        
        bayesian_score = (avg_num_votes * avg_rating + movie_num_votes * movie_rating) / (avg_num_votes + movie_num_votes)
        bayesian_score = (smoothing_factor * avg_rating + movie_num_votes * bayesian_score) / (smoothing_factor + movie_num_votes)
        return bayesian_score

    def sort_movies(self, movie_rating, movie_num_votes):
        """
        Sorts the list of selected movies using Bayesian calculation
        Returns: [[movie_title, year, movie_type]]
        """
        sorted_movies = sorted(self.data, key=lambda x: self.bayesian_score(json.loads(x[6])[0], json.loads(x[6])[1]), reverse=True)
        return [[movie[0], movie[2], movie[4], movie[5], movie[6]] for movie in sorted_movies]

class Model:
    def __init__(self, sql_query, input_tuple) -> None:
        self.sql_query = sql_query
        self.input_tuple = input_tuple

    def get_sqlite_data(self):
        with sqlite3.connect("backend/data/imdb.db") as connection:
            cursor = connection.cursor()
            cursor.execute(self.sql_query, self.input_tuple)
            result = cursor.fetchall()
        
        return result

def linear_ponder_generator():
    numbers = []

    # Calculate the common difference for the linear relationship
    common_difference = 100 / 15

    # Generate the numbers
    for i in range(5, 0, -1):
        num = i * common_difference
        numbers.append(num)

    sum_numbers_list = sum(numbers)
    numbers = [round(num/sum_numbers_list, 2) for num in numbers]
    
    return numbers



# print(linear_ponder_generator())
