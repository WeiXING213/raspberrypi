/*
gcc c_gpio_test.c -o blink -l wirlingPi
test diff
*/
#include <stdio.h>
#include <wiringPi.h>

#define LED 18  /*LED number actually it is BCM GPIO number*/

int main(void){
  printf ("Raspberry Pi blink\n");
  #ifdef DEBUG 
  int setup = wiringPiSetupGpio();
  printf("Debug 1: setup: %d\n", setup);
  #endif
  pinMode(LED, OUTPUT);
  
  int i;
  int value; 
  unsigned int delay_time = 1000;  

  for(i=0; i<5; i++){
    printf("blink..\n");
    digitalWrite (LED, HIGH); 
    delay (delay_time);
    value = digitalRead(LED);
    printf("digital read after led set to higt:  %d\n", value);
    
    digitalWrite (LED, LOW);  
    delay (delay_time);
    value = digitalRead(LED);  
    printf("digital read after led set to lowt:  %d\n", value);
    
  }
  return 0;
}


