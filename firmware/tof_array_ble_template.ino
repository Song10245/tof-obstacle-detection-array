/*
  VL53L1X ToF array BLE firmware template
  Public-safe portfolio version.

  Replace TODO sections with your board, BLE library and sensor-address logic.
*/

#include <Wire.h>

const int NUM_SENSORS = 10;
uint16_t distances_mm[NUM_SENSORS];

void setup() {
  Serial.begin(115200);
  Wire.begin();

  // TODO: Initialise BLE service and characteristic.
  // TODO: Initialise each VL53L1X sensor and assign unique I2C addresses.
}

void loop() {
  for (int i = 0; i < NUM_SENSORS; ++i) {
    // TODO: Replace with actual sensor read.
    distances_mm[i] = 0;
  }

  // TODO: Pack readings into a BLE packet.
  // Example CSV fallback for debugging:
  for (int i = 0; i < NUM_SENSORS; ++i) {
    Serial.print(distances_mm[i]);
    if (i < NUM_SENSORS - 1) Serial.print(',');
  }
  Serial.println();

  delay(50); // Approx. 20 Hz update rate.
}
