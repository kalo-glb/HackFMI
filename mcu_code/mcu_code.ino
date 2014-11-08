int blue_sensors[] = {A0, A2, A3, A5};
int orange_sensors[] = {2, 4, 7, 8};
#define red_led 5
#define white_led 6
#define detection_treshold 20

int detection_count[8];
int detection_state[8];

char pattern[4];
int new_pattern_recieved = 0;
int count = 0;
int lock = 0;

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
    {
      detection_count[id]++;
    }
    else if(HIGH == (digitalRead(blue_sensors[id])))
    {
      detection_count[id]--;
    }
    
    if(detection_count[id] > detection_treshold)
    {
      detection_state[id] = 1;
      detection_count[id] = detection_treshold;
    }
    else if(detection_count[id] < 0)
    {
      detection_state[id] = 0;
      detection_count[id] = 0;
    }
  }
  else if('o' == color)
  {
    if(LOW == (digitalRead(orange_sensors[id])))
    {
      detection_count[id + 4]++;
    }
    else if(HIGH == (digitalRead(orange_sensors[id])))
    {
      detection_count[id + 4]--;
    }
    
    if(detection_count[id + 4] > detection_treshold)
    {
      detection_state[id + 4] = 1;
      detection_count[id + 4] = detection_treshold;
    }
    else if(detection_count[id + 4] < 0)
    {
      detection_state[id + 4] = 0;
      detection_count[id + 4] = 0;
    }
  }
  
  if('o' == color)id += 4;
  return detection_state[id];
}

int get_detection_state(int id, char color)
{
  if('o' == color)id += 4;
  return detection_state[id];
}

int any_other_detected(int id, char color)
{
  if('o' == color)id += 4;
  for(int i = 0; i < 8; i++)
  {
    if(i == id)
      continue;
    if(detection_state[i])
      return 1;
  }
  return 0;
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
  
  for(int i = 0; i < 4; i++)
  {
    update_detection_buffer(i, 'b');
    update_detection_buffer(i, 'o');
  }
  
  if((1 == new_pattern_recieved) && (count < 4))
  {
    if(!lock)
    {
      if(any_other_detected(count, pattern[count]))
      {
        return_error();
      }
      else if(get_detection_state(count, pattern[count]))
      {
        count++;
        lock = !lock;
      }
    }
    else if(!(get_detection_state((count - 1), pattern[count - 1])))
    {
      lock = !lock;
    }
  }
  
  /*
  for(int i = 0; i < 8; i++)
  {
    Serial.print(detection_count[i]);
    Serial.print(' ');
  }
  */
  Serial.println(count);
}
