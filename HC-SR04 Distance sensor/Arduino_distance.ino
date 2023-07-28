#define trigPin 10
#define echoPin 13

float duration, distance;
unsigned long start_time = 0; // Variable to store the starting time in milliseconds

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  start_time = millis(); // Record the starting time
}

void loop() {
  // Write a pulse to the HC-SR04 Trigger Pin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Measure the response from the HC-SR04 Echo Pin
  duration = pulseIn(echoPin, HIGH);

  // Determine distance from duration
  // Use 343 meters per second as the speed of sound
  distance = (duration / 2) * 0.0343;

  // Send results to Serial Monitor

  if (distance >= 400 || distance <= 2) {
    Serial.println("Out of range");
  } else {
    // Get the current time in seconds with four decimal points
    float current_time = (millis() - start_time) / 1000.0;

    // Send the timestamp and distance to the computer through Serial
    Serial.print(current_time, 3); // The second argument (4) specifies the number of decimal points
    Serial.print(",");
    Serial.println(distance);

    delay(0);
  }
  delay(0);
}
