/**
 * @author    Manuel Andruccioli
 * @file      WiFiHonoClient.cpp
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include "WiFiHonoClient.h"

void setupWiFi() {
    Serial.begin(115200);

    // Connect to WiFi
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }

    // Print the WiFi connection details
    Serial.println("Connected to WiFi");
    Serial.println("IP address: " + WiFi.localIP().toString());
}

int sendTelemetryToHono(String payload) {
    HTTPClient http;

    http.begin(HONO_ENDPOINT);
    http.setAuthorization(HONO_USERNAME, HONO_PASSWORD);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(payload);
    String response = http.getString();

    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    Serial.println(response);

    http.end();

    return httpResponseCode;
}
