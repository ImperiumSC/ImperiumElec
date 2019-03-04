void setup() {
 
Serial.begin(9600);       //begin serial com at 9600 bps (bits)
pinMode(12, OUTPUT);
pinMode(13, OUTPUT);      //enable internal pull up resistor to make those pins outputs
}

void loop() {
  
  int input = analogRead(A0);     //input the pin you're reading from. Signal voltage value
  
  //arduino board ADC reads voltages on a 0-1023 scale for 0-5V
  float voltage = input * (5/1023);
  Serial.println(voltage);

  
  //math to convert our voltage value to a current value      the equation is defined on the flexscada website
  int CF = .0224;    // math constant for conversion of sensor
  float current = (voltage - 2.5)/.0224;
  Serial.println(current);


if(current > 40){                   // if the current gets above certain thresholds then light up two warning lights
  digitalWrite(12,HIGH);
  
}
if(current >= 50) {
  digitalWrite(13, HIGH);
    
  }
  
}


  /*
  int voltage = 10;
  int current = 5;
  Serial.println(voltage);
  Serial.println(current);
  */
  



  
