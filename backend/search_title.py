import json
import sqlite3


class MovieSearcher:
    def __init__(self, search_keyword: str) -> None:
        self.search_keyword = search_keyword.title()

    def get_keyword_data(self):
        """
        find movie titles based on the inputed keyword
        return {title: [type, rating, number of votes]}
        """
        connection = sqlite3.connect("backend/data/imdb.db")
        cursor = connection.cursor()
        cursor.execute('''
            SELECT tconst, primaryTitle, titleType, startYear, rating_votes FROM title_basics WHERE primaryTitle LIKE ?
            ''', ('%' + self.search_keyword + '%',))
        rows = cursor.fetchall()
        connection.close()

        return rows
    
    def sort(self):
        data_for_processing = self.get_keyword_data()

        def custom_sort_key(row):
            title = row[1]
            starts_with_keyword = title.startswith(self.search_keyword)
            keyword_match = title == self.search_keyword

            return (not starts_with_keyword, not keyword_match, -json.loads(row[4])[0])

        rows = sorted(data_for_processing, key=custom_sort_key)[:15]

        return [[row[0], row[1], row[3], json.loads(row[4])[0]] for row in rows]

   

    # def sort_secondary_keys(self):
    #     data_for_processing = self.get_keyword_data()

    #     # sorts result using two conditions with lambda: average rating and year (descending).
    #     rows = sorted(data_for_processing, key=lambda x: (
    #         json.loads(x[4])[0], -x[3]), reverse=True)[:20]
    #     print(rows)
    #     result = [[row[0], row[1], row[3], json.loads(
    #         row[4])[0]] for row in rows if row[4] != None]

    #     return result

    # def search_results(self):
    #     set_primary_results = set(tuple(row)
    #                               for row in self.sort_primary_keys())
    #     set_secondary_results = set(tuple(row)
    #                                 for row in self.sort_secondary_keys())
    #     print(set_primary_results)

    #     grouped_results = list(set_primary_results) + \
    #         list(set_secondary_results - set_primary_results)

    #     convert_to_list = [list(element) for element in grouped_results]
    #     return convert_to_list[:15]


# FINISHED
# MovieSearcher('Rambo').sort()
