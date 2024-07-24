/**
 * @author    Manuel Andruccioli
 *
 */

#include "utils.h"

void log(const String &msg) {
    Serial.println(msg);
    if (u8g2) {
        u8g2->clearBuffer();
        char buf[256];
        u8g2->drawStr(0, 12, msg.c_str());
        u8g2->sendBuffer();
    }
}
