import keyboard
import time
import threading
import random
from tkinter import Tk, Label, Entry, Button, StringVar, DoubleVar

# Globale Variablen
is_paused = False

# Funktion für das Drücken der Taste
def press_e():
    global is_paused
    time.sleep(float(initial_wait_time.get()))  # Wartezeit vor der ersten Eingabe
    while True:
        if not is_paused:
            keyboard.press_and_release(default_key.get())
            print(f"Taste '{default_key.get()}' gedrückt.")
        try:
            min_wait_time = float(default_wait_time.get()) - 0.2
            max_wait_time = float(default_wait_time.get()) + 1.2
            wait_time = random.uniform(min_wait_time, max_wait_time)
            time.sleep(wait_time)
        except ValueError:
            print("Ungültige Eingabe für die Wartezeit. Bitte eine Zahl eingeben.")

# Funktion zum Umschalten der Pause
def toggle_pause():
    global is_paused
    while True:
        if keyboard.is_pressed(default_pause_key.get()):
            is_paused = not is_paused
            if is_paused:
                print("Pausiert.")
            else:
                print("Fortgesetzt.")
            time.sleep(1)

# Funktion zum Starten der Threads
def start_threads():
    thread_e = threading.Thread(target=press_e)
    thread_toggle = threading.Thread(target=toggle_pause)

    thread_e.daemon = True
    thread_toggle.daemon = True

    thread_e.start()
    thread_toggle.start()

# GUI-Funktion
def create_gui():
    global default_key, default_pause_key, default_wait_time, initial_wait_time

    root = Tk()
    root.title("Automatischer Tastendruck")

    # Funktion zur Konvertierung von Zahlen mit Komma in Punkt
    def convert_to_float(value):
        try:
            return float(str(value).replace(',', '.'))
        except ValueError:
            return 0.0

    # Funktion zur Validierung von Eingaben (nur Zahlen zulassen)
    def validate_numeric_input(event, var):
        value = var.get()
        if not value.replace(',', '.').replace('.', '', 1).isdigit():
            var.set(''.join([c for c in value if c.isdigit() or c in [',', '.']]))

    # Funktion zur Validierung der Eingabe-Taste (nur erster Buchstabe zulassen)
    def validate_key_input(event, var):
        value = var.get()
        if len(value) > 1:
            var.set(value[0])

    # tkinter-Variablen initialisieren
    default_key = StringVar(root, value='e')
    default_pause_key = StringVar(root, value='k')
    default_wait_time = StringVar(root, value='28.5')  # Als String für Verarbeitung
    initial_wait_time = StringVar(root, value='5.0')  # Als String für Verarbeitung

    # Taste-Label und Eingabefeld
    Label(root, text="Welche Taste soll automatisch gedrückt werden?").grid(row=0, column=0, padx=10, pady=10)
    key_entry = Entry(root, textvariable=default_key)
    key_entry.grid(row=0, column=1, padx=10, pady=10)
    key_entry.bind('<KeyRelease>', lambda event: validate_key_input(event, default_key))

    # Pause-Taste-Label und Eingabefeld
    Label(root, text="Welche Taste pausiert das Programm?").grid(row=1, column=0, padx=10, pady=10)
    pause_key_entry = Entry(root, textvariable=default_pause_key)
    pause_key_entry.grid(row=1, column=1, padx=10, pady=10)
    pause_key_entry.bind('<KeyRelease>', lambda event: validate_key_input(event, default_pause_key))

    # Wartezeit-Label und Eingabefeld
    Label(root, text="Wie lange soll zwischen den Eingaben gewartet werden (Sekunden)?").grid(row=2, column=0, padx=10, pady=10)
    wait_time_entry = Entry(root, textvariable=default_wait_time)
    wait_time_entry.grid(row=2, column=1, padx=10, pady=10)
    wait_time_entry.bind('<KeyRelease>', lambda event: validate_numeric_input(event, default_wait_time))

    # Initial-Wartezeit-Label und Eingabefeld
    Label(root, text="Wie lange soll vor der ersten Eingabe gewartet werden (Sekunden)?").grid(row=3, column=0, padx=10, pady=10)
    initial_time_entry = Entry(root, textvariable=initial_wait_time)
    initial_time_entry.grid(row=3, column=1, padx=10, pady=10)
    initial_time_entry.bind('<KeyRelease>', lambda event: validate_numeric_input(event, initial_wait_time))

    # Überwachung der Eingaben zur automatischen Konvertierung
    def update_values():
        try:
            converted_wait_time = convert_to_float(default_wait_time.get())
            converted_initial_time = convert_to_float(initial_wait_time.get())
            default_wait_time.set(f"{converted_wait_time:.1f}")  # Intern konvertieren, aber String beibehalten
            initial_wait_time.set(f"{converted_initial_time:.1f}")  # Intern konvertieren, aber String beibehalten
        except ValueError:
            print("Ungültige Eingabe für die Wartezeit. Bitte eine Zahl eingeben.")
        root.after(100, update_values)

    # Start-Button
    Button(root, text="Start", command=start_threads).grid(row=4, column=0, columnspan=2, pady=20)

    update_values()
    root.mainloop()

# Start der GUI
if __name__ == "__main__":
    create_gui()