#include <SoftwareSerial.h>

// Define pins
#define GSM_TX 2
#define GSM_RX 3
#define RELAY_PIN 4
#define UNLOCK_BTN 5
#define PAY_RENT_BTN 6

SoftwareSerial GSM(GSM_TX, GSM_RX);

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(UNLOCK_BTN, INPUT_PULLUP);
  pinMode(PAY_RENT_BTN, INPUT_PULLUP);
  GSM.begin(9600);
  Serial.begin(9600);
  digitalWrite(RELAY_PIN, LOW); // Lock is initially locked
}

void loop() {
  // Unlock button pressed
  if (digitalRead(UNLOCK_BTN) == LOW) {
    sendCommand("AUTH"); // Authenticate user
    String response = receiveResponse();
    if (response == "TRUE") {
      unlockDoor();
    } else {
      Serial.println("Access Denied");
    }
  }

  // Pay rent button pressed
  if (digitalRead(PAY_RENT_BTN) == LOW) {
    sendCommand("TR"); // Send rent payment
    String response = receiveResponse();
    if (response == "SUCCESS") {
      Serial.println("Rent Paid");
    } else {
      Serial.println("Transaction Failed");
    }
  }
}

void unlockDoor() {
  digitalWrite(RELAY_PIN, HIGH); // Unlock door
  Serial.println("Door Unlocked");
  delay(5000); // Keep unlocked for 5 seconds
  digitalWrite(RELAY_PIN, LOW);  // Lock the door
}

void sendCommand(String command) {
  GSM.println(command);
  Serial.print("Sent: ");
  Serial.println(command);
}

String receiveResponse() {
  String response = "";
  while (GSM.available()) {
    response += char(GSM.read());
  }
  Serial.print("Response: ");
  Serial.println(response);
  return response;
}