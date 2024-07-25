/**
 * @author    Manuel Andruccioli
 * @file      WiFiHonoClient.h
 */

#pragma once

#include <Arduino.h>

#define WIFI_SSID "wifi-ssid"
#define WIFI_PASSWORD "wifi-password"

#define HONO_ENDPOINT "hono-endpoint"
#define HONO_USERNAME "my-device@my-tenant"
#define HONO_PASSWORD "my-password"

void setupWiFi();

int sendTelemetryToHono(String payload);
