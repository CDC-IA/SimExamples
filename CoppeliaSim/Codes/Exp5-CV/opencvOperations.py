import cv2
import time
import numpy as np
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# Setting simulation connection
client = RemoteAPIClient()
sim = client.getObject('sim')
cam_handle = sim.getObject("/Vision_sensor")

# start simulation
sim.startSimulation()
time.sleep(1)

# while simulation is running show vision sensor image
while (sim.getSimulationState() == sim.simulation_advancing_running):

    image, resolution = sim.getVisionSensorImg(cam_handle)
    img = np.frombuffer(image, dtype=np.uint8)
    img = img.reshape((resolution[1], resolution[0], 3))
    img = cv2.flip(img, 0)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # # erosion
    # kernel = np.ones((5, 5), np.uint8) 
    # img = cv2.erode(img, kernel)  

    # Display the image
    cv2.imshow('Vision Sensor', img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        sim.stopSimulation()
        break

cv2.destroyAllWindows()