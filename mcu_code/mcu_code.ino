int blue_sensors[] = {A0, A2, A3, A5};
int orange_sensors[] = {2, 4, 7, 8};
#define red_led 5
#define white_led 6

#define start_byte 0x02
#define end_byte   0x03

void setup()
{
  for(int i = 0; i < 4; i++)
  {
    pinMode(blue_sensors[i], INPUT);
    pinMode(orange_sensors[i], INPUT);
  }
  
  pinMode(red_led, OUTPUT);
  pinMode(white_led, OUTPUT);
  
  Serial.begin(9600);
}

void loop()
{
  digitalWrite(red_led, HIGH);
  digitalWrite(white_led, HIGH);
  delay(1000);
  digitalWrite(red_led, LOW);
  digitalWrite(white_led, LOW);
  delay(1000);
}
