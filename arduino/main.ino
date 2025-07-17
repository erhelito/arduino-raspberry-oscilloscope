void setup() {
  Serial.begin(9600);
}

void loop() {
  int value1 = analogRead(A0);
  int value2 = analogRead(A1);

  Serial.print(value1);
  Serial.print(";");
  Serial.println(value2);
}