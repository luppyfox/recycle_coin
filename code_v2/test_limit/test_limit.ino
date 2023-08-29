void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(8,INPUT);
  
}

void loop() {
  // put your main code here, to run repeatedly:
//  int e = digitalRead(8);
  Serial.println(digitalRead(8));
//  while(e != 1){
//     e = digitalRead(8);
//     Serial.println(e);
//     delay(1);
//  }
//  Serial.println("Finished !!!!!!!!!!!!!!!");
}
