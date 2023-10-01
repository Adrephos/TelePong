#include "../include/tpp.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

char pathVariable[100];

int setPath(char *path) {
  sprintf(pathVariable, "%s", path);
  return 0;
}

char *getTime() {
  time_t rawtime;
  struct tm *timeinfo;

  time(&rawtime);
  timeinfo = localtime(&rawtime);

  char *processedTime = ctime(&rawtime);
  processedTime[strcspn(processedTime, "\n")] = 0;

  return processedTime;
}

char *logMessage(char *msgType, char *logRegister) {
  char *msgToLog;
  if (strcmp(msgType, CREATE) == 0) {
    sprintf(msgToLog, "Game created with id %s", logRegister);
		return msgToLog;
	}if (strcmp(msgType, START) == 0) {
    sprintf(msgToLog, "Game with id %s started", logRegister);
		return msgToLog;
	} else {
		sprintf(msgToLog, "%s", logRegister);
		return msgToLog;
	}
}

int logWrite(const char *type, const char *logRegister) {
  FILE *file;
  if ((file = fopen(pathVariable, "a")) == NULL) {
    printf("Error opening file %s\n", pathVariable);
    return 1;
  }

  char *time = getTime();

  // Calculate the required memory size for the log buffer
  int logBufferSize = strlen(time) + strlen(type) + strlen(logRegister) +
                      20; // 20 for formatting characters

  char *log =
      (char *)malloc(logBufferSize); // Allocate memory for the log buffer

  if (log == NULL) {
    printf("Error allocating memory for log buffer.\n");
    fclose(file);
    return 1;
  }

  sprintf(log, "[ %s ] %s : %s\n", time, type, logRegister);

  if (fputs(log, file) >= 0) {
    printf("%s", log);
  }

  free(log); // Deallocate memory for the log buffer
  fclose(file);

  return 0;
}
