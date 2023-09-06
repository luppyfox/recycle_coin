#include <Servo.h>

#define ENCA 2
#define ENCB 3
#define PWM 5
#define IN2 6
#define IN1 7
#define LIM 8

#define Trig_PIN 12  // Pin connect to Trig pin
#define Echo_PIN 13  // Pin connect to Echo pin

// PI Constant
float kp = 0;
float ki = 0;
// long prevT = 0;
// float eprev = 0;
// float eintegral = 0;
int max_pwm;
int min_pwm;
int tolerance;

int pos = 0;
int set_pwm = 0;
int num_bin = 4;          // number of bin
float ppr_dist = 62.832;  //62.832 แก้เป็นระยะที่วัดได้จากโลกจริง เป็นหน่วย มม. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
float ppr_tig = 290;      //667 290.909 331ค่าที่ปริ้นท์จากโค้ด test_enc !!!!!!!!!!!!!!!!!!!!!!!!!!!
float bin_dist = 294;     //(295)distance between bin to bin, unit = mm

int setz = 0;
int state = 1;

String Pyinput;
int integerValue = 0;

Servo servo1;
Servo servo2;

int i = 0;

void setup() {
  Serial.begin(9600);
  pinMode(LIM, INPUT);

  pinMode(ENCA, INPUT);
  pinMode(ENCB, INPUT);

  pinMode(Trig_PIN, OUTPUT);
  pinMode(Echo_PIN, INPUT);

  servo1.attach(9);
  servo2.attach(10);

  servo1.write(0);
  servo2.write(180);

  attachInterrupt(digitalPinToInterrupt(ENCA), readEncoder, RISING);
  //while (true){setMotor(1, set_pwm, PWM, IN1, IN2);}
  //Serial.println("target pos");
}

