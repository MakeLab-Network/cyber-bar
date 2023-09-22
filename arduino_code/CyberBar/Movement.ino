#define NOTHING 0
#define MOVING_TO_DISPENSER 1
#define DISPENSER_POURING 2
#define MOVING_TO_CUSTOMER 3
int movement = NOTHING;
unsigned long stopPouringTime = 0;

void handleMovement() {
//  Serial.print("movement");
//  Serial.println(movement);
  switch (movement) {
    case NOTHING: {
        if (debugLevel >= 5)
        {
          Serial.println("moving nothing 1");
        }
//        stopMotors();
        if (debugLevel >= 5)
        {
          Serial.println("moving nothing 2");
        }
        break;
      }
    case MOVING_TO_DISPENSER: {
        if (debugLevel >= 5)
        {
          Serial.println("moving to dispenser 1");
        }
        //      Serial.println("moving...");
        if (millis() > mercyTime) { // don't search for magnets on the first moments, so you won't see the magnet you are on
          calculateCurrentLocation();
        }
        moveMotorsToTargetDispenser();
        if (current_location != last_location) {
          railTimeoutBetweenMagnetsTime = millis() + railTimeoutBetweenMagnetsInterval;
        }
        last_location = current_location;
        if (debugLevel >= 5)
        {
          Serial.println("moving to dispenser 2");
        }
        if (current_location == target_dispenser) {
          // done!!
          Serial.print("Reached Dispenser ");
          Serial.println(target_dispenser);
          stopMotors();
          movement = DISPENSER_POURING;
          openDispenser(target_dispenser);
          stopPouringTime = millis() + next_pouring_interval;
        }
        else if (millis() > railTimeoutBetweenMagnetsTime) {
          Serial.println("timeout between magnets!!");
          //          stopMotors();
          leftMotor(0); // stop immediatly
          ledRingOn(RED);
          delay(1000);
          movement = NOTHING;
          calibrateRail();
        }
        if (debugLevel >= 5)
        {
          Serial.println("moving to dispenser 3");
        }
        break;
      }
    case DISPENSER_POURING: {
        if (debugLevel >= 5)
        {
          Serial.println("moving pouring 1");
        }
        if (millis() >= stopPouringTime) {
          closeDispenser(target_dispenser);
          movement = NOTHING;
          ledRingOff();
          delay(1);
          Serial.println("end pour");
          Serial.println("$reached");
          delay(1);
        }
        if (debugLevel >= 3)
        {
          Serial.println("pouring");
          delay(1);
        }
        break;
      }
    case MOVING_TO_CUSTOMER: {
        break;
      }
  }
}
