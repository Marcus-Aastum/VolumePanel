// include the library code:
#include <LiquidCrystal.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
const int playpause = 7;
const int skip = 9;
const int volume = A0;
void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  lcd.begin(16, 2);
  lcd.print("start");
  pinMode(playpause, INPUT);
  pinMode(skip, INPUT);
}

void loop() {

  //Reads sensor info
  int playpauseread = digitalRead(playpause);
  int skipread = digitalRead(skip);
  int volumeread = analogRead(volume);

  int linenr;
  char serial_byte;

  //Transmits sensor info
  Serial.print(playpauseread);
  Serial.print(skipread);
  Serial.println(volumeread);
  delay(400);

  if (Serial.available()) {
    delay(100);  //wait some time for the data to fully be read
    lcd.clear();
    
    //Writes on the lcd
    while (Serial.available() > 0)
  {
    serial_byte = Serial.read();
    switch (serial_byte) {
        case '\1':
        lcd.setCursor(0,1);
        break;
        case '\0':
        lcd.setCursor(0,0);
        break;
        default:
        lcd.print(char(serial_byte));
  }
}
}
}
