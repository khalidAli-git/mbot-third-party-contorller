#include <MeMCore.h>


MeDCMotor motor_9(M1);
MeDCMotor motor_10(M2);

uint8_t motorSpeed = 150;

void moveForward();
void moveBackward();
void turnLeft();
void turnRight();
void stopMotors();

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    if (command == 'F') {
      moveForward();
    } else if (command == 'B') {
      moveBackward();
    } else if (command == 'L') {
      turnLeft();
    } else if (command == 'R') {
      turnRight();
    } else if (command == 'S') {
      stopMotors();
    }
  }
}

void moveForward() {
  motor_9.run(motorSpeed);     
  motor_10.run(-motorSpeed);
}

void moveBackward() {
  motor_9.run(-motorSpeed);
  motor_10.run(motorSpeed);
}

void turnLeft() {
  motor_9.run(-motorSpeed);
  motor_10.run(-motorSpeed);
}

void turnRight() {
  motor_9.run(motorSpeed);
  motor_10.run(motorSpeed);
}

void stopMotors() {
  motor_9.run(0);
  motor_10.run(0);
}
