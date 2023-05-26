import json
import random
import sqlite3
from backend.utils import BayesianSort, Model


class TitleData:
    def __init__(self, title_id) -> None:
        self.title_id = title_id

    def get_title_data(self):
        """
        return title info based on title_id: movie title, type, year, genre, rating, number of votes, director, writer, actors
        """
        
        sql = f"SELECT * FROM title_basics WHERE tconst = ?"
        input_data = (self.title_id, )
        result = Model(sql, input_data).get_sqlite_data()
        
        return result
    
    
class SortTitles:
    def __init__(self, title_data, titles_data) -> None:
        self.title_data = title_data
        self.titles_data = titles_data
        self.rating_list = json.loads(self.title_data[0][6])

    def bayesian_sort(self):
        if self.titles_data is not None:
            return BayesianSort(self.titles_data).sort_movies(self.rating_list[0], self.rating_list[1])
        else:
            return []
    

class Crew:
    def __init__(self, title_id) -> None:
        """
        The title_id (identifier) represents the ID of the selected title for which we are seeking suggestions. 
        """
        self.title_id = title_id
        self.title_data = TitleData(self.title_id).get_title_data()

    
    def get_data_with_condition(self, value, same_value: bool, column, table):
        """
        value -- director name, actor name, or writer name; same_value -- True = exact value, False = partial match; column -- column name; table -- table name
        """
        operator = "=" if same_value else "LIKE"
        value_operator = value if same_value else f"%{value}%"

        title_type = self.title_data[0][1]

        with sqlite3.connect("backend/data/imdb.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT * FROM {table} WHERE {column} {operator} ? AND tconst != ? AND titleType = ?",
                (value_operator, self.title_id, title_type)
            )
            result = cursor.fetchall()

        return result

        
    def get_director_titles(self):
        """
        Select a title with the same director as input.
        Returns one title with the same director.
        """
        if len(self.title_data) > 0 and len(self.title_data[0]) > 7 and self.title_data[0][7] is not None:
            director = self.title_data[0][7] # PROBLEM
            result = self.get_data_with_condition(director, True, 'director', 'title_basics')
            result = SortTitles(self.title_data, result).bayesian_sort()[:5]
            if result:
                result = random.choice(result)
        else:
            result = []
        return result


    def get_writer_titles(self):
        """
        select writer title rated like input
        return one title with same writer
        """
        if len(self.title_data) > 0 and len(self.title_data[0]) > 8 and self.title_data[0][8] is not None:
            writer = self.title_data[0][8]
            result = self.get_data_with_condition(writer, True, 'writer', 'title_basics')
            result = SortTitles(self.title_data, result).bayesian_sort()[:5]
            if result:
                result = random.choice(result)
        else:
            result = []
        
        return result

    def get_leading_actor_titles(self):
        """
        finds titles with selected actor, Bayesian sort and extracts 3 results with highest score then randomly choose one
        return one random title with same actor
        """

        if len(self.title_data) > 0 and len(self.title_data[0]) > 9 and self.title_data[0][9] is not None:
            actors = json.loads(self.title_data[0][9])
            actors_data = self.get_data_with_condition(actors[0], False, "actors", "title_basics")
            result = SortTitles(self.title_data, actors_data).bayesian_sort()[:5]
            if result:
                result = random.choice(result)
        else:
            result = []
        
        return result

    def get_suporting_actor_titles(self):
        """
        select actor title rated like input
        return one title with same actor
        """

        if len(self.title_data) > 0 and len(self.title_data[0]) > 9 and self.title_data[0][9] is not None:
            actors = json.loads(self.title_data[0][9])
            actors_data = self.get_data_with_condition(actors[1], False, "actors", "title_basics")
            result = SortTitles(self.title_data, actors_data).bayesian_sort()[:5]
            if result:
                result = random.choice(result)
            
        else:
            result = []
        
        return result
    
    def crew_suggestions(self):

        suggestions = []

        # add director title
        director_title = self.get_director_titles()
        if director_title:
            suggestions.append(director_title)

        # add writer title
        writer_title = self.get_writer_titles()
        if writer_title and writer_title not in suggestions:
            suggestions.append(writer_title)

        leading_actor_titles = self.get_leading_actor_titles()
        if leading_actor_titles and leading_actor_titles not in suggestions:
            suggestions.append(leading_actor_titles)

        supporting_actor_titles = self.get_suporting_actor_titles()
        if supporting_actor_titles and supporting_actor_titles not in suggestions:
            suggestions.append(supporting_actor_titles)

        return suggestions

# FINISHED
# print(Crew("tt0084255").crew_suggestions())
# print(Crew("tt0018714").get_leading_actor_titles())

# FINISHED
class GenreAndYear:
    def __init__(self, title_id) -> None:
        """
        title_id is the id of selected move that we are looking for suggestions
        """
        self.title_id = title_id
        self.title_data = TitleData(self.title_id).get_title_data()
        self.type = self.title_data[0][1]
        self.year = self.title_data[0][4]
        self.genre = self.title_data[0][5]
        self.rating = json.loads(self.title_data[0][6])[0]
        self.votes = json.loads(self.title_data[0][6])[1]

    def get_same_genre_titles(self):
        
        """
        first: selecting complete db data by genre. Complete genre list and first genre, without duplicates
        """

        sql = "SELECT * FROM title_basics WHERE genres = ? AND titleType = ?"
        input_data = (self.genre, self.type)
        result = Model(sql, input_data).get_sqlite_data()

        result = [list(x) for x in result]
        
        return result

    def sort_genre_results(self):
        data = self.get_same_genre_titles()

        # selected title year
        year = self.year

        # add weight element (titles closer to selected year have stronger weight)
        for i in data:
            if year != i[4]:
                weight = 1/abs(year - i[4])
                i.append(round(weight,2))

        # sort by weight
        data_sort_year = sorted(data, key=lambda x: float(x[10]) if len(x) > 10 and isinstance(x[10], (int, float, str)) else float('-inf'), reverse=True)[:200]
        
        # remove weight from result
        for x in data_sort_year:
            x.pop()
        
        #convert it back to list of tuples
        result = [tuple(x) for x in data_sort_year]

        # Bayesian sort
        result = SortTitles(self.title_data, result).bayesian_sort()

        return result[:20]

        

class ClearAndMergeResults:
    def __init__(self, title_id):
        self.title_id = title_id
        self.title_data = TitleData(title_id).get_title_data()
    
    def merge_results(self):
        crew_data = Crew(self.title_id).crew_suggestions()
        genre_data = GenreAndYear(self.title_id).sort_genre_results()

        suggestions = crew_data

        for title in genre_data:
            if not title[0] in crew_data and len(suggestions) < 15:
                suggestions.append(title)      
        
        random.shuffle(suggestions)
        return suggestions



#print(TitleData("tt0018714").get_title_data())
#print(GenreAndYear("tt0084255").sort_genre_results())

# FINISHED        

#print(ClearAndMergeResults("tt0023590").merge_results())