/*
 * Brett Reich, Rick Taylor, Ken Hale
 * Dummy test JSON output format for use in testing Sensors.py code.
 * For Xbee Usage:
 *   FOR 32U4 architectures: find-replace `Ser ial` with `Ser ial1`
 *   FOR ATMEGA-382 (Uno): find-replace `Ser ial1` with `Ser ial`
 *   (spaced out on purpose to fool bad find-replace programs)
*/
#include <ArduinoJson.h>
#include <limits.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM9DS0.h>


/*
 * Reminder of limits.h constants:
 * http://www.tutorialspoint.com/c_standard_library/limits_h.htm
 * ULONG_MAX
 * LONG_MAX
 * LONG_MIN
 * UINT_MAX
 * INT_MAX
 * INT_MIN
 * USHRT_MAX
 * SHRT_MAX
 * SHRT_MIN
 * MB_LEN_MAX
 * UCHAR_MAX
 * CHAR_MAX
 * CHAR_MIN
 * CHAR_BIT
 */
#define BUFFERSIZE       200
#define JSONBUFFERSIZE   BUFFERSIZE
#define SerialBUFFERSIZE BUFFERSIZE
#define TRUE 1
#define FALSE 0
#define PRESSURE_ANALOG_PIN 0
#define USEC_PER_METER (100.0*58.0) // Using: HC-SR04
  // (17.0/100.0) = (millimeters / uSec) for US-100  Sonic Sensor,
  // (1.0/58.0)   = (centimeters / uSec) for HC-SR04 Sonic Sensor,
#define PSI_PER_VOLT (1250.0) //Using: NPI-15A-353AH
  // (1250.0) = (PSI / Voltage) for NPI-15A-353AH Pressure Transducer
#define PSI_OFFSET (-625.0) //Using: NPI-15A-353AH
  // (-625.0) = (PSI offset) for NPI-15A-353AH Pressure Transducer
#define ACC_X_G_OFF 0
#define ACC_Y_G_OFF 0
#define ACC_Z_G_OFF 0
#define ACC_X_G_PER_V 1
#define ACC_Y_G_PER_V 1
#define ACC_Z_G_PER_V 1
//#define ...etc...
#define key_len 8
#define MAX_LEN 50
const char key_str[][MAX_LEN]    = {"all_data", "sonic_us", "pressure_bits", "battery_bits", "acc_g", "velocity_ms", "dist_mm", "compass_degN"};
//{"all", "son", "pre", "bat", "acc", "vel", "dis", "deg"};
//low-size and normal-size testing gets about 5Hz refresh logging output

bool key_bool[key_len]           = {false}; //[0, 0,...0].len() => key_str.len()
float key_test_value[]           = {FALSE, 0.03948*USEC_PER_METER, (2341.5-PSI_OFFSET)/PSI_PER_VOLT, 5.101, 1.001,      0.02,    0.001,          110.3}; //57% paint full 
#define ALL_DATA 0
#define SONIC    1
#define PRESSURE 2
#define BATTERY  3
#define ACC      4
#define VELOCITY 5
#define DISTANCE 6
#define COMPASS  7

#define PSI_FULL_PIN 13

#define PSI_FULL_LEVEL 3000 //psi
//Filter Variables for Accel
double alpha = 0.5; // This is the coefficient of EMA filtering
double gxFilt = 0;
double gyFilt = 0;
double gzFilt = 0;
double accX = 0;
double accY = 0;
double accZ = 0;

Adafruit_LSM9DS0 lsm = Adafruit_LSM9DS0();

void setupSensor()
{
  // 1.) Set the accelerometer range
  lsm.setupAccel(lsm.LSM9DS0_ACCELRANGE_2G);

  // 2.) Set the magnetometer sensitivity
  lsm.setupMag(lsm.LSM9DS0_MAGGAIN_2GAUSS);

  // 3.) Setup the gyroscope
  lsm.setupGyro(lsm.LSM9DS0_GYROSCALE_245DPS);
}


void psiFullTest( void ) {
  pinMode(PSI_FULL_PIN, OUTPUT);
  pinMode(PRESSURE_ANALOG_PIN, INPUT);
  int bits = analogRead(PRESSURE_ANALOG_PIN);
  int voltage = (bits / 206.0) + 0.034;
  int psi = voltage * 1250 + (-625);
  if ( psi > PSI_FULL_LEVEL ) {
    digitalWrite(PSI_FULL_PIN, TRUE);
  } else {
    digitalWrite(PSI_FULL_PIN, FALSE);
  }
}

void powerLED(void) {
    pinMode(10, OUTPUT);
    pinMode(11, OUTPUT);
    digitalWrite(10, LOW);
    digitalWrite(11, HIGH);
}

#define SONIC_TRIG_PIN 2
#define SONIC_ECHO_PIN 3
unsigned long sonic_end_time = 0;
unsigned long sonic_start_time = 0;

char Serial_BUF[SerialBUFFERSIZE];
bool PRINT = FALSE;



void setup(void) {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  //powerLED();
 
}


void loop(void){

  //Read in Accel Data and filter

  delay(100);

 // Try to initialise and warn if we couldn't detect the chip
  if (!lsm.begin())
  {
    Serial.println("Oops ... unable to initialize the LSM9DS0. Check your wiring!");
    while (1);
  }
  
  lsm.read();
  accX = lsm.accelData.x; //Reading in XYZ accel data
  accY = lsm.accelData.y;
  accZ = lsm.accelData.z;
  // Smoothing using EMA, alpha is defined above.
  gxFilt = (1 - alpha)*gxFilt + alpha*accX; 
  gyFilt = (1 - alpha)*gyFilt + alpha*accY;
  gzFilt = (1 - alpha)*gzFilt + alpha*accZ;
  

  psiFullTest();
  StaticJsonBuffer<JSONBUFFERSIZE> JSON_BUF_IN;
  StaticJsonBuffer<JSONBUFFERSIZE> JSON_BUF_OUT;
  if (1)
  {
    int k = 0;
    while(Serial.available() && (k < SerialBUFFERSIZE) )
    {
      Serial_BUF[k] = Serial.read();
      k++;
      delay(10);
    }
    Serial_BUF[k] = '\0';
  }
  JsonObject& JSON_INPUT_ROOT  = JSON_BUF_IN.parseObject(/*json*/ Serial_BUF);
  JsonObject& JSON_OUTPUT_ROOT = JSON_BUF_OUT.createObject();
  if (1)
  {
    if (JSON_INPUT_ROOT.success())
    {
      for (int i = 0; i < key_len; i++)
      {
        key_bool[i] = (JSON_INPUT_ROOT[key_str[i]] == TRUE);
      }
    }
  }
  if (key_bool[ALL_DATA] == TRUE)
  {
    for (int i = 1; i < key_len; i++)
    {
      key_bool[i] = TRUE;
    }
    key_bool[ALL_DATA] = FALSE;
    PRINT = TRUE;
  }
  /*
  for (int i = 1; i < key_len; i++)
  {
    if (key_bool[i] == TRUE)
    {
      JsonArray& key_index = JSON_OUTPUT_ROOT.createNestedArray(key_str[i]);
      if(i == ACC){
        key_index.add(0.08);
        key_index.add(0.02);
        }
      key_index.add(key_test_value[i]);
      key_bool[i] = FALSE;
      PRINT = TRUE;
    }
  }
  */
  if (key_bool[SONIC] == TRUE)
  {
    JsonArray& key_index = JSON_OUTPUT_ROOT.createNestedArray(key_str[SONIC]);
    pinMode(SONIC_TRIG_PIN, OUTPUT);
    digitalWrite(SONIC_TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(SONIC_TRIG_PIN, HIGH);
    delayMicroseconds(100);
    digitalWrite(SONIC_TRIG_PIN, LOW);
    
    pinMode(SONIC_ECHO_PIN, INPUT);
    unsigned long duration = pulseIn(SONIC_ECHO_PIN, HIGH);
    key_index.add(duration);
    key_bool[SONIC] = FALSE;
    PRINT = TRUE;      
  }
  
  if (key_bool[PRESSURE] == TRUE)
  {
    JsonArray& key_index = JSON_OUTPUT_ROOT.createNestedArray(key_str[PRESSURE]);
    int voltage_bits = analogRead(PRESSURE_ANALOG_PIN); //PF7 aka A0
    key_index.add(voltage_bits);
    key_bool[PRESSURE] = FALSE;
    PRINT = TRUE;
  }
  if (key_bool[BATTERY] == TRUE)
  {
    JsonArray& key_index = JSON_OUTPUT_ROOT.createNestedArray(key_str[BATTERY]);
    int voltage_bits = analogRead(1); //PF6 aka A1
    key_index.add(voltage_bits);
    key_bool[BATTERY] = FALSE;
    PRINT = TRUE;
  }
  if (key_bool[ACC] == TRUE)
  {
    JsonArray& key_index = JSON_OUTPUT_ROOT.createNestedArray(key_str[ACC]);
    key_index.add(gxFilt);
    key_index.add(gyFilt);
    key_index.add(gzFilt);
    key_bool[ACC] = FALSE;
    PRINT = TRUE;
  }
  if (key_bool[VELOCITY] == TRUE)
  {
    JsonArray& key_index = JSON_OUTPUT_ROOT.createNestedArray(key_str[VELOCITY]);
    key_index.add(key_test_value[VELOCITY]);
    key_bool[VELOCITY] = FALSE;
    PRINT = TRUE;
  }
  if (key_bool[DISTANCE] == TRUE)
  {
    JsonArray& key_index = JSON_OUTPUT_ROOT.createNestedArray(key_str[DISTANCE]);
    key_index.add(key_test_value[DISTANCE]);
    key_bool[DISTANCE] = FALSE;
    PRINT = TRUE;
  }
  if (key_bool[COMPASS] == TRUE)
  {
    JsonArray& key_index = JSON_OUTPUT_ROOT.createNestedArray(key_str[COMPASS]);
    key_index.add(key_test_value[COMPASS]);
    key_bool[COMPASS] = FALSE;
    PRINT = TRUE;
  }
  
  if (PRINT == TRUE){
    JSON_OUTPUT_ROOT.printTo(Serial);
    Serial.println();
    PRINT = FALSE;
  }
  //digitalWrite(13, !digitalRead(13));
}

