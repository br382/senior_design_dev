#include <SPI.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_LSM9DS0.h>
#include <Kalman.h> // Source: https://github.com/TKJElectronics/KalmanFilter

//#define RESTRICT_PITCH // Comment out to restrict roll to ±90deg instead - please read: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf

Kalman kalmanX; // Create the Kalman instances
Kalman kalmanY;
Adafruit_LSM9DS0 lsm = Adafruit_LSM9DS0();

/* IMU Data */
double accX, accY, accZ;
double gyroX, gyroY, gyroZ;

double gyroXangle, gyroYangle; // Angle calculate using the gyro only
double compAngleX, compAngleY; // Calculated angle using a complementary filter
double kalAngleX, kalAngleY; // Calculated angle using a Kalman filter

uint32_t timer;

void setupSensor()
{
  // 1.) Set the accelerometer range
  lsm.setupAccel(lsm.LSM9DS0_ACCELRANGE_2G);

  // 2.) Set the magnetometer sensitivity
  lsm.setupMag(lsm.LSM9DS0_MAGGAIN_2GAUSS);

  // 3.) Setup the gyroscope
  lsm.setupGyro(lsm.LSM9DS0_GYROSCALE_245DPS);
}


void setup() {
  Serial.begin(115200);

  delay(100); // Wait for sensor to stabilize

  Serial.println("LSM raw read demo");

  // Try to initialise and warn if we couldn't detect the chip
  if (!lsm.begin())
  {
    Serial.println("Oops ... unable to initialize the LSM9DS0. Check your wiring!");
    while (1);
  }
  Serial.println("Found LSM9DS0 9DOF");
  Serial.println("");
  Serial.println("");

  /* Set kalman and gyro starting angle */
  lsm.read();
  accX = lsm.accelData.x;
  accY = lsm.accelData.y;
  accZ = lsm.accelData.z;

  // Source: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf eq. 25 and eq. 26
  // atan2 outputs the value of -π to π (radians) - see http://en.wikipedia.org/wiki/Atan2
  // It is then converted from radians to degrees

// Eq. 28 and 29
  double roll  = atan(accY / sqrt(accX * accX + accZ * accZ)) * RAD_TO_DEG;
  double pitch = atan2(-accX, accZ) * RAD_TO_DEG;

  kalmanX.setAngle(roll); // Set starting angle
  kalmanY.setAngle(pitch);
  gyroXangle = roll;
  gyroYangle = pitch;
  compAngleX = roll;
  compAngleY = pitch;

  timer = micros();
}

void loop() {
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

  // Source: http://www.freescale.com/files/sensors/doc/app_note/AN3461.pdf eq. 25 and eq. 26
  // atan2 outputs the value of -π to π (radians) - see http://en.wikipedia.org/wiki/Atan2
  // It is then converted from radians to degrees

// Eq. 28 and 29
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
  //gyroXangle += kalmanX.getRate() * dt; // Calculate gyro angle using the unbiased rate
  //gyroYangle += kalmanY.getRate() * dt;

  compAngleX = 0.93 * (compAngleX + gyroXrate * dt) + 0.07 * roll; // Calculate the angle using a Complimentary filter
  compAngleY = 0.93 * (compAngleY + gyroYrate * dt) + 0.07 * pitch;

  // Reset the gyro angle when it has drifted too much
  if (gyroXangle < -180 || gyroXangle > 180)
    gyroXangle = kalAngleX;
  if (gyroYangle < -180 || gyroYangle > 180)
    gyroYangle = kalAngleY;



      /* Get a new sensor event */ 
  sensors_event_t accel, mag, gyro, temp;

  lsm.getEvent(&accel, &mag, &gyro, &temp); 

  // print out accelleration data
  Serial.print("Accel X: "); Serial.print(accel.acceleration.x); Serial.print(" ");
  Serial.print("  \tY: "); Serial.print(accel.acceleration.y);       Serial.print(" ");
  Serial.print("  \tZ: "); Serial.print(accel.acceleration.z);     Serial.println("  \tm/s^2");

//  // print out magnetometer data
//  Serial.print("Magn. X: "); Serial.print(mag.magnetic.x); Serial.print(" ");
//  Serial.print("  \tY: "); Serial.print(mag.magnetic.y);       Serial.print(" ");
//  Serial.print("  \tZ: "); Serial.print(mag.magnetic.z);     Serial.println("  \tgauss");
//  
//  // print out gyroscopic data
//  Serial.print("Gyro  X: "); Serial.print(gyro.gyro.x); Serial.print(" ");
//  Serial.print("  \tY: "); Serial.print(gyro.gyro.y);       Serial.print(" ");
//  Serial.print("  \tZ: "); Serial.print(gyro.gyro.z);     Serial.println("  \tdps");
//
//  // print out temperature data
//  Serial.print("Temp: "); Serial.print(temp.temperature); Serial.println(" *C");
//
//  Serial.println("**********************\n");

//  /* Print Data */
//#if 1 // Set to 1 to activate
//  Serial.print(accX); Serial.print("\t");
//  Serial.print(accY); Serial.print("\t");
//  Serial.print(accZ); Serial.print("\t");
//
////  Serial.print(gyroX); Serial.print("\t");
////  Serial.print(gyroY); Serial.print("\t");
////  Serial.print(gyroZ); Serial.print("\t");
//
//  Serial.print("\t");
//#endif
////
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
//  delay(2);
}
