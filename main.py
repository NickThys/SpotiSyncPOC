import os
import requests
import logging
from Refresh import Refresh


class SaveSongs:
    def __init__(self):
        self.user_id = os.environ.get("SPOTIFY_USER_ID")
        self.spotify_token = self.call_refresh()
        self.playlistToSync = ""
        self.playlistToAdd = []
        self.playlistToSyncTracks = []
        self.tracksToAdd = []

    def sync_playlist(self, playlistIdToSync, playlistIdsToAdd):
        nrOfSongs = 0
        tracksToAdd = []
        playlistToSyncTracks = self.get_playlist_tracks(playlistIdToSync)
        print("------------------------------------")
        print("Sync playlist: " + self.get_playlist_name(playlistIdToSync))
        print("from playlist:")

        for playlistId in playlistIdsToAdd:
            print(self.get_playlist_name(playlistId))
            tracks = self.get_playlist_tracks(playlistId)
            for track in tracks:
                if track not in playlistToSyncTracks:
                    tracksToAdd.append(track)
            nrOfSongs += len(tracks)
        print("------------------------------------")
        self.post_new_songs(tracksToAdd, playlistIdToSync)

        print("------------------------------------")
        print("nr of songs to added: " + str(len(tracksToAdd)))
        print()

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

    def get_playlist_name(self, playlistId):
        query = "https://api.spotify.com/v1/playlists/{}".format(playlistId)
        response_json = self.get_request(query)
        return response_json["name"]

    def get_playlist_tracks(self, playlistId):
        tracks = []
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlistId)
        response_json = self.get_request(query)
        for i in response_json['items']:
            tracks.append(i["track"]["uri"])

        if response_json["next"] is not None:
            response_json = self.get_request(response_json["next"])
            for i in response_json['items']:
                tracks.append(i["track"]["uri"])
            while response_json["next"] is not None:
                response_json = self.get_request(response_json["next"])
                for i in response_json['items']:
                    tracks.append(i["track"]["uri"])

        return tracks

    def post_new_songs(self, tracks, playlistId):
        n = 100
        trackChunks = [tracks[i:i + n] for i in range(0, len(tracks), n)]
        for chunk in trackChunks:
            tracklist = self.make_comma_separated_list(chunk)
            response = self.post_songs(playlistId, tracklist)
            while "error" in response:
                songToDelete = response['error']['message'][19:]
                print("song to add manually: " + songToDelete[16:])
                song = []
                strLen = 15
                while len(song) != 1:
                    strLen += 1
                    song = [string for string in chunk if songToDelete[0:strLen] in string]
                chunk.remove(song[0])
                if len(chunk) != 0:
                    tracklist = self.make_comma_separated_list(chunk)
                    response = self.post_songs(playlistId, tracklist)
                else:
                    response.pop('error')

    def post_songs(self, playlistId, tracklist):
        response = requests.post(
            "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(playlistId, tracklist),
            headers={"content-type": "application/json",
                     "Authorization": "Bearer {}".format(
                         self.spotify_token)})
        return response.json()

    @staticmethod
    def make_comma_separated_list(tracks):
        trackList = ""
        for track in tracks:
            trackList += track + ","
        return trackList[:-1]

    def get_request(self, uri):
        response = requests.get(uri, headers={"content-type": "application/json",
                                              "Authorization": "Bearer {}".format(
                                                  self.spotify_token)})
        return response.json()

    @staticmethod
    def call_refresh():
        refreshCaller = Refresh()
        return refreshCaller.refresh()


# base playlists
country = "2hruTJvK3brxybteWid7Kb"
dutch = "51SDyMXGsNm78nHAyzius1"
studio_100 = "57fUeeCcT64L8EcWZn5pJ6"
gestappoKnallmuzik = "1X4u7Uf3lH4sr81dj8T7T1"
boysbands = "6YhbLW5eVotSmEai2WSe5h"
rock = "6OixDFDmJLktl7eCHnuQGH"
metal = "5a6w0edGwVWPmtH106uZ0X"
soundtracks = "4R3p6g4XjgcQPgPl1iBbHX"

# mixed playlists
mix = "78fXmzyr7HiD7mAE00FXTg"
Dutch_Country = "2YnlFTeZbwmujK0hRfLznQ"
Metal_Rock = "2ww6BZrSBOrgPkb9UzIm3I"
Dutch_Country_Studio100_GK_BB_Rock = "1oHBWcbOpZZgKq8wWIvceK"
Dutch_Country_Studio100 = "3ImR64RSbJODpd1VB5DNUv"
Dutch_Country_Studio100_BB_Rock = "15m96zT4vyVU60JisQT4vF"
Dutch_Studio100_GK_BB_Rock = "3wNp92Dimj8KHGKuMQ8UQj"
Dutch_Country_Studio100_Rock = "6kDQH7h02JvwGQrJLs3fd6"
Dutch_Country_Rock = "24lPtYaKv0SPKFPHC9c8iK"
Soundtrack_Studio100_GK_BB_Rock = "3L0J1pvc7sCPr77uOCCNlV"
a = SaveSongs()
a.sync_playlist(mix, [country, dutch, studio_100, gestappoKnallmuzik, boysbands, rock, metal, soundtracks])
logging.warning('Mix Synced')
a.sync_playlist(Dutch_Country, [country, dutch])
logging.warning('Dutch_Country Synced')
a.sync_playlist(Metal_Rock, [rock, metal])
logging.warning('Metal_Rock Synced')
a.sync_playlist(Dutch_Country_Studio100_GK_BB_Rock, [country, dutch, studio_100, gestappoKnallmuzik, boysbands, rock])
logging.warning('Dutch_Country_Studio100_GK_BB_Rock Synced')
a.sync_playlist(Dutch_Country_Studio100, [country, dutch, studio_100])
logging.warning('Dutch_Country_Studio100 Synced')
a.sync_playlist(Dutch_Country_Studio100_BB_Rock, [country, dutch, studio_100, boysbands, rock])
logging.warning('Dutch_Country_Studio100_BB_Rock Synced')
a.sync_playlist(Dutch_Studio100_GK_BB_Rock, [dutch, studio_100, gestappoKnallmuzik, boysbands, rock])
logging.warning('Dutch_Studio100_GK_BB_Rock Synced')
a.sync_playlist(Dutch_Country_Studio100_Rock, [country, dutch, studio_100, rock])
logging.warning('Dutch_Country_Studio100_Rock Synced')
a.sync_playlist(Dutch_Country_Rock, [country, dutch, rock])
logging.warning('Dutch_Country_Rock Synced')
a.sync_playlist(Soundtrack_Studio100_GK_BB_Rock, [studio_100, gestappoKnallmuzik, boysbands, rock, soundtracks])
logging.warning('Soundtrack_Studio100_GK_BB_Rock Synced')
