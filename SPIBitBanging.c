#include <stdint.h>
#include "SPIBitBanging.h"
#include "setupHardware.h"
#include "utils.h"

/* SPI MODE 0 : Clock Polarity(0), Clock Phase(0)
 * SPI MODE 1 : Clock Polarity(0), Clock Phase(1)
 * SPI MODE 2 : Clock Polarity(1), Clock Phase(0)
 * SPI MODE 3 : Clock Polarity(1), Clock Phase(1)
 */

uint8_t SPIProtocol(uint8_t DataOut,uint8_t spiMode,uint8_t clockCycles)
{
    uint8_t ChipSelect = 0x00;
    uint8_t Clock = 0x00;
    uint8_t DataIn = 0x00;
    uint8_t count = 0;
    uint8_t slaveIn = DataOut;  
    
    (spiMode>>1)?(Clock=0xff):(Clock=0x00);
    do{ 
        OutputByte((Clock&CLKMASK)|(slaveIn&DOMASK)|(ChipSelect&CSMASK)); //leading edge
        Usleep(HALFCLOCK);
        (!(spiMode%2))?(DataIn = (DataIn<<1)|((InputByte()&DIMASK)>>2)):(slaveIn=DataOut<<count);
        OutputByte((~Clock&CLKMASK)|(slaveIn&DOMASK)|(ChipSelect&CSMASK)); //trailing edge
        Usleep(HALFCLOCK);
		(spiMode%2) ?(DataIn = (DataIn<<1)|((InputByte()&DIMASK)>>2)):(slaveIn = DataOut<<(count+1)); 
    }while ( ++count<clockCycles);
    OutputByte((Clock&CLKMASK)|(ChipSelect&CSMASK)|(slaveIn&DOMASK));
    return DataIn;
}

