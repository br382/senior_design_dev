char sep   = '\t';
char delim = '\n';
void setup() {
  Serial.begin(9600); 
}

void loop(){ //DO NOT CONVERT VALUES HERE!!!! LOGGING ONLY!!!
 //Serial.print(micros());
  // read the input on analog pin 0:
 Serial.print(millis());      Serial.print(sep);
 Serial.print(analogRead(0)); Serial.print(sep);
 Serial.print(analogRead(1)); Serial.print(sep);
 Serial.print(analogRead(2)); Serial.print(sep);
 //Serial.print(analogRead(3)); Serial.print(sep);
 //Serial.print(analogRead(4)); Serial.print(sep);
 //Serial.print(analogRead(5)); //Serial.print(sep);
 //These Outputs Are disabled for when not needed for extra speed.
 Serial.print(delim);
 delay(1000);
}
