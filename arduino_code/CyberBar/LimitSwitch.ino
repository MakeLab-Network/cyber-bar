#define RAIL_LIMIT_SWITCH_PIN 6
#define RIGHT_RAIL_LIMIT_SWITCH_PIN 7
void setupLimitSwitch() {
  pinMode(RAIL_LIMIT_SWITCH_PIN, INPUT_PULLUP);
//  pinMode(RIGHT_RAIL_LIMIT_SWITCH_PIN, INPUT_PULLUP);
}

bool limitSwitchReached() {
  return !digitalRead(RAIL_LIMIT_SWITCH_PIN);
}

bool rightLimitSwitchReached() {
  return !digitalRead(RIGHT_RAIL_LIMIT_SWITCH_PIN);
}
