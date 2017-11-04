#include <Sparki.h>

//Motor Variables
int rightMotorSpeed = 0;
int leftMotorSpeed = 0;

//Timing Variables
int loopCycles = 0;
int totalElapsedTime = 0;
int delayTime = 0;

//State Variables
int state = 1;
int randomlyChooseState = 0; //1 true, 0 false

void setup(){
  if(randomlyChooseState){
    state = random(1, 4); //Randomly selects a state, unless overwritten
  }
  
  if(state == 1){
    int speed = random(1, 101);
    rightMotorSpeed = speed;
    leftMotorSpeed = speed;
  }
}

void loop(){
  //State Machine
  switch(state){
    case 1 : //Linear Path of Variable Speed
      sparki.motorRotate(MOTOR_RIGHT, DIR_CW,  rightMotorSpeed);
      sparki.motorRotate(MOTOR_LEFT, DIR_CCW,  leftMotorSpeed);
      break;
    case 2 : //Circular Path of Variable Speed
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
