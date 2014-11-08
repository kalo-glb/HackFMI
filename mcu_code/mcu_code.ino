int blue_sensors[] = {A0, A2, A3, A5};
int orange_sensors[] = {2, 4, 7, 8};
#define red_led 5
#define white_led 6

#define start_byte 0x02
#define end_byte   0x03

byte ser_buf[20];

enum Events
{
  set_pattern,
  correct_sensor_hit,
  incorrect_sensor_hit,
  game_start,
  game_end,
  
  max_event
};

typedef struct
{
  byte ser_buf[20];
  byte index = 0;
} SerialBuffer;

typedef struct
{
  int event_type = max_event;
  byte event_data[10];
} Message;

Message msg;

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

/*
int processCommand()
{
  static SerialBuffer buf;
  int start_index = 0;
  int end_index = 0;
  byte c = 0;
  int message_bounds_detected = 0;
  if(Serial.available())
  {
    c = Serial.read();
    if(end_byte == c)
    {
      end_index = buf.index;
      message_bounds_detected++;
    }
    buf.ser_buf[buf.index++] = c;
    buf.index %= sizeof(buf.ser_buf);
  }
  
  if(1 != message_bounds_detected)
  {
    // find start byte
    for(int i = 0; i < sizeof(buf.ser_buf); i++)
    {
      if(start_byte == buf.ser_buf[i])
      {
        start_index = i;
        message_bounds_detected++;
      }
    }
  }
  
  int idx = 0;
  if(2 == message_bounds_detected)
  {// start_index != 0; end_index != 0 => parse message
    idx = (start_index + 1) % sizeof(buf.ser_buf)
    msg.event_type = buf.ser_buf[idx]
    for(int i = 0; i < (start_index + 1) % sizeof(buf.ser_buf)
  }
  
}*/

void loop()
{
  /*static int pwm_value = 0;
  static int pwm_step = 20;
  analogWrite(red_led, pwm_value);
  pwm_value += pwm_step;
  if(pwm_value < 0 || pwm_value > 255)
  {
    pwm_step = -pwm_step; 
  }*/
  digitalWrite(red_led, HIGH);
  digitalWrite(white_led, HIGH);
  delay(1000);
  digitalWrite(red_led, LOW);
  digitalWrite(white_led, LOW);
  delay(1000);
}
