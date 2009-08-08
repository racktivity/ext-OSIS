/usr/bin/c++ -c c_interface_dht.cpp -I ../src/ -I../src/

/usr/bin/c++  -shared    -funswitch-loops -fgcse-after-reload -ftree-vectorize -fpredictive-commoning -Wextra -Wall  -Wextra -Wfloat-equal -Wlong-long  -Wredundant-decls -Wstrict-overflow=5   -Wredundant-decls -Wunused-function  -Wunused-label  -Wunused-parameter -Wunused-value -Wunused-variable -std=c++98 -Wall -ansi -D_FORTIFY_SOURCE=2 -fno-stack-protector -D_FILE_OFFSET_BITS=64 -O3 -DNDEBUG -Wuninitialized    c_interface_dht.o  -o  libc_interface_dht.so -rdynamic ../src/build/Linux/Release/lib/libPDkademlialib.a ../src/build/Linux/Release/lib/libPDrpcprotocollib.a  ../src/build/Linux/Release/lib/libPDtransportlib.a  ../src/build/Linux/Release/lib/libPDbaselib.a  ../src/build/Linux/Release/lib/libPDpbmsgslib.a -lgtest ../src/build/Linux/Release/lib/libPDupnplib.a -Wl,-Bstatic -lboost_thread-gcc43-mt -lsqlite3 -lprotobuf -lboost_system-gcc43-mt -lboost_filesystem-gcc43-mt -lcryptopp -lboost_regex-gcc43-mt -lboost_date_time-gcc43-mt -Wl,-Bdynamic -lrt -lc -lm -ldl -lpthread  -ltokyocabinet  -L /usr/local/lib 


cp -R libc_interface_dht.so /usr/lib/
cp -R libc_interface_dht.so /opt/qbase3/lib/

if [ -f "dht.so" ]; then
	rm -f dht.so
fi

if [ -f "dht.c" ]; then
	rm -f dht.c
fi

# To generate a interface module
python setup.py  build_ext --inplace
