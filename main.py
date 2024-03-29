from dotenv import load_dotenv
from requests import post,get
import json
import pandas as pd
from auth import get_token,get_auth_header
from data import albums, artists
from imgdl import download_imgs

token = get_token()
##send request to web api
def spotify_search(token,album_name,artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f'?q={album_name.replace(" ","+")}+{artist_name.replace(" ","+")}&type=album&market=US&limit=1&offset=0'

    q_url = url + query
    result = get(q_url,headers=headers)
    json_result = json.loads(result.content)['albums']['items']
    if len(json_result) == 0:
        print("No album(s) found...")
        return None
    return {"Album":str(json_result[0]['name']),
            "Artist":str(json_result[0]['artists'][0]['name']),
            "Album Picture Url":str(json_result[0]['images'][1]['url'])}

album_data = []
print("Creating CSV...")
for album,artist in zip(albums, artists):
    album_id=spotify_search(token,album,artist)
    if album_id == None:
        album_data.append({"Album":"No Album Found","Artist":"None","Album Picture Url":"None"})
        print("No Album Found...")
    else:
        album_data.append(album_id)
        print(str(album_id) + ' added...')
top_albums = pd.DataFrame(album_data)

# change column positions.
new_cols = ['Artist','Album','Album Picture Url']
top_albums = top_albums.reindex(columns=new_cols)

# export 
if len(top_albums) > 5:
    export_csv = top_albums.to_csv(r'top-30-albums.csv',index=None,header = True)
else:
    export_csv = top_albums.to_csv(r'top-adds.csv',index=None,header = True)

print("Downloading Images...")
download_imgs(top_albums)
print("Done.")