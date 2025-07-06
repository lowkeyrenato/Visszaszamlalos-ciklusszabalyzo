# -*- coding: utf-8 -*-

# HOGYAN FUTTASD A FEKETE PARANCSSORI ABLAK (CMD) NÉLKÜL:
# Egyszerűen nevezd át ezt a fájlt 'legzes.py'-ról 'legzes.pyw'-ra.

import sys
import tkinter as tk
from tkinter import messagebox
import traceback
from threading import Thread # <<< ÚJ IMPORT: A párhuzamos futtatáshoz

# by lowkeyrenato

# --- MEGBÍZHATÓ HANGKEZELÉS KÜLSŐ FÁJL NÉLKÜL ---
try:
    import winsound
    SOUND_AVAILABLE = True
except ImportError:
    SOUND_AVAILABLE = False

# Beágyazott WAV hangadatok
WAV_DATA = b'RIFFb\x05\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80>\x00\x00\x00}\x01\x00\x02\x00\x10\x00data^\x05\x00\x00\x00\x00\x01\x00\xfd\xff\x01\x00\x00\x00\xfb\xff\xea\xef\xee\xee\xeb\xef\x0f\xf8\x8a\xfc3\xfd\xee\xfc\xf1\xfb\xa5\xfa-\xfa\x9a\xf9\x1f\xf9\xe0\xf8\xad\xf8\x90\xf8o\xf8\xb7\xf8\xff\xf8\x91\xf9\xf9\xf9\xd2\xfa\x80\xfb7\xfc\xfa\xfc\xbb\xfd\x99\xfe\x01\xffH\xff\x86\xff\x8d\xff\x86\xff?\xff\x14\xff\xcf\xfe\x8b\xfe\x15\xfe2\xfd\xe4\xfb\xac\xfa5\xf9\xe0\xf7g\xf6\xb8\xf4\x81\xf3\xfc\xf1\x18\xf1\x84\xf0\xdf\xef\xf0\xf0A\xf1\xf2\xf2\x9e\xf4\xf2\xf6\xba\xf9"\xfc\xca\xfe\x8e\x00Z\x02\xe6\x03\x8f\x04\xf1\x04\x9e\x04\xf1\x03~\x02\xfb\x00\xd0\xfe*\xfc\xac\xf9\xb7\xf6\xc6\xf3\x11\xf1\xfd\xee4\xed[\xec*\xeb\xb3\xea\x8e\xea\xbb\xea\x17\xeb\xcb\xeb\x9d\xec\x97\xed\xbf\xee\x13\xf0\x91\xf1\x1e\xf3\xb4\xf4\xeb\xf6\x1e\xf9\x84\xfb\xc6\xfd\x16\xff\x9d\x00a\x01\x8c\x01\x8b\x01n\x01\x1f\x01\xbe\x00\xee\xff\x91\xff\x03\xff\x9d\xfe\x05\xfeL\xfd]\xfc`\xfb\xa2\xfa\xd5\xf9\x05\xf9\x10\xf8;\xf7B\xf6\xa8\xf5\x13\xf5h\xf4\xa2\xf3\xde\xf2\x15\xf2)\xf1\xc1\xf0\xfa\xf0\x01\xf1\x88\xf1\xc8\xf2\x11\xf4\xa1\xf5\xea\xf7\xfd\xf9\x85\xfc\x13\xff#\x01\xf4\x02\xac\x04\x82\x06\x1b\x07x\x07\xb1\x06\xf6\x04\x8e\x02)\x00\xc9\xfd\x15\xfb\xcb\xf8\xdb\xf5\xe2\xf2\xbb\xef\xfa\xec\xa9\xea;\xe9\xfa\xe7t\xe6\xa3\xe5\x1b\xe5\xcf\xe4\x9a\xe4\x9d\xe4\xae\xe4\xd0\xe4\xfd\xe4\x1e\xe5&\xe5\x1b\xe5\xfb\xe4\xdc\xe4\xc0\xe4\xaa\xe4\x98\xe4\xa7\xe4\xd0\xe4\x0f\xe50\xe5f\xe5v\xe5w\xe5l\xe5L\xe5\x1f\xe5\xfc\xe4\xe0\xe4\xd1\xe4\xd2\xe4\xe1\xe4\xfe\xe4\x1f\xe53\xe5Y\xe5p\xe5\x81\xe5\x89\xe5\x88\xe5r\xe5I\xe5\x1e\xe5\xf2\xe4\xd0\xe4\xb8\xe4\xb4\xe4\xc5\xe4\xe2\xe4\xfa\xe4\x0c\xe5\x17\xe5\x1b\xe5\x1b\xe5\x1d\xe5#\xe5.\xe5;\xe5A\xe5C\xe5@\xe59\xe50\xe5(\xe5\x1f\xe5\x18\xe5\x13\xe5\x13\xe5\x17\xe5\x1c\xe5!\xe5(\xe50\xe58\xe5?\xe5C\xe5D\xe5A\xe5;\xe53\xe5+\xe5#\xe5\x1b\xe5\x19\xe5\x19\xe5\x1c\xe5 \xe5$\xe5)\xe5/\xe55\xe5;\xe5A\xe5C\xe5B\xe5=\xe56\xe5.\xe5&\xe5\x1e\xe5\x1a\xe5\x18\xe5\x18\xe5\x1a\xe5\x1d\xe5 \xe5#\xe5\'\xe5+\xe5/\xe53\xe56\xe58\xe59\xe59\xe58\xe56\xe53\xe5/\xe5+\xe5\'\xe5#\xe5 \xe5\x1d\xe5\x1b\xe5\x19\xe5\x18\xe5\x18\xe5\x19\xe5\x1a\xe5\x1c\xe5\x1e\xe5 \xe5!\xe5"\xe5#\xe5#\xe5"\xe5!\xe5 \xe5\x1e\xe5\x1c\xe5\x1b\xe5\x1a\xe5\x19\xe5\x19\xe5\x19\xe5\x1a\xe5\x1b\xe5\x1c\xe5\x1d\xe5\x1d\xe5\x1e\xe5\x1e\xe5\x1d\xe5\x1d\xe5\x1c\xe5\x1b\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1b\xe5\x1b\xe5\x1c\xe5\x1c\xe5\x1c\xe5\x1c\xe5\x1c\xe5\x1b\xe5\x1b\xe5\x1b\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1b\xe5\x1b\xe5\x1b\xe5\x1b\xe5\x1b\xe5\x1b\xe5\x1b\xe5\x1b\xe5\x1b\xe5\x1b\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x19\xe5\x19\xe5\x19\xe5\x1a\xe5\x1a\xe5\x1a\xe5\x19\xe5\x19\xe5\x19\xe5\x1a\x00\x00'

