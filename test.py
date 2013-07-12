import PBBDevices
import time
import syslog
import socket


class HVPrint:
	def __init__(self):
		PBBDevices.initializeHardware()
		PBBDevices.deSelectSPISlaves(0)
		self.configureTempSensor()
	
	def __del__(self):
		PBBDevices.freeHardwareResources()
		
	""" Configure Temperature Sensor """
	def configureTempSensor(self):
		PBBDevices.selectSPISlave(4,3) 
		PBBDevices.configureTSensor(3)
		PBBDevices.deSelectSPISlaves(3)
		
	""" Read Temperature Sensor """		
	def measureTemperature(self):	
		print PBBDevices.selectSPISlave(4,3)
		print PBBDevices.readTemperature(3)
		PBBDevices.deSelectSPISlaves(3)
		
		""" GPIO configuration and reading """
	def enableHV(self):
		PBBDevices.selectSPISlave(3,0)
		print PBBDevices.configureGPIO(0)
		PBBDevices.deSelectSPISlaves(0)
		PBBDevices.selectSPISlave(3,0)
		print PBBDevices.readGPIOConfiguration(0)
		PBBDevices.deSelectSPISlaves(0)
		PBBDevices.selectSPISlave(3,0)
		print PBBDevices.enableHV(0)
		PBBDevices.deSelectSPISlaves(0)

		PBBDevices.selectSPISlave(3,0)
		print PBBDevices.disableHV(0)
		PBBDevices.deSelectSPISlaves(0)
	
	def setCLMidVoltage(self):
		vinput = float(raw_input("Enter the voltage you want to set:"))
		vmax = 10
		if (vinput<vmax):
			digInput = int(((float(vinput))*0x10000)/vmax)
			PBBDevices.selectSPISlave(0,3)
			PBBDevices.setDAC7731(digInput>>8,3)
			PBBDevices.deSelectSPISlaves(3)
			PBBDevices.selectSPISlave(0,3)
			PBBDevices.setDAC7731(digInput & 0x00ff,3)
			PBBDevices.deSelectSPISlaves(3)
			PBBDevices.deSelectSPISlaves(0)
			PBBDevices.selectSPISlave(1,0)
			PBBDevices.deSelectSPISlaves(0)
			
			PBBDevices.selectSPISlave(0,3)
			config1 = int(PBBDevices.setDAC7731(digInput>>8,3))
			PBBDevices.deSelectSPISlaves(3)
			PBBDevices.selectSPISlave(0,3)
			config2 = int(PBBDevices.setDAC7731(digInput & 0x00ff,3))
			PBBDevices.deSelectSPISlaves(3)
			PBBDevices.deSelectSPISlaves(0)
			PBBDevices.selectSPISlave(1,0)
			PBBDevices.deSelectSPISlaves(0)
			
			if (digInput == (config1<<8|config2)):
				#time.sleep(1)
				print "Desired voltage is set"
			else:
				print "worng input, input voltage should be less than 10 Volts"
	
	def measurePowerSupplies(self):
		for i in range(7):
			PBBDevices.selectSPISlave(2,0)
			PBBDevices.deSelectSPISlaves(0)
			PBBDevices.selectSPISlave(2,0)
			PBBDevices.deSelectSPISlaves(0)
			PBBDevices.selectSPISlave(2,0)
			val = PBBDevices.configure7949(i,0)
			PBBDevices.deSelectSPISlaves(0)
			PBBDevices.selectSPISlave(2,0)
			ignore = 1
			attempts = 0
			while(ignore and attempts<10):
				val = PBBDevices.read7949(0)
				print "Voltage readback at channel %i is %f, ignore: %i" %((i,(float((val & 0x7ffe0000)>>17)/float(0x3fff)) * 4.096,ignore))
				cfg = ((val & 0x0001fff8)>>3)
				ignore = val>>31
				attempts+=1
			print "Voltage readback at channel %i is %f, ignore: %i" %((i,(float((val & 0x7ffe0000)>>17)/float(0x3fff)) * 4.096,ignore))
			PBBDevices.deSelectSPISlaves(0)
		
	
if (__name__ == "__main__"):
	excclass = "error"
	message = "first error"
	syslog.syslog("Processing started")
	syslog.syslog(syslog.LOG_ERR, "%s: %s" % (excclass, message))
	#PBBDevices.initializeHardware()
	#PBBDevices.deSelectSPISlaves(0)
	#PBBDevices.selectSPISlave(2,0)
	#PBBDevices.freeHardwareResources()
	#
	x = HVPrint()
	x.measureTemperature()
	#x.enableHV()
	#x.measurePowerSupplies()
	x.setCLMidVoltage()
	
	#	if error:
#		syslog.syslog(syslog.LOG_ERR, 'Processing started')
	


