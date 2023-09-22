int hallEffectTreshold = 500; // with magnet 200-400 without magnet 515
int hallEffectSensorPin = A0;

void setupHallSensor() {
  pinMode(hallEffectSensorPin, INPUT);
}
bool senseMagnet() {
  int hallEffectReading = analogRead(hallEffectSensorPin);
//  Serial.print("Hall sensor: ");
//  Serial.println(hallEffectReading);
  bool magnet = hallEffectReading < hallEffectTreshold;
  if(magnet) {
    ledRingOn(GREEN);
  }
  else {
    ledRingOff();
  }
  return magnet;
}
//
//void hallEffectHandler() // Handles the hall effect sensor reading and debouncing
//{
//  hallEffectReading = analogRead(hallEffect);
//
//  if (hallEffectReading > hallEffectTreshold)
//  {
//    hallEffectLastDebounceTime = millis();
//  }
//
//  if ((millis() - hallEffectLastDebounceTime) > hallEffectDebounceDelay)
//  {
//    if (hallEffectReading > hallEffectTreshold)
//    {
//      stationDetected = true;
//    }
//  }
//
//}


//void updateCartPosition() // Updates the cart position based on the hall effect sensor reading (after debouncing)
//{
//  hallEffectHandler();
//
//  if (stationDetected)
//  {
//    stationDetected = false;
//    if (currentCartDirection == 1)
//    {
//      cartPosition++;
//    }
//    else if (currentCartDirection == 2)
//    {
//      cartPosition--;
//    }
//    else
//    {
//      //Do nothing
//    }
//  }
//
//}
