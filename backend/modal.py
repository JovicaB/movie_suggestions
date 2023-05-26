import requests
import bs4
import json


class TitleInfo:
    def __init__(self, title_id) -> None:
        self.title_id = title_id

    def request_data(self):
        imdb_url = "https://www.imdb.com/title/" + self.title_id + "/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        response = requests.get(imdb_url, headers=headers)

        soup = bs4.BeautifulSoup(response.content, "html.parser")

        script_tag = soup.find("script", {"type": "application/ld+json"})
        if script_tag is None:
            # Handle the case when the script tag is not found
            return {}

        try:
            json_data = json.loads(script_tag.text)
        except json.JSONDecodeError:
            # Handle the case when JSON decoding fails
            return {}

        return json_data


    def modal_data(self):
        data = self.request_data()
        title = data.get("name")
        year = data.get("datePublished")[:4] if data.get("datePublished") else None

        synopsis = data.get("description")
        director = data.get("director")
        director_name = director[0].get("name") if director else None
        actors = data.get("actor")
        actors_names = [name['name'] for name in actors]
        genre = data.get("genre")
        
        aggregate_rating = data.get("aggregateRating")
        rating_value = aggregate_rating.get("ratingValue") if aggregate_rating else None
        rating_count = aggregate_rating.get("ratingCount") if aggregate_rating else None
        ratings = f"{rating_value} ({rating_count})" if rating_value and rating_count else None
        trailer = data.get("trailer")['embedUrl'] if data.get("trailer") else None
        image = data.get("image")

        title_dict = {
            'title': title,
            'year': year,
            'director': director_name,
            'actors': actors_names,
            'synopsis': synopsis,
            'genre': genre,
            'ratings': ratings,
            'trailer': trailer,
            'image': image
        }
        return title_dict



print(TitleInfo("tt0120663").modal_data())
