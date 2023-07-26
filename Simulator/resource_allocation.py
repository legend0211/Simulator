import math
import random
import Delay.settings2 as settings2
import numpy as np
import global_arrays as ga


def camera_distance():
    grid_size = 5000
    num_points = 30

    # Generate a list of all possible grid points
    all_points = [(x, y) for x in range(grid_size) for y in range(grid_size)]
    all_points.remove((2500,2500))

    # Select 30 random points from the list
    random_points = random.sample(all_points, num_points)
    distances = []
    random_points.sort()

    # Print the selected random points
    print("\nPoint","\t\t","Distance")
    for point in random_points:
        distances.append(math.sqrt((2500 - point[0])**2 + (2500 - point[1])**2))
        print(point,"\t",distances[len(distances)-1])    
    print("\n")    

# Function to find size of group of frames of 1 second
def generate_gop_size(arr):
    video_1080p = []
    video_720p = []
    video_480p = []
    video_360p = []

    for i in arr:
        # For 1080p video, find out the lower video quality sizes as well
        if(i=="1080"):
            random_number = random.randint(2, 8)
            video_1080p.append(random_number)
            video_720p.append(float(format(random_number*0.75, ".2f")))
            video_480p.append(float(format(random_number*0.5, ".2f")))
            video_360p.append(float(format(random_number*0.25, ".2f")))

        # For 720p video, find out the lower video quality sizes as well and set higher video quality as -1
        elif(i=="720"):
            random_number = random.randint(2, 6)
            video_1080p.append(-1)
            video_720p.append(random_number)
            video_480p.append(float(format(random_number*0.66, ".2f")))
            video_360p.append(float(format(random_number*0.33, ".2f")))

        # For 480p video, find out the lower video quality sizes as well and set higher video quality as -1
        elif(i=="480"):
            random_number = random.randint(1, 4)
            video_1080p.append(-1)
            video_720p.append(-1)
            video_480p.append(random_number)
            video_360p.append(float(format(random_number*0.5, ".2f")))

        # For 360p video, find out the lower video quality sizes as well and set higher video quality as -1
        elif(i=="360"):
            random_number = random.uniform(0.25, 2)
            video_1080p.append(-1)
            video_720p.append(-1)
            video_480p.append(-1)
            video_360p.append(float(format(random_number, ".2f")))
            
        else:
            print("Wrong input")
            exit()
        

    return video_1080p, video_720p, video_480p, video_360p

# Function to allocate data rate to share video
def allocate_data_rate(arr):
    # Use a uniform distribution to allocate data rate for each video
    uniform_dist = [random.randint(2, 8) for _ in range(len(arr))]
    return uniform_dist

# Function to transmit the video
def transmit_video(video, i, str):
    """
    # Do transfer of (video)
    """
    with open('Transfer details.txt', 'a') as f:
        f.write(f"\nTransmitted video from camera {i} with quality {str}")

# Function to find only i-frames of the no event videos
def get_i_frame(video):
    """
    input_video = video
    output_video = "output_video.mp4"

    # Extract I-frames only
    ffmpeg_command = f"ffmpeg -i {input_video} -vf select='eq(pict_type\,I)' -vsync vfr {output_video}"
    subprocess.call(ffmpeg_command, shell=True)

    """

