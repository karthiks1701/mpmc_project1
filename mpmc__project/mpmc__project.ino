
#include<avr/io.h>
#include<util/delay.h>

char ch;

void usart_init(void)
{
  UCSR0C=(1<<UCSZ01)|(1<<UCSZ00);
  UCSR0B=(1<<RXEN0)|(1<<TXEN0);
  UBRR0L=0x67;
  UCSR0A=0x00;
}
void usart_send(char a)
{
  while(UCSR0A!=(UCSR0A|1<<UDRE0));
  UDR0=a;
}
char usart_receive()
{
  while(UCSR0A!=(UCSR0A|1<<RXC0));
  ch=UDR0;
  return ch;
}

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
     OCR2B = 30;
     _delay_ms(500);
        }
      else if(left==0)
      {
        OCR2B = 8;
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

  OCR2B = 19;                          // base initially facing the center
  TCCR2A |= (1 << COM2B1);             //Non-inverting mode
  //Fast PWM
  TCCR2A |= (1 << WGM20) | (1 << WGM21);
  TCCR2B |= (1 << CS22) | (1 << CS21) | (1 << CS20);     // 1024 prescaler for timer 2
}

int main()
{ 
 
 char data;
 int left,up,pick;
 usart_init();
 timer02();
 usart_send('a');
 while(1)
 {
 data = usart_receive();
 usart_send(data);
 if (data == '2')
{
basemov(1);
}
else if (data == '3')
{
basemov(0);

}
if (data == '1')
{
armmov(1);
}
else if (data == '0')
{
armmov(0);

}
 }
 _delay_ms(500);
 //armmov(0);
 //basemov(0);
 //gripmov(1);
 return 0; 
  }
