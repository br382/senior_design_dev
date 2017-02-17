#include <Wire.h>
#include <SPI.h>
#include <Adafruit_LSM9DS0.h>
#include <Adafruit_Sensor.h>  // not used in this demo but required!

// i2c
Adafruit_LSM9DS0 lsm = Adafruit_LSM9DS0();

/*
 * //Source: http://www.timzaman.com/2011/04/heading-calculating-heading-with-tilted-compass/
int getcompasscourse(){
  int ax,ay,az,cx,cz,cy;
  MMA7660.getValues(&ax,&ay,&az);
  HMC.getValues(&cx,&cz,&cy);
 
  float xh,yh,ayf,axf;
  ayf=ay/57.0;//Convert to rad
  axf=ax/57.0;//Convert to rad
  xh=cx*cos(ayf)+cy*sin(ayf)*sin(axf)-cz*cos(axf)*sin(ayf);
  yh=cy*cos(axf)+cz*sin(axf);
 
  var_compass=atan2((double)yh,(double)xh) * (180 / PI) -90; // angle in degrees
  if (var_compass>0){var_compass=var_compass-360;}
  var_compass=360+var_compass;
 
  return (var_compass);
}
*/

float getCompassCourse(int acc_x, int acc_y, int acc_z, int mag_x, int mag_y, int mag_z)
{
  float compass_deg_out;
  float xh, yh, acc_yf, acc_xf;
  acc_yf = float(acc_y)/57.0; //Convert to Rad
  acc_xf = float(acc_x)/57.0; //Convert to Rad
  xh     = (mag_x * cos(acc_yf) ) + (mag_y * sin(acc_yf) ) - (mag_z * cos(acc_xf)*sin(acc_yf));
  yh     = (mag_y * cos(acc_xf) ) + (mag_y * sin(acc_xf) );
  compass_deg_out = atan2( (double)yh, (double)xh ) * (180.0 / PI) - 90.0; //angle in degrees
  if (compass_deg_out <= 0) { compass_deg_out += 360.0; }
  return( compass_deg_out );
}

void setupSensor()
{
  lsm.setupAccel(lsm.LSM9DS0_ACCELRANGE_2G);
  lsm.setupMag(lsm.LSM9DS0_MAGGAIN_2GAUSS);
  lsm.setupGyro(lsm.LSM9DS0_GYROSCALE_245DPS);
}

void setup() 
{
#ifndef ESP8266
  while (!Serial);     // will pause Zero, Leonardo, etc until serial console opens
#endif
  Serial.begin(9600);
  Serial.println("LSM raw read demo");
  if (!lsm.begin())
  {
    Serial.println("CHIP: LSM9DS0 NOT FOUND");
    while (1);
  }
}


int   count = 0;
int   max_c = 100;
float alpha = 0.99;
float deg_n = 0;
void loop() 
{
  lsm.read();
  /*
  Serial.print("Accel X: "); Serial.print((int)lsm.accelData.x); Serial.print(" ");
  Serial.print("Y: "); Serial.print((int)lsm.accelData.y);       Serial.print(" ");
  Serial.print("Z: "); Serial.println((int)lsm.accelData.z);     Serial.print(" ");
  Serial.print("Mag X: "); Serial.print((int)lsm.magData.x);     Serial.print(" ");
  Serial.print("Y: "); Serial.print((int)lsm.magData.y);         Serial.print(" ");
  Serial.print("Z: "); Serial.println((int)lsm.magData.z);       Serial.print(" ");
  Serial.print("Gyro X: "); Serial.print((int)lsm.gyroData.x);   Serial.print(" ");
  Serial.print("Y: "); Serial.print((int)lsm.gyroData.y);        Serial.print(" ");
  Serial.print("Z: "); Serial.println((int)lsm.gyroData.z);      Serial.println(" ");
  Serial.print("Temp: "); Serial.print((int)lsm.temperature);    Serial.println(" ");
  */
  deg_n = alpha * deg_n + (1 - alpha) * getCompassCourse((int)lsm.accelData.x, (int)lsm.accelData.y, (int)lsm.accelData.z,
                                   (int)lsm.magData.x,   (int)lsm.magData.y,   (int)lsm.magData.y );
  count += 1;
  if (1/*count > max_c*/)
  {
    count = count % max_c;
    Serial.print("DegN: ");
    Serial.println( deg_n );
  }
  //delay(200);
}
