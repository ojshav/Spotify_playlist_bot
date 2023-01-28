from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = "42bbc2ac5c434d45afbc014ad5e2d22c"
SPOTIFY_CLIENT_SECRET = "30718f778d904eadadacb77151aad261"
SPOTIFY_REDIRECT_URI = "https://example.com/callback/"

SPOTIFY_SCOPE = "playlist-modify"


# ------------------- Scrape Billboard Charts ------------------------
date = input("Which date would you like to relive? (yyyy-mm-dd)")
year = date.split("-")[0]

URL = "https://www.billboard.com/charts/hot-100/"

response = requests.get(URL + date).text

soup = BeautifulSoup(response, "html.parser")

songtitle_list = [songtitle.text.strip() for songtitle in
                  soup.find_all(name="h3", id="title-of-a-story", class_="a-no-trucate")]
artist_list = [artist.text.strip() for artist in soup.find_all(name="span", class_="a-no-trucate")]
print(songtitle_list)
print(artist_list)






sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=SPOTIFY_REDIRECT_URI,
                                               scope=SPOTIFY_SCOPE))
user = sp.current_user()["id"]




spotify_song_uris = []

for song in songtitle_list:
    index = songtitle_list.index(song)
    result = sp.search(f"{song} {artist_list[index]}")
    #### much better results by search for song name and artist without year
    ########################################################################
    try:
        spotify_song_uris.append(result["tracks"]["items"][0]["uri"])
    except IndexError:
        print(song)
        print(artist_list[index])
        print("Could not find this song")

print(spotify_song_uris)

# ------------------- Spotify create playlist ------------------------

response = sp.user_playlist_create(user, f"{date} Billboard 100")
playlist_id = response["id"]

# ------------------- Spotify add songs ------------------------

result = sp.playlist_add_items(playlist_id, spotify_song_uris)
