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
        #########################
        # CÓDIGO PARA PREENCHER #
        
        #########################
        pass

    def moveForward(self, dist = 1, vel = 0.1):
        #########################
        # CÓDIGO PARA PREENCHER #
        
        #########################
        pass

sim.startSimulation()
bot = LineBot(0.027, 0.0595)
bot.moveForward(1)

time.sleep(5)
sim.stopSimulation()