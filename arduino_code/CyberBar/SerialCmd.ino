void handleSerialCommands() {
  bool got_command = false;
//  if(got_command) {
//    int command_type =0; // parse
//    switch(command) {
//      case 
//    }
//  }
}

void commandGoAndPourDrink(int dispenser_index, int pouring_interval) {
  stopMotors(); // make sure to stop any prev engagement
  closeDispenser(target_dispenser); // make sure to stop any prev engagement
  
  movement = MOVING_TO_DISPENSER;
  target_dispenser = dispenser_index;
  next_pouring_interval = pouring_interval;
}
