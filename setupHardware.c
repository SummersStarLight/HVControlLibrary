#include <stdio.h>
#include <unistd.h>
#include <ftdi.h>
#include <stdint.h>

void* ftdic;

int OutputByte(uint8_t output_b)
{
    int result=0; // returned error code
    ftdi_write_data((struct ftdi_context*)ftdic, &output_b, 1);
    return result;
}

uint8_t InputByte()
{
    uint8_t buf;
    ftdi_read_pins((struct ftdi_context*)ftdic,&buf);
    return buf;
}

int initializeHardware()
{
    int f;
    ftdic = (struct ftdi_context*)malloc(sizeof(struct ftdi_context));
    if (ftdi_init((struct ftdi_context*)ftdic) < 0)
    {
        fprintf(stderr, "ftdi_init failed\n");
        return EXIT_FAILURE;
    }

    f = ftdi_usb_open((struct ftdi_context*)ftdic, 0x0403, 0x6014);
    if (f < 0 && f != -5)
    {
        fprintf(stderr, "unable to open ftdi device: %d (%s)\n", f, ftdi_get_error_string((struct ftdi_context*)ftdic));
        exit(-1);
    }

    ftdi_set_interface((struct ftdi_context*)ftdic,INTERFACE_A);
    ftdi_set_bitmode((struct ftdi_context*)ftdic, 0xfb, BITMODE_BITBANG);
    return 0;
}

int freeHardwareResources()
{
    ftdi_disable_bitbang((struct ftdi_context*)ftdic);
    ftdi_usb_close((struct ftdi_context*)ftdic);
    ftdi_deinit((struct ftdi_context*)ftdic);
    free(ftdic);
    return 0;
}


