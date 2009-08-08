#ifndef __C_INTERFACE_DHT1_H
#define __C_INTERFACE_DHT1_H

#include<stdio.h>
void START(char *ip,int port,int pport_to_start);
void STOP();
char * DHT_GET(char *key, int flag);
void DHT_PUT(char *key , char *value);
void DHT_START_AS_SERVER(int port);


#endif
