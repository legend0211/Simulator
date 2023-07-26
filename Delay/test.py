import math
import random
import settings2 as settings2

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
        print(point,"\t",format(distances[len(distances)-1],".2f"))
        
    print("\n")    

# Function to find size of group of frames of 1 second
def generate_gop_size(cnt, arr):
    video_1080p = []
    video_720p = []
    video_480p = []
    video_360p = []

    cnt = 0
    for i in arr:
        # For 1080p video, find out the lower video quality sizes as well
        if(i=="1080"):
            random_number = random.randint(2, 8)
            video_1080p.append(random_number)
            video_720p.append(float(format(random_number*0.75, ".2f")))
            video_480p.append(float(format(random_number*0.5, ".2f")))
            video_360p.append(float(format(random_number*0.25, ".2f")))
            req_data_rate_1080p[cnt].append(video_1080p[len(video_1080p)-1])
            req_data_rate_720p[cnt].append(video_720p[len(video_720p)-1])
            req_data_rate_480p[cnt].append(video_480p[len(video_480p)-1])
            req_data_rate_360p[cnt].append(video_360p[len(video_360p)-1])

        # For 720p video, find out the lower video quality sizes as well and set higher video quality as -1
        elif(i=="720"):
            random_number = random.randint(2, 6)
            video_1080p.append(-1)
            video_720p.append(random_number)
            video_480p.append(float(format(random_number*0.66, ".2f")))
            video_360p.append(float(format(random_number*0.33, ".2f")))
            req_data_rate_1080p[cnt].append(video_1080p[len(video_1080p)-1])
            req_data_rate_720p[cnt].append(video_720p[len(video_720p)-1])
            req_data_rate_480p[cnt].append(video_480p[len(video_480p)-1])
            req_data_rate_360p[cnt].append(video_360p[len(video_360p)-1])

        # For 480p video, find out the lower video quality sizes as well and set higher video quality as -1
        elif(i=="480"):
            random_number = random.randint(1, 4)
            video_1080p.append(-1)
            video_720p.append(-1)
            video_480p.append(random_number)
            video_360p.append(float(format(random_number*0.5, ".2f")))
            req_data_rate_1080p[cnt].append(video_1080p[len(video_1080p)-1])
            req_data_rate_720p[cnt].append(video_720p[len(video_720p)-1])
            req_data_rate_480p[cnt].append(video_480p[len(video_480p)-1])
            req_data_rate_360p[cnt].append(video_360p[len(video_360p)-1])

        # For 360p video, find out the lower video quality sizes as well and set higher video quality as -1
        elif(i=="360"):
            random_number = random.uniform(0.25, 2)
            video_1080p.append(-1)
            video_720p.append(-1)
            video_480p.append(-1)
            video_360p.append(float(format(random_number, ".2f")))
            req_data_rate_1080p[cnt].append(video_1080p[len(video_1080p)-1])
            req_data_rate_720p[cnt].append(video_720p[len(video_720p)-1])
            req_data_rate_480p[cnt].append(video_480p[len(video_480p)-1])
            req_data_rate_360p[cnt].append(video_360p[len(video_360p)-1])
            
        else:
            print("Wrong input")
            exit()
        
        cnt += 1

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
    # print(f"Transmitted video from camera {i} with quality {str}")

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
                        # print(f"Dropped video from camera {i+1}")


def main(cnt):
    arr = settings2.main()
    video_1080p, video_720p, video_480p, video_360p = generate_gop_size(cnt, arr)
    # print("1080p GOP sizes : \n",video_1080p)
    # print("\n720p GOP sizes : \n",video_720p)
    # print("\n480p GOP sizes : \n",video_480p)
    # print("\n360p GOP sizes : \n",video_360p)
    # print("\n")

    data_rate_allocated = allocate_data_rate(arr)
    for i in range(len(data_rate_allocated)):
        alloc_data_rate[i].append(data_rate_allocated[i])

    event_probability = [random.randint(1, 100) for _ in range(len(arr))]
    event_array = []
    for i in event_probability:
        if(i%20 == 0):
            event_array.append(1)
        else:
            event_array.append(0)
    # print("\nEvent array : \n",event_array)
    # print("\n")

    send_video(event_array, data_rate_allocated, video_1080p, video_720p, video_480p, video_360p)

print("SAMPLE FOR 100 SECONDS")
print("================================================================\n")
# camera_distance()
req_data_rate_1080p=[[] * 100 for _ in range(30)]
req_data_rate_720p=[[] * 100 for _ in range(30)]
req_data_rate_480p=[[] * 100 for _ in range(30)]
req_data_rate_360p=[[] * 100 for _ in range(30)]
alloc_data_rate=[[] * 100 for _ in range(30)]

for i in range(100):
    main(i)

avg_alloc_data_rate = []
for i in range(30):
    avg_alloc_data_rate.append(sum(alloc_data_rate[i])/100)

print("SNR values : ")
snr_values = []
for i in range(len(alloc_data_rate)):
    snr_values.append(float(format((2**((sum(alloc_data_rate[i])/100)/20))-1,"0.2f")))
    
for i in range(len(snr_values)):
    print(f"Camera {i+1} : ",snr_values[i])
print()
pdf = {}
total_elements = len(snr_values)
for value in snr_values:
    if value in pdf:
        pdf[value] += 1
    else:
        pdf[value] = 1

# Normalize to get probabilities
for value in pdf:
    pdf[value] = float(format((pdf[value] / total_elements), "0.2f"))

# Print PDF
print("PDF of SNR :")
print("SNR\t Probability")
for i,j in zip(pdf.keys(), pdf.values()):
    print(i,"\t:",j)
print()
print()


delay_1080 = []
for i in range(len(alloc_data_rate)):
    alloc_cnt = 0
    req_cnt = 0
    delay_1080.append(0)
    for j in range(len(alloc_data_rate[0])):
        alloc_cnt += alloc_data_rate[i][j]
        req_cnt += req_data_rate_1080p[i][j]
        if(alloc_cnt >= req_cnt):
            delay_1080[i] = 0
        else:
            delay_1080[i] = req_cnt-alloc_cnt

for i in range(len(delay_1080)) :
    delay_1080[i] = float(format(delay_1080[i]/avg_alloc_data_rate[i],"0.2f"))

print("Delay for 1080p : ")
print(delay_1080)
print()

delay_720 = []
for i in range(len(alloc_data_rate)):
    alloc_cnt = 0
    req_cnt = 0
    delay_720.append(0)
    for j in range(len(alloc_data_rate[0])):
        alloc_cnt += alloc_data_rate[i][j]
        req_cnt += req_data_rate_720p[i][j]
        if(alloc_cnt >= req_cnt):
            delay_720[i] = 0
        else:
            delay_720[i] = req_cnt-alloc_cnt

for i in range(len(delay_720)) :
    delay_720[i] = float(format(delay_720[i]/avg_alloc_data_rate[i],"0.2f"))
print("Delay for 720p : ")
print(delay_720)
print()

delay_480 = []
for i in range(len(alloc_data_rate)):
    alloc_cnt = 0
    req_cnt = 0
    delay_480.append(0)
    for j in range(len(alloc_data_rate[0])):
        alloc_cnt += alloc_data_rate[i][j]
        req_cnt += req_data_rate_480p[i][j]
        if(alloc_cnt >= req_cnt):
            delay_480[i] = 0
        else:
            delay_480[i] = req_cnt-alloc_cnt

for i in range(len(delay_480)) :
    delay_480[i] = float(format(delay_480[i]/avg_alloc_data_rate[i],"0.2f"))
print("Delay for 480p : ")
print(delay_480)
print()

delay_360 = []
for i in range(len(alloc_data_rate)):
    alloc_cnt = 0
    req_cnt = 0
    delay_360.append(0)
    for j in range(len(alloc_data_rate[0])):
        alloc_cnt += alloc_data_rate[i][j]
        req_cnt += req_data_rate_360p[i][j]
        if(alloc_cnt >= req_cnt):
            delay_360[i] = 0
        else:
            delay_360[i] = req_cnt-alloc_cnt

for i in range(len(delay_360)) :
    delay_360[i] = float(format(delay_360[i]/avg_alloc_data_rate[i],"0.2f"))
print("Delay for 360p : ")
print(delay_360)

