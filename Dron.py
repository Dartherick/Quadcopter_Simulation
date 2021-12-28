import sim
from time import sleep

class Quadcopter_Drone():
	def __init__(self,ClientID,Area):
		self.ClientID = ClientID
		self.Size = Area

	def Handles(self, Dummy): 	#Funcion para obtener los handles
		self.Dummy = sim.simxGetObjectHandle(self.clientID, Dummy, sim.simx_opmode_blocking)[-1]

		#self.__InitalizeSensors()

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

		def SetPosition(self,Position):
			sim.simxSetObjectPosition(self.ClientID, self.Dummy, -1, Position)
