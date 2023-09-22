int rail_power = 2000;
unsigned long railCalibrationTimeoutBetweenMagnetsTime = 0;
int railCalibrationTimeoutBetweenMagnetsInterval = 3500;

void calibrateRail() { // move to limit switch
  Serial.println("going to limit switch for calibration");
  ledRingOn(PURPLE);
  railCalibrationTimeoutBetweenMagnetsTime = millis() + railCalibrationTimeoutBetweenMagnetsInterval;
  bool old_sense_magnet = senseMagnet();
  while (millis() < railCalibrationTimeoutBetweenMagnetsTime && !limitSwitchReached()) {
    leftMotor(-1000);
    bool sense_magnet = senseMagnet();

    if (sense_magnet != old_sense_magnet) {
      railCalibrationTimeoutBetweenMagnetsTime = millis() + railCalibrationTimeoutBetweenMagnetsInterval;
      old_sense_magnet = sense_magnet;
      ledRingOn(PURPLE);
    }
  }

  leftMotor(0);
  if (millis() >= railCalibrationTimeoutBetweenMagnetsTime) {
    Serial.println("Calibration Timeout reached!!!");
    ledRingOn(RED);
    while (true);
  }
  ledRingOff();
  current_location = -1;
  Serial.println("finished rail calibration");
}
void moveMotorsToTargetDispenser() {
  if (current_location == target_dispenser) {
    // done!! reachedDispenser();
    //    Serial.println("go up");
  }
  else if (current_location < target_dispenser) {
    //    rightMotor(4095);
    leftMotor(rail_power);
    //    Serial.println("go up");
    cart_direction = 1;
  }
  else {
    //    rightMotor(-4095);
    leftMotor(-rail_power);
    //    Serial.println("go down");
    cart_direction = -1;
  }
}

void calculateCurrentLocation() {
  // from hall sens
  bool nearMagnet = senseMagnet();
  if (waiting_for_no_magnet) {
    if (!nearMagnet) {
      waiting_for_no_magnet = false;
    }
  }
  else if (nearMagnet) {
    // found station!

    current_location = current_location + cart_direction;
    Serial.print("reached station ");
    Serial.println(current_location);
    waiting_for_no_magnet = true;
  }
}
