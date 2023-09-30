#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../include/parser.h"

char **parseArgs(char *buffer) {
	char *token;
	char *aux = strdup(buffer);
	const char s[2] = " ";

	token = strtok(aux, s);

	char **gameState = (char**) malloc(6 * sizeof(char*));
	int i = 0;
	while (token != NULL) {
		gameState[i] = token;
		token = strtok(NULL, s);
		i++;
	}

	return gameState;
}

// From buffer, call the method that corresponds to the message type
void parseMessage(player_t *player, char *buffer) {
	char **parsedArgs = parseArgs(buffer);

  char *msgType = parsedArgs[0];
	char *payload = parsedArgs[1];

	char *padPos = parsedArgs[2];
	char *ballX = parsedArgs[3];
	char *ballY = parsedArgs[4];
	char *ballDx = parsedArgs[5];
	char *ballDy = parsedArgs[6];

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

