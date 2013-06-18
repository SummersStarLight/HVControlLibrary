PROJECT = PBBDevices
LIB=-lftdi -lpython2.7
INC=-I/usr/include/python2.7/ -I/usr/lib/python2.7/config/
CC=gcc
SWIG=swig
LINKER=ld
CFLAGS=-Wall -fPIC -fno-stack-protector
TGT=_$(PROJECT).so
SRCS=$(wildcard *.c)
WRAPSRC=$(wildcard *.i)
OBJS=$(SRCS:.c=.o) $(WRAPSRC:.i=_wrap.o) 

# clear out all suffixes
.SUFFIXES:
# list only those we use
.SUFFIXES: .o .c .i

all: $(TGT)

# define a suffix rule for .c -> .o
.c.o :
	$(CC) $(CFLAGS) -c $< $(LIB) $(INC)

%_wrap.c: %.i
	$(SWIG) -python $<

$(TGT): $(OBJS) 
	$(LINKER) -shared -o $@ $^ $(LIB) $(INC)
	
clean:
	rm -f $(TGT) *.o *.pyc *_wrap.c $(PROJECT).py
