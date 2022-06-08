import json
import os

import requests

from Refresh import Refresh


class SaveSongs:
    def __init__(self, playlistIdToSync, playlistIdsToAdd):
        self.user_id = os.environ.get("SPOTIFY_USER_ID")
        self.spotify_token = self.call_refresh()
        self.playlistToSync = playlistIdToSync
        self.playlistToAdd = playlistIdsToAdd
        self.playlistToSyncTracks = self.get_playlist_tracks(playlistIdToSync)
        self.tracksToAdd = []
        self.find_playlist_to_sync()

    def find_playlist_to_sync(self):
        nrOfSongs = 0
        for playlistId in self.playlistToAdd:
            tracks = self.get_playlist_tracks(playlistId)
            for i in tracks:
                if i not in self.playlistToSyncTracks:
                    self.tracksToAdd.append(i)
            nrOfSongs += len(tracks)
        # print(self.tracksToAdd)
        print("nr of songs to add: " + str(len(self.tracksToAdd)))
        print("total nr of songs in playlists: " + str(nrOfSongs))

    def get_playlist_tracks(self, playlistId):
        tracks = []
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlistId)
        response_json = self.get_next_tracks(query)
        for i in response_json["tracks"]['items']:
            tracks.append(i["track"]["uri"])

        if response_json["tracks"]["next"] is not None:
            response_json = self.get_next_tracks(response_json["tracks"]["next"])
            for i in response_json['items']:
                tracks.append(i["track"]["uri"])
            while response_json["next"] is not None:
                response_json = self.get_next_tracks(response_json["next"])
                for i in response_json['items']:
                    tracks.append(i["track"]["uri"])

        return tracks

    def get_next_tracks(self, uri):
        response = requests.get(uri, headers={"content-type": "application/json",
                                              "Authorization": "Bearer {}".format(
                                                  self.spotify_token)})
        return response.json()

    @staticmethod
    def call_refresh():
        refreshCaller = Refresh()
        return refreshCaller.refresh()


a = SaveSongs("1q73eSEEJ6q99aua79qXP4?si=2c87b78f4ff04101",
              ["5PngbJOftkO1hi4RBnBIaM?si=1a6a044adce54c18", "1hw99deRNbyB5cogPPipin?si=c8a982a991674585"])