void loop() {
  //limit switch
  int limit_check = digitalRead(LIM);
  //Serial.println(limit_check);

  if (setz == 0) {
    setMotor(-1, 100, PWM, IN1, IN2);
    //Serial.println("setz");
    if (limit_check == 1) {
      setMotor(0, 0, PWM, IN1, IN2);
      pos = 0;
      state = 1;
      setz = 1;
    }
    //รับส่งค่า
  } else if (setz == 1) {
    //ขั้นกลางการทำงาน
    // Serial.println("STATE INPUT");

    Pyinput = Serial.readString();
    // integerValue = 2;  //Pyinput.toInt();

    // For test loop from bin 1 to bin 2
    integerValue = integerValue + 1;
    if (integerValue == 5){integerValue = 1;}

    if (integerValue == 1) {
      // Serial.println(integerValue);
      state = 1;
      setz = 2;
      max_pwm = 100;
      min_pwm = 60;
      kp = 1;
      tolerance = -15;
      //  ki = 0;

    } else if (integerValue == 2) {
      // Serial.println(integerValue);
      state = 2;
      setz = 2;
      max_pwm = 200;
      min_pwm = 50;
      kp = 0.15;
      tolerance = 0;
      //  ki = 0.006;

    } else if (integerValue == 3) {
      // Serial.println(integerValue);
      state = 3;
      setz = 2;
      max_pwm = 255;
      min_pwm = 100;
      kp = 0.17;
      tolerance = 0;
      //  ki = 0.006;

    } else if (integerValue == 4) {
      // Serial.println(integerValue);
      state = 4;
      setz = 2;
      max_pwm = 255;
      min_pwm = 130;
      kp = 0.17;
      tolerance = 0;
      //  ki = 0.006;

    } else if (Pyinput == "") {
      setz = 1;
    }


    //ทำงานttt
  } else if (setz == 2) {
    // Serial.println("GO!!!!!!!!!!!");
    while (setz == 2) {
      // error
      int e = pos - pprToGoal(state);

      // ปัญหาไม่ยอมวิ้งกลับ//

      // motor direction
      int dir = 1;
      if (e > 0) {
        dir = -1;
      }

      // // PI Controller
      // // time difference
      // long currT = micros();
      // float deltaT = ((float)(currT - prevT)) / (1.0e6);
      // prevT = currT;

      // // integral
      // eintegral = eintegral + abs(e) * deltaT;

      // // PI Control pwm
      // set_pwm = abs(e) * kp + eintegral * ki;

      // P control pwm
      set_pwm = abs(e) * kp;

      if (set_pwm >= max_pwm) {
        set_pwm = max_pwm;
      } else if (set_pwm <= min_pwm) {
        set_pwm = min_pwm;
      }
      if (e >= tolerance) {
        set_pwm = 0;
        e = 0;
      }

      setMotor(dir, set_pwm, PWM, IN1, IN2);

      // // store previous error
      // eprev = e;

      // For serial print
      Serial.print("Error is ");
      Serial.print(e);
      Serial.print(" Goal is ");
      Serial.print(pprToGoal(state));
      Serial.print(" Position is ");
      Serial.print(pos);
      Serial.print(" Speed value is ");
      Serial.print(set_pwm);
      Serial.println();

      // // For serial plot
      // Serial.print("e:");
      // Serial.print(e);
      // Serial.print(",");
      // Serial.print("pos:");
      // Serial.print(pos);
      // Serial.print(",");
      // Serial.print("set_pwm:");
      // Serial.println(set_pwm);

      if (e == 0 && state == 1) {
        Serial.print("State1 test value is ");
        Serial.println(state);

        setMotor(0, 0, PWM, IN1, IN2);
        for (i = 0; i <= 90; i++) {
          servo1.write(i);        // 0 --> 90
          servo2.write(180 - i);  // 180 --> 90
        }

        delay(5000);

        for (i = 90; i <= 180; i++) {
          servo2.write(i);       // 180 --> 90
          servo1.write(90 - i);  // 90 --> 0
        }

        delay(5000);

        setz = 0;

      } else if (e == 0 && state == 2) {
        Serial.print("State1 test value is ");
        Serial.println(state);

        setMotor(0, 0, PWM, IN1, IN2);
        for (i = 0; i <= 90; i++) {
          servo1.write(i);        // 0 --> 90
          servo2.write(180 - i);  // 180 --> 90
        }

        delay(5000);

        for (i = 90; i <= 180; i++) {
          servo2.write(i);       // 180 --> 90
          servo1.write(90 - i);  // 90 --> 0
        }

        delay(5000);
        setz = 0;

      } else if (e == 0 && state == 3) {
        Serial.print("State1 test value is ");
        Serial.println(state);

        setMotor(0, 0, PWM, IN1, IN2);
        for (i = 0; i <= 90; i++) {
          servo1.write(i);        // 0 --> 90
          servo2.write(180 - i);  // 180 --> 90
        }

        delay(5000);

        for (i = 90; i <= 180; i++) {
          servo2.write(i);       // 180 --> 90
          servo1.write(90 - i);  // 90 --> 0
        }

        delay(5000);
        setz = 0;

      } else if (e == 0 && state == 4) {
        Serial.print("State1 test value is ");
        Serial.println(state);

        setMotor(0, 0, PWM, IN1, IN2);
        delay(5000);
        for (i = 0; i <= 90; i++) {
          servo1.write(i);        // 0 --> 90
          servo2.write(180 - i);  // 180 --> 90
        }

        delay(5000);

        for (i = 90; i <= 180; i++) {
          servo2.write(i);       // 180 --> 90
          servo1.write(90 - i);  // 90 --> 0
        }

        delay(5000);
        setz = 0;
      }
    }
  }
}

void setMotor(int dir, int pwmVal, int pwm, int in1, int in2) {
  analogWrite(pwm, pwmVal);
  if (dir == 1) {
    digitalWrite(in1, HIGH);
    digitalWrite(in2, LOW);
  } else if (dir == -1) {
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
  } else {
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
  }
}
int pprToGoal(int state_num) {
  float target = (ppr_tig / ppr_dist) * (bin_dist * (state_num - 1));
  return (target);
}

void readEncoder() {
  int b = digitalRead(ENCB);
  if (b > 0) {
    pos++;
  } else {
    pos--;
  }
}
