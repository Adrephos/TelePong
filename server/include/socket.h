#ifndef SOCKET_H
#define SOCKET_H
#include <arpa/inet.h>
#include <netinet/in.h>
#include <pthread.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>


void *sendMsg(int ConnectFD, char *response);
void acceptClientConnection(int SocketFD);

#endif
