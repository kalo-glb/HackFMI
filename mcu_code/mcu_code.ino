#include <Servo.h>

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
int box = 0;

int servo_state[] = {0, 0, 0};
Servo s1, s2, s3;


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
  
  digitalWrite(white_led, HIGH);
  digitalWrite(red_led, HIGH);
  
  s1.attach(3);
  s2.attach(10);
  s3.attach(11);
  
  //63 143 110
  s1.write(63);
  s2.write(143);
  s3.write(35);
  
  Serial.begin(9600);
}

void return_success()
{
  count = 0;
  new_pattern_recieved = 0;
  Serial.println('4');
  digitalWrite(white_led, LOW);
}

void return_error()
{
  Serial.println('e');
  new_pattern_recieved = 0;
  count = 0;
  digitalWrite(red_led, LOW);
}

void control_box(int box_number, int isOpening)
{
  
  int from_pos = 0;
  int to_pos = 0;
  Servo servo;
  switch(box_number)
  {
    case 1:
    {
      from_pos = 63;
      to_pos = 118;
      servo = s1;
      break;
    }
    case 2:
    {
      from_pos = 143;
      to_pos = 50;
      servo = s2;
      break;
    }
    case 3:
    {
      from_pos = 35;
      to_pos = 110;
      servo = s3;
      break;
    }
  }
  
  if(0 == isOpening)
  {
    int temp = from_pos;
    from_pos = to_pos;
    to_pos = temp;
  }
  
  servo_state[box_number -1] = 1;
  
  if(from_pos > to_pos)
  {
    for(int i=from_pos; i > to_pos; i--)
    {
      servo.write(i);
      delay(30);
    }
  }
  else
  {
    for(int i=from_pos; i < to_pos; i++)
    {
      servo.write(i);
      delay(30);
    }
  }
  
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
  if('o' == color)
  {
    id += 4;
  }
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
    for(int i =0;i<3;i++)
    {
      if(1 == servo_state[i])
      {
        control_box(i+1, 0);
      }
    }
    
    if(5 == Serial.available())
    {
      for(int i = 0; i < 4; i++)
      {
        pattern[i] = Serial.read();
      }
      
      box = ((Serial.read()) - '0');
      
      control_box(box,1);
      
      count = 0;
      new_pattern_recieved = 1;
      
      digitalWrite(white_led, HIGH);
      digitalWrite(red_led, HIGH);
    }
  }
  
  for(int i = 0; i < 4; i++)
  {
    update_detection_buffer(i, 'b');
    update_detection_buffer(i, 'o');
  }
  
  if((1 == new_pattern_recieved) && (count < 4))
  {
    if(detection_state[count] == 1)
    {
      if(pattern[count] == 'b')
        count++;
      else
        return_error();
    }
    if(detection_state[count + 4] == 1)
    {
      if(pattern[count] == 'o')
        count++;
      else
        return_error();
    }
    
  }
  if(count == 4)
  {
    return_success();
  }
  
}
