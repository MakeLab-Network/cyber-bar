void SetupDispensers() {
  for (int i = 0; i < NUM_OF_DISPENSERS; i++) {
    pinMode(dispenserPin[i], OUTPUT);
  }
}

void openDispenser(int index) {
  digitalWrite(dispenserPin[index], HIGH);
}
void closeDispenser(int index) {
  digitalWrite(dispenserPin[index], LOW);
}


void testOneDispenserEndlessly (int index) {
  Serial.println("Start single dispenser loop test");
  while (true) {
        openDispenser(index);
        delay(1000);
        closeDispenser(index);
        delay(1000);
  }
}

void testAllDispensers() {
  Serial.println("Start all dispensers test - once");
  for (int i = 0; i < NUM_OF_DISPENSERS; i++) {
    openDispenser(i);
    delay(1000);
    closeDispenser(i);
    delay(500);
  }
}

//void openDispenser(int index, int interval) {
//  Serial.print("Open dispenser ");
//  Serial.print(index);
//  Serial.print("for ");
//  Serial.print(interval);
//  Serial.println(" millis");
//  if (index > NUM_OF_DISPENSERS) {
//    Serial.println("error too big dispenser index, exiting func");
//    return;
//  }
//  //  setPWM(index, 4095);
//  digitalWrite(dispenser[index][2], HIGH);
//  dispenser[index][0] = millis() + interval;
//  dispenser[index][1] = DISPENSER_CLOSE;
//}

//void handleDispensers() {
//  for (int i = 0; i < NUM_OF_DISPENSERS; i++) {
//    if (millis() >= dispenser[i][0] && dispenser[i][0] != 0) {
//
//      Serial.print("Dispenser timer reached for dispenser ");
//      Serial.print(i);
//      Serial.print(" doing action: ");
//      Serial.println(dispenser[i][1]);
//      if (dispenser[i][1] == DISPENSER_CLOSE) {
//        //        setPWM(i, 4095);
//        digitalWrite(dispenser[i][2], LOW);
//      }
//      else if (dispenser[i][1] == DISPENSER_OPEN) { // action: open
//        //        setPWM(i, 0);
//        digitalWrite(dispenser[i][2], HIGH);
//      }
//      dispenser[i][0] = 0; // set timer to "None"
//      dispenser[i][1] = DISPENSER_NONE; // set action to "None"
//    }
//  }
//}
