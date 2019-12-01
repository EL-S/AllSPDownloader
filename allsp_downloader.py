import os
import requests
from bs4 import BeautifulSoup

episode_start = 1 #1 first ep
episode_end = 300 #293 last ep so far

directory = "Episodes/"

# improve speed
# find a better way to get the source

def init():
    global directory
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)

def download_episodes(episode_start,episode_end=episode_start):
    global directory
    for i in range(episode_start,episode_end):
        try:
            url = "http://allsp.ch/l.php?id={}".format(i)
            page = requests.get(url).text
            soup = BeautifulSoup(page, "lxml")
            video_src_container = soup.find("iframe").get("src")
            try:
                if (video_src_container != "ads/300.php"):
                    
                    response = requests.get(video_src_container)
                    episode_container_page = response.content
                    soup = BeautifulSoup(episode_container_page, "lxml")

                    video_src_uri = soup.find("script").text.strip().split('[{"play_url":"')[1].split('","format_id":')[0].replace(r"\u003d", "=").replace(r"\u0026", "&")
                    host = video_src_uri.split("/")[2]
                    headers={'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Accept-Language': 'en-US, en; q=0.5',
                            'Connection': 'Keep-Alive',
                            'Host': host,
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'}
                    print("Downloading Episode: {}".format(i))
                    video_data = requests.get(video_src_uri, headers=headers)
                    with open(directory+"South Park - EP{}.mp4".format(i), "wb") as file:
                        file.write(video_data.content)

                    print("Downloaded Episode: {}".format(i))
                else:
                    print("No Episode Available {}".format(i))
            except:
                print("Can't open video_src or stream (Episode {})".format(i))
        except:
            print("Can't find video or page (Episode {})".format(i))

init()

download_episodes(episode_start,episode_end)