# Function which decides how video should be transmitted
def send_video(event_array, data_rate_allocated, video_1080p, video_720p, video_480p, video_360p):
    
    for i in range(len(event_array)):
        # If event occurs we share the full video with no frame drop
        # If allocated data rate is less then we lower video quality and then send the video
        if(event_array[i] == 1):
            # Check if we can share 1080p video
            if(data_rate_allocated[i] >= video_1080p[i] and video_1080p[i] != -1):
                transmit_video(video_1080p[i], i+1, "1080p (All frames)")
            
            # Check if we can share 720p video
            elif(data_rate_allocated[i] >= video_720p[i] and video_720p[i] != -1):
                transmit_video(video_720p[i], i+1, "720p (All frames)")
            
            # Check if we can share 480p video
            elif(data_rate_allocated[i] >= video_480p[i] and video_480p[i] != -1):
                transmit_video(video_480p[i], i+1, "480p (All frames)")
            
            # We share 360p video
            else:
                transmit_video(video_360p[i], i+1, "360p (All frames)")

        # If event doesn't occur we share the video with highest quality but with frame drop if required
        # If allocated data rate is less then we drop the p and b frames
        # If allocated data rate is less than i-frame then we drop the whole GOP
        # Here we consider 40% of a video is i-frame
        else:
            # Check if 1080p video is available and if we can share whole video
            if(video_1080p[i] != -1 and data_rate_allocated[i] >= video_1080p[i]):
                transmit_video(video_1080p[i], i+1, "1080p (All frames)")

            # Check if 1080p video is available and if we can share i-frame and some frames
            elif(video_1080p[i] != -1 and data_rate_allocated[i] >= 0.4*video_1080p[i]):
                iframe_video = get_i_frame(video_1080p[i])
                remaining_frames = math.floor(float(format(data_rate_allocated[i] - 0.4*video_1080p[i], "0.2f"))*29/(0.6*video_1080p[i]))
                transmit_video(iframe_video, i+1, f"1080p (i-frame & {remaining_frames} other frames)")

            # Check if 720p video is available and if we can share whole video
            elif(video_720p[i] != -1 and data_rate_allocated[i] >= video_720p[i]):
                transmit_video(video_720p[i], i+1, "720p (All frames)")

            # Check if 720p video is available and if we can share i-frame and some frames
            elif(video_720p[i] != -1 and data_rate_allocated[i] >= 0.4*video_720p[i]):
                iframe_video = get_i_frame(video_720p[i])
                remaining_frames = math.floor(float(format(data_rate_allocated[i] - 0.4*video_720p[i], "0.2f"))*29/(0.6*video_720p[i]))
                transmit_video(iframe_video, i+1, f"720p (i-frame & {remaining_frames} other frames)")

            # Check if 480p video is available and if we can share whole video
            elif(video_480p[i] != -1 and data_rate_allocated[i] >= video_480p[i]):
                transmit_video(video_480p[i], i+1, "480p (All frames)")

            # Check if 480p video is available and if we can share i-frame and some frames
            elif(video_480p[i] != -1 and data_rate_allocated[i] >= 0.4*video_480p[i]):
                iframe_video = get_i_frame(video_480p[i])
                remaining_frames = math.floor(float(format(data_rate_allocated[i] - 0.4*video_480p[i], "0.2f"))*29/(0.6*video_480p[i]))
                transmit_video(iframe_video, i+1, f"480p (i-frame & {remaining_frames} other frames)")

            # Share 360p video
            else:
                # Check if we can share whole video
                if(data_rate_allocated[i] >= video_360p[i]):
                    transmit_video(video_360p[i], i+1, "360p (All frames)")
                else:
                    # Check if we can share only i frame
                    if(data_rate_allocated[i] >= 0.4*video_360p[i]):
                        iframe_video = get_i_frame(video_360p[i])
                        remaining_frames = math.floor(float(format(data_rate_allocated[i] - 0.4*video_360p[i], "0.2f"))*29/(0.6*video_360p[i]))
                        transmit_video(iframe_video, i+1, f"360p (i-frame & {remaining_frames} other frames)")
                    else:
                        """
                        Drop this GOP
                        """
                        with open('Transfer details.txt', 'a') as f:
                            f.write(f"\nDropped video from camera {i+1}")
    with open('Transfer details.txt', 'a') as f:
        f.write("\n========================================================================\n")

def main(ii):
    arr = settings2.main()
    video_1080p, video_720p, video_480p, video_360p = generate_gop_size(arr)
    if(ii == 0):
        with open('GOP sizes.txt', 'w') as f:
            text = f"SAMPLE SECOND {ii+1}\n"
            text += "================================================\n"
            text += "\n1080p GOP sizes : " + str(video_1080p) + "\n"
            text += "\n720p GOP sizes : " + str(video_720p) + "\n"
            text += "\n480p GOP sizes : " + str(video_480p) + "\n"
            text += "\n360p GOP sizes : " + str(video_360p) + "\n\n\n"
            f.write(text)
        with open('Transfer details.txt', 'w') as f:
            f.write(f"SAMPLE SECOND {ii+1}\n")
            
    else:
        with open('GOP sizes.txt', 'a') as f:
            text = f"SAMPLE SECOND {ii+1}\n"
            text += "================================================\n"
            text += "\n1080p GOP sizes : " + str(video_1080p) + "\n"
            text += "\n720p GOP sizes : " + str(video_720p) + "\n"
            text += "\n480p GOP sizes : " + str(video_480p) + "\n"
            text += "\n360p GOP sizes : " + str(video_360p) + "\n\n\n"
            f.write(text)
        with open('Transfer details.txt', 'a') as f:
            f.write(f"\nSAMPLE SECOND {ii+1}\n")

    data_rate_allocated = allocate_data_rate(arr)

    event_array = ga.prediction_array[ii]
    
    send_video(event_array, data_rate_allocated, video_1080p, video_720p, video_480p, video_360p)
