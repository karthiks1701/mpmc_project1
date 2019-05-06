
#include<avr/io.h>
#include<util/delay.h>

void armmov(int up)
{    if(!up)
        {
     OCR0B = 22;
     _delay_ms(500);
        }
      else if(up)
      {
        OCR0B = 10;
     _delay_ms(500);
      }
          
}

void basemov(int left)
{
   if(left)
        {
     OCR2B = 16;
     _delay_ms(500);
        }
      else if(left==0)
      {
        OCR2B = 4;
     _delay_ms(500);
      }
          
}
void gripmov(int pick)
{
     if(pick)
        {
     OCR0A = 26;
     _delay_ms(500);
        }
      else if(pick==0)
      {
        OCR0A = 14;
     _delay_ms(500);
      }
          
}
void timer02() {
  DDRD |= (1 << 5) | (1 << 6) | (1 << 3);
  //Initila duty cycle 0
  OCR0A = 20;                                          //gripper initially released
  OCR0B = 16;                                           //arm initially postion
  TCCR0A |= (1 << COM0A1) | (1 << COM0B1);             //Non-inverting mode
  //Fast PWM
  TCCR0A |= (1 << WGM00) | (1 << WGM01);
  TCCR0B |= (1 << CS02) | (1 << CS00);                              //Start the Timer with 1024 prescaler

  OCR2B = 10;                          // base initially facing the center
  TCCR2A |= (1 << COM2B1);             //Non-inverting mode
  //Fast PWM
  TCCR2A |= (1 << WGM20) | (1 << WGM21);
  TCCR2B |= (1 << CS22) | (1 << CS21) | (1 << CS20);     // 1024 prescaler for timer 2
}

int main()
{
 int left,up,pick;
 timer02();
 _delay_ms(500);
 //armmov(0);
 //basemov(0);
 gripmov(1);
 return 0; 
  }
