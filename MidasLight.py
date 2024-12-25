import keyboard
import time
import random
import threading

# Globale Variable, um den Status zu verfolgen
is_running = True

def get_random_delay():
    """Generiert eine zufällige Verzögerung zwischen 0,2 und 0,5 Sekunden."""
    return random.uniform(0.2, 0.5)

def press_e_key():
    """Simuliert das Drücken der Taste 'E' in zufälligen Abständen."""
    global is_running
    while True:
        if is_running:
            keyboard.press_and_release('e')
            random_delay = get_random_delay()
            time.sleep(1.0 + random_delay)
        else:
            time.sleep(0.1)  # Kurze Pause, um CPU-Last zu minimieren

def listen_for_key():
    """Hört auf die Taste 'K', um den Status umzuschalten."""
    global is_running
    while True:
        if keyboard.is_pressed('k'):
            is_running = not is_running
            print("Fortgesetzt" if is_running else "Pausiert")
            time.sleep(0.5)  # Debounce, um wiederholtes Umschalten zu vermeiden

if __name__ == "__main__":
    print("Drücke STRG + C, um das Programm zu beenden.")
    print("Drücke K, um das Programm zu pausieren/fortzusetzen.")

    # Threads starten
    key_listener_thread = threading.Thread(target=listen_for_key, daemon=True)
    key_listener_thread.start()

    # Hauptfunktion starten
    try:
        press_e_key()
    except KeyboardInterrupt:
        print("Programm beendet.")