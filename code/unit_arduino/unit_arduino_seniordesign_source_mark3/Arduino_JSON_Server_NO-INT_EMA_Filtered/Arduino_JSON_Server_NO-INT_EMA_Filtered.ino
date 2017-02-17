/*
 * Brett Reich, Rick Taylor
 * Dummy test JSON output format for use in testing Sensors.py code.
 * For Xbee Usage:
 *   FOR 32U4 architectures: find-replace `Ser ial` with `Ser ial1`
 *   FOR ATMEGA-382 (Uno): find-replace `Ser ial1` with `Ser ial`
 *   (spaced out on purpose to fool bad find-replace programs)
 * Issue with Adafruit LSM9DS0 I2C communication `if (!lsm.begin())` statement.
 *   It will hang forever (tested on Arduino Pro Mini 5V 16MHz AtMega328) if no I2C device attached.
 *   Using DIP-Switch style hardware `setup()` detection instead.
 *   UID = int( [`MIN_UID_DIG_PIN is LSB`, ..., `MAX_UID_DIG_PIN is MSB`] ) + 1;
 *     if UID == 1: lsm==TRUE,  sonic==TRUE,  psi==FALSE
 *     else:        lsm==FALSE, sonic==FALSE, psi==TRUE
 *     default:     All other sensors are read by all valid: `0 < UID <= 2^num_dip_pins`
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
const char key_str[][MAX_LEN]    = {"all_data", "sonic_us", "pressure_bits", "battery_bits", "acc_g", "velocity_ms", "dist_mm", "magnetometer"};
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
double alpha = 0.9;
double gxEMA = 0;
double gyEMA = 0;
double gzEMA = 0;
double accX  = 0;
double accY  = 0;
double accZ  = 0;
double magX  = 0;
double magY  = 0;
double magZ  = 0;
double mxEMA = 0;
double myEMA = 0;
double mzEMA = 0;
float heading = 0;
#define accel_mg_lsb 0.061
#define mag_mg_lsb 0.08

bool lsm_enabled     = TRUE;
bool sonic_enabled   = TRUE;
bool psi_enabled     = TRUE;
Adafruit_LSM9DS0 lsm = Adafruit_LSM9DS0();
void setupSensor() {
  lsm.setupAccel(lsm.LSM9DS0_ACCELRANGE_2G);
  lsm.setupMag(lsm.LSM9DS0_MAGGAIN_2GAUSS);
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

//pin-jumper determined on startup.
#define MIN_UID_DIG_PIN 4
#define MAX_UID_DIG_PIN 9
int UID_VALUE = 0; // inverse bitwise logical of pins, MIN as LSB, MAX as MSB (internal pullup used) + 1 (to handle null error).
// only UID_VALUE == 1 allows lsm interface to be enabled.

void setup(void) {
  Serial.begin(9600);
  for (int pin = MIN_UID_DIG_PIN; pin <= MAX_UID_DIG_PIN; pin++) {
    pinMode(pin, INPUT);
    digitalWrite(pin, HIGH); //turn on pullup resistors
    delay(10);
    UID_VALUE = UID_VALUE + ( !digitalRead(pin) << ( pin - MIN_UID_DIG_PIN ));
  }
  UID_VALUE += 1;
  Serial.print("{\"UID_VALUE\": "); Serial.print(UID_VALUE); Serial.println("}");
  powerLED();
  pinMode(13, OUTPUT);
  lsm_enabled = (UID_VALUE == 1); //USING DIP-PIN SELECTION!!!!
  if (lsm_enabled == TRUE) {
    if (!lsm.begin()) { //THIS METHOD WILL HANG FOREVER IF I2C DOES NOT EXIST!!!! USING DIP-PIN SELECTION!!!!
      Serial.println("Oops ... unable to initialize the LSM9DS0. Check your wiring!");
      lsm_enabled = FALSE;
    }
  }
  sonic_enabled =  lsm_enabled;
  psi_enabled   = !lsm_enabled;
}


void loop(void){
  if (lsm_enabled == TRUE) {
    lsm.read();
    accX  = lsm.accelData.x;
    accY  = lsm.accelData.y;
    accZ  = lsm.accelData.z;
    gxEMA = alpha*gxEMA + (1 - alpha)*accX; 
    gyEMA = alpha*gyEMA + (1 - alpha)*accY;
    gzEMA = alpha*gzEMA + (1 - alpha)*accZ;

    gxEMA = (gxEMA * accel_mg_lsb) / 100.0;  // Converting to G's
    gyEMA = (gyEMA * accel_mg_lsb) / 100.0;
    gzEMA = (gzEMA * accel_mg_lsb) / 100.0;

//    Serial.print("Accel X: ");
//    Serial.print(gxEMA);
//    Serial.print("     ");   
//    Serial.print("Accel Y: ");
//    Serial.print(gyEMA);
//    Serial.print("     "); 
//    Serial.print("Accel Z: ");
//    Serial.print(gzEMA);
//    Serial.println("");
//    
    magX  = lsm.magData.x;
    magY  = lsm.magData.y;
    magZ  = lsm.magData.z;
    mxEMA = alpha*mxEMA + (1 - alpha)*magX; 
    myEMA = alpha*myEMA + (1 - alpha)*magY;
    mzEMA = alpha*mzEMA + (1 - alpha)*magZ;

//    mxEMA = (mxEMA * mag_mg_lsb);  // Converting to Gauss
//    myEMA = (myEMA * mag_mg_lsb);
//    mzEMA = (mzEMA * mag_mg_lsb);
//    Serial.print("Mag X: ");
//    Serial.print(mxEMA);
//    Serial.print("     ");   
//    Serial.print("Mag Y: ");
//    Serial.print(myEMA);
//    Serial.print("     "); 
//    Serial.print("Mag Z: ");
//    Serial.print(mzEMA);
//    Serial.println("");
//  if (myEMA > 0)
//    heading = 90 - (atan(mxEMA/myEMA)*(180/PI));
//  else if (myEMA < 0) 
//    heading = 270 - (atan(mxEMA/myEMA)*(180/PI));
//  else if (myEMA == 0 && mxEMA < 0)
//    heading = 180.0;
//  else if (myEMA == 0 && mxEMA > 0)
//    heading = 0;
//    heading = 12 + (atan2(myEMA,mxEMA) * (180 / PI));
//  Serial.print("Heading: ");
//  Serial.println(heading, 2);

  }

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
        key_bool[i] = (int(JSON_INPUT_ROOT[key_str[i]]) == UID_VALUE);
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
      JsonArray& key_index = JSON_OUTPUT_ROOT.createNestedArray("UID_VALUE");
      key_index.add(UID_VALUE);
    }
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
  if ((key_bool[SONIC] == TRUE) && (sonic_enabled == TRUE))
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
  
  if ((key_bool[PRESSURE] == TRUE) && (psi_enabled == TRUE))
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
  if ((key_bool[ACC] == TRUE) && (lsm_enabled == TRUE))
  {
    JsonArray& key_index = JSON_OUTPUT_ROOT.createNestedArray(key_str[ACC]);
    key_index.add(gxEMA);
    key_index.add(gyEMA);
    key_index.add(gzEMA);
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
  if ((key_bool[COMPASS] == TRUE) && (lsm_enabled == TRUE))
  {
    JsonArray& key_index = JSON_OUTPUT_ROOT.createNestedArray(key_str[COMPASS]);
    key_index.add(mxEMA);
    key_index.add(myEMA);
    key_index.add(mzEMA);
    key_bool[COMPASS] = FALSE;
    PRINT = TRUE;
  }
  
  if (PRINT == TRUE){
    JSON_OUTPUT_ROOT.printTo(Serial);
    Serial.println();
    PRINT = FALSE;
  }
  digitalWrite(13, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(10);              // wait for a second
  digitalWrite(13, LOW);    // turn the LED off by making the voltage LOW
  delay(10);   
}

