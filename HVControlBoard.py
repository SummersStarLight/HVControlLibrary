from __future__ import division
from HALConstants import *  #all constants part of this file
import PBBDevices
import time
import syslog
import socket

class HVControlBoard:
	def __init__(self):
		syslog.syslog(LOG_STSW_PRI,"> HVControlBoard:__init__")
		PBBDevices.initializeHardware()
		PBBDevices.deSelectSPISlaves(SPI_MODE_0)
		self.configureTempSensor()
		self.configureGPIO()
		self.enableHV()
		syslog.syslog(LOG_STSW_PRI,"< HVControlBoard:__init__")
	
	def __del__(self):
		syslog.syslog(LOG_STSW_PRI," HVControlBoard:__del__")
		self.disableHV()
		PBBDevices.freeHardwareResources()
		syslog.syslog(LOG_STSW_PRI,"< HVControlBoard:__del__")
		
	""" Configure Temperature Sensor """
	def configureTempSensor(self):
		syslog.syslog(LOG_STSW_PRI,"> HVControlBoard:configureTempSensor")
		PBBDevices.selectSPISlave(TSENSOR_ID,SPI_MODE_3) 
		PBBDevices.configureTSensor(SPI_MODE_3)
		PBBDevices.deSelectSPISlaves(SPI_MODE_3)
		syslog.syslog(LOG_STSW_PRI,"< HVControlBoard:configureTempSensor")
		
	""" Read Temperature Sensor """		
	def measureTemperature(self):	
		syslog.syslog(LOG_STSW_PRI,"> HVControlBoard:measureTemperature")
		PBBDevices.selectSPISlave(TSENSOR_ID,SPI_MODE_3)
		controlBoardTemp = PBBDevices.readTemperature(SPI_MODE_3)
		PBBDevices.deSelectSPISlaves(SPI_MODE_3)
		syslog.syslog(LOG_STSW_PRI,"< HVControlBoard:measureTemperature")
		return controlBoardTemp
		
		
		""" GPIO configuration """
	def configureGPIO(self):
		syslog.syslog(LOG_STSW_PRI,"> HVControlBoard:configureGPIO")
		PBBDevices.selectSPISlave(GPIO_ID,SPI_MODE_0)
		PBBDevices.configureGPIO(SPI_MODE_0)
		PBBDevices.deSelectSPISlaves(SPI_MODE_0)
		PBBDevices.selectSPISlave(GPIO_ID,SPI_MODE_0)
		PBBDevices.readGPIOConfiguration(SPI_MODE_0)
		PBBDevices.deSelectSPISlaves(SPI_MODE_0)
		syslog.syslog(LOG_STSW_PRI,"< HVControlBoard:configureGPIO")
		
	def enableHV(self):
		syslog.syslog(LOG_STSW_PRI,"> HVControlBoard:enableHV")
		PBBDevices.selectSPISlave(GPIO_ID,SPI_MODE_0)
		PBBDevices.enableHV(SPI_MODE_0)
		PBBDevices.deSelectSPISlaves(SPI_MODE_0)
		syslog.syslog(LOG_STSW_PRI,"< HVControlBoard:enableHV")

	def disableHV(self):
		syslog.syslog(LOG_STSW_PRI,"> HVControlBoard:disableHV")
		PBBDevices.selectSPISlave(GPIO_ID,SPI_MODE_0)
		PBBDevices.disableHV(SPI_MODE_0)
		PBBDevices.deSelectSPISlaves(SPI_MODE_0)
		syslog.syslog(LOG_STSW_PRI,"< HVControlBoard:disableHV")
			
	def setCLMidVoltage(self,vinput):
		syslog.syslog(LOG_STSW_PRI,"> HVControlBoard:setCLMidVoltage")
		vmax = 2000
		if (vinput<vmax):
			digInput = int(round(vinput*0x10000/vmax))
			PBBDevices.selectSPISlave(DAC_LOAD_ID,SPI_MODE_3)
			PBBDevices.setDAC7731(digInput>>8,SPI_MODE_3)
			PBBDevices.deSelectSPISlaves(SPI_MODE_3)
			PBBDevices.selectSPISlave(DAC_LOAD_ID,SPI_MODE_3)
			PBBDevices.setDAC7731(digInput & 0x00ff,SPI_MODE_3)
			PBBDevices.deSelectSPISlaves(SPI_MODE_3)
			PBBDevices.deSelectSPISlaves(SPI_MODE_0)
			PBBDevices.selectSPISlave(DAC_OPUT_ID,SPI_MODE_0)
			PBBDevices.deSelectSPISlaves(SPI_MODE_0)
			
			PBBDevices.selectSPISlave(DAC_LOAD_ID,SPI_MODE_3)
			config1 = int(PBBDevices.setDAC7731(digInput>>8,SPI_MODE_3))
			PBBDevices.deSelectSPISlaves(SPI_MODE_3)
			PBBDevices.selectSPISlave(DAC_LOAD_ID,SPI_MODE_3)
			config2 = int(PBBDevices.setDAC7731(digInput & 0x00ff,SPI_MODE_3))
			PBBDevices.deSelectSPISlaves(SPI_MODE_3)
			PBBDevices.deSelectSPISlaves(SPI_MODE_0)
			PBBDevices.selectSPISlave(DAC_OPUT_ID,SPI_MODE_0)
			PBBDevices.deSelectSPISlaves(SPI_MODE_0)
			
			if (digInput == (config1<<8|config2)):
				print "Desired voltage is set"
			else:
				print "Unable to set desired Voltage"
		else:
			print "wrong input, input voltage should be less than 10 Volts"
		syslog.syslog(LOG_STSW_PRI,"< HVControlBoard:setCLMidVoltage")

	def measurePowerSupplies(self):
		syslog.syslog(LOG_STSW_PRI,"> HVControlBoard:measurePowerSupplies")
		voltageReadback = []
		channel = 0                #start with this channel
		PBBDevices.selectSPISlave(ADC_ID,SPI_MODE_0)
		val = PBBDevices.configure7949(channel,SPI_MODE_0)
		PBBDevices.deSelectSPISlaves(SPI_MODE_0)
		
		for channel in range(1,8):
			PBBDevices.selectSPISlave(ADC_ID,SPI_MODE_0)
			val = PBBDevices.configure7949(channel,SPI_MODE_0)
			PBBDevices.deSelectSPISlaves(SPI_MODE_0)

			PBBDevices.selectSPISlave(ADC_ID,SPI_MODE_0)				
			val = PBBDevices.read7949(SPI_MODE_0)
			cfg = ((val & 0x0003fff0)>>4)
			PBBDevices.deSelectSPISlaves(SPI_MODE_0)
			voltageReadback.append((((val & 0xfffc0000)>>18)/0x3fff * 4.096))
				
		PBBDevices.selectSPISlave(ADC_ID,SPI_MODE_0)
		val = PBBDevices.read7949(SPI_MODE_0)
		cfg = ((val & 0x0003fff0)>>4)
		PBBDevices.deSelectSPISlaves(SPI_MODE_0)
		voltageReadback.append((((val & 0xfffc0000)>>18)/0x3fff * 4.096))
		syslog.syslog(LOG_STSW_PRI,"< HVControlBoard:measurePowerSupplies")
		return voltageReadback
	
	""" measure only CL Mid Voltage"""
	def getCLMidVoltage(self):
		syslog.syslog(LOG_STSW_PRI,"> HVControlBoard:getCLMidVoltage")
		PBBDevices.selectSPISlave(ADC_ID,SPI_MODE_0)
		val = PBBDevices.configure7949(HV_U_MON_CHAN,SPI_MODE_0)
		PBBDevices.deSelectSPISlaves(SPI_MODE_0)
		
		PBBDevices.selectSPISlave(ADC_ID,SPI_MODE_0)				
		val = PBBDevices.read7949(SPI_MODE_0)
		PBBDevices.deSelectSPISlaves(SPI_MODE_0)

		PBBDevices.selectSPISlave(ADC_ID,SPI_MODE_0)				
		val = PBBDevices.read7949(SPI_MODE_0)
		PBBDevices.deSelectSPISlaves(SPI_MODE_0)
		syslog.syslog(LOG_STSW_PRI,"< HVControlBoard:getCLMidVoltage")
		return((((val & 0xfffc0000)>>18)/0x3fff)*4.096*3*200)
		
	""" measure only CL Mid Current"""
	def getCLMidCurrent(self):
		syslog.syslog(LOG_STSW_PRI,"> HVControlBoard:getCLMidCurrent")
		PBBDevices.selectSPISlave(ADC_ID,SPI_MODE_0)
		val = PBBDevices.configure7949(HV_I_MON_CHAN,SPI_MODE_0)
		PBBDevices.deSelectSPISlaves(SPI_MODE_0)

		PBBDevices.selectSPISlave(ADC_ID,SPI_MODE_0)
		val = PBBDevices.read7949(SPI_MODE_0)
		PBBDevices.deSelectSPISlaves(SPI_MODE_0)

		PBBDevices.selectSPISlave(ADC_ID,SPI_MODE_0)
		val = PBBDevices.read7949(SPI_MODE_0)
		PBBDevices.deSelectSPISlaves(SPI_MODE_0)
		syslog.syslog(LOG_STSW_PRI,"< HVControlBoard:getCLMidCurrent")
		return((((val & 0xfffc0000)>>18)/0x3fff)*4.096*3)
	

if (__name__ == "__main__"):
	x = HVControlBoard()
	print "Control Board Temperature: %f" %(x.measureTemperature())
	x.setCLMidVoltage(0)
	print x.measurePowerSupplies()
	print x.getCLMidVoltage()
	print x.getCLMidCurrent()
	del(x)


