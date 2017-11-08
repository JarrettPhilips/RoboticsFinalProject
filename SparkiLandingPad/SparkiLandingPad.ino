#include <Sparki.h>

//Motor Variables
int speed = 0;
int percentageOfSpeed = 100;
int rightMotorSpeed = 0;
int leftMotorSpeed = 0;

//Timing Variables
int loopCycles = 0;
int totalElapsedTime = 0;
int delayTime = 0;
float intervalMultiplier = 3.0;
int adjustedLoopTime = round(100 * intervalMultiplier); //100ms * intervalMultiplier

//State Variables
int state = 1;
int randomlyChooseState = 0; //1 true, 0 false
int randomlyChooseStateVariables = 0;

void setup(){
  if(randomlyChooseState){
    state = random(1, 4); //Randomly selects a state, unless overwritten
  }
  
  if(randomlyChooseStateVariables){
    speed = random(1, 101);
    rightMotorSpeed = speed;
    leftMotorSpeed = speed;
  
    if(state == 2){
      percentageOfSpeed = random(25, 76);
      leftMotorSpeed = percentageOfSpeed * speed;
    }
  }
}

void loop(){
  //State Machine (Depending on how we implement the sin path, we may not even need this)
  switch(state){
    case 1 : //Linear Path of Variable Speed
      sparki.motorRotate(MOTOR_RIGHT, DIR_CW,  rightMotorSpeed);
      sparki.motorRotate(MOTOR_LEFT, DIR_CCW,  leftMotorSpeed);
      break;
    case 2 : //Circular Path of Variable Speed and Radius (will always go CCW)
      sparki.motorRotate(MOTOR_RIGHT, DIR_CW,  rightMotorSpeed);
      sparki.motorRotate(MOTOR_LEFT, DIR_CCW,  leftMotorSpeed);
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
