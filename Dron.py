import sim
from time import sleep
import numpy as np

class Quadcopter_Drone():
	def __init__(self,ClientID,Area):
		self.ClientID = ClientID
		self.Size = Area

	def Handles(self, Dummy): 	#Funcion para obtener los handles
		self.ThermalCamera = sim.simxGetObjectHandle(self.clientID, Dummy, sim.simx_opmode_blocking)[-1]

		#self.__InitalizeSensors()

	def __InitalizeSensors(self):
		'''Funcion para inicializar los sensores de vision
		se necesitan como minimo 0.02 segundos entre el modo streaming y buffer'''

		#Sensores para detectar el bloque
		sim.simxGetVisionSensorImage(self.clientID,self.ThermalCamera,0,sim.simx_opmode_streaming)
		sleep(0.02)
		_,Resolution,_ = sim.simxGetVisionSensorImage(self.clientID,self.ThermalCamera,0,sim.simx_opmode_buffer)

	def GetThermalCamera(self,Resolution):
		_, _, RGB = sim.simxGetVisionSensorImage(self.clientID,self.ThermalCamera,0,sim.simx_opmode_buffer) 
		img = np.array(RGB,dtype=np.uint8)
		img.resize([Resolution[0],Resolution[1],3])
		return img