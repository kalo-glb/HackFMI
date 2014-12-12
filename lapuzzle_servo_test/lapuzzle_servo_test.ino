#include <Servo.h>

Servo s1, s2, s3;

void setup()
{
  s1.attach(3);
  s2.attach(10);
  s3.attach(11);
  
  /* zatvpreno
  s1.write(118);//118
  s2.write(50);//50
  s3.write(35);//110
  */
  
  s1.write(118);//118
  s2.write(50);//50
  s3.write(35);//110
}

void loop()
{
  delay(3000);
  s1.write(59);//59 118
  s2.write(143);//143 50
  s3.write(110);//35 110
}
