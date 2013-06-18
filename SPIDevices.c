#include <stdio.h>
#include <stdint.h>
#include "utils.h"
#include "SPIBitBanging.h"
#include "setupHardware.h"

void configureTSensor(uint8_t slaveMode)
{
    Usleep(HALFCLOCK);
    SPIProtocol(0x80,slaveMode,8);
    Usleep(SHORTSLEEP);
    SPIProtocol(0x04,slaveMode,8);
}

float readTemperature(uint8_t slaveMode)
{
    uint8_t temp;
    float temperature;
    Usleep(SHORTSLEEP);
    temp = SPIProtocol(0x02,slaveMode,8);
    Usleep(SHORTSLEEP);
    temp = SPIProtocol(0x00,slaveMode,8);
    Usleep(SHORTSLEEP);
    temperature = (float)temp;
    temp = SPIProtocol(0x00,slaveMode,8);
    temperature +=(float)temp/256;
    Usleep(SHORTSLEEP);
    temp = SPIProtocol(0x00,slaveMode,8);
    return temperature;	
}

uint8_t configureGPIO(uint8_t slaveMode)
{
	uint8_t temp;
	Usleep(SHORTSLEEP);
	temp = SPIProtocol(0x40,slaveMode,8);
	Usleep(SHORTSLEEP);
	temp = SPIProtocol(0x00,slaveMode,8);
	Usleep(SHORTSLEEP);
	temp = SPIProtocol(0xc0,slaveMode,8);
	Usleep(SHORTSLEEP);
	return temp;
}

uint8_t readGPIOConfiguration(uint8_t slaveMode)
{
	uint8_t temp;
	Usleep(SHORTSLEEP);
	temp = SPIProtocol(0x41,slaveMode,8);
	Usleep(SHORTSLEEP);
	temp = SPIProtocol(0x00,slaveMode,8);
	Usleep(SHORTSLEEP);
	temp = SPIProtocol(0x00,slaveMode,8);
	Usleep(SHORTSLEEP);
	return temp;
}

uint8_t enableHV(uint8_t slaveMode)
{
	uint8_t temp;
	Usleep(SHORTSLEEP);
	temp = SPIProtocol(0x40,slaveMode,8);
	Usleep(SHORTSLEEP);
	temp = SPIProtocol(0x09,slaveMode,8);
	Usleep(SHORTSLEEP);
	temp = SPIProtocol(0x01,slaveMode,8);
	Usleep(SHORTSLEEP);
	return temp;
}

uint8_t disableHV(uint8_t slaveMode)
{
	uint8_t temp;
	Usleep(SHORTSLEEP);
	temp = SPIProtocol(0x40,slaveMode,8);
	Usleep(SHORTSLEEP);
	temp = SPIProtocol(0x09,slaveMode,8);
	Usleep(SHORTSLEEP);
	temp = SPIProtocol(0x00,slaveMode,8);
	Usleep(SHORTSLEEP);
	return temp;
}

uint8_t HVEnableStatus(uint8_t slaveMode)
{
	uint8_t temp;
	Usleep(SHORTSLEEP);
	temp = SPIProtocol(0x41,slaveMode,8);
	Usleep(SHORTSLEEP);
	temp = SPIProtocol(0x09,slaveMode,8);
	Usleep(SHORTSLEEP);
	temp = SPIProtocol(0x01,slaveMode,8);
	Usleep(SHORTSLEEP);
	return temp;
}

uint8_t configure7949(uint8_t channel,uint8_t spiMode)
{
	uint8_t temp1, temp2, temp3,temp4;
	uint32_t config=1;  //initialized to update configuration register -1bit
	uint8_t inputChannelConfiguration = 0x06; //3 bits
	uint8_t bandwidthConfiguration = 0x00; //half bandwidth configuration - 1bit
	uint8_t referenceSelection = 0x01; //3 bits
	uint8_t sequencerConfiguration = 0x00; //2 bits
	uint8_t readbackConfiguration = 0x00; //1bit 
	uint32_t result;
	
	config = config<<3|inputChannelConfiguration;
	config = config<<3|channel;
	config = config<<1|bandwidthConfiguration;
	config = config<<3|referenceSelection;
	config = config<<2|sequencerConfiguration;
	config = config<<1|readbackConfiguration;
	
	config<<=2; //14 configuration bits must be in the beginning of the 16 bit configuration word

	temp1 = SPIProtocol(config>>8,spiMode,8);
	temp2 = SPIProtocol(config & 0x00ff,spiMode,8);
	temp3 = SPIProtocol(0x00,spiMode,8);
	temp4 = SPIProtocol(0x00,spiMode,8);
	Usleep(LONGSLEEP);	
	result = (temp1<<24|temp2<<16|temp3<<8|temp4);
	//return (result>>5);
	return result;
}

uint8_t read7949(uint8_t spiMode)
{
	uint8_t temp1, temp2, temp3,temp4;
	uint32_t result;

	temp1 = SPIProtocol(0x00,spiMode,8);
	temp2 = SPIProtocol(0x00,spiMode,8);
	temp3 = SPIProtocol(0x00,spiMode,8);
	temp4 = SPIProtocol(0x00,spiMode,8);
	Usleep(LONGSLEEP);	
	result = (temp1<<24|temp2<<16|temp3<<8|temp4);
	//return (result>>5);
	return result;
}

uint8_t setDAC7731(uint8_t digInput,uint8_t slaveMode)
{
	uint8_t temp1,temp2;
	Usleep(SHORTSLEEP);
    temp1 =SPIProtocol(digInput,slaveMode,8);
    Usleep(SHORTSLEEP);
    return temp1;
}

void deSelectSPISlaves(uint8_t slaveMode)
{
    (slaveMode>>1)?OutputByte(0x03):OutputByte(0x01);  //raise the chipselect for the deselection
    Usleep(LONGSLEEP);
}

uint8_t selectSPISlave(uint8_t SPIaddress, uint8_t slaveMode)
{
    uint8_t temp, avrMode;   
    deSelectSPISlaves(0);
    Usleep(SHORTSLEEP);
    avrMode = 0xc0|(slaveMode>>1)<<3|(slaveMode%2)<<2;   
    temp = SPIProtocol(avrMode,0,8);
    Usleep(SHORTSLEEP);
    deSelectSPISlaves(0);
    deSelectSPISlaves(slaveMode);
    temp = SPIProtocol(SPIaddress,slaveMode,8);
    //OutputByte(0x00);
    Usleep(LONGSLEEP);
    return temp;
}


