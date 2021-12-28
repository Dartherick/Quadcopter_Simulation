import sim
from time import sleep

class Quadricopter_Drone():
	def __init__(self,Port):
		'''
		Para enlazar coppelia sim con el codigo realizado en python,coloca la siguiente funcion en un script en coppelia
			simExtRemoteApiStart(Port)
		Donde Port tiene que ser esxactamente el mismo colocado en python
		'''
		sim.simxFinish(-1) #Cerrando cualquier comunicacion previamente abierta
		self.clientID = sim.simxStart('127.0.0.1',Port,True,True,5000,5) #Conectando coppelia con el codigo

		if self.clientID!=-1:
			print ("Connected to remote API server")
			sim.simxStartSimulation(self.clientID,sim.simx_opmode_oneshot)
		else:
			print("Not connected to remote API server")
			exit()

	def Handles(self): 	#Funcion para obtener los handles
		pass
		self.Motor = sim.simxGetObjectHandle(self.clientID, "Name", sim.simx_opmode_blocking)[-1]

		self.__InitalizeSensors()

	def __InitalizeSensors(self):
		'''Funcion para inicializar los sensores de vision
		se necesitan como minimo 0.02 segundos entre el modo streaming y buffer'''

		#Sensores de vision para detectar las lineas
		sim.simxGetVisionSensorImage(self.clientID,self.LSensor,0,sim.simx_opmode_streaming)[-1]
		sim.simxGetVisionSensorImage(self.clientID,self.RSensor,0,sim.simx_opmode_streaming)[-1]

		#Sensores para detectar el bloque
		sim.simxGetVisionSensorImage(self.clientID,self.BColorSensor,0,sim.simx_opmode_streaming)[-1]
		sim.simxReadProximitySensor(self.clientID,self.BAproxSensor,sim.simx_opmode_streaming)[-1]

		sleep(0.02)