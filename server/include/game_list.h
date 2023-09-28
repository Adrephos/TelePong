#ifndef GAME_LIST_H
#define GAME_LIST_H


typedef struct {
  char *username;
  int ConnectFD;
} player_t;

typedef struct {
	char *x;
	char *y;
	char *dx;
	char *dy;
} ball_t;

typedef struct {
  char *leftPaddle;
  char *rigthPaddle;
	player_t *player1;
	player_t *player2;
	ball_t *ball;
} game_t;


game_t emptyGame();
int isEmptyGame(game_t game);
char *newKey();
void insert(char key[], game_t game_state);
game_t get(char key[]);
void printGameList();

#endif
