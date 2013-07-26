#ifndef SPIDEVICES_H
#define SPIDEVICES_H
void configureTSensor(uint8_t);
float readTemperature(uint8_t);
uint8_t selectSPISlave(uint8_t,uint8_t);
void deSelectSPISlaves(uint8_t);
uint8_t setDAC7731(uint16_t,uint8_t);
uint8_t readGPIOConfiguration(uint8_t);
uint8_t configureGPIO(uint8_t slaveMode);
uint8_t enableHV(uint8_t);
uint8_t disableHV(uint8_t);
uint8_t HVEnableStatus(uint8_t);
uint8_t MCP23SRegisterTransaction(uint8_t,uint8_t, uint8_t, uint8_t);
uint32_t configure7949(uint8_t,uint8_t);
uint32_t read7949(uint8_t);
#endif
