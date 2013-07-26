def main():
	import HVControlBoard
	x = HVControlBoard.HVControlBoard()
	print "Control Board Temperature: %f" %(x.measureTemperature())
	x.setCLMidVoltage(1200)
	print x.measurePowerSupplies()
	print x.getCLMidVoltage()
	print x.getCLMidCurrent()


if (__name__ == "__main__"):
	main()
	
	


