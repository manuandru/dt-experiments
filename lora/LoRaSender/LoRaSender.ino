/**
 * @author    Manuel Andruccioli
 * @file      LoRaSender.ino
 */

#include "utils.h"
#include "LoRaClient.h"

int makeMeasurement() {
    return random(20, 31); // just random values for the sake of the example
}

void setup() {
    setupLoRa();
}

void loop()
{
    int measure = makeMeasurement();
    String packet = "{\"measure\": " + String(measure) + "}";
    Serial.println("Sending with LoRa: " + packet);

    if (u8g2) {
        u8g2->clearBuffer();
        u8g2->drawStr(0, 12, "Sending with LoRa:");
        u8g2->drawStr(0, 30, packet.c_str());
        u8g2->sendBuffer();
    }

    sendPacket(packet);
    Serial.println("Sending: " + packet);

    if (u8g2) {
        u8g2->drawStr(0, 48, "Message Sent!");
        u8g2->sendBuffer();
    }

    delay(1000);
}
