#ifndef LOGFILE_H
#define LOGFILE_H

int setPath(char *path);
int logWrite(char *type, char *logRegister);
char *logMessage(char *msgType, char *logRegister);

#endif
