#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../include/protocol.h"
#include "../include/parser.h"

// From buffer, call the method that corresponds to the message type
int parseMessage(void *arg, char *buffer) {
  char *token;
  char payload[100];
  const char s[2] = " ";

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
  if (strcmp(msgType, "CREATE") == 0) {
    createGame(arg, payload);
		return 1;
  } else if (strcmp(msgType, "JOIN") == 0) {
    joinGame(arg, payload);
		return 2;
  } else {
    printf("Invalid message type\n");
  }
	return 0;
}
