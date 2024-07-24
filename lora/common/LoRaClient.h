/**
 * @author    Manuel Andruccioli
 * @file      LoRaClient.h
 */

#pragma once
#include "LoRaBoards.h"
#include "LoRa.h"

#define SYNC_WORD_LORA 0x23

void setupLoRa();

void sendPacket(String packet);

/*
* @return String. Empty string if no data is available.
*/
String parsePacketPayload();
