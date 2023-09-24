#include <arpa/inet.h>
#include <netinet/in.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#include "../include/socket.h"

// Send a message to a client
void *send_msg(void *arg, char *response) {
  int ConnectFD = *((int *)arg);

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
void *mange_client(void *arg) {
  int ConnectFD = *((int *)arg);

  // Read from the client
  char buffer[1024];
  ssize_t bytesRead;

  for (;;) {
    bytesRead = read(ConnectFD, buffer, sizeof(buffer));
		printf("%d", ConnectFD);

    if (bytesRead == -1) {
      perror("read failed");
      close(ConnectFD);
      break;
    }

    if (bytesRead == 0) {
      printf("Client disconnected\n");
      break;
    } else {
      buffer[bytesRead] = '\0'; // Null-terminate the received data
      printf("Received data from client: %s\n", buffer);

      // Write a response back to the client
      const char *response = "Hello from the server!";
      ssize_t bytesWritten = write(ConnectFD, response, strlen(response));
      if (bytesWritten == -1) {
        perror("write failed");
        close(ConnectFD);
        break;
      }
    }
  }

  close(ConnectFD); // Cierra el socket cuando hayas terminado de manejar al
                    // cliente
  return NULL;
}

int init_server(int port) {
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
    perror("bind failed");
    close(SocketFD);
    exit(EXIT_FAILURE);
  }

  if (listen(SocketFD, 10) == -1) {
    perror("listen failed");
    close(SocketFD);
    exit(EXIT_FAILURE);
  }

  for (;;) {
    int ConnectFD = accept(SocketFD, NULL, NULL);
    printf("ConnectFD: %d\n", ConnectFD);
    printf("SocketFD: %d\n", SocketFD);
    if (ConnectFD == -1) {
      perror("accept failed");
      continue;
    }

    // Crea un nuevo hilo para manejar al cliente actual
    pthread_t thread;
    pthread_create(&thread, NULL, mange_client, (void *)&ConnectFD);

    // No necesitas hacer un pthread_join aquí

    printf("Client connected\n");
  }

  // Cierra el socket principal solo cuando desees finalizar el servidor
  close(SocketFD);
  return EXIT_SUCCESS;
}
