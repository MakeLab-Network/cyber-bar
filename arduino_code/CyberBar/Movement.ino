#define NOTHING 0
#define MOVING_TO_DISPENSER 1
#define DISPENSER_POURING 2
#define MOVING_TO_CUSTOMER 3
int movement = NOTHING;
unsigned long stopPouringTime = 0;

void handleMovement() {
  switch (movement) {
    case NOTHING: {
        stopMotors();
        break;
      }
    case MOVING_TO_DISPENSER: {
        calculateCurrentLocation();
        moveMotorsToTargetDispenser();
        if (current_location == target_dispenser) {
          // done!!
          Serial.print("Reached Dispenser ");
          Serial.println(target_dispenser);
          stopMotors();
          movement = DISPENSER_POURING;
          openDispenser(target_dispenser);
          stopPouringTime = millis() + next_pouring_interval;
        }
        break;
      }
    case DISPENSER_POURING: {
        if (millis() >= stopPouringTime) {
          closeDispenser(target_dispenser);
          movement = NOTHING;
        }
        break;
      }
    case MOVING_TO_CUSTOMER: {
        break;
      }
  }
}
