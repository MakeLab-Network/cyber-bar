void handleSerialCommands() {
  if (debugLevel >= 5)
  {
    Serial.println("start serialHandler");
  }
  if (Serial.available() > 0) {
    if (debugLevel >= 5)
    {
      Serial.print("got command");
    }
    delay(5);
    byte sByte = Serial.read();
//    Serial.println(sByte);
    if (sByte == '?') {
      Serial.println("available commands:");
      Serial.println("  t5 500 - go to point 5 and pour 500 millis");
      Serial.println("  z - test all dispensers in order");
//      Serial.println("  c2 - new current location 2");
    }
    if (sByte == 't') {
      int dst = Serial.parseInt();
      delay(5);
      Serial.read(); // read 1 whitespace
      int duration = Serial.parseInt();
      if (dst >= NUM_OF_DISPENSERS) {
        Serial.println("Error, target dispenser too big, ignoring");
        Serial.println("$err");
        Serial.println("$ready");
        ledRingOn(RED);
      }
      else {
        commandGoAndPourDrink(dst, duration);
      }
    }
    if (sByte == 'z') {
      testAllDispensers();
    }
    else if (sByte == 'c') {
      current_location = Serial.parseInt();
      Serial.print("new current_location: ");
      Serial.println(current_location);
    }
  }
  while (Serial.available() > 0) {
    Serial.read();
    if (debugLevel >= 5)
    {
      Serial.println("more garbage serial");
    }
  }
  if (debugLevel >= 5)
  {
    Serial.println("end of serial");
  }
}

void commandGoAndPourDrink(int dispenser_index, int pouring_interval) {
  Serial.print("Going to Pour drink from dispenser: ");
  Serial.print(dispenser_index);
  Serial.print(" for ");
  Serial.print(pouring_interval);
  Serial.println(" millis");
  stopMotors(); // make sure to stop any prev engagement
  closeDispenser(target_dispenser); // make sure to stop any prev engagement

  waiting_for_no_magnet = true;
  movement = MOVING_TO_DISPENSER;
  railTimeoutBetweenMagnetsTime = millis() + railTimeoutBetweenMagnetsInterval;
  mercyTime = millis() + mercyInterval;
  target_dispenser = dispenser_index;
  next_pouring_interval = pouring_interval;
}
