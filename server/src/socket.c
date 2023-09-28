#include "../include/parser.h"
#include "../include/socket.h"

// Send a message to a client
void *sendMsg(int ConnectFD, char *response) {
  // Read from the client
  char buffer[1024];

  ssize_t bytesRead;
  // Write a response back to the client
  ssize_t bytesWritten = write(ConnectFD, response, strlen(response));
  if (bytesWritten == -1) {
    perror("write failed");
    close(ConnectFD);
  }

  return NULL;
}

// Función que maneja a cada cliente
void *manageClient(void *arg) {
  int clientNumber = 0;
	// Create player
	player_t player;
	player.ConnectFD = *((int *)arg);
  printf("ConnectFD: %d\n", player.ConnectFD);

  // Read from the client
  char buffer[1024];
  ssize_t bytesRead;


  for (;;) {
    bytesRead = read(player.ConnectFD, buffer, sizeof(buffer));

    if (bytesRead == -1) {
      perror("read failed");
      close(player.ConnectFD);
      break;
    }

    if (bytesRead == 0) {
      printf("Client disconnected\n");
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
  int ConnectFD = accept(SocketFD, NULL, NULL);
  if (ConnectFD == -1) {
    // TODO: call logger
    perror("accept failed");
    return;
  }

  // Crea un nuevo hilo para manejar al cliente actual
  pthread_t thread;
  pthread_create(&thread, NULL, manageClient, (void *)&ConnectFD);

  // TODO: call logger
  printf("Client connected\n");
}


