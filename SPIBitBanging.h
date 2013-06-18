#ifndef SPI_H
#define SPI_H
#define CSMASK    0x01
#define CLKMASK   0x02
#define DIMASK    0x04
#define DOMASK    0x80

//delay between 
#define LONGSLEEP 100
#define SHORTSLEEP 20 
#define HALFCLOCK 4

uint8_t SPIProtocol(uint8_t,uint8_t,uint8_t);
//uint8_t SPIAD7949Protocol(uint8_t DataOut);
#endif
