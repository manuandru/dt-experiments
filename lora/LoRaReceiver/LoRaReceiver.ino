/**
 * @author    Manuel Andruccioli
 * @file      LoRaReceiver.ino
 */

#include "LoRaClient.h"
#include "WiFiHonoClient.h"

#define MAX_TIME_TO_WAIT_FOR_LORA_PACKET_MS 10000

void handlePacketFromLoRa(String packet) {
    Serial.println("Receive from LoRa: " + packet);
    if (u8g2) {
        u8g2->clearBuffer();
        u8g2->drawStr(0, 12, "Receive from LoRa:");
        u8g2->drawStr(0, 30, packet.c_str());
        u8g2->sendBuffer();
    }

    sendPacketToHono(packet);
}

void sendPacketToHono(String packet) {
    int httpResponseCode = sendTelemetryToHono(packet);

    if (httpResponseCode >= 200 && httpResponseCode <= 299) {
        Serial.println("Telemetry sent to Hono successfully");
        if (u8g2) {
            u8g2->drawStr(0, 48, "Hono OK!");
            u8g2->sendBuffer();
        }
    } else {
        Serial.println("Failed to send telemetry to Hono");
        if (u8g2) {
            u8g2->drawStr(0, 48, "Hono FAIL!");
            u8g2->sendBuffer();
        }
    }
}

int forecastMeasure() {
    return random(0, 41); // just random values for the sake of the example
}

void handleForecasting() {
    int measure = forecastMeasure();
    Serial.println("No packets received for more than 5 seconds");
    if (u8g2) {
        u8g2->clearBuffer();
        u8g2->drawStr(0, 12, "No LoRa packets");
        String msg = "Forecast: " + String(measure);
        u8g2->drawStr(0, 30, msg.c_str());
        u8g2->sendBuffer();
    }

    String packet = "{\"measure\": " + String(measure) + ", \"forecast\": \"true\"}";
    sendPacketToHono(packet);
}

void setup() {
    Serial.begin(115200);
    setupLoRa();
    setupWiFi();
}

unsigned long lastPacketTime = 0;

void loop() {
    // try to parse packet
    String packet = parsePacketPayload();
    if (packet != "") {
        lastPacketTime = millis();
        handlePacketFromLoRa(packet);
    } else {
        unsigned long currentTime = millis();
        unsigned long elapsedTimeBetweenLastPacket = currentTime - lastPacketTime;

        // Forecasting measure if not receiving
        if (elapsedTimeBetweenLastPacket > MAX_TIME_TO_WAIT_FOR_LORA_PACKET_MS) {
            lastPacketTime = millis();
            handleForecasting();
        }
    }
}
