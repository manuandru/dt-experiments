// Only supports SX1276/SX1278
#include "utils.h"
#include "LoRaClient.h"

void setup() {
    setupLoRa();
}

void loop() {

    // // try to parse packet
    String packet = parsePacketPayload();
    if (packet != "") {
        if (u8g2) {
            u8g2->clearBuffer();
            char buf[256];
            u8g2->drawStr(0, 12, "Received OK!");
            u8g2->drawStr(0, 26, packet.c_str());
            u8g2->sendBuffer();
        }
    }
}
