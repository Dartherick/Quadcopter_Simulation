import sim
from time import sleep
import numpy as np
import cv2

Scale = 5

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

VisionSensor = sim.simxGetObjectHandle(clientID, 'Vision', sim.simx_opmode_blocking)[-1]

sim.simxGetVisionSensorImage(clientID,VisionSensor,0,sim.simx_opmode_streaming)
sleep(1)
_,Resolution,_ = sim.simxGetVisionSensorImage(clientID,VisionSensor,0,sim.simx_opmode_buffer)
print(Resolution*3)

while True:
	_, _, RGB = sim.simxGetVisionSensorImage(clientID,VisionSensor,0,sim.simx_opmode_buffer) 
	Img = np.array(RGB,dtype=np.uint8)					#Convert the image list into a numpy array
	Img.resize([Resolution[0],Resolution[1],3])			#Convert the numpy array into a image
	Img = cv2.cvtColor(Img,cv2.COLOR_BGR2RGB)			#Change BGR to RGB	
	Img = cv2.resize(Img,np.array(Resolution)*Scale)	#Scale the image
	cv2.imshow('Thermal camera',Img)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cv2.destroyAllWindows()