#define MAX_GAME_STATE_SIZE 1000

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../include/parser.h"

char **parseArgs(char *buffer) {
	printf("Parsing args ----------------------\n");
	char *token;
	char *aux = strdup(buffer);
	const char s[2] = " ";
	printf("Aux executed ----------------------\n");

	token = strtok(aux, s);

	printf("Before gameState ----------------------\n");

	char **gameState = (char**) malloc(MAX_GAME_STATE_SIZE * sizeof(char*));
	//char** gameState = malloc(MAX_GAME_STATE_SIZE * sizeof(char*));
	//memset(gameState, 0, sizeof(gameState)); // initialize the array to NULL
	printf("After gameState ----------------------\n");
	
	int i = 0;
	while (token != NULL) {	//&& i < MAX_GAME_STATE_SIZE
		gameState[i] = token;
		token = strtok(NULL, s);
		i++;
	}
	printf("Finish method  ----------------------\n");

	return gameState;
}

// From buffer, call the method that corresponds to the message type
void parseMessage(player_t *player, char *buffer) {
	char **parsedArgs = parseArgs(buffer);

  char *msgType = parsedArgs[0];
	char *payload = parsedArgs[1];

  if (strcmp(msgType, CREATE) == 0) {
    createGame(player);
  } else if (strcmp(msgType, JOIN) == 0) {
    joinGame(player, payload);
  } else if (strcmp(msgType, REGISTER) == 0) {
    registerPlayer(player, payload);
  } else if (strcmp(msgType, POST_STATE) == 0) {
		postGameStateRequest(player, parsedArgs);
  } else if (strcmp(msgType, GET_STATE) == 0) {
		postGameStateResponse(player);
  } else if (strcmp(msgType, QUIT) == 0) {
    response(player, QUIT, "See yaa!!");
  } else {
    response(player, ERR, "Invalid message type");
  }
  return;
}

