#include <stdio.h>
#include <stdlib.h>

#include "../include/socket.h"
#include "../include/protocol.h"
#include "../include/game_list.h"

// Set messsage types
enum msgType { CREATE, JOIN, POST_STATE, GET_STATE, END_GAME, QUIT};

// msgType to string
char *msgTypeToString(int msgType) {
	switch(msgType) {
		case CREATE:
			return "CREATE";
		case JOIN:
			return "JOIN";
		case POST_STATE:
			return "POST_STATE";
		case GET_STATE:
			return "GET_STATE";
		case END_GAME:
			return "END_GAME";
		case QUIT:
			return "QUIT";
		default:
			return "UNKNOWN";
	}
}

// Message structure
typedef struct {
  int msgType;
  char *payload;
} message;

message newMessage(int msgType, char *payload){
	message m = { msgType, payload };
	return m;
}

char* messageToString(message m) {
	char *str = malloc(sizeof(char) * 100);
	sprintf(str, "%s -> %s", msgTypeToString(m.msgType), m.payload);
	return str;
}

// Create game
void createGame(void *arg, char *gameId) {
	int ConnectFd = *((int *)arg);

	int gamePlayers[] = { ConnectFd, -1 };

	char *payload = malloc(sizeof(char) * 100);

	// Add game to list
	insert(gameId, gamePlayers);
	printf("%s\n ", gameId);
	printGameList();

	sprintf(payload, "Game created with id: %s", gameId);

	// Create message
	message m = newMessage(CREATE, payload);
	char *msg = messageToString(m);

	// Send message
	sendMsg(arg, msg);
}

void joinGame(void *arg, char *gameId) {
	int ConnectFd = *((int *)arg);
	
	int* gamePlayers = get(gameId);

	if (gamePlayers == NULL) {
		sendMsg(arg, "Game does not exist");
		return;
	} else if (gamePlayers[1] == -1) {
		gamePlayers[1] = ConnectFd;
	} else {
		sendMsg(arg, "Game is full");
		return;
	}

	insert(gameId, gamePlayers);
	printf("%s\n ", gameId);
	printGameList();

	char *payload = malloc(sizeof(char) * 100);

	sprintf(payload, "Joined game with id: %s", gameId);

	// Create message
	message m = newMessage(JOIN, payload);
	char *msg = messageToString(m);

	// Send message 
	sendMsg(arg, msg);
}

void ping(void *arg, char *payload) {
	// Create message
	message m = newMessage(POST_STATE, payload);
	char *msg = messageToString(m);

	// Send message 
	sendMsg(arg, msg);
}
