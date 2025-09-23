struct COORDS {
  long *street;
  uint16_t length;
};

struct CHUNK {
  COORDS *lon;
  COORDS *lat;
  uint16_t length;
  double lon_max;
  double lon_min;
  double lat_max;
  double lat_min;
};