try:
    import customtkinter as ctk
except ImportError:
    # ... (hibakezelő kód változatlan)
    error_title = "Hiányzó Könyvtár"
    error_message = ("A program futtatásához szükséges 'customtkinter' könyvtár nincs telepítve.\n\nKérjük, telepítsd a következő paranccsal egy parancssorban:\n\npip install customtkinter")
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(error_title, error_message)
    except tk.TclError:
        print(f"HIBA: {error_title}\n{error_message}")
    sys.exit(1)

PHASES = [("Belégzés", "🌬️"), ("Tartsd bent", "⏸️"), ("Kilégzés", "😮‍💨"), ("Tartsd kint", "⏳")]

class BreathingApp:
    def __init__(self, master: ctk.CTk):
        self.master = master
        self.master.title("Box Légzésgyakorlat")

        window_width, window_height = 450, 530
        screen_width, screen_height = self.master.winfo_screenwidth(), self.master.winfo_screenheight()
        center_x, center_y = int(screen_width/2 - window_width / 2), int(screen_height/2 - window_height / 2)
        self.master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.master.resizable(False, False)

        self.is_running = False
        self.timer_id = None
        self.current_cycle = 0
        self.current_phase_index = 0
        self.time_left = 0
        self.topmost_var = tk.BooleanVar(value=False)
        self.sound_enabled_var = tk.BooleanVar(value=False)

        if not PHASES:
            messagebox.showerror("Konfigurációs Hiba", "A légzési fázisok (PHASES) listája üres!")
            self.master.after(100, self.master.destroy)
            return

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.create_widgets()

    def create_widgets(self):
        # A GUI elemek létrehozása változatlan
        self.master.grid_columnconfigure(0, weight=1)
        settings_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        settings_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        settings_frame.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkLabel(settings_frame, text="Ciklusok:", font=ctk.CTkFont(size=14)).grid(row=0, column=0, sticky='w')
        self.cycles_var = tk.IntVar(value=4)
        ctk.CTkLabel(settings_frame, textvariable=self.cycles_var, font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky='e', padx=10)
        self.cycles_slider = ctk.CTkSlider(settings_frame, from_=1, to=20, number_of_steps=19, variable=self.cycles_var)
        self.cycles_slider.grid(row=1, column=0, padx=(0, 10), pady=(5, 10), sticky="ew")
        ctk.CTkLabel(settings_frame, text="Időtartam (mp):", font=ctk.CTkFont(size=14)).grid(row=0, column=1, sticky='w', padx=(10, 0))
        self.duration_var = tk.IntVar(value=4)
        ctk.CTkLabel(settings_frame, textvariable=self.duration_var, font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=1, sticky='e', padx=10)
        self.duration_slider = ctk.CTkSlider(settings_frame, from_=2, to=10, number_of_steps=8, variable=self.duration_var)
        self.duration_slider.grid(row=1, column=1, padx=(10, 0), pady=(5, 10), sticky="ew")
        self.topmost_checkbox = ctk.CTkCheckBox(settings_frame, text="Mindig felül", variable=self.topmost_var, onvalue=True, offvalue=False, command=self.toggle_topmost, font=ctk.CTkFont(size=12))
        self.topmost_checkbox.grid(row=2, column=0, columnspan=2, pady=(10, 0), sticky="w")
        self.sound_switch = ctk.CTkSwitch(settings_frame, text="Hangjelzés", variable=self.sound_enabled_var, onvalue=True, offvalue=False, font=ctk.CTkFont(size=12))
        self.sound_switch.grid(row=3, column=0, columnspan=2, pady=(10, 0), sticky="w")
        if not SOUND_AVAILABLE:
            self.sound_switch.configure(state="disabled")
            ctk.CTkLabel(settings_frame, text="(Csak Windows rendszeren elérhető)", font=ctk.CTkFont(size=10)).grid(row=4, column=0, columnspan=2, sticky="w", padx=20)
        self.cycle_label = ctk.CTkLabel(self.master, text="Nyomj Start-ot az indításhoz!", font=ctk.CTkFont(size=18, weight="bold"))
        self.cycle_label.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="ew")
        self.status_label = ctk.CTkLabel(self.master, text="Készen állsz?", font=ctk.CTkFont(size=30))
        self.status_label.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.timer_label = ctk.CTkLabel(self.master, text="", font=ctk.CTkFont(size=96, weight="bold"), text_color="#5E81AC")
        self.timer_label.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        button_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        button_frame.grid(row=4, column=0, padx=20, pady=(20, 20), sticky="ew")
        button_frame.grid_columnconfigure((0, 1), weight=1)
        self.start_button = ctk.CTkButton(button_frame, text="Start", command=self.start_exercise, height=40, font=ctk.CTkFont(size=14, weight="bold"))
        self.start_button.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.stop_button = ctk.CTkButton(button_frame, text="Stop", command=self.stop_exercise, state="disabled", height=40, fg_color="#D08770", hover_color="#BF616A", font=ctk.CTkFont(size=14, weight="bold"))
        self.stop_button.grid(row=0, column=1, padx=(10, 0), sticky="ew")

    def toggle_topmost(self):
        self.master.attributes("-topmost", self.topmost_var.get())

    # --- ÚJ METÓDUS A HANG KÜLÖN SZÁLON VALÓ LEJÁTSZÁSÁHOZ ---
    def _play_sound_in_thread(self):
        """
        A hang lejátszása egy külön szálon, hogy a GUI soha ne fagyjon le.
        Ez a metódus a háttérben fut, és nem zavarja a visszaszámlálót.
        """
        try:
            # SND_MEMORY: a hangot a memóriából (a WAV_DATA változóból) játssza le
            # SND_NODEFAULT: ha a hangfájlunk hibás, ne játssza le a Windows alapértelmezett hangját
            winsound.PlaySound(WAV_DATA, winsound.SND_MEMORY | winsound.SND_NODEFAULT)
        except Exception as e:
            # Ha a háttérben hiba történik, az ne állítsa le a programot.
            # A hibakereséshez kiírhatjuk a konzolra.
            print(f"Hiba a hang lejátszása közben (a háttérben): {e}")

    def start_exercise(self):
        # ... (változatlan)
        if self.is_running: return
        self.is_running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.cycles_slider.configure(state="disabled")
        self.duration_slider.configure(state="disabled")
        self.topmost_checkbox.configure(state="disabled")
        self.sound_switch.configure(state="disabled")
        self.current_cycle, self.current_phase_index = 1, -1
        self.next_phase()

    def stop_exercise(self, interrupted=True):
        # ... (változatlan)
        if not self.is_running: return
        self.is_running = False
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None
        if interrupted:
            self.cycle_label.configure(text="⛔ Megszakítva")
            self.status_label.configure(text="A nyugalom erő. - Gemini")
        else:
            self.cycle_label.configure(text="✅ Befejezve")
            self.status_label.configure(text="Szép munka!")
        self.timer_label.configure(text="")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.cycles_slider.configure(state="normal")
        self.duration_slider.configure(state="normal")
        self.topmost_checkbox.configure(state="normal")
        if SOUND_AVAILABLE: self.sound_switch.configure(state="normal")

    def next_phase(self):
        # ... (változatlan)
        if not self.is_running: return
        self.current_phase_index += 1
        if self.current_phase_index >= len(PHASES):
            self.current_phase_index = 0
            self.current_cycle += 1
        total_cycles = self.cycles_var.get()
        if self.current_cycle > total_cycles:
            self.stop_exercise(interrupted=False)
            return
        phase_name, phase_emoji = PHASES[self.current_phase_index]
        self.cycle_label.configure(text=f"Ciklus {self.current_cycle}/{total_cycles}")
        self.status_label.configure(text=f"{phase_emoji} {phase_name}")
        self.time_left = self.duration_var.get()
        self.update_timer()

    def update_timer(self):
        if not self.is_running: return
        if self.time_left > 0:
            self.timer_label.configure(text=str(self.time_left))
            
            # --- JAVÍTOTT HANG LEJÁTSZÁS ---
            if self.sound_enabled_var.get() and SOUND_AVAILABLE:
                # Elindítjuk a hang lejátszását egy külön szálon.
                # A 'daemon=True' biztosítja, hogy a szál bezáródjon a főprogrammal együtt.
                sound_thread = Thread(target=self._play_sound_in_thread, daemon=True)
                sound_thread.start()

            # A program azonnal továbblép ide, nem vár a hang lejátszására.
            self.time_left -= 1
            self.timer_id = self.master.after(1000, self.update_timer)
        else:
            self.timer_label.configure(text="OK")
            self.timer_id = self.master.after(500, self.next_phase)

    def on_closing(self):
        # ... (változatlan)
        if self.is_running: self.stop_exercise(interrupted=False)
        if self.timer_id: self.master.after_cancel(self.timer_id)
        self.master.destroy()

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    app = BreathingApp(root)
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # ... (hibakezelő kód változatlan)
        error_title = "Váratlan Hiba"
        error_details = traceback.format_exc()
        error_message = ("Sajnáljuk, egy váratlan hiba történt a program futása közben.\n\n" f"Hiba típusa: {type(e).__name__}\n" f"Hiba üzenete: {e}\n\n" "Részletek (hibakereséshez):\n" f"{error_details}")
        try:
            root_err = tk.Tk()
            root_err.withdraw()
            messagebox.showerror(error_title, error_message)
        except tk.TclError:
            print(f"KRITIKUS HIBA: {error_title}\n{error_message}")
        sys.exit(1)
