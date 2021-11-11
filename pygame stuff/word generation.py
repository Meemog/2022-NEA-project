import requests
import json
import random
import re

API_KEY = "031542d08a5d97e13560b759e3094416"

def getWords(API_KEY):
    payload = f"chart.tracks.get?apikey={API_KEY}&country=us&f_has_lyrics=1&explicit=0&page_size=100"
    str(payload).encode()
    response = requests.get("https://api.musixmatch.com/ws/1.1/" + payload)
    return response

def getLyrics(API_KEY, trackID):
    payload = f"track.lyrics.get?apikey={API_KEY}&track_id={trackID}"
    str(payload).encode()
    response = requests.get("https://api.musixmatch.com/ws/1.1/" + payload)
    return response

#length in number of words
def cutLyrics(lyrics, length):
    lyrics = re.split(" |\n", lyrics)
    newLyrics = ""
    for i in range(length):
        newLyrics += f"{lyrics[i]} "
    return newLyrics

words = getWords(API_KEY).json()
tracknames = []
for track in words['message']['body']['track_list']:
    tracknames.append(track['track'])

randomTrack = tracknames[random.randint(0, len(tracknames)) - 1]

print(cutLyrics((getLyrics(API_KEY, randomTrack['track_id']).json())['message']['body']['lyrics']['lyrics_body'], 50))