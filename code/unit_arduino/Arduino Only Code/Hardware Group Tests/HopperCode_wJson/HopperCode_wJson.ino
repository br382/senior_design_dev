//* This code collects and processes data from an Ultrasonic sensor and
// * Accelerometer/Gyroscope for determining the current paint available in
// * a hopper. This data is then transmitted wirelessly via the NRF24L01
// * transceiver to be displayed to the user
// *
// * ***HARDWARE CONNECTIONS***
// *
// * Ultrasonic Sensor Circuit:
// * VCC connection of the sensor attached to +5V
// * GND connection of the sensor attached to ground
// * TRIG connection of the sensor attached to digital pin 5
// * ECHO connection of the sensor attached to digital pin 4
// *
// * Accelerometer Circuit:
// * Vin connection of the sensor attached to +5V
// * GND connection of the sensor attached to groung
// * SCL connection of the sensor attached to A5
// * SDA connection of the sensor attached to A4
// *


//Inclusion of all libraries and definition of all constants

#include <SPI.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM9DS0.h>
#include <Kalman.h>
#include <NewPing.h>
#define trigPin 5  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define echoPin 4  // Arduino pin tied to echo pin on the ultrasonic sensor.

NewPing sonar(trigPin, echoPin);

int paintLevel = 0; // One element array to hold paint level indicator

// Create the Kalman instances
Kalman kalmanX;
Kalman kalmanY;
Adafruit_LSM9DS0 lsm = Adafruit_LSM9DS0(1000);

// IMU Data
double accX, accY, accZ;
double gyroX, gyroY, gyroZ;

double gyroXangle, gyroYangle; // Angle calculated using the gyro only
double compAngleX, compAngleY; // Calculated angle using a complementary filter
double kalAngleX, kalAngleY; // Calculated angle using a Kalman filter
uint32_t timer;

void setupSensor() //Setting up the Accelerometer/Gyroscope
{
  // 1.) Set the accelerometer range
  lsm.setupAccel(lsm.LSM9DS0_ACCELRANGE_2G);

  // 2.) Set the magnetometer sensitivity
  lsm.setupMag(lsm.LSM9DS0_MAGGAIN_2GAUSS);

  // 3.) Setup the gyroscope
  lsm.setupGyro(lsm.LSM9DS0_GYROSCALE_245DPS);
}

void setup() {
  Serial.begin(9600); // Initialize serial communication
    /*-------Test Connection and gather initial values for Accelerometer----*/
    delay(100); // Wait for Accelerometer to stabilize
  
    //Serial.println("LSM raw read demo");
  
    // Try to initialise and warn if we couldn't detect the chip
    if (!lsm.begin())
    {
      Serial.println("Oops ... unable to initialize the LSM9DS0. Check your wiring!");
      while (1);
    }
    //Serial.println("Found LSM9DS0 9DOF");
    //Serial.println("");
    //Serial.println("");
  
    /* Set kalman and gyro starting angle */
    lsm.read();
    accX = lsm.accelData.x;
    accY = lsm.accelData.y;
    accZ = lsm.accelData.z;
    double roll  = atan(accY / sqrt(accX * accX + accZ * accZ)) * RAD_TO_DEG;
    double pitch = atan2(-accX, accZ) * RAD_TO_DEG;
  
    kalmanX.setAngle(roll); // Set starting angle
    kalmanY.setAngle(pitch);
    gyroXangle = roll;
    gyroYangle = pitch;
    compAngleX = roll;
    compAngleY = pitch;
  
    timer = micros();
  
    /*-------End: Test Connection and gather initial values for Accelerometer----*/
  
}

void loop() {
    /* ------------------Ultrasonic Data Collection---------------------- */
    delay(50);
    long duration = sonar.ping_median();
      //Serial.println(duration);
  
    /*---------------- End of Ultrasonic Data Collection----------------- */
  
    /*---------------- Accelerometer/Gyro Data Collection----------------- */
  
    lsm.read();
    /* Update all the values */
    accX = lsm.accelData.x;
    accY = lsm.accelData.y;
    accZ = lsm.accelData.z;
    gyroX = lsm.gyroData.x;
    gyroY = lsm.gyroData.y;
    gyroZ = lsm.gyroData.z;
  
    double dt = (double)(micros() - timer) / 1000000; // Calculate delta time
    timer = micros();
    double roll  = atan(accY / sqrt(accX * accX + accZ * accZ)) * RAD_TO_DEG;
    double pitch = atan2(-accX, accZ) * RAD_TO_DEG;
  
    double gyroXrate = gyroX / 131.0; // Convert to deg/s
    double gyroYrate = gyroY / 131.0; // Convert to deg/s
  
    // This fixes the transition problem when the accelerometer angle jumps between -180 and 180 degrees
    if ((pitch < -90 && kalAngleY > 90) || (pitch > 90 && kalAngleY < -90)) {
      kalmanY.setAngle(pitch);
      compAngleY = pitch;
      kalAngleY = pitch;
      gyroYangle = pitch;
    } else
      kalAngleY = kalmanY.getAngle(pitch, gyroYrate, dt); // Calculate the angle using a Kalman filter
  
    if (abs(kalAngleY) > 90)
      gyroXrate = -gyroXrate; // Invert rate, so it fits the restriced accelerometer reading
      kalAngleX = kalmanX.getAngle(roll, gyroXrate, dt); // Calculate the angle using a Kalman filter
  
      gyroXangle += gyroXrate * dt; // Calculate gyro angle without any filter
      gyroYangle += gyroYrate * dt;
  
      compAngleX = 0.93 * (compAngleX + gyroXrate * dt) + 0.07 * roll; // Calculate the angle using a Complimentary filter
      compAngleY = 0.93 * (compAngleY + gyroYrate * dt) + 0.07 * pitch;
  
    // Reset the gyro angle when it has drifted too much
    if (gyroXangle < -180 || gyroXangle > 180)
      gyroXangle = kalAngleX;
    if (gyroYangle < -180 || gyroYangle > 180)
      gyroYangle = kalAngleY;
  
    //  Serial.print(roll); Serial.print("\t");
    //  Serial.print(gyroXangle); Serial.print("\t");
    //  Serial.print(compAngleX); Serial.print("\t");
    //  Serial.print(kalAngleX); Serial.print("\t");
    //
    //  Serial.print("\t");
    //
    //  Serial.print(pitch); Serial.print("\t");
    //  Serial.print(gyroYangle); Serial.print("\t");
    //  Serial.print(compAngleY); Serial.print("\t");
    //  Serial.print(kalAngleY); Serial.print("\t");
    //
    //
    //  Serial.print("\r\n");
    delay(2);
  
  
  
    /*---------------- End Accelerometer/Gyro Data Collection----------------- */
  
  
    /*----------------Hopper Logic----------------- */
    // if statements for paint level indicator
    if (kalAngleX >= -30 && kalAngleX <= 30 && kalAngleY >= -30 && kalAngleY <= 30 ) {
      if (duration < 150)
      {
        paintLevel = 4;
      }
      else if (duration < 250)
      {
        paintLevel = 3;
      }
      else if (duration < 350)
      {
        paintLevel = 2;
      }
      else
        paintLevel = 1;
    }
  Serial.println(paintLevel);
  
  
}
