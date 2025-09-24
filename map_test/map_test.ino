/**
 * @file map_test.ino
 * @author Gaspar Fabrega Ragni
 * @brief M5Cardputer GPS map test
 * @version 0.1
 * @date 2024-08-23
 *
 *
 * @Hardware: M5Cardputer
 * @Platform Version: Arduino v2.3.2
 * @Dependent Library:
 * M5GFX: https://github.com/m5stack/M5GFX
 * M5Cardputer: https://github.com/m5stack/M5Cardputer
 *
 * variable length array struct:
 * https://forum.arduino.cc/t/multi-dimensional-arrays-with-different-number-of-elements/557252/2
 *
 */

#define len(x) (sizeof(x) / sizeof(x[0]))

#include "M5Cardputer.h"
#include <TinyGPSPlus.h>
#include "structs.h"
#include "maps.h"
#include "chunks.h"

const uint32_t GPSBaud = 9600;
TinyGPSPlus gps;
HardwareSerial GPS_Serial(2);

bool first_time = true;

int ii = 0;
int jj = 0;
int kk = 39;

int kk_o = kk;

void setup() {
  auto cfg = M5.config();
  // Serial.begin(9600);
  M5Cardputer.begin(cfg);
  int textsize = M5Cardputer.Display.height() / 70;
  if (textsize == 0) {
    textsize = 1;
  }
  M5Cardputer.Display.setTextSize(textsize);
  // Comenzar comunicacion serial con el gps
  GPS_Serial.begin(9600, SERIAL_8N1, 1, -1);
}

void loop() {

  for (uint16_t rowCnt = 0; rowCnt < maps[kk].length; rowCnt++) {
    for (uint16_t colCnt = 0; colCnt < maps[kk].lon[rowCnt].length - 1; colCnt++) {
      int x0 = int(map(maps[kk].lon[rowCnt].street[colCnt], maps[kk].lon_min, maps[kk].lon_max, M5Cardputer.Display.width(), 0));
      int x1 = int(map(maps[kk].lon[rowCnt].street[colCnt + 1], maps[kk].lon_min, maps[kk].lon_max, M5Cardputer.Display.width(), 0));
      int y0 = int(map(maps[kk].lat[rowCnt].street[colCnt], maps[kk].lat_min, maps[kk].lat_max, 0, M5Cardputer.Display.height()));
      int y1 = int(map(maps[kk].lat[rowCnt].street[colCnt + 1], maps[kk].lat_min, maps[kk].lat_max, 0, M5Cardputer.Display.height()));
      M5Cardputer.Display.drawLine(x0, y0, x1, y1, 0x8c00ffU);
    }
  }
  M5Cardputer.Display.drawString("INICIALIZANDO GPS ...", 100, 60);

  while (true) {
    delay_gps(3000);
    if (gps.location.lng() != 0) {
    // if (true) {

      ii = map_double(gps.location.lng(), box_lon_min, box_lon_max, 0.0, n_lon);
      jj = map_double(gps.location.lat(), box_lat_min, box_lat_max, 0.0, n_lat);
      // ii = map_double(-70.5790919, box_lon_min, box_lon_max, 0, 4);
      // jj = map_double(-33.4118781, box_lat_min, box_lat_max, 0, 6);
      // ii = map_double(-70.6113078, box_lon_min, box_lon_max, 0, 3);
      // jj = map_double(-33.4317265, box_lat_min, box_lat_max, 0, 5);
      kk_o = kk;
      kk = ii*(n_lat) + jj;
      // M5Cardputer.Display.drawNumber(ii, 60, 10);M5Cardputer.Display.drawFloat(map_double_test(gps.location.lng(), box_lon_min, box_lon_max, 0.0, n_lon), 6, 80, 10);
      // M5Cardputer.Display.drawNumber(jj, 60, 20);M5Cardputer.Display.drawFloat(map_double_test(gps.location.lat(), box_lat_min, box_lat_max, 0.0, n_lat), 6, 80, 20);
      // M5Cardputer.Display.drawNumber(kk, 60, 30);

      if ((kk_o != kk) || (first_time)) {
        first_time = false;
        M5Cardputer.Display.clear();
        for (uint16_t rowCnt = 0; rowCnt < maps[kk].length; rowCnt++) {
          for (uint16_t colCnt = 0; colCnt < maps[kk].lon[rowCnt].length - 1; colCnt++) {
            int x0 = int(map(maps[kk].lon[rowCnt].street[colCnt], maps[kk].lon_min, maps[kk].lon_max, M5Cardputer.Display.width(), 0));
            int x1 = int(map(maps[kk].lon[rowCnt].street[colCnt + 1], maps[kk].lon_min, maps[kk].lon_max, M5Cardputer.Display.width(), 0));
            int y0 = int(map(maps[kk].lat[rowCnt].street[colCnt], maps[kk].lat_min, maps[kk].lat_max, 0, M5Cardputer.Display.height()));
            int y1 = int(map(maps[kk].lat[rowCnt].street[colCnt + 1], maps[kk].lat_min, maps[kk].lat_max, 0, M5Cardputer.Display.height()));
            M5Cardputer.Display.drawLine(x0, y0, x1, y1, 0x8c00ffU);
            // M5Cardputer.Display.drawNumber(ii, 150, 50);
            // M5Cardputer.Display.drawNumber(jj, 150, 60);
            // M5Cardputer.Display.drawNumber(kk, 150, 70);
          }
        }
      }

      double lat_min = box_lat_min + jj * d_lat;
      double lat_max = box_lat_min + (jj + 1) * d_lat;
      double lon_min = box_lon_min + ii * d_lon;
      double lon_max = box_lon_min + (ii + 1) * d_lon;

      int x0 = map_double(gps.location.lng(), lon_min, lon_max, 0, M5Cardputer.Display.width());
      int y0 = map_double(gps.location.lat(), lat_min, lat_max, M5Cardputer.Display.height(), 0);
      // x0 = map_double(-70.5790919, lon_min, lon_max, 0, M5Cardputer.Display.width());
      // y0 = map_double(-33.4118781, lat_min, lat_max, M5Cardputer.Display.height(), 0);

      // escribir valores de gps y punto
      M5Cardputer.Display.drawCircle(x0, y0, 2, 0xff0000U);
      M5Cardputer.Display.drawNumber(gps.satellites.value(), 10, 10);
      M5Cardputer.Display.drawNumber(gps.satellites.isValid(), 40, 10);
      M5Cardputer.Display.drawFloat(float(gps.location.lat()), 6, 5, 90);
      M5Cardputer.Display.drawFloat(float(gps.location.lng()), 6, 5, 100);
      // M5Cardputer.Display.drawNumber(y0, 100, 70);
      // M5Cardputer.Display.drawNumber(x0, 100, 90);
    }
  }
}

// map for double precision floats
int map_double(double x, double in_min, double in_max, double out_min, double out_max) {
  return int(floor((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min));
}

double map_double_test(double x, double in_min, double in_max, double out_min, double out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

int map_float(float x, float in_min, float in_max, float out_min, float out_max) {
  return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min);
}

// This custom version of delay() ensures that GPS objects work properly.
static void delay_gps(unsigned long ms) {
  unsigned long start = millis();
  do {
    while (GPS_Serial.available()) gps.encode(GPS_Serial.read());
  } while (millis() - start < ms);
}