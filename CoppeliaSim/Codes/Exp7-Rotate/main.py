import math
import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.getObject('sim')
right_joint_handle = sim.getObject("/*/DynamicRightJoint")
left_joint_handle = sim.getObject("/*/DynamicLeftJoint")

class LineBot:
    def __init__(self, wheel_radius, wheel_track):
        self.wheel_radius = wheel_radius
        self.wheel_track = wheel_track

        self.setInitialTime()
        self.setJointsVelocities(0,0)

    def setInitialTime(self):
        self.__initialTime = sim.getSimulationTime()

    def getInitialTime(self):
        return self.__initialTime

    def setJointsVelocities(self, vel_left, vel_right):
        omega_left = vel_left/self.wheel_radius
        omega_right = vel_right/self.wheel_radius

        sim.setJointTargetVelocity(left_joint_handle, omega_left)
        sim.setJointTargetVelocity(right_joint_handle, omega_right)

    def moveForward(self, dist = 1, vel = 0.1):

        delta_t = dist/vel

        # wait until finish
        self.setInitialTime()
        self.setJointsVelocities(vel,vel)
        while (sim.getSimulationTime() - self.getInitialTime()) < delta_t:
            pass

        # stop movement
        self.setJointsVelocities(0,0)
    
    def rotate(self, angle, omega_robot = 15):

        # Convert to radians
        angle = math.radians(angle)
        omega_robot = math.radians(omega_robot)

        # find wheel velocities
        vel_robot = omega_robot*self.wheel_track
        delta_t = angle/omega_robot

        # wait until finish
        self.setInitialTime()
        self.setJointsVelocities(vel_robot,-vel_robot)

        while (sim.getSimulationTime() - self.getInitialTime()) < delta_t:
            pass
        
        # stop movement
        self.setJointsVelocities(0,0)

    
sim.startSimulation()
bot = LineBot(0.027, 0.0595)
bot.rotate(180)

time.sleep(5)
sim.stopSimulation()