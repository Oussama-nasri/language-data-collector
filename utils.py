import requests
import re
import pafy
def verify_youtube_link(url):
    #Check if the link is a youtube link
    youtube_pattern = r'^(https?://)?(www\.)?(m\.)?(youtube\.com/(watch\?v=[a-zA-Z0-9_-]{11}(\&[a-zA-Z0-9_=-]+)*|v/[a-zA-Z0-9_-]{11}(\?[a-zA-Z0-9_=-]+)*))|(youtu\.be/[a-zA-Z0-9_-]{11}(\?[a-zA-Z0-9_=-]+)?)$'

    youtu_be_pattern = r'^(https?://)?(www\.)?youtu\.be/[a-zA-Z0-9_-]{11}(\?[a-zA-Z0-9_=-]+)?$'

    if re.match(youtube_pattern, url) or re.match(youtu_be_pattern, url):
        #Verify that link is for available video
        request = requests.get(url).text
        if "unavailable_video.png" in request:
            print("The youtube link does not exist")
            return False
        else:
            return True
    else:
        print("The link appears to be not a youtube link")
        return False
    
def check_youtube_duration(url):
    pattern = r'"approxDurationMs":"(\d+)"'
    request = requests.get(url).text
    match = re.search(pattern, request)
    if match:
        return int(match.group(1))  # Convert the captured number to an integer
    else:
        return None
    


if __name__ == "__main__":
        "dur="
        "approxDurationMs"
        urls = [
        "https://www.youtube.com/watch?v=GWERih5c4mM",
        "http://youtube.com/watch?v=-wtIMTCHWuI",
        "http://m.youtube.com/watch?v=-wtIMTCHWuI",
        "http://www.youtube.com/watch?v=yZv2daTWRZU&feature=em-uploademail",
        "http://www.youtube.com/watch?v=0zM3nApSvMg#t=0m10s",
        "http://www.youtube.com/watch?v=cKZDdG9FTKY&feature=channel",
        "http://www.youtube.com/watch?v=lalOy8Mbfdc&feature=youtu.be",
        "http://www.youtube.com/v/dQw4w9WgXcQ",
        "http://youtu.be/-wtIMTCHWuI",
        "http://youtu.be/dQw4w9WgXcQ?feature=youtube_gdata_player"

        ]
        for url in urls :
            print(check_youtube_duration(url))
