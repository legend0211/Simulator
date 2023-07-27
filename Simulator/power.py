import copy
import numpy as np
from scipy.stats import pareto
from global_arrays import camera_no as a
from global_arrays import power_list as c
from global_arrays import prediction_array as p

def main(size, ii, sec):
    bb = 0
    var_arr = []
    
    boolean = 0
    b=copy.deepcopy(p[ii])
    if any(b):
        boolean = 1
        bb = 1
    
    c_0 = []
    c_1 = []
    for i in range(len(b)):
        if(b[i]==0):
            c_0.append(c[i])
        else:
            c_1.append(c[i])
    sorted_indices = np.argsort(b)
    a_sorted_b = []
    for i in sorted_indices:
        a_sorted_b.append(a[i])
    
    b.sort()
    a_0 = []
    a_1 = []
    for i in range(len(a_sorted_b)):
        if(b[i]==0):
            a_0.append(a_sorted_b[i])
        else:
            a_1.append(a_sorted_b[i])
    aa_0 = []
    aa_1 = []
    sorted_indices = np.argsort(c_0)
    for i in sorted_indices:
        aa_0.append(a_0[i])
    sorted_indices = np.argsort(c_1)
    for i in sorted_indices:
        aa_1.append(a_1[i])
    camera_list = aa_1 + aa_0
    
    # Pareto distribution
    if(boolean == 0):
        alpha = 100
    else:
        alpha = 5
    samples = pareto(alpha).rvs(size=size)
    total_sum = np.sum(samples)
    scaling_factor = (15 * size) / total_sum
    scaled_samples = samples * scaling_factor
    samples = np.clip(scaled_samples, 11, 24)
    rescaling_factor = (15 * size) / np.sum(samples)
    samples = samples * rescaling_factor
    
    if(bb == 0):
        samples = [15] * int(size)
    samples.sort()
       
    
    if(ii == 0):
        with open(r"output\camera_power.txt", 'w') as f:
            f.write("SAMPLE SECOND : "+str(ii+1)+"\n\n")
            for i in range(size):
                f.write(f"CCTV Camera {camera_list[(size-1)-i]}: {samples[i]:.5f} watts\n")
                c[camera_list[(size-1)-i]-1] += samples[i]
            f.write("================================================================\n\n")
    else:
        with open(r"output\camera_power.txt", 'a') as f:
            f.write("SAMPLE SECOND : "+str(ii+1)+"\n\n")
            for i in range(size):
                f.write(f"CCTV Camera {camera_list[(size-1)-i]}: {samples[i]:.5f} watts\n")
                c[camera_list[(size-1)-i]-1] += samples[i]
            f.write("================================================================\n\n")
            
    if(ii == sec-1):
        with open(r"output\camera_power.txt", 'a') as f:
            f.write("================================================================\n")
            f.write("================================================================\n")
            f.write(f"SAMPLE of {sec} SECONDS : \n\n")
            for i in range(size):
                f.write(f"CCTV Camera {i}: Average {(c[i]/sec):.5f} watts\n")
                var_arr.append(c[i]/sec)
            f.write(f"\nVariance = {np.var(var_arr)}\n")
            f.write("================================================================\n\n")
        return 1