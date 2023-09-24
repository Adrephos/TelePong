CC=gcc
IDIR =./include
CFLAGS=-I$(IDIR)

ODIR=./obj
LDIR =./lib
SDIR =./src
BDIR =./bin

LIBS=-lm

_DEPS = socket.h constants.h
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = main.o socket.o 
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

_SRC = main.c socket.c 
SRC = $(patsubst %,$(SDIR)/%,$(_SRC))

$(ODIR)/%.o: $(SRC) $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

PongServer: $(OBJ)
	$(CC) -o $(BDIR)/$@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~ 
