import math
import random
from global_arrays import kiosk_for_cam

def distance(num_points, kiosks):
    grid_size = 5000

    # Generate a list of all possible grid points
    all_points = [(x, y) for x in range(grid_size) for y in range(grid_size)]
    
    # Select "x" random points from the list
    random_kiosks = random.sample(all_points, kiosks)
    kiosk_index = [i+1 for i in range(kiosks)]
    with open(r'output\Camera details.txt', 'w') as f:
        f.write(f"Kiosk details : \n")
        for i in kiosk_index:
            f.write(f"{i}. {random_kiosks[i-1]}\n")
        f.write("\n\n")
    
    for i in random_kiosks:
        all_points.remove(i)

    # Select "x" random points from the list
    random_points = random.sample(all_points, num_points)
    with open(r'output\Camera details.txt', 'a') as f:
        f.write(f"Camera details : \n")
        for i in range(len(random_points)):
            f.write(f"{i+1}. {random_points[i]}\n")
        f.write("\n\n")
    
    distances = []
    kiosks = []

    # Print the selected random points
    with open(r'output\Camera details.txt', 'a') as f:
        f.write("Camera\tKiosk\tDistance\n")
    c = 0
    for point in random_points:
        kiosks = []
        for k in random_kiosks:
            kiosks.append(math.sqrt((k[0] - point[0])**2 + (k[1] - point[1])**2))
        
        sorted_kiosks = sorted(zip(kiosks, random_kiosks, kiosk_index))
        distances.append(sorted_kiosks[0][0])
        with open(r'output\Camera details.txt', 'a') as f:
            f.write(f"{c+1}\t\t{sorted_kiosks[0][2]}\t\t{format(distances[len(distances)-1],'.2f')}\n")
        kiosk_for_cam[c] = sorted_kiosks[0][2]
        c = c+1
    print("\n")
    print(kiosk_for_cam)

# distance(30,5)