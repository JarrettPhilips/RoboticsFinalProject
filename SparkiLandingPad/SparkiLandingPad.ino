#include <Sparki.h>

//Timing Variables
int loopCycles = 0;
int totalElapsedTime = 0;
int delayTime = 0;

//State Variables
int state = 0;
int randomlyChooseState = 1; //1 true, 0 false

void setup(){
  //Randomly selects a state, unless overwritten
  
}

void loop() {
  //State Machine
  switch(state){
    case 1 : //Linear Path of Variable Speed
      break;
    case 2 : //Cicular Path of Variable Speed
      break;
    case 3 : //Sin Path of Variable Speed
      break;
  }
  
  //Timing Code
  int loopTime = millis() - totalElapsedTime;
  if((adjustedLoopTime + delayTime) - loopTime < 0){
      sparki.clearLCD();
      sparki.print("Error: Loop exceeded alloted time");
      sparki.updateLCD();
      sparki.moveStop();
  }
  delay((adjustedLoopTime + delayTime) - loopTime);
  totalElapsedTime += (adjustedLoopTime + delayTime);
  loopCycles ++;
  delayTime = 0;
}
