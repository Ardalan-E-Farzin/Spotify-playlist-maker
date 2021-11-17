import requests
from bs4 import BeautifulSoup
import lxml
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# ------------------------BILLBOARD----------------------#
date = input("What date you are looking for (YYY-MM_DD)? ")
response_for_billboard = requests.get(f"https://www.billboard.com/charts/rock-songs/{date}")
source = response_for_billboard.text
list_soup = BeautifulSoup(source, "lxml")
ranks = list_soup.findAll(name="div", class_="chart-list-item__rank ")
songs = list_soup.findAll(name="span", class_="chart-list-item__title-text")
# artist_name = list_soup.findAll(name="span", class_="chart-element__information__artist "
#                                                     "text--truncate color--secondary")
ranks_number = [rank.getText() for rank in ranks]
song_name = [song.getText() for song in songs]
# artists_list = [artist.getText() for artist in artist_name]
# print(ranks_number[0])
# print(song_name)
# print(artists_list[0])

# ------------------------SPOTIFY----------------------#
Client_ID = "###"
Client_Secret = "###"
URL = "http://example.com"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                                                    redirect_uri=URL,
                                                    client_id=Client_ID,
                                                    client_secret=Client_Secret,
                                                    show_dialog=True,
                                                    cache_path="token.txt"))
user_id = spotify.current_user()["id"]
song_uris = []
year = date.split("-")[0]
for song in song_name:
    result = spotify.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
# print(song_uris)
playlist = spotify.user_playlist_create(user=user_id, name=f"{date} 100 Billboard", public=False)
print(playlist["id"])
spotify.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
