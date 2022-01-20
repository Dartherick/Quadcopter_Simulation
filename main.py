import re
from Dron import Quadcopter_Drone
import sim
import math
from time import sleep
import numpy as np

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

def StartSimulation():
	sim.simxStartSimulation(clientID,sim.simx_opmode_oneshot) 	

def StopSimulation():
	sim.simxPauseSimulation(clientID,sim.simx_opmode_oneshot) 	


Drone = Quadcopter_Drone(clientID,(1,1))
AreaSize = (5,5)
Start = sim.simxGetObjectHandle(clientID, 'Dummy', sim.simx_opmode_blocking)[-1]
Target = sim.simxGetObjectHandle(clientID, 'Quadcopter_target', sim.simx_opmode_blocking)[-1]
Body = sim.simxGetObjectHandle(clientID, 'Quadcopter', sim.simx_opmode_blocking)[-1]
Fire = sim.simxGetObjectHandle(clientID, 'Fire', sim.simx_opmode_blocking)[-1]

sim.simxGetObjectPosition(clientID, Target, Start, sim.simx_opmode_streaming)
TargetPosition = sim.simxGetObjectPosition(clientID, Target, Start, sim.simx_opmode_buffer)[-1]

sim.simxGetObjectOrientation(clientID,Target,Start,sim.simx_opmode_streaming)

sim.simxGetObjectPosition(clientID, Body, Start, sim.simx_opmode_streaming)
sim.simxGetObjectPosition(clientID, Fire, Start, sim.simx_opmode_streaming)
sleep(0.2)


def ValidatePosition():
	while True:
		BodyPosition = sim.simxGetObjectPosition(clientID, Body, Start, sim.simx_opmode_buffer)[-1]
		BodyPosition = [round(x,2) for x in BodyPosition]
		
		TargetPosition = sim.simxGetObjectPosition(clientID, Target, Start, sim.simx_opmode_buffer)[-1]
		TargetPosition = [round(x,2) for x in TargetPosition]

		if BodyPosition == TargetPosition:
			break

def ValidateOrientation():
	while True:
		BodyOrientation = sim.simxGetObjectOrientation(clientID,Body,Start,sim.simx_opmode_buffer)[-1]
		BodyOrientation = [round(x,2) for x in BodyOrientation]
		
		TargetOrientation = sim.simxGetObjectOrientation(clientID,Target,Start,sim.simx_opmode_buffer)[-1]
		TargetOrientation = [round(x,2) for x in TargetOrientation]

		if BodyOrientation == TargetOrientation:
			break

def DetectFire():
	TargetPosition = sim.simxGetObjectPosition(clientID, Body, Start, sim.simx_opmode_buffer)[-1]
	TargetPosition = [round(x,0) for x in TargetPosition]

	FirePosition = sim.simxGetObjectPosition(clientID, Fire, Start, sim.simx_opmode_buffer)[-1]
	FirePosition = [round(x,0) for x in FirePosition]
	
	#print(f'Target {TargetPosition[0:2]} ; Fire {FirePosition[0:2]}')
	print(f'Drone position {TargetPosition}')

	if FirePosition[0] == TargetPosition[0]:
		if FirePosition[1] == (TargetPosition[1]+1):
			return True
	
Altura = 2.4

Z = list(np.arange(0, Altura, 0.2))

for Depth in Z:
	sleep(0.05)
	sim.simxSetObjectPosition(clientID,Target,Start,[0,0,Depth],sim.simx_opmode_oneshot)


X = list(np.arange(0, 0.1, 0.005))
Y = list(np.arange(0, 5, 0.05))
referencia = sim.simxGetObjectOrientation(clientID,Target,Start,sim.simx_opmode_buffer)[-1]
Ubicacion = sim.simxGetObjectOrientation(clientID,Target,Start,sim.simx_opmode_buffer)[-1]
RotationAngle = list(np.arange(referencia[-1], 0, 0.0001))
RotationAngle1 = list(np.arange(-1.570796012878418, 0, 0.0001))

sleep(2)

i,j = 0,0
SleepTime = 0.05
SleepTime1 = 0.03

Detected = False

while True:
	#Izq a Derecha
	for j in Y:
		sleep(SleepTime)
		sim.simxSetObjectPosition(clientID,Target,Start,[i,j,Altura],sim.simx_opmode_oneshot)
		Detected = DetectFire()
		if Detected: 
			break
		#ValidatePosition()

	if Detected: 
		break

	sleep(1)
	
	#Rotacion 45 grados a izq
	for Angle in RotationAngle:
		sim.simxSetObjectOrientation(clientID,Target,Start,[0,0,Angle],sim.simx_opmode_oneshot)
	
	sleep(1)

	#Mov eje x
	for Temp in X:
		i -= Temp
		sleep(SleepTime1)
		sim.simxSetObjectPosition(clientID,Target,Start,[i,j,Altura],sim.simx_opmode_oneshot)
		#ValidatePosition()
	
	sleep(1)
	
	#Rotacion 45 grados a izq
	for Angle in reversed(RotationAngle1):
		sim.simxSetObjectOrientation(clientID,Target,Start,[0,0,-Angle],sim.simx_opmode_oneshot)
	
	sleep(1)
	
	#Mov eje -Y
	for j in reversed(Y):
		sleep(SleepTime)
		sim.simxSetObjectPosition(clientID,Target,Start,[i,j,Altura],sim.simx_opmode_oneshot)
		Detected = DetectFire()
		if Detected: 
			break
		#ValidatePosition()

	if Detected: 
		break

	sleep(1)
	
	for Angle in RotationAngle1:
		sim.simxSetObjectOrientation(clientID,Target,Start,[0,0,-Angle],sim.simx_opmode_oneshot)

	for Temp in X:
		i -= Temp
		sleep(SleepTime1)
		sim.simxSetObjectPosition(clientID,Target,Start,[i,j,Altura],sim.simx_opmode_oneshot)
		#ValidatePosition()

	sleep(1)

	#Rotacion 45 grados a izq
	for Angle in reversed(RotationAngle):
		sim.simxSetObjectOrientation(clientID,Target,Start,[0,0,Angle],sim.simx_opmode_oneshot)

FirePosition = sim.simxGetObjectPosition(clientID, Fire, Start, sim.simx_opmode_buffer)[-1]
FirePosition = [round(x,3) for x in FirePosition[0:2]]

DialogHandle = sim.simxDisplayDialog(clientID,'Fuego detectado!','Fuego detectado en la ubicacion '+str(FirePosition),sim.sim_dlgstyle_message,'',None,None,sim.simx_opmode_blocking)[1]
sleep(5)
sim.simxEndDialog(clientID,DialogHandle,sim.simx_opmode_oneshot)
sim.simxStopSimulation(clientID,sim.simx_opmode_oneshot)
print('\nFin de la simulacion')