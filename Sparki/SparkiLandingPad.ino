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
int randomlyChooseState = 1; //1 true, 0 false
int randomlyChooseStateVariables = 1;

void playFanfare(){
  int melody[] = {NOTE_A5 , NOTE_A5, NOTE_A5, NOTE_A5, NOTE_F5, NOTE_G, NOTE_A, NOTE_G, NOTE_A}
  int noteDurations[] = {8, 8, 8, 4, 3, 8, 8, 4, 8, 2}
  
  for (int thisNote = 0; thisNote < melody.size(); thisNote++) {
 
    // calculate the note duration as 1 second divided by note type.
    //e.g. quarter note = 1000 / 4, eighth note = 1000/8, etc.
    int noteDuration = 1000/noteDurations[thisNote];
    sparki.beep(melody[thisNote],noteDuration);
    }
 
    // to distinguish the notes, set a minimum time between them.
    // the note's duration + 30% seems to work well:
    int pauseBetweenNotes = noteDuration * 1.20;
    delay(pauseBetweenNotes);
    // stop the tone playing:
    sparki.noBeep();
  }
  
  
}

void setup(){
  randomSeed(analogRead(0)); 
  if(randomlyChooseState){
    state = random(1, 3); //Randomly selects a state, unless overwritten
  }
  
  if(randomlyChooseStateVariables){
    speed = random(50, 101);
    rightMotorSpeed = speed;
    leftMotorSpeed = speed;
  
    if(state == 2){
      percentageOfSpeed = random(25, 76);
      leftMotorSpeed = percentageOfSpeed * speed;
    }
  }
  sparki.clearLCD();
  sparki.println(state);
  sparki.println(leftMotorSpeed, rightMotorSpeed);
  sparki.updateLCD();
}

void loop(){
  sparki.motorRotate(MOTOR_RIGHT, DIR_CW,  rightMotorSpeed);
  sparki.motorRotate(MOTOR_LEFT, DIR_CCW,  leftMotorSpeed);
  
  #testcode for beep when drone is caught
  if(sparki.accelY() < -1){
      sparki.moveStop();  
      playFanfare();
      delay(-1)
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
