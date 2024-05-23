#define TRIGGER_PIN1 8 // Brown
#define ECHO_PIN1 9 //Blue
#define TRIGGER_PIN2 10 //Brown
#define ECHO_PIN2 11 //Blue
#define TRIGGER_PIN3 12 //Brown
#define ECHO_PIN3 13 //Blue
#define OUTPUT_PIN 7 //Output pin to red LED
#define THRESHOLD 85 // Threshold value of 85 cm, according to datasheet.

long duration1, duration2, duration3;
int distance1, distance2, distance3;

void setup() {
  pinMode(TRIGGER_PIN1, OUTPUT);
  pinMode(ECHO_PIN1, INPUT);
  pinMode(TRIGGER_PIN2, OUTPUT);
  pinMode(ECHO_PIN2, INPUT);
  pinMode(TRIGGER_PIN3, OUTPUT);
  pinMode(ECHO_PIN3, INPUT);
  pinMode(OUTPUT_PIN, OUTPUT);
  Serial.begin(9600); // Starts the serial communication on baud rate 9600
}

void loop() {
  // Sensor 1
  digitalWrite(TRIGGER_PIN1, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN1, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN1, LOW);
  duration1 = pulseIn(ECHO_PIN1, HIGH);
  distance1 = duration1 * 0.034 / 2;

  // Sensor 2
  digitalWrite(TRIGGER_PIN2, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN2, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN2, LOW);
  duration2 = pulseIn(ECHO_PIN2, HIGH);
  distance2 = duration2 * 0.034 / 2;

  // Sensor 3
  digitalWrite(TRIGGER_PIN3, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIGGER_PIN3, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN3, LOW);
  duration3 = pulseIn(ECHO_PIN3, HIGH);
  distance3 = duration3 * 0.034 / 2;

  // Print distances to the serial port
  Serial.print("Distance1: ");
  Serial.print(distance1);
  Serial.print(" cm, Distance2: ");
  Serial.print(distance2);
  Serial.print(" cm, Distance3: ");
  Serial.println(distance3); // Use println here to add a newline at the end

  // If any sensor reads a distance less than the threshold, set the output pin to HIGH
  if (distance1 < THRESHOLD || distance2 < THRESHOLD || distance3 < THRESHOLD) {
    digitalWrite(OUTPUT_PIN, HIGH);
  } else {
    digitalWrite(OUTPUT_PIN, LOW);
  }
}
