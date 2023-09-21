
void moveMotorsToTargetDispenser() {
  if(current_location == target_dispenser) {
    // done!! reachedDispenser();
  }
  else if(current_location < target_dispenser) {
    rightMotor(4095);
    leftMotor(-4095);
  }
  else {
    rightMotor(-4095);
    leftMotor(4095);
  }
}

void calculateCurrentLocation() {
  // from hall sens
}
