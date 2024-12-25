#include <windows.h>
#include <iostream>
#include <thread>
#include <chrono>
#include <atomic>
#include <random>

std::atomic<bool> isRunning(true);

// Funktion, um eine zufällige Zahl zwischen 0,2 und 0,5 zu generieren
double getRandomDelay() {
    static std::random_device rd;
    static std::mt19937 gen(rd());
    static std::uniform_real_distribution<> dis(0.2, 0.5);
    return dis(gen);
}

void pressEKey() {
    // INPUT-Struktur vorbereiten
    INPUT input = { 0 };
    input.type = INPUT_KEYBOARD;
    input.ki.wVk = 'E'; // Virtueller Tastencode für die Taste 'E'

    while (true) {
        if (isRunning) {
            // "E" drücken
            SendInput(1, &input, sizeof(INPUT));

            // "E" loslassen
            input.ki.dwFlags = KEYEVENTF_KEYUP;
            SendInput(1, &input, sizeof(INPUT));

            // Zurücksetzen für den nächsten Durchlauf
            input.ki.dwFlags = 0;
        }

        // Zufällige Verzögerung zwischen 0,2 und 0,5 Sekunden berechnen
        double randomDelay = getRandomDelay();
        std::this_thread::sleep_for(std::chrono::duration<double>(1.0 + randomDelay));
    }
}

void listenForKey() {
    while (true) {
        if (GetAsyncKeyState('K') & 0x8000) {
            isRunning = !isRunning; // Umschalten zwischen Pause und Aktiv
            std::cout << (isRunning ? "Fortgesetzt" : "Pausiert") << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(500)); // Debounce
        }
    }
}

int main() {
    std::cout << "Druecke STRG + C, um das Programm zu beenden." << std::endl;
    std::cout << "Druecke K, um das Programm zu pausieren/fortzusetzen." << std::endl;

    // Thread für Tasteneingabe starten
    std::thread keyListener(listenForKey);

    // Spammer starten
    pressEKey();

    keyListener.join();
    return 0;
}
