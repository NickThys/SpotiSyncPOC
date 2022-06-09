import os

import requests


class Refresh:
    def __init__(self):
        self.refresh_token = os.environ.get("SPOTIFY_REFRESH_TOKEN")
        self.base_64 = os.environ.get("BASE_64")

    def refresh(self):
        query = "https://accounts.spotify.com/api/token"
        response = requests.post(query, data={"grant_type": "refresh_token", "refresh_token": self.refresh_token},
                                 headers={"Authorization": "Basic " + self.base_64})
        return response.json()["access_token"]
