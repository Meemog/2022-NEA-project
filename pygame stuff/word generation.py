import requests
import json

def getWords():
    request = "chart.tracks.get?chart_name=top&page=1&page_size=5&country=it&f_has_lyrics=1"
    response = requests.get("http://api.musixmatch.com/ws/1.1/", request)
    return response

words = getWords()  
print(words.json())
#this is a wip, waiting on api code