CC=gcc
IDIR =./include
CFLAGS=-I$(IDIR) -g

ODIR=./obj
LDIR =./lib
SDIR =./src
BDIR =./bin

_DEPS = socket.h constants.h game_list.h tpp.h parser.h logfile.h
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = main.o socket.o game_list.o game_list.o tpp.o parser.o logfile.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

$(ODIR)/%.o: $(SDIR)/%.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

PongServer: $(OBJ)
	$(CC) -o $(BDIR)/$@ $^ $(CFLAGS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~ 
