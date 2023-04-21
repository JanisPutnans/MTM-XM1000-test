
#include "stdmansos.h"



 
void Print()                  
{

  while (1) {

uint16_t light = lightRead();
uint16_t humidity = humidityRead();
uint16_t temperature = temperatureRead();

      
      //PRINTF("light = x", light);
      //PRINTF("humidity = %u\n", humidity);
      //PRINTF("temperature = %u\n", temperature);

      PRINTF("%u %u %u\n", temperature,humidity,light)
     
        msleep(1000); // sleep two seconds

            };


}




void appMain(void)
{
  
   Print();


}
