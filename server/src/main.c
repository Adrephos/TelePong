#include "../include/tpp.h"
#include "../include/logfile.h"
#include "../include/constants.h"
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
	if (argc != 3) {
		printf("Usage: %s <port> <logfile>\n", argv[0]);
		exit(1);
	}
	setPath(argv[2]);
	initServer(atoi(argv[1]));
	
	return 0;
}
