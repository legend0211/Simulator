import os
import time
import cnn
import random
import threading
import numpy as np
from queue import Queue
from global_arrays import prediction_array

def print_array(arr):
    cnt =0
    while True:
        with open('pred.txt', 'w') as f:
            np.savetxt(f, arr, fmt='%d')
        print(cnt)
        cnt += 10
        time.sleep(9)
        
def file_writer(q, filename):
    while True:
        arr = q.get()
        with open(filename, 'a') as f:
            np.savetxt(f, [arr], fmt='%d')
        q.task_done()

def array_generator(node_index, q, fps, filename):
    value, cnt = 0, 0
    ii = 0
    while True:    
        # frame_size = (1920, 1080)
        # frame = np.zeros((frame_size[1], frame_size[0], 3), dtype=np.uint8)           # BLACK
        # frame = np.ones((frame_size[1], frame_size[0], 3), dtype=np.uint8) * 255      # WHITE
                    
        if(cnt > 0):
            cnt = cnt - 1
            frames = []
            frames.append(int(1))
        else:
            value = random.randint(1,1000)
            if(value % 200 == 0):
                cnt = 30
                value = 1
            else:
                value = 0

            frames = []
            frames.append(int(0))

        # Make prediction using i-frame
        prediction_array[ii][node_index] = cnn.predict(frames)

        q.put(frames)
        
        ii += 1
        time.sleep(1)

def main(fps, nodes):
    queues = []
    for i in range(nodes):
        q = Queue()
        queues.append(q)

    file_threads = []
    for i in range(nodes):
        filename = os.path.join('video', f'video_{i+1}.txt')
        t = threading.Thread(target=file_writer, args=(queues[i], filename))
        t.start()
        file_threads.append(t)

    array_threads = []
    for i in range(nodes):
        filename = os.path.join('video', f'video_{i+1}.txt')
        q = queues[i]
        t = threading.Thread(target=array_generator, args=(i, q, fps, filename))
        t.start()
        array_threads.append(t)
    
    t = threading.Thread(target=print_array, args=(prediction_array,))
    t.start()

    for q in queues:
        q.join()

# prediction_array = [[0] * 30 for _ in range(86400)]

# main(30,30)
