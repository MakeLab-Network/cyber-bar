
void setupLeds() {
  pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
  ledRingOff();
}

void ledRingOn(int color) {
  for (int i = 0; i < NUMPIXELS; i++) { // For each pixel...

    // pixels.Color() takes RGB values, from 0,0,0 up to 255,255,255
    // Here we're using a moderately bright green color:
    if (color == GREEN) {
      pixels.setPixelColor(i, pixels.Color(0, 150, 0));
    }
    else if (color == PURPLE) {
      pixels.setPixelColor(i, pixels.Color(120, 0, 150));
    }
    else if (color == RED) {
      pixels.setPixelColor(i, pixels.Color(150, 0, 0));
    }
    pixels.show();   // Send the updated pixel colors to the hardware.
  }
}

void ledRingOff() {
  pixels.clear(); // Set all pixel colors to 'off'
  pixels.show();
}
