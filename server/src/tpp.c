/*
 * tpp.c
 *  TelePong protocol
 *
 *  This file contains the functions that handle the TelePong protocol
 */
#include "../include/tpp.h"
#include "../include/game_list.h"
#include "../include/socket.h"
#include <stdio.h>
#include <stdlib.h>

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
  message_t m = newMessage(msgType, payload);
  char *msg = messageToString(m);
  sendMsg(player->ConnectFD, msg);
}

void registerPlayer(player_t *player, char username[]) {
  player->username = strdup(username);
	char *payload = malloc(sizeof(char) * 100);
	sprintf(payload, "Player registered with username: %s", username);
  response(player, SUCC, payload);
}

// Create game
void createGame(player_t *player) {
  char *gameId = newKey();

  // Create game
  game_t game;
  game.player1 = player;
  game.player2 = NULL;

  // Add game to list
  insert(gameId, game);
  // TODO: log game created
  printf("%s\n ", gameId);
  printGameList();

  char *payload = malloc(sizeof(char) * 100);
  sprintf(payload, "Game created with id: %s", gameId);

  response(player, SUCC, payload);
}

void startGame(char *gameId) {
	game_t game = get(gameId);

	response(game.player1, START, "");
}

void joinGame(player_t *player, char *gameId) {
  game_t game = get(gameId);

  if (isEmptyGame(game) == 1) {
    // TODO: log game does not exist and make response func
    response(player, ERR, "Game does not exist");
    return;
  } 

	if (game.player2 == NULL) {
    game.player2 = player;
  } else {
    // TODO: log game is full and make response func
    response(player, ERR, "Game is full");
    return;
  }

  insert(gameId, game);
  printGameList();

  char *payload = malloc(sizeof(char) * 100);

  // TODO: log game joined
  sprintf(payload, "Joined game with id: %s", gameId);

  response(player, SUCC, payload);
	//
	startGame(gameId);
}



int initServer(int port) {
  struct sockaddr_in sa;
  int SocketFD = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
  if (SocketFD == -1) {
    perror("cannot create socket");
    exit(EXIT_FAILURE);
  }

  memset(&sa, 0, sizeof sa);

  sa.sin_family = AF_INET;
  sa.sin_port = htons(port);
  sa.sin_addr.s_addr = htonl(INADDR_ANY);

  if (bind(SocketFD, (struct sockaddr *)&sa, sizeof sa) == -1) {
    // TODO: call logger
    perror("bind failed");
    close(SocketFD);
    exit(EXIT_FAILURE);
  }

  if (listen(SocketFD, 10) == -1) {
    // TODO: call logger
    perror("listen failed");
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

  // Cierra el socket principal solo cuando desees finalizar el servidor
  close(SocketFD);
  return EXIT_SUCCESS;
}
