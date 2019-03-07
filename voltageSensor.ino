void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(A0,INPUT);
  pinMode(A1,INPUT);
  pinMode(12, OUTPUT);
  pinMode(13,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  float input = analogRead(A0);
  float v0 = input * (5/1023);   //ADC converted input voltage
  // we are going to have a two stage stepdown if we use this thing so the voltage division will be a little goofy
  //which means that we can handle large voltages with ** Reasonable ** accuracy    I think it might be better for the arduino
  //current-wise if we have a little more resistance between it and the main power supply   correct me if I'm wrong

  //10x stepdown with a 90K (R1) resistor and a 10K (R2) resistor        attached to the 10K resistor is a 30K (R3) and 7.5K (R4) stepdown (5x)
  int R1 = 90000;
  int R2 = 10000;
  int R3 = 30000;
  int R4 = 7500;
  float voltage;                                             //car's voltage 
 
  voltage = (((R1+R2)*(R3*R4)) / (R2*R4)) * v0;           //solving for the cars voltage based off of the input voltage
  Serial.println(voltage);
  

  
}
