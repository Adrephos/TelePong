#include "../include/parser.h"
#include "../include/socket.h"
#include "../include/constants.h"
#include "../include/logfile.h"
#include <stdlib.h>

// Send a message to a client
void *sendMsg(int ConnectFD, char *response) {
  // Write a response back to the client
	char *logMsg = malloc(sizeof(char) * 100);
  ssize_t bytesWritten = write(ConnectFD, response, strlen(response));
  if (bytesWritten == -1) {
		sprintf(logMsg, "Could not write to client FD %d", ConnectFD);
		logWrite(ERR, logMsg);
    close(ConnectFD);
  }

  return NULL;
}

// Function that handles each client
void *manageClient(void *arg) {
  int clientNumber = 0;
	char *logMsg = malloc(sizeof(char) * 100);
	// Create player
	player_t player;
	player.ConnectFD = *((int *)arg);
	sprintf(logMsg, "Client connected with FD %d", player.ConnectFD);
	logWrite(SUCC, logMsg);

  // Read from the client
  char buffer[RECV_BUFFER_SIZE];
  ssize_t bytesRead;


  for (;;) {
    bytesRead = read(player.ConnectFD, buffer, sizeof(buffer));

    if (bytesRead == -1) {
			sprintf(logMsg, "Could not read from client FD %d", player.ConnectFD);
			logWrite(ERR, logMsg);
      close(player.ConnectFD);
      break;
    }

    if (bytesRead == 0) {
			sprintf(logMsg, "Client with FD %d disconnected", player.ConnectFD);
			logWrite(QUIT, logMsg);
      break;
    } else {
      buffer[bytesRead] = '\0'; // Null-terminate the received data

      parseMessage(&player, buffer);

    }

  }

  close(player.ConnectFD); // Close the socket
  return NULL;
}

void acceptClientConnection(int SocketFD) {
	char *logMsg = malloc(sizeof(char) * 100);
  int ConnectFD = accept(SocketFD, NULL, NULL);
  if (ConnectFD == -1) {
		sprintf(logMsg, "Accept failed");
		logWrite(ERR, logMsg);
    return;
  }

  // Create a new thread to handle the current client
  pthread_t thread;
  pthread_create(&thread, NULL, manageClient, (void *)&ConnectFD);
}


