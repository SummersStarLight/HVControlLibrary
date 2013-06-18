#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include "utils.h"
void Usleep(uint16_t usec)
{
  volatile uint32_t i;
  for(i=0;i<usec*10000;i++);
}
