void setPWM(int pin, int power)
{
  power = constrain(power, 0, 4095);

    pwm.setPWM(pin, 0, power); // Go !  (note: 0,4095 is fully on while 0,4096 is fully off... )
  // Read here: https://learn.adafruit.com/16-channel-pwm-servo-driver/library-reference

}

void rightMotor(int power)
{
  setPWM(rightMotorClockwisePwmPin, power > 0 ? abs(power) : 0);
  setPWM(rightMotorCounterClockwisePwmPin, power > 0 ? 0 : abs(power));

  if (debugLevel >= 5)
  {
    Serial.print("Right motor PWM: ");
    Serial.print(abs(power));
    Serial.print(", CC pin: ");
    Serial.print((power > 0));
    Serial.print(", CW pin: ");
    Serial.println((power <= 0));
  }
}

void leftMotor(int power)
{
  setPWM(leftMotorClockwisePwmPin, power > 0 ? 0 : abs(power));
  setPWM(leftMotorCounterClockwisePwmPin, power > 0 ? abs(power) : 0);
  if (debugLevel >= 5)
  {
    Serial.print("Left motor PWM: ");
    Serial.print(abs(power));
    Serial.print(", CC pin: ");
    Serial.print((power > 0));
    Serial.print(", CW pin: ");
    Serial.println((power <= 0));
  }
}

void drive(int powerRightInput, int powerLeftInput)
{

  /*if (!robotGo) {
    powerRightInput = 0;
    powerLeftInput = 0;
    }*/
  if (showMotorValues) {
    Serial.print("powerRight: ");
    Serial.print(powerRightInput);
    Serial.print(", powerLeft: ");
    Serial.println(powerLeftInput);
  }
  motorGo(CONVEYOR_RIGHT_MOTOR, powerRightInput);
  motorGo(CONVEYOR_LEFT_MOTOR, powerLeftInput);

}

void setupMotors()
{
  pwm.begin();
  pwm.setPWMFreq(1600);  // This is the maximum PWM frequency
  Wire.setClock(400000);
  stopMotors();
}

void stopMotors()
{
  leftMotor(0);
//  drive(0, 0);
}
