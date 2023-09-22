#define RAIL_LIMIT_SWITCH_PIN 6
void setupLimitSwitch() {
  pinMode(RAIL_LIMIT_SWITCH_PIN, INPUT_PULLUP);
}

bool limitSwitchReached() {
  return !digitalRead(RAIL_LIMIT_SWITCH_PIN);
}
