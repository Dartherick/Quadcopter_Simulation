from Dron import Quadcopter_Drone
import sim
import math
from time import sleep

'''
Para enlazar coppelia sim con el codigo realizado en python,coloca la siguiente funcion en un script en coppelia
	simExtRemoteApiStart(Port)
Donde Port tiene que ser esxactamente el mismo colocado en python
'''
Port = 2429
sim.simxFinish(-1) #Cerrando cualquier comunicacion previamente abierta
clientID = sim.simxStart('127.0.0.1',Port,True,True,5000,5) #Conectando coppelia con el codigo

if clientID != -1:
	print ("Connected to remote API server")
	sim.simxStartSimulation(clientID,sim.simx_opmode_oneshot)
else:
	print("Not connected to remote API server")
	exit()

AreaSize = (5,5) #Area size of the simulation in meters
Quadcopter = Quadcopter_Drone(clientID,(1,1))

for i in range(AreaSize[0]):
	sim.simxGetObjectPosition()


def Hipotenusa():
	Dummy = sim.simxGetObjectHandle(clientID, 'Quadcopter_target', sim.simx_opmode_blocking)[-1]
	sim.simxGetObjectPosition(clientID, Dummy, -1, sim.simx_opmode_streaming)
	sleep(0.2)
	Position = sim.simxGetObjectPosition(clientID, Dummy, -1, sim.simx_opmode_buffer)[-1]
	print(Position)

	FinalPosition = (0,0,Position[-1])

	CatetoX = abs(Position[0] - FinalPosition[0]) 
	CatetoY = abs(Position[1] - FinalPosition[1]) 
	Hipotenusa = math.sqrt(CatetoX**2 + CatetoY**2)

	b = math.radians(math.asin(CatetoX/Hipotenusa))

	for a in range(91):
		X = ((math.atan(b) * Position[0] + math.tan(a) * FinalPosition[0]) / (math.atan(b)+math.tan(a)))
		Y = ((math.atan(b) * Position[0] + math.tan(a) * FinalPosition[0]) / (math.atan(b)+math.tan(a)))
		print(f'X={X}  Y={Y}')
		#sleep(1)
		#sim.simxSetObjectPosition(clientID, Dummy, -1, (X,Y,Position[-1]),sim.simx_opmode_oneshot)