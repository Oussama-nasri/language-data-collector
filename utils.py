import requests
import urllib.request
def verify_youtube_link(link):
    #Verify that link is for available video
    r = requests.get("https://www.youtube.com/watch?v=48415").text
    if "unavailable_video.png" in r:
        print(True)
    else:
        print(False)
    

if __name__ == "__main__":
    verify_youtube_link("hi")