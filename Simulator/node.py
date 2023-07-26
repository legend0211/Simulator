import cnn
import random
import numpy as np
from global_arrays import prediction_array
import global_arrays as ga
import settings
_,_,_,event_probability = settings.main()

def print_array(arr):
    with open('pred.txt', 'w') as f:
        np.savetxt(f, arr, fmt='%d')

def array_generator(node_index, fps):
    
    if(ga.cnt[node_index] > 0):
        ga.cnt[node_index] = ga.cnt[node_index] - 1
        frame = 1
    else:
        probability = [1-float(event_probability), float(event_probability)]
        choices = [0, 1]
        value = random.choices(choices, probability)[0]
        # value = random.randint(1,1000)
        # if(value % 200 == 0):
        if(value == 1):
            ga.cnt[node_index] = 30
            ga.value = 1
        else:
            ga.value = 0
        frame = 0

    # Make prediction using i-frame
    prediction_array[ga.count_pred[node_index]][node_index] = cnn.predict(frame)
    
    ga.count_pred[node_index] += 1

def main(fps, nodes):
    for i in range(nodes):
        array_generator(i, fps)
    
    print_array(prediction_array)
    
