import requests
import json
import random

class WordGenerator:
    def __init__(self):
        #private so API key cant be accessed outside this object
        file = open("APIKEY.txt", "r")
        self.__API_KEY = file.readline()  

    #function to get a response object with 100 songs
    def __GetSong(self):
        #private as it does not need to be accessed outside the object
        #string with the request for list of top 100 songs that have lyrics is made
        payload = f"chart.tracks.get?apikey={self.__API_KEY}&country=us&f_has_lyrics=1&explicit=0&page_size=100"
        #uses response library to make request to the correct domain
        response = requests.get("https://api.musixmatch.com/ws/1.1/" + payload)
        #converts list of songs to json format
        response = response.json()
        #gets a random track_id
        tracks = response["message"]["body"]["track_list"]
        randomTrack = tracks[random.randint(0, len(tracks) - 1)]["track"]["track_id"]
        return randomTrack

    #function to get lyrics of a specific track
    def __GetLyrics(self, trackID):
        #private as it does not need to be accessed outside the object
        #string with API request to retrieve lyrics for given trackID
        payload = f"track.lyrics.get?apikey={self.__API_KEY}&track_id={trackID}"
        str(payload).encode()
        response = requests.get("https://api.musixmatch.com/ws/1.1/" + payload).json()
        response = response["message"]["body"]["lyrics"]["lyrics_body"]
        return response
    
    #cuts lyrics down to certain length and removes newlines
    def __CutLyrics(self, lyrics, length):
        #private as it does not need to be accessed outside the object
        #cuts out watermark at the end of string so that if the length required is longer than the actual lyrics it will loop
        lyrics = lyrics.split("...")[0]
        lyrics = lyrics.lower()
        lyrics = list(lyrics)

        #Replaces newlines with spaces
        x = 0
        while x <= len(lyrics) - 1:
            if lyrics[x] == '\n':
                lyrics[x] = " "

            x += 1

        #Removes duplicate spaces
        x = 0
        while x < len(lyrics) - 1:
            if lyrics[x] ==  " " and lyrics[x+1] == " ":
                lyrics.pop(x)
            else:
                x += 1

        newLyrics = ""
        #adds length number of words to a string

        x = 0
        spaces = 0

        #counts spaces
        while length >= spaces:
            #loops to the front of the string if lyrics runs out of words
            if x == len(lyrics) - 1:
                x = 0

            #appends word from lyrics to newLyrics 
            newLyrics += lyrics[x]
            if lyrics[x] == " ":
                spaces += 1
            x += 1

        return newLyrics

    #main function that is to generate a number of words to be displayed in the game
    def GetWordsForProgram(self, numberOfWords):
        #public as it is effectively the main() of this class
        #returns string with numberOfWords words
        return self.__CutLyrics(self.__GetLyrics(self.__GetSong()), numberOfWords)