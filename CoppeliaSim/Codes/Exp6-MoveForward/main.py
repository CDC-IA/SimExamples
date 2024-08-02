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
        self.setJointsVelocities(vel,vel)

        delta_t = dist/vel

        while sim.getSimulationTime() < delta_t:
            pass

        self.setJointsVelocities(0,0)

    
sim.startSimulation()
bot = LineBot(0.027, 0.0595)
bot.moveForward(1)

time.sleep(5)
sim.stopSimulation()