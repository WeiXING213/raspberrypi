/*
gcc c_gpio_test.c blink -l wirlingPi
*/
#include <stdio.h>
#include <wiringPi.h>

#define LED 17  /*wiringPi pin number O, position on GPIO header 11*/

int main(void){
  printf ("Raspberry Pi blink\n");
  wiringPiSetupGpio();
  pinMode(LED, OUTPUT);
  
  int i;
  for(i=0; i<5; i++){
    digitalWrite (LED, HIGH);
    delay (500);
    digitalWrite (LED, LOW);
    delay (500);

  }
  return 0;
}


