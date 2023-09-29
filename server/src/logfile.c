#include <stdio.h>
#include <string.h>
#include <time.h>

char pathVariable[100];

int setPath(char *path) {
    sprintf(pathVariable, path);
    return 0;
}

char* getTime(){
    time_t rawtime;
    struct tm * timeinfo;

    time ( &rawtime );
    timeinfo = localtime ( &rawtime );

    char *processedTime = ctime(&rawtime);
    processedTime[strcspn(processedTime, "\n")] = 0;

    return processedTime; 
}

int logWrite(char *type, char *logRegister) {
    FILE *file;
    if ((file = fopen(pathVariable, "a")) == NULL) {
        printf("Error opening file.\n");
        return 1;
    }

    char *time = getTime();
    char *log;
    printf(time);

    sprintf( log, "[ %s ] %s : %s\n", time, type, logRegister );
    if (fputs(log, file) >= 0) {
        printf(log);
    }
    fclose(file);

    return 0;
}