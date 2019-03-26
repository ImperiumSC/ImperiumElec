const int voltage_tap_5v = A5;

void setup() {
 
Serial.begin(9600);       //begin serial com at 9600 bps (bits)
pinMode(voltage_tap_5v, INPUT);
}

void loop() {
  
  double input = analogRead(voltage_tap_5v);     //input the pin you're reading from. Signal voltage value
  
  //arduino board ADC reads voltages on a 0-1023 scale for 0-5V
  float voltage = input * (5.0/1023.0);
  double res = 25;
  voltage = voltage*res;
  voltage = 0.8386*voltage-0.1781 //R^2=0.9999, intercept = (0,-0.1781), point (0,0) included, not forced
  Serial.println(voltage);
}
  
