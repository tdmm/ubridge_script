import  time
import json
# from urllib import request ,parse
import  requests
import xlrd
import logging
import threading



boxid = "phoenix"
signature = "xXjKY0v0bzMQvCCm84U8gIqoDQnRz8GlafXO3Ao8qdy1499wH/KsviwvJwDj0D9MwSIxnh5qX0HrLobRpZcgnSY2ivD7Y7ggHs2mXGJ" \
            "o9wECZ3gtWRbVN5yVjPsebM0Ua74nqzAgD2IWtCJCASQaO2Tztvz0g1bdlXpHe8ZmfXgr1M7E0iXYaAj8QnjQu6xAhkT67AxqRGkQzHK" \
            "q1zENka3k+3L0NttHQAURvasiG9wC28dtcZoC2OVKODWrvhQb8VikWqTCm2D6yfe1NoOGE9U7RJdoERM9LycJFwYXzDA="

i = 0
firt_time =0

# 为线程定义一个函数
def print_time():

   while 1:

      send_coin_url(threading.current_thread().name)
   #   print(threading.current_thread().name, i )

def send_coin_url(str):
    body = {"boxid":boxid,"signature":signature}
    url = 'http://localhost:3259/box/heartbeat'
    r = requests.post(url, data=body)
    time.sleep(1.0001)
    global i
    i = i + 1
    now =time.time()
    peer =i/(now - firt_time)
    print(str,"the time",i,r.text,"every second:",peer)

if __name__ == '__main__':

    firt_time = time.time()


    j =1
    while j>0:
        j=j-1
        time.sleep(0.001)
        t = threading.Thread(target=print_time, name="Thread"+j.__str__())
        t.start()




    # t1 = threading.Thread(target=print_time, name="Thread-1")
    # t2 = threading.Thread(target=print_time, name="Thread-2")
    # t1.start()
    # t2.start()
