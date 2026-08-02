#include <MeMCore.h>

// Initialize the dual motor driver on port M1 and M2
MeDCMotor motor_9(M1);
MeDCMotor motor_10(M2);

// Set default movement speed (0 to 255)
uint8_t motorSpeed = 150;

// Forward declare functions so PlatformIO sees them
void moveForward();
void moveBackward();
void turnLeft();
void turnRight();
void stopMotors();

void setup() {
  // Start serial communication at the standard baud rate
  Serial.begin(9600);
}

void loop() {
  // Check if data is coming from the computer/remote via serial
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    // Process single-character movement commands
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