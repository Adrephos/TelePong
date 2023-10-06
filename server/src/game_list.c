#include "../include/game_list.h"
#include "../include/constants.h"
#include "../include/logfile.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int size = 0;                  // Current number of elements in the map
char keys[GAME_LIST_SIZE][10]; // Array to store the keys or game id
game_t values[GAME_LIST_SIZE]; // Array to store the state of each game
int currKey = 999;             // Current key to be used

char *newKey() {
  char *keyGen = malloc(sizeof(char) * 10);
  currKey++;
  sprintf(keyGen, "%d", currKey);

  return keyGen;
}

// Function to create an empty game
game_t *emptyGame() {
  game_t *empty_game = malloc(sizeof(game_t));
	ball_t *ball = malloc(sizeof(ball_t));

  empty_game->player1 = NULL;
  empty_game->player2 = NULL;
	empty_game->leftPaddle = "20";
	empty_game->rigthPaddle = "20";
	empty_game->ball = ball;
	empty_game->ball->x = "640";
	empty_game->ball->y = "360";
	empty_game->ball->dx = "1";
	empty_game->ball->dy = "-1";
	empty_game->ball->speed = "10";

  free(ball);

  return empty_game;
}

// Function to know if a game is empty
int isEmptyGame(game_t game) {
  if (game.player1 == NULL && game.player2 == NULL) {
    return 1;
  } else {
    return 0;
  }
}

// Function to get the index of a key in the keys array
int getIndex(char key[]) {
  for (int i = 0; i < size; i++) {
    if (strcmp(keys[i], key) == 0) {
      return i;
    }
  }
  return -1; // Key not found
}

// Function to insert a key-value pair into the map
void insert(char key[], game_t game) {
  int index = getIndex(key);
  if (index == -1) { // Key not found
    strcpy(keys[size], key);
    values[size] = game;
    size++;
  } else { // Key found
    values[index] = game;
  }
}

// Function to get the value of a key in the map
game_t get(char key[]) {
  int index = getIndex(key);
  if (index == -1) { // Key not found
    // Return an empty game
    return *emptyGame();
  } else { // Key found
    return values[index];
  }
}

// Function to print the map
void printGameList() {
  char *logMsg = malloc(sizeof(char) * 200);
  char *logMsg2 = malloc(sizeof(char) * 100);
  strcpy(logMsg, "\n");

  for (int i = 0; i < size; i++) {
    // If not null print
    if (values[i].player1 != NULL) {
      sprintf(logMsg2, "			Game: %s\n", keys[i]);
      strcat(logMsg, logMsg2);
      sprintf(logMsg2, "			Player 1: %s\n", values[i].player1->username);
      strcat(logMsg, logMsg2);
      if (values[i].player2 != NULL) {
        sprintf(logMsg2, "			Player 2: %s\n", values[i].player2->username);
        strcat(logMsg, logMsg2);
      }
    }
  }
  logWrite("GAME LIST", logMsg);

  free(logMsg);
  free(logMsg2);
}
