// Only supports SX1276/SX1278
#include "utils.h"
#include "LoRaClient.h"

int counter = 0;

void setup() {
    setupLoRa();
}

void loop()
{
    Serial.print("Sending packet: ");
    Serial.println(counter);

    sendPacket(String(counter));

    if (u8g2) {
        char buf[256];
        u8g2->clearBuffer();
        u8g2->drawStr(0, 12, "Transmitting: OK!");
        snprintf(buf, sizeof(buf), "Sending: %d", counter);
        u8g2->drawStr(0, 30, buf);
        u8g2->sendBuffer();
    }
    counter++;
    delay(500);
}