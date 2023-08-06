#define trigPin 10
#define echoPin 13

float get_distance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  unsigned long pulse_start = micros();
  unsigned long pulse_end = pulse_start;

  // Wait for the pulse to start
  while (digitalRead(echoPin) == LOW && (pulse_end - pulse_start) < 10000) {
    pulse_start = micros();
  }

  // Wait for the pulse to end
  while (digitalRead(echoPin) == HIGH && (pulse_end - pulse_start) < 10000) {
    pulse_end = micros();
  }

  unsigned long pulse_duration = pulse_end - pulse_start;
  float distance = pulse_duration * 0.0343 / 2.0; // Speed of sound in air is ~343 m/s

  return distance;
}

void setup() {
  Serial.begin(9600); // Start serial communication

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  // Read the distance from the HC-SR04 sensor
  float distance = get_distance();

  // Send the distance to the Raspberry Pi over Serial
  Serial.print(distance);

  delay(1); // Adjust the delay time as needed
}
