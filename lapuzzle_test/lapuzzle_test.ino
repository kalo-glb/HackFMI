int blue_sensors[] = {A5, A3, A2, A0};
int orange_sensors[] = {2, 4, 7, 8};

void setup()
{
  for(int i = 0; i < 4; i++)
  {
    pinMode(blue_sensors[i], INPUT);
    pinMode(orange_sensors[i], INPUT);
    digitalWrite(blue_sensors[i], HIGH);
    digitalWrite(orange_sensors[i], HIGH);
  }
  
  Serial.begin(9600);
}

void loop()
{
  for(int i = 0; i < 4; i++)
  {
    Serial.print(digitalRead(blue_sensors[i]));
    Serial.print(" ");
    Serial.print(digitalRead(orange_sensors[i]));
    Serial.print(" ");
  }
  Serial.println();
}
