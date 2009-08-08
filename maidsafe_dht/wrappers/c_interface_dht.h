#ifndef __C_INTERFACE_DHT_H
#define __C_INTERFACE_DHT_H


void initialise_and_connect_to_network(char *ip,int port,int pport_to_start);
void disconnect_from_network();
char const  * wrapper_for_dht_get(char *key,int flag );
void wrapper_for_dht_put(char *key , char *value);
void wrapper_for_dht_start_as_server(int port);



extern "C" void START(char *ip,int port,int pport_to_start){
	initialise_and_connect_to_network(ip,port,pport_to_start);
}

extern "C" void STOP(){
	disconnect_from_network();
}

extern "C" char const * DHT_GET(char *key,int flag=0 )
{
	return  wrapper_for_dht_get(key,flag);
}
extern "C" void DHT_PUT(char *key , char *value)
{
	 wrapper_for_dht_put(key , value);
}
extern "C" void DHT_START_AS_SERVER(int port)
{
	 wrapper_for_dht_start_as_server(port);
}


#endif
