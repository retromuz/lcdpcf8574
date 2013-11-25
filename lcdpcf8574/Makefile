lcdpcf8574test: liblcdpcf8574.so lcdpcf8574test.o
	$(CXX) -Wall -L. lcdpcf8574test.cpp -lrt -llcdpcf8574 -lwiringPi -o lcdpcf8574test.o 
liblcdpcf8574.so: lcdpcf8574.cpp
	$(CXX) -fPIC -c lcdpcf8574.cpp -o lcdpcf8574.o
	$(CXX) -shared -Wl,-soname,liblcdpcf8574.so.1 -lwiringPi -o liblcdpcf8574.so.1.0 lcdpcf8574.o
	ln -sf liblcdpcf8574.so.1.0 liblcdpcf8574.so
	ln -sf liblcdpcf8574.so.1.0 liblcdpcf8574.so.1
install: liblcdpcf8574.so
	cp lcdpcf8574.h /usr/local/include/lcdpcf8574.h
	cp liblcdpcf8574.so.1.0 /usr/local/lib/
	ln -sf /usr/local/lib/liblcdpcf8574.so.1.0 /usr/local/lib/liblcdpcf8574.so
	ln -sf /usr/local/lib/liblcdpcf8574.so.1.0 /usr/local/lib/liblcdpcf8574.so.1
	ldconfig
clean:
	@rm *.o *.so *.so.*
