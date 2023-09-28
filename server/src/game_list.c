#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../include/constants.h"
#include "../include/game_list.h"

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
game_t emptyGame() {
  game_t empty_game;
  empty_game.player1 = NULL;
  empty_game.player2 = NULL;
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
    return emptyGame();
  } else { // Key found
    return values[index];
  }
}

// Function to print the map
void printGameList() {
  for (int i = 0; i < size; i++) {
		// If not null print
		if (values[i].player1 != NULL) {
			printf("Game: %s\n", keys[i]);
			printf("	Player 1: %s\n", values[i].player1->username);
			if (values[i].player2 != NULL) {
				printf("	Player 2: %s\n", values[i].player2->username);
			}
    }
  }
}
