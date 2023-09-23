#define RED_BUTTON_PIN 46
#define BLUE_BUTTON_PIN 47
#define GREEN_BUTTON_PIN 48
#define YELLOW_BUTTON_PIN 49
bool red_button_is_pressed = false, blue_button_is_pressed = false, green_button_is_pressed = false, yellow_button_is_pressed = false;

void setupButtons() {
  pinMode(RED_BUTTON_PIN, INPUT_PULLUP);
  pinMode(BLUE_BUTTON_PIN, INPUT_PULLUP);
  pinMode(GREEN_BUTTON_PIN, INPUT_PULLUP);
  pinMode(YELLOW_BUTTON_PIN, INPUT_PULLUP);
}

void checkButtons() {
//  Serial.println(digitalRead(RED_BUTTON_PIN));
  if (digitalRead(RED_BUTTON_PIN) == HIGH) {
    if (red_button_is_pressed) { // if was pressed but now released, full press
      // press red
      Serial.println("@0");
      delay(20);
      //      Serial.println("Red was pressed");
    }
    red_button_is_pressed = false;
  }
  else {
    red_button_is_pressed = true;
  }

  if (digitalRead(BLUE_BUTTON_PIN) == HIGH) {
    if (blue_button_is_pressed) { // if was pressed but now released, full press
      // press red
      Serial.println("@2");
      delay(20);
      //      Serial.println("Blue was pressed");
    }
    blue_button_is_pressed = false;
  }
  else {
    blue_button_is_pressed = true;
  }

  if (digitalRead(GREEN_BUTTON_PIN) == HIGH) {
    if (green_button_is_pressed) { // if was pressed but now released, full press
      Serial.println("@1");
      delay(20);
    }
    green_button_is_pressed = false;
  }
  else {
    green_button_is_pressed = true;
  }

  if (digitalRead(YELLOW_BUTTON_PIN) == HIGH) {
    if (yellow_button_is_pressed) { // if was pressed but now released, full press
      Serial.println("@3");
      delay(20);
    }
    yellow_button_is_pressed = false;
  }
  else {
    yellow_button_is_pressed = true;
  }
}
