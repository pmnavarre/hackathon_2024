import requests
import json
import streamlit as st

PAGE_SIZE = 20


class TMDB:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "accept": "application/json",
        }

    def discover_movies(self, params: dict, num_movies: int = PAGE_SIZE) -> list:
        url = "https://api.themoviedb.org/3/discover/movie"
        response = []
        for i in range(num_movies // PAGE_SIZE):
            params["page"] = i + 1
            response += requests.get(url, headers=self.headers, params=params).json()[
                "results"
            ]
        return response

    def get_popular_movies(self) -> dict:
        url = "https://api.themoviedb.org/3/movie/popular"
        params = {"language": "en-US", "page": "1"}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def add_to_watchlist(self, media_id: str, account_id: str = "21124543") -> dict:
        url = f"https://api.themoviedb.org/3/account/{account_id}/watchlist"
        payload = {"media_type": "movie", "media_id": media_id, "watchlist": True}
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

    def get_watchlist(self, account_id: str = "21124543") -> dict:
        url = f"https://api.themoviedb.org/3/account/{account_id}/watchlist/movies"
        params = {
            "language": "en-US",
            "page": "1",
            "sort_by": "created_at.asc",
        }
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_request_token(self) -> dict:
        url = "https://api.themoviedb.org/3/authentication/token/new"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_movie_reviews(self, movie_id: str) -> dict:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?language=en-US&page=1"
        params = {"language": "en-US", "page": "1"}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_watch_providers(self, movie_id: str) -> dict:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def search_keyword(self, keyword: str) -> dict:
        url = "https://api.themoviedb.org/3/search/keyword"
        params = {"query": keyword}
        response = requests.get(url, headers=self.headers, params=params)
        return {res["name"]: res["id"] for res in response.json()["results"]}

    def get_actor_id(self, person_id: str) -> str:
        url = "https://api.themoviedb.org/3/search/person"
        params = {"query": person_id, "language": "en-US"}
        response = requests.get(url, headers=self.headers, params=params)
        return str(response.json()["results"][0]["id"])


if __name__ == "__main__":
    params = {
        "include_adult": "false",
        "include_video": "false",
        "language": "en-US",
        "page": "1",
        "sort_by": "popularity.desc",
        "primary_release_year": "2023",
    }
