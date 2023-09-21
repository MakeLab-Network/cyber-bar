int debugLevel = 3;

#include <Adafruit_PWMServoDriver.h>
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
// ------------------ Motors stuff ---------------------------------
// -- not actual pins, connections of the servo server.
int leftMotorClockwisePwmPin = 7, leftMotorCounterClockwisePwmPin = 6,
    rightMotorClockwisePwmPin = 11, rightMotorCounterClockwisePwmPin = 10,
    powerRight = 0, powerLeft = 0;
bool showMotorValues = false;
/// ########## 120919 Avi - Acceleration stuff
int maxAllowedPowerChangePerSecond[] = {10000, 10000, 30000}; // max Accelerate and deaccelerate per sec
int maxMotorChangeAllowedWithBigStep[] = {500, 500, 2000}; // should never reach that, this is only in case of delay or code blocking

#define CW 0
#define CCW 1
#define CONVEYOR_RIGHT_MOTOR 0
#define CONVEYOR_LEFT_MOTOR 1
#define NUM_OF_MOTORS 2

int maxMotorPwm[] = {4095, 4095, 4095};
unsigned long lastMotorUpdateTime[] = {0, 0, 0};
int oldPower[] = {0, 0, 0};


// ------------ Dispensers
#define NUM_OF_DISPENSERS 7
#define DISPENSER_NONE 0
#define DISPENSER_CLOSE 1
#define DISPENSER_OPEN 2
int dispenserPin[NUM_OF_DISPENSERS] = {30, 31, 32, 33, 34, 35, 36};
int next_pouring_interval = 200, target_dispenser = 0;

// --------------- Rail
int current_location = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("\nbegin setup CyberBar Ver 1 (Geekcon)");
  setupMotors();
  SetupDispensers();
  //  testOneDispenserEndlessly(0);


  Serial.println("End of Setup");
}

void loop() {
//  testAllDispensers();
    handleSerialCommands();
    handleMovement();
}
