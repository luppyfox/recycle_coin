#define ENCA 2
#define ENCB 3
#define PWM 5
#define IN2 6
#define IN1 7
#define LIM 8


//คำนวณ Encoder
int pos = 0;
long prevT = 0;
float eprev = 0;
float eintegral = 0;

int set_pwm = 255;
int num_bin = 4;            // number of bin
float ppr_dist = 62.832;         //แก้เป็นระยะที่วัดได้จากโลกจริง เป็นหน่วย มม. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
float ppr_tig = 675;          //ค่าที่ปริ้นท์จากโค้ด test_enc !!!!!!!!!!!!!!!!!!!!!!!!!!!
float bin_dist = 294;       //(295)distance between bin to bin, unit = mm

//สร้างขึ้นใหม่
int setz = 0;



void setup() {
  Serial.begin(9600);
  pinMode(LIM, INPUT);

  pinMode(ENCA, INPUT);
  pinMode(ENCB, INPUT);

  attachInterrupt(digitalPinToInterrupt(ENCA), readEncoder, RISING);
  //Serial.println("target pos");
  while (true){setMotor(1, set_pwm, PWM, IN1, IN2);int e = pos - pprToGoal(1);Serial.println(e);}
 
}

void loop() {
  //limit switch
  int state = 1;
  int limit_check = digitalRead(LIM);
  //Serial.println(limit_check);

  //มาเพิ่มจุดลงที่หลังแถวตรงนี้
  if (setz == 0){
    //setzero
      Serial.println("setzero");
      
      while (setz == 0){
        int blocking = 0;

        int npos = 0;
        int e = pos - pprToGoal(state);
        Serial.print("ตำแหน่ง e ");
        Serial.println(e);
        
        setMotor(-1, set_pwm, PWM, IN1, IN2);
        if (blocking == 0 && limit_check == 1){
            //เพิ่มตัวแปรเก็บตำแหน่งแรกไปใช้
            setMotor(0, set_pwm, PWM, IN1, IN2);
            npos = e -1000;
          
        }else if(blocking == 1){
          setMotor(1, set_pwm, PWM, IN1, IN2);
          if (e == npos){
              setMotor(0, set_pwm, PWM, IN1, IN2);
              setz = 1; //setzero สำเร็จแล้ว
              break;
           }
        }
     }
  }   
 
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
int pprToGoal(int state_num) {
  float target = (ppr_tig / ppr_dist) * (bin_dist*(state_num-1));
  return (target);
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
