%module PBBDevices
%{
    #include "setupHardware.h"
    #include "utils.h"
    #include "SPIDevices.h"
    #include "ftdi.h"
%}

%include "utils.h"
%include "setupHardware.h"
%include "SPIDevices.h"
%include "stdint.i"
