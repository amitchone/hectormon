#include <DHT.h>

#define CDHTPIN 2
#define HDHTPIN 7
#define DHTTYPE DHT22

DHT cdht(CDHTPIN, DHTTYPE);
DHT hdht(HDHTPIN, DHTTYPE);

float ctemp;
float chum;
float htemp;
float hhum;


void setup() {
  Serial.begin(9600);
  cdht.begin();
  hdht.begin();
}

void loop() {
  ctemp = cdht.readTemperature();
  chum = cdht.readHumidity();
  htemp = hdht.readTemperature();
  hhum = hdht.readHumidity();

  Serial.print(ctemp);
  Serial.print(",");
  Serial.print(chum);
  Serial.print(",");
  Serial.print(htemp);
  Serial.print(",");
  Serial.print(hhum);
  Serial.println("");

  delay(2000);
}

