import cv2
import time
import numpy as np
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# Load YOLO
net = cv2.dnn.readNet("yolov3.weights", "C:\\Users\\Senaisp\\Desktop\\darknet\\cfg\\yolov3.cfg")
with open("C:\\Users\\Senaisp\\Desktop\\darknet\\data\\coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

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

    frame = img
    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Information to show on screen
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * resolution[1])
                center_y = int(detection[1] * resolution[0])
                w = int(detection[2] * resolution[1])
                h = int(detection[3] * resolution[0])

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Non-max suppression
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
 

    # Display the image
    cv2.imshow('Vision Sensor', img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        sim.stopSimulation()
        break

cv2.destroyAllWindows()