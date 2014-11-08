int blue_sensors[] = {A0, A2, A3, A5};
int orange_sensors[] = {2, 4, 7, 8};
#define red_led 5
#define white_led 6
#define detection_treshold 50

int detection_count[8];
int detection_state[8];

char pattern[4];
int new_pattern_recieved = 0;
int count = 0;

enum color
{
  blue,
  orange
} color;

void setup()
{
  for(int i = 0; i < 4; i++)
  {
    pinMode(blue_sensors[i], INPUT);
    pinMode(orange_sensors[i], INPUT);
    //digitalWrite(blue_sensors[i], HIGH);
    //digitalWrite(orange_sensors[i], HIGH);
  }
  
  for(int i = 0; i < 8; i++)
  {
    detection_count[i] = 0;
  }
  
  pinMode(red_led, OUTPUT);
  pinMode(white_led, OUTPUT);
  
  Serial.begin(9600);
}

void return_error()
{
  Serial.println('e');
}

int update_detection_buffer(int id, char color)
{
  if('b' == color)
  {
    if(LOW == (digitalRead(blue_sensors[id])))
  }
}

void loop()
{
  if(new_pattern_recieved == 0)
  {
    if(4 == Serial.available())
    {
      for(int i = 0; i < 4; i++)
      {
        pattern[i] = Serial.read();
      }
      count = 0;
      new_pattern_recieved = 1;
    }
  }
  
  if((1 == new_pattern_recieved) && (count < 4))
  {
    if(pattern[count] == 'o')
    {
      if(LOW == (digitalRead(blue_sensors[count])))
        return_error();
      else if(LOW == (digitalRead(orange_sensors[count])))
        count++;
    }
    else if(pattern[count] == 'b')
    {
      if(LOW == (digitalRead(orange_sensors[count])))
        return_error();
      else if(LOW == (digitalRead(blue_sensors[count])))
        count++;
    }
  }
  
  //Serial.println(count);
  //delay(100);
}
