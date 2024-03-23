import requests
import os
import json


class TMDB:
    def __init__(self, api_key):
        self.api_key = api_key

    def discover_movies(self, params):
        url = "https://api.themoviedb.org/3/discover/movie"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "accept": "application/json",
        }
        response = requests.get(url, headers=headers, params=params)
        return response.json()


if __name__ == "__main__":
    params = {
        "include_adult": "false",
        "include_video": "false",
        "language": "en-US",
        "page": "1",
        "sort_by": "popularity.desc",
        "primary_release_year": "2023",
    }

    tmdb = TMDB(os.environ.get("TMDB_API_KEY"))
    res = tmdb.discover_movies(params)
    print(json.dumps(res, indent=4))
    print(res["results"][0].keys())
    print(len(res["results"]))
    print(res.keys())

    for movie in res["results"]:
        print(movie["title"])
        print(
            movie["poster_path"]
        )  # https://image.tmdb.org/t/p/w200/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg
