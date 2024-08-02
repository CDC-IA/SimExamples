import numpy as np
import matplotlib.pyplot as plt
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.getObject('sim')
joint_handle = sim.getObject("/*/Revolute_joint")

sim.startSimulation()

# Vou gravar 10 ciclos da onda (1 ciclo = 60 segundos).
n = 10
t = [sim.getSimulationTime()]
vel = [0]

while t[-1] < n*60: 
    t.append(sim.getSimulationTime())
    vel.append(sim.getJointVelocity(joint_handle))

sim.stopSimulation()

print(f"Tamanho do vetor de velocidade: {len(vel)}")

# Sufixo dos dados e imagens
suffix = "TEST"

## Plotando Série Temporal
temp = plt.figure()
plt.plot(t,vel)
plt.suptitle("Leitura do Encoder da Junta")
plt.xlabel("Tempo (s)")
plt.ylabel("Velocidade (rad/s)")
temp.savefig(f"encoder{suffix}.svg")

np.save(f"data/vel{suffix}.npy",np.array(vel))