import threading
import requests
import time

def chiamata(url):
    response = requests.request("GET", url)

start = time.time()
thlist = []
for i in range(19):
    thlist.append(threading.Thread(target=chiamata, args=("https://letterboxd.com/GiuDiMax/films/diary/page/"+str(i), )))
for thread in thlist:
    thread.start()
for thread in thlist:
    thread.join()
print(time.time()-start)