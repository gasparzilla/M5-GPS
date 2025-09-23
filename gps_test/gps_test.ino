#include <TinyGPSPlus.h>
#include "M5Cardputer.h"

static const uint32_t GPSBaud = 9600;

TinyGPSPlus gps;
HardwareSerial ss(2);

void setup() {
  auto cfg = M5.config();
  M5Cardputer.begin(cfg);
  int textsize = M5Cardputer.Display.height() / 60;
  if (textsize == 0) {
    textsize = 1;
  }
  M5Cardputer.Display.setTextSize(textsize);
  ss.begin(9600, SERIAL_8N1, 1, -1);
}

void loop() {
  M5Cardputer.Display.drawString("GPSTEST", 10, 100);
  static const double LONDON_LAT = 51.508131, LONDON_LON = -0.128002;
  M5Cardputer.Display.drawNumber(gps.satellites.value(), 10, 10);
  M5Cardputer.Display.drawNumber(gps.satellites.isValid(), 40, 10);
  // M5Cardputer.Display.drawString(String(gps.location.lat(),6), 10, 50);
  // M5Cardputer.Display.drawString(String(gps.location.lng(),6), 10, 80);
  M5Cardputer.Display.drawFloat(float(gps.location.lat()), 6, 10, 50);
  M5Cardputer.Display.drawFloat(float(gps.location.lng()), 6, 10, 80);
  // Serial.println(gps.date);

  // unsigned long distanceKmToLondon =
  //     (unsigned long)TinyGPSPlus::distanceBetween(
  //         gps.location.lat(), gps.location.lng(), LONDON_LAT, LONDON_LON) /
  //     1000;
  // printInt(distanceKmToLondon, gps.location.isValid(), 9);

  // double courseToLondon = TinyGPSPlus::courseTo(
  //     gps.location.lat(), gps.location.lng(), LONDON_LAT, LONDON_LON);

  // printFloat(courseToLondon, gps.location.isValid(), 7, 2);

  // const char *cardinalToLondon = TinyGPSPlus::cardinal(courseToLondon);

  // printStr(gps.location.isValid() ? cardinalToLondon : "*** ", 6);

  // printInt(gps.charsProcessed(), true, 6);
  // printInt(gps.sentencesWithFix(), true, 10);
  // printInt(gps.failedChecksum(), true, 9);
  // M5.Lcd.println();

  delay_gps(1000);
}

// This custom version of delay() ensures that GPS objects work properly.
static void delay_gps(unsigned long ms) {
  unsigned long start = millis();
  do {
    while (ss.available()) gps.encode(ss.read());
  } while (millis() - start < ms);
}