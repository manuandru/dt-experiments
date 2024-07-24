/**
 * @author    Manuel Andruccioli
 * @file      LoRaClient.cpp
 */

#include "LoRaClient.h"

void setupLoRa() {
    setupBoards();
    // When the power is turned on, a delay is required.
    delay(1500);

#ifdef RADIO_TCXO_ENABLE
    pinMode(RADIO_TCXO_ENABLE, OUTPUT);
    digitalWrite(RADIO_TCXO_ENABLE, HIGH);
#endif

    Serial.println("LoRa Sender");
    LoRa.setPins(RADIO_CS_PIN, RADIO_RST_PIN, RADIO_DIO0_PIN);
    if (!LoRa.begin(LORA_FREQ_CONFIG))
    {
        Serial.println("Starting LoRa failed!");
        while (1)
            ;
    }
    LoRa.setSyncWord(SYNC_WORD_LORA);
}

void sendPacket(String packet) {
    LoRa.beginPacket();
    LoRa.print(packet);
    LoRa.endPacket();
}

String parsePacketPayload() {
    int packetSize = LoRa.parsePacket(); // non-blocking
    if (packetSize) {
        String recv = "";

        // read packet
        while (LoRa.available()) {
            recv += (char)LoRa.read();
        }

        return recv;
    }
    return "";
}
