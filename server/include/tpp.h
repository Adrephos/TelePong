#ifndef PROTOCOL_H
#define PROTOCOL_H

#include "game_list.h"

#define REGISTER "REGISTER"
#define CREATE "CREATE"
#define JOIN "JOIN"
#define START "START"
#define POST_STATE "POST_STATE"
#define GET_STATE "GET_STATE"
#define QUIT "QUIT"
#define SUCC "SUCC"
#define ERR "ERR"

// Message structure
typedef struct {
  char *msgType;
  char *payload;
} message_t;

message_t newMessage(char *msgType, char *payload);

void response(player_t *player, char *msgType, char *payload);
void registerPlayer(player_t* player, char *username);
void createGame(player_t* player);
void joinGame(player_t* player, char *gameId);
void postGameStateResponse(player_t *player);
void postGameStateRequest(player_t *player, char **commandArgs);
int initServer(int port);

#endif
