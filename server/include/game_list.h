#ifndef GAME_LIST_H
#define GAME_LIST_H


typedef struct {
  char *username;
  char *gameId;
  int ConnectFD;
  int PlayerNumber;
} player_t;

typedef struct {
	char *x;
	char *y;
	char *dx;
	char *dy;
	char *speed;
} ball_t;

typedef struct {
  char *leftPaddle;
  char *rigthPaddle;
	char *score1;
	char *score2;
	player_t *player1;
	player_t *player2;
	ball_t *ball;
} game_t;


game_t *emptyGame();
int isEmptyGame(game_t game);
char *newKey();
void insert(char key[], game_t game_state);
game_t get(char key[]);
void printGameList();

#endif
