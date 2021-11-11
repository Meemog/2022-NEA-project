import requests
import json
import random
import re

class wordGenerator:
    def __init__(self):
        #private so API key cant be accessed outside this object
        self.__API_KEY = "031542d08a5d97e13560b759e3094416"

    #function to get a response object with 100 songs
    def __getSong(self):
        #private as it does not need to be accessed outside the object
        #string with the request for list of top 100 songs that have lyrics is made
        payload = f"chart.tracks.get?apikey={self.__API_KEY}&country=us&f_has_lyrics=1&explicit=0&page_size=100"
        #encoded using UTF-8 (default for encode())
        str(payload).encode()
        #uses response library to make request to the correct domain
        response = requests.get("https://api.musixmatch.com/ws/1.1/" + payload)
        return response

    #function to get lyrics of a specific track
    def __getLyrics(self, trackID):
        #private as it does not need to be accessed outside the object
        #string with API request to retrieve lyrics for given trackID
        payload = f"track.lyrics.get?apikey={self.__API_KEY}&track_id={trackID}"
        str(payload).encode()
        response = requests.get("https://api.musixmatch.com/ws/1.1/" + payload)
        return response

    #cuts lyrics down to certain length and removes newlines
    def __cutLyrics(self, lyrics, length):
        #private as it does not need to be accessed outside the object
        #splits the lyrics string with eithe a space or newline character
        lyrics = re.split(" |\n", lyrics)
        newLyrics = ""
        #adds length number of words to a string
        for i in range(length + 1):
            newLyrics += f"{lyrics[i]} "
        return newLyrics

    #main function that is to generate a number of words to be displayed in the game
    def getWordsForProgram(self, numberOfWords):
        #public as it is effectively the main() of this class
        #converts list of songs to json format
        words = self.__getSong().json()
        tracknames = []
        #makes list of all tracks, this is in json format so other necessary information is also passed with it 
        for track in words['message']['body']['track_list']:
            tracknames.append(track['track'])

        #gets a random track
        randomTrack = tracknames[random.randint(0, len(tracknames)) - 1]

        #returns string with numberOfWords words
        return (self.__cutLyrics((self.__getLyrics(randomTrack['track_id']).json())['message']['body']['lyrics']['lyrics_body'], numberOfWords))

wordGen = wordGenerator()
print(wordGen.getWordsForProgram(50))