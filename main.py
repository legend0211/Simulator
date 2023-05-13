import os
import shutil
try:
    shutil.rmtree("video")
except:
    """"""

os.makedirs("video")

from time import sleep
import settings, node, power

nodes, receiver, fps, event_probability = settings.main()

node.main(int(fps), int(nodes))

sleep(2)

power.main(int(nodes))

exit()