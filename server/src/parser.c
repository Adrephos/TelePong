#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../include/parser.h"

// From buffer, call the method that corresponds to the message type
void parseMessage(player_t* player, char *buffer) {
  char *token;
  char payload[100];
  const char s[2] = " ";

	// TODO: log message received
  printf("Parsing message %s\n", buffer);

  token = strtok(buffer, s);

	char *msgType = token;

  int i = 0;
  while (token != NULL) {
    if (i > 0) {
			if (i == 1) {
				strcpy(payload, "");
			} else if (i > 1) {
				strcat(payload, s);
			}
			strcat(payload, token);
    }
    token = strtok(NULL, s);
		i++;
  }

  if (strcmp(msgType, CREATE) == 0) {
    createGame(player);
  } else if (strcmp(msgType, JOIN) == 0) {
    joinGame(player, payload);
  } else if (strcmp(msgType, REGISTER) == 0) {
    registerPlayer(player, payload);
  } else if (strcmp(msgType, QUIT) == 0) {
		response(player, QUIT, "See yaa!!");
  } else {
		response(player, ERR, "Invalid message type");
  }
	return;
}
