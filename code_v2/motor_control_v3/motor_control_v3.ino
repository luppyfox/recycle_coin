#define ENCA 2
#define ENCB 3
#define PWM 5
#define IN2 6
#define IN1 7
#define LIM 8

int pos = 0;
long prevT = 0;
float eprev = 0;
float eintegral = 0;

int set_pwm = 255;
int num_bin = 4;            // number of bin
float ppr_dist = 62.832;         //แก้เป็นระยะที่วัดได้จากโลกจริง เป็นหน่วย มม. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
float ppr_tig = 675;          //ค่าที่ปริ้นท์จากโค้ด test_enc !!!!!!!!!!!!!!!!!!!!!!!!!!!
float bin_dist = 294;       //(295)distance between bin to bin, unit = mm


void setup() {
  Serial.begin(9600);
  pinMode(LIM, INPUT);

  pinMode(ENCA, INPUT);
  pinMode(ENCB, INPUT);

  attachInterrupt(digitalPinToInterrupt(ENCA), readEncoder, RISING);
  Serial.println("target pos");
}

void loop() {

  //limit switch
  int state = 1;
  int limit_check = digitalRead(LIM);
  //Serial.println("test 1");
   
  if (limit_check == 1) {
    while (state <= num_bin) {
  

      
      // error
      int e = pos - pprToGoal(state);




      // ปัญหาไม่ยอมวิ้งกลับ//
      ///////////////////////////////////////
      // motor direction
      int dir = 1;
      if (e > 0) {
        dir = -1;
      }

      // signal the motor

      Serial.print(dir);
      setMotor(dir, set_pwm, PWM, IN1, IN2);

      //////////////////////////////////////
      // store previous error
      eprev = e;
      Serial.print("Error is ");
      Serial.println(e);
      Serial.print("Goal is ");
      Serial.print(pprToGoal(state));
      Serial.print(" Position is ");
      Serial.print(pos);
      Serial.println();
      if (e == 0 && state == 1){
        Serial.print("State1 test value is ");
        Serial.println(state);
        setMotor(0, 0, PWM, IN1, IN2);
        delay(5000);
        state++;
        break;
      }
      else if (e == 0) {
        Serial.print("State is ");
        Serial.println(state);
        setMotor(0, 0, PWM, IN1, IN2);
        delay(5000);
        state++;
        break;
      }
    }
  }//fix this left right
  else if (limit_check == 0) {
    setMotor(-1, set_pwm, PWM, IN1, IN2);
    pos = 0;
    //Serial.println("test 3");
  }
  //Serial.println(limit_check);
//  else {
//    setMotor(0, 0, PWM, IN1, IN2);
//
//  }
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
