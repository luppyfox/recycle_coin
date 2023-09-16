

//คำเตือน1 กูไม่มั่นใจว่ามอตเตอ์จะหมุนไปทางไหน ให้เลื่อนกล่องไปอยู่กลางๆ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

//วิธีการทำ
//มาร์คจุดกึ่งกลางแกนมอตเอร์ไว้ พอโค้ดทำงานเสร็จให้วัดว่าจากเริ่มต้นมันมากี่มิล(จดไว้ หรืออะไรก็ได้)
//เอาโค้ดนี้สั่งการ motor แล้วเอาค่าที่มัน print ออกมาเก็บไว้(จดไว้ หรืออะไรก็ได้)

#define ENCA 2
#define ENCB 3
#define PWM 5
#define IN2 6
#define IN1 7
#define LIM 8

int pos = 0;
int set_pwm = 0;

void setup() {
  Serial.begin(9600);
  pinMode(ENCA, INPUT);
  pinMode(ENCB, INPUT);
  attachInterrupt(digitalPinToInterrupt(ENCA), readEncoder, RISING);
  pinMode(LIM, INPUT);
  setMotor(1, set_pwm, PWM, IN1, IN2);
  delay(2000);
//  for (int i; i <= 2000; i++) {
  while(digitalRead(LIM) == 0){
    setMotor(1, set_pwm, PWM, IN1, IN2);
//    delay(1);
    Serial.println(pos);
  }
  setMotor(0, 0, PWM, IN1, IN2);
  Serial.println(pos);
  Serial.println("Finished !!!!!!!!!!!!!!!!!!!");
}

void loop() {
}

void setMotor(int dir, int pwmVal, int pwm, int in1, int in2) {
  analogWrite(pwm, pwmVal);
  if (dir == 1) {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  }
  else if (dir == -1) {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  }
  else {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
  }
}

void readEncoder() {
  int b = digitalRead(ENCB);
  if (b > 0) {
    pos++;
  }
  else {
    pos--;
  }

}
