#include <stdio.h>
#include <string.h>

#include "../include/constants.h"
#include "../include/game_list.h"


int size = 0; // Current number of elements in the map
char keys[GAME_LIST_SIZE][100]; // Array to store the keys or game id
int values[GAME_LIST_SIZE][2]; // Array to store the ConnectedFD of each client

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
void insert(char key[], int value[2]) {
	int index = getIndex(key);
	if (index == -1) { // Key not found
		strcpy(keys[size], key);
		for (int i = 0; i < 2; i++) {
			values[size][i] = value[i];
		}
		size++;
	}
	else { // Key found
		for (int i = 0; i < 2; i++) {
			values[index][i] = value[i];
		}
	}
}

// Function to get the value of a key in the map
int* get(char key[]) {
	int index = getIndex(key);
	if (index == -1) { // Key not found
		return NULL;
	}
	else { // Key found
		return values[index];
	}
}

// Function to print the map
void printGameList() {
	for (int i = 0; i < size; i++) {
		printf("%s: %d, %d\n", keys[i], values[i][0], values[i][1]);
	}
}
