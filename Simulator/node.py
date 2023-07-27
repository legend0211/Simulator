import cnn
import random
import numpy as np
from global_arrays import prediction_array
import global_arrays as ga
import settings
_,_,_,event_probability,_ = settings.main()

def print_array(arr):
    with open(r'output\pred.txt', 'w') as f:
        np.savetxt(f, arr, fmt='%d')

def array_generator(node_index, fps):
    # Check if event is happening
    if(ga.cnt[node_index] > 0):
        ga.cnt[node_index] = ga.cnt[node_index] - 1
        frame = 1
    # Check if event will happen or not based on probability
    else:
        probability = [1-float(event_probability), float(event_probability)]
        choices = [0, 1]
        value = random.choices(choices, probability)[0]
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
        # Observing if the event is occuring or not
        array_generator(i, fps)
    
    print_array(prediction_array)