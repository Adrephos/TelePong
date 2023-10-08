/*
 * tpp.c
 *  TelePong protocol
 *
 *  This file contains the functions that handle the TelePong protocol
 */
#include "../include/tpp.h"
#include "../include/game_list.h"
#include "../include/logfile.h"
#include "../include/socket.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Create a message struct
message_t newMessage(char *msgType, char *payload) {
  message_t m = {msgType, payload};
  return m;
}

// Convert a message struct to a string
char *messageToString(message_t m) {
  char *str = malloc(sizeof(char) * 100);
  sprintf(str, "%s %s", m.msgType, m.payload);
  return str;
}

// Send a message to a client
void response(player_t *player, char *msgType, char *payload) {
  message_t m = newMessage(strdup(msgType), strdup(payload));
  char *msg = messageToString(m);
  char *logMsg = logMessage(strdup(msgType), strdup(payload));
  sendMsg(player->ConnectFD, msg);
	logWrite(msgType, logMsg);
}

void registerPlayer(player_t *player, char username[]) {
  player->username = strdup(username);
  char *payload = malloc(sizeof(char) * 100);
  sprintf(payload, "Player registered with username %s", username);
  response(player, SUCC, payload);
}

// Create game
void createGame(player_t *player) {
  char *gameId = newKey();

  // Set player number and game id
  player->PlayerNumber = 1;
  player->gameId = strdup(gameId);
  // Create game
  game_t game = *emptyGame();
  game.player1 = player;
  game.player2 = NULL;

  // Add game to list
  insert(gameId, game);

  char *payload = malloc(sizeof(char) * 100);
  sprintf(payload, "%s", gameId);

  response(player, CREATE, payload);
  printGameList();
}

void startGame(char *gameId) {
  game_t game = get(gameId);

  response(game.player1, START, game.player2->username);

	// Print paddle and ball-
	printf("Paddle 1: %s Paddle 2: %s\n", game.leftPaddle, game.rigthPaddle);
	// Print plyers fd and player PlayerNumber
	printf("Player 1 fd: %d %d Player 2 fd: %d %d\n", game.player1->ConnectFD, game.player1->PlayerNumber, game.player2->ConnectFD, game.player2->PlayerNumber);

	postGameStateResponse(game.player1);
	postGameStateResponse(game.player2);
}

void joinGame(player_t *player, char *gameId) {
  player->PlayerNumber = 2;
  player->gameId = gameId;
  game_t game = get(gameId);

  if (isEmptyGame(game) == 1) {
    response(player, ERR, "Game does not exist");
    return;
  }

  if (game.player2 == NULL) {
    game.player2 = player;
  } else {
    response(player, ERR, "Game is full");
    return;
  }

  insert(gameId, game);

  char *payload = malloc(sizeof(char) * 100);

  sprintf(payload, "%s", game.player1->username);
  response(player, SUCC, payload);
  printGameList();
  startGame(gameId);
}

void postGameStateResponse(player_t *player) {
  game_t game = get(player->gameId);
  char *payload = malloc(sizeof(char) * 100);
  char *paddle = malloc(sizeof(char) * 100);

  if (player->PlayerNumber == 1) {
    strcpy(paddle, game.rigthPaddle);
  } else {
    strcpy(paddle, game.leftPaddle);
  }

  sprintf(payload, "%s %s %s %s %s %s", paddle, game.ball->x, game.ball->y,
          game.ball->dx, game.ball->dy, game.ball->speed);

  response(player, POST_STATE, payload);
}

void postGameStateRequest(player_t *player, char **commandArgs) {
  game_t game = get(player->gameId);

  if (player->PlayerNumber == 1) {
    game.leftPaddle = strdup(commandArgs[1]);
  } else {
    game.rigthPaddle = strdup(commandArgs[1]);
  }
  game.ball->x = strdup(commandArgs[2]);
  game.ball->y = strdup(commandArgs[3]);
  game.ball->dx = strdup(commandArgs[4]);
  game.ball->dy = strdup(commandArgs[5]);
  game.ball->speed = strdup(commandArgs[6]);

  insert(player->gameId, game);

  char *logMsg = malloc(sizeof(char) * 100);
  sprintf(logMsg, "Game state updated for game %s from player %s",
          player->gameId, player->username);

	// Send game state to other player
	if (player->PlayerNumber == 1) {
		postGameStateResponse(game.player2);
	} else {
		postGameStateResponse(game.player1);
	}

  // response(player, SUCC, strdup(logMsg));
}

int initServer(int port) {
  struct sockaddr_in sa;
  int SocketFD = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
  char *logMsg = malloc(sizeof(char) * 100);
  if (SocketFD == -1) {
    sprintf(logMsg, "Cannot create socket");
    logWrite(ERR, logMsg);
    exit(EXIT_FAILURE);
  }

  memset(&sa, 0, sizeof sa);

  sa.sin_family = AF_INET;
  sa.sin_port = htons(port);
  sa.sin_addr.s_addr = htonl(INADDR_ANY);

  if (bind(SocketFD, (struct sockaddr *)&sa, sizeof sa) == -1) {
    sprintf(logMsg, "Bind failed");
    logWrite(ERR, logMsg);
    close(SocketFD);
    exit(EXIT_FAILURE);
  }

  if (listen(SocketFD, 10) == -1) {
    // TODO: call logger
    sprintf(logMsg, "Listen failed");
    logWrite(ERR, logMsg);
    close(SocketFD);
    exit(EXIT_FAILURE);
  }

  // Ready
  char *msg = malloc(sizeof(char) * 100);
  sprintf(msg, "\033[1;32mServer ready\033[1;33m\nPort: %d \nIP: %s", port,
          inet_ntoa(sa.sin_addr));
  printf("%s\033[0m\n------------------\n", msg);

  for (;;) {
    acceptClientConnection(SocketFD);
  }

  // Close the main socket only when we want to terminate the server.
  close(SocketFD);
  return EXIT_SUCCESS;
}
