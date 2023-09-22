int debugLevel = 3;
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
// ------------------ Motors stuff ---------------------------------
// -- not actual pins, connections of the servo server.
int leftMotorClockwisePwmPin = 0, leftMotorCounterClockwisePwmPin = 1,
    rightMotorClockwisePwmPin = 2, rightMotorCounterClockwisePwmPin = 3,
    powerRight = 0, powerLeft = 0;
bool showMotorValues = true;
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
#define NUM_OF_DISPENSERS 14
#define DISPENSER_NONE 0
#define DISPENSER_CLOSE 1
#define DISPENSER_OPEN 2
int dispenserPin[NUM_OF_DISPENSERS] = {33, 34, 35, 36, 37, 32, 38, 39, 40, 41, 42, 43, 44, 45};
int next_pouring_interval = 200, target_dispenser = 0;

// --------------- Rail
int current_location = 3, last_location = -2;
int cart_direction = 1;
bool waiting_for_no_magnet = true;
unsigned long mercyTime = 0, railTimeoutBetweenMagnetsTime = 0;
int mercyInterval = 50, railTimeoutBetweenMagnetsInterval = 1800;

// ------------------ LEDS
#include <Adafruit_NeoPixel.h>
#define NUMPIXELS 24 // Popular NeoPixel ring size
#define CUP_LED_RING_PIN 5
Adafruit_NeoPixel pixels(NUMPIXELS, CUP_LED_RING_PIN, NEO_GRB + NEO_KHZ800);
#define GREEN 0
#define PURPLE 1
#define RED 2

unsigned long send_pc_ka_time = 0; // dont ask
int send_pc_ka_interval = 20;

void setup() {
  Serial.begin(9600);
  Serial.println("\nbegin setup CyberBar Ver 1 (Geekcon 2023)");
  setupMotors();
  Serial.setTimeout(1000);
  setupLeds();
  setupHallSensor();
  setupLimitSwitch();
  // hard code stop // remove later
  //  pwm.setPWM(leftMotorClockwisePwmPin, 0, 0);
  //  pwm.setPWM(leftMotorCounterClockwisePwmPin, 0, 0);
  //  pwm.setPWM(rightMotorClockwisePwmPin, 0, 0);
  //  pwm.setPWM(rightMotorCounterClockwisePwmPin, 0, 0);

  SetupDispensers();
  //  testOneDispenserEndlessly(0);

  //  while (true) {
  //    //    if(senseMagnet()) {
  //    //      ledRingOn(GREEN);
  //    //    }
  //    //    else {
  //    //      ledRingOff();
  //    //    }
  //        leftMotor(2000);
  //        delay(1000);
  //        leftMotor(0);
  //        delay(1000);
  //        leftMotor(-2000);
  //        delay(1000);
  //        leftMotor(0);
  //        delay(1000);
  //
  //  }


  //  commandGoAndPourDrink(1, 1000);

  calibrateRail();
  Serial.println("End of Setup");
}


void loop() {
  delay(2);
  if(millies() > send_pc_ka_time) {
     send_pc_ka_time = millis() + send_pc_ka_interval;
     Serial.println("ka!");
  }
  // for debug
  //  senseMagnet();
  //  if (millis() % 1000 > 500) {
  //    ledRingOn(GREEN);
  //    //    pwm.setPWM(8, 0, 150);
  //  }
  //  else {
  //    ledRingOn(RED);
  //    //    pwm.setPWM(8, 0, 600);
  //  }
//  pwm.setPWM(8, 0, 150 + ((millis() - 450) % 900));
  //  testAllDispensers();
  if (debugLevel >= 5)
  {
    Serial.println("loop 1");
  }
//  handleSerialCommands();
  if (debugLevel >= 5)
  {
    Serial.println("loop 2");
  }
  handleMovement();
}
