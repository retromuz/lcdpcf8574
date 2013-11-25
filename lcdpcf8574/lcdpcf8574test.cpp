/*
 *  lcdpcf8574test.cpp:
 *  Test program for I²C based PCF8574 driver for HD44780 based LCD
 *  to be used with wiringPi for Raspberry Pi
 *
 * Copyright (c) 2013 Prageeth Karunadheera. http://karunadheera.com/
 ***********************************************************************
 *
 *    lcdpcf8574 is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU Lesser General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    lcdpcf8574 is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU Lesser General Public License for more details.
 *
 *    You should have received a copy of the GNU Lesser General Public License
 *    along with wiringPi.  If not, see <http://www.gnu.org/licenses/>.
 ***********************************************************************
 */

#include <sys/time.h>
#include "lcdpcf8574.h"

using namespace std;

int volatile keepRunning = 1;

void intHandler(int dummy) {
    keepRunning = 0;
    printf("intHandler called\n");
}

void show_time(lcdpcf8574 m){
	struct tm *t ;
	time_t tim ;
	struct timespec timx, timy, timst, timend;
	timx.tv_sec = 0;
//	100ms (0.1s)
//	timx.tv_nsec = 100000000;
	timx.tv_nsec = 1000000;

	char buf[32];

	for(;keepRunning == 1;){

		clock_gettime(CLOCK_REALTIME, &timst); // Works on Linux

		tim = time (NULL);
		t = localtime (&tim);

		sprintf (buf, "%02d:%02d:%02d", t->tm_hour, t->tm_min, t->tm_sec) ;

		m.lcd_puts(buf, 1, 0);

		sprintf (buf, "%02d/%02d/%04d", t->tm_mday, t->tm_mon + 1, t->tm_year+1900) ;
		m.lcd_puts(buf, 2, 0);

		if(nanosleep(&timx , &timy) < 0 ) {
			printf("Nano sleep system call failed \n");
		}
		clock_gettime(CLOCK_REALTIME, &timend); // Works on Linux

		sprintf(buf, "%ld:%ld", timend.tv_sec - timst.tv_sec, timend.tv_nsec - timst.tv_nsec);

		m.lcd_puts(buf, 3, 0);
	}
}


void clear_display_nice(lcdpcf8574 m){
	char msg[] = "clear display";
	m.lcd_puts(msg, 0, 0);
	char msg2[] = "then show time again";
	m.lcd_puts(msg2, 1, 0);

	char space[] = " ";
	char dot[] = ".";

//	sleep 1s
	usleep(1000000);
	int i, j;
	for(j=0;j<4;j++){
		for(i=0;i<20;i++){
			m.lcd_puts(space, j, i);
			usleep(10000);
		}
	}
	for(j=3;j>-1;j--){
		for(i=19;i>-1;i--){
			m.lcd_puts(dot, j, i);
			usleep(10000);
		}
	}
	for(j=0;j<4;j++){
		for(i=0;i<20;i++){
			m.lcd_puts(space, j, i);
			usleep(10000);
		}
	}
}


int main(int argc, char *argv[]) {
	signal(SIGINT, intHandler);
	lcdpcf8574 m(0x38, 0, 0, 0);
	unsigned int customfonts[8][8] = {
			 {0b00001110, 0b00011011, 0b00010001, 0b00010001, 0b00010001, 0b00010001, 0b00010001, 0b00011111}
			,{0b00001110, 0b00011011, 0b00010001, 0b00010001, 0b00010001, 0b00010001, 0b00011111, 0b00011111}
			,{0b00001110, 0b00011011, 0b00010001, 0b00010001, 0b00010001, 0b00011111, 0b00011111, 0b00011111}
			,{0b00001110, 0b00011011, 0b00010001, 0b00010001, 0b00011111, 0b00011111, 0b00011111, 0b00011111}
			,{0b00001110, 0b00011011, 0b00010001, 0b00011111, 0b00011111, 0b00011111, 0b00011111, 0b00011111}
			,{0b00001110, 0b00011011, 0b00011111, 0b00011111, 0b00011111, 0b00011111, 0b00011111, 0b00011111}
			,{0b00001110, 0b00011111, 0b00011111, 0b00011111, 0b00011111, 0b00011111, 0b00011111, 0b00011111}
			,{0b00001110, 0b00011111, 0b00011111, 0b00011111, 0b00011111, 0b00011111, 0b00011111, 0b00011111}
	};

	CustomFontsStruct *fs = (CustomFontsStruct *) malloc(sizeof(CustomFontsStruct));

	for(int x=0;x<8;x++){
		for(int y=0;y<8;y++){
			fs->array[x][y] = customfonts[x][y];
		}
	}
	m.loadcustomfonts(fs);
	char hello[] = "Hello";
	m.lcd_puts(hello, 0, 0);
	m.lcd_put_custom(0x04, 0, 19);
	for(;keepRunning == 1;){
		show_time(m);
//		clear_display_nice(m);
	}
	m.lcd_clear();
	free(fs);

}
