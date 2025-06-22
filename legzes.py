# -*- coding: utf-8 -*-

import sys
import tkinter as tk
from tkinter import messagebox
import traceback

#by lowkeyrenato

# --- 1. Hibaellenőrzés: Függőség (customtkinter) megléte ---
try:
    import customtkinter as ctk
except ImportError:
    # Ha a customtkinter nincs telepítve, barátságos üzenetet adunk és kilépünk.
    error_title = "Hiányzó Könyvtár"
    error_message = (
        "A program futtatásához szükséges 'customtkinter' könyvtár nincs telepítve.\n\n"
        "Kérjük, telepítsd a következő paranccsal egy parancssorban:\n\n"
        "pip install customtkinter"
    )
    # Próbálunk egy egyszerű tkinter ablakot létrehozni az üzenetnek.
    try:
        root = tk.Tk()
        root.withdraw()  # A fő ablakot elrejtjük
        messagebox.showerror(error_title, error_message)
    except tk.TclError:
        # Ha még a tkinter sem érhető el (nagyon ritka), a konzolra írunk.
        print(f"HIBA: {error_title}\n{error_message}")
    sys.exit(1) # Kilépés hibakóddal


# --- Konstansok ---
# Fázisok definíciója: (Név, Emoji)
PHASES = [
    ("Belégzés", "🌬️"),
    ("Tartsd bent", "⏸️"),
    ("Kilégzés", "😮‍💨"),
    ("Tartsd kint", "⏳")
]

# --- Alkalmazás osztály ---

class BreathingApp:
    """
    A Box Légzésgyakorlat alkalmazás fő osztálya, amely a GUI-t és a logikát kezeli.
    """
    def __init__(self, master: ctk.CTk):
        """Az alkalmazás inicializálása, a GUI elemek létrehozása és eseménykezelők beállítása."""
        self.master = master
        self.master.title("Box Légzésgyakorlat")

        # Ablak középre helyezése
        window_width = 450
        window_height = 450
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.master.resizable(False, False)

        # Állapotváltozók
        self.is_running = False
        self.timer_id = None
        self.current_cycle = 0
        self.current_phase_index = 0
        self.time_left = 0
        
        # --- 2. Hibaellenőrzés: Belső logikai ellenőrzés ---
        if not PHASES:
            messagebox.showerror("Konfigurációs Hiba", "A légzési fázisok (PHASES) listája üres!")
            self.master.after(100, self.master.destroy) # Azonnali kilépés
            return

        # --- 3. Hibaellenőrzés: Ablak bezárásának biztonságos kezelése ---
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # GUI elemek létrehozása
        self.create_widgets()

    def create_widgets(self):
        """A GUI elemek (widgetek) létrehozása és elrendezése az ablakban."""
        self.master.grid_columnconfigure(0, weight=1)

        # Beállítások keret
        settings_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        settings_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        settings_frame.grid_columnconfigure((0, 1), weight=1)

        # Ciklusok beállítása
        ctk.CTkLabel(settings_frame, text="Ciklusok:", font=ctk.CTkFont(size=14)).grid(row=0, column=0, sticky='w')
        self.cycles_var = tk.IntVar(value=4)
        ctk.CTkLabel(settings_frame, textvariable=self.cycles_var, font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=0, sticky='e', padx=10)
        self.cycles_slider = ctk.CTkSlider(settings_frame, from_=1, to=20, number_of_steps=19, variable=self.cycles_var)
        self.cycles_slider.grid(row=1, column=0, padx=(0, 10), pady=(5, 15), sticky="ew")
        
        # Időtartam beállítása
        ctk.CTkLabel(settings_frame, text="Időtartam (mp):", font=ctk.CTkFont(size=14)).grid(row=0, column=1, sticky='w', padx=(10, 0))
        self.duration_var = tk.IntVar(value=4)
        ctk.CTkLabel(settings_frame, textvariable=self.duration_var, font=ctk.CTkFont(size=14, weight="bold")).grid(row=0, column=1, sticky='e', padx=10)
        self.duration_slider = ctk.CTkSlider(settings_frame, from_=2, to=10, number_of_steps=8, variable=self.duration_var)
        self.duration_slider.grid(row=1, column=1, padx=(10, 0), pady=(5, 15), sticky="ew")

        # Kijelzők
        self.cycle_label = ctk.CTkLabel(self.master, text="Nyomj Start-ot az indításhoz!", font=ctk.CTkFont(size=18, weight="bold"))
        self.cycle_label.grid(row=1, column=0, padx=20, pady=(10, 5), sticky="ew")

        self.status_label = ctk.CTkLabel(self.master, text="Készen állsz?", font=ctk.CTkFont(size=30))
        self.status_label.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.timer_label = ctk.CTkLabel(self.master, text="", font=ctk.CTkFont(size=96, weight="bold"), text_color="#5E81AC") # Nord-kék
        self.timer_label.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        # Gombok
        button_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        button_frame.grid(row=4, column=0, padx=20, pady=(20, 20), sticky="ew")
        button_frame.grid_columnconfigure((0, 1), weight=1)

        self.start_button = ctk.CTkButton(button_frame, text="Start", command=self.start_exercise, height=40, font=ctk.CTkFont(size=14, weight="bold"))
        self.start_button.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.stop_button = ctk.CTkButton(button_frame, text="Stop", command=self.stop_exercise, state="disabled", height=40, fg_color="#D08770", hover_color="#BF616A", font=ctk.CTkFont(size=14, weight="bold"))
        self.stop_button.grid(row=0, column=1, padx=(10, 0), sticky="ew")

    def start_exercise(self):
        """A légzésgyakorlat indítása, a vezérlők letiltása."""
        if self.is_running: return
        self.is_running = True
        
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.cycles_slider.configure(state="disabled")
        self.duration_slider.configure(state="disabled")
        
        self.current_cycle = 1
        self.current_phase_index = -1
        self.next_phase()

    def stop_exercise(self, interrupted=True):
        """A légzésgyakorlat leállítása, a vezérlők engedélyezése."""
        if not self.is_running: return
        self.is_running = False
        
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            self.timer_id = None
            
        if interrupted:
            self.cycle_label.configure(text="⛔ Megszakítva")
            self.status_label.configure(text="A nyugalom erő.")
        else:
            self.cycle_label.configure(text="✅ Befejezve")
            self.status_label.configure(text="Szép munka!")
            
        self.timer_label.configure(text="")
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.cycles_slider.configure(state="normal")
        self.duration_slider.configure(state="normal")
    
    def next_phase(self):
        """A következő légzési fázisra lépés és a kijelzők frissítése."""
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
        """A visszaszámláló frissítése másodpercenként a 'root.after' segítségével."""
        if not self.is_running: return

        if self.time_left > 0:
            self.timer_label.configure(text=str(self.time_left))
            self.time_left -= 1
            self.timer_id = self.master.after(1000, self.update_timer)
        else:
            self.timer_label.configure(text="OK")
            self.timer_id = self.master.after(500, self.next_phase)

    def on_closing(self):
        """Biztonságos kilépési protokoll, ami leállítja az időzítőt bezárás előtt."""
        if self.is_running:
            self.stop_exercise(interrupted=False) # Állítsuk le a gyakorlatot
        
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
            
        self.master.destroy()

# --- Fő program ---
def main():
    """A fő belépési pont, ami beállítja a témát és elindítja az alkalmazást."""
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    app = BreathingApp(root)
    root.mainloop()

if __name__ == "__main__":
    # --- 4. Hibaellenőrzés: Általános, mindent elkapó hibakezelő ---
    try:
        main()
    except Exception as e:
        # Ha bármilyen váratlan hiba történik, ezt egy ablakban jelezzük.
        error_title = "Váratlan Hiba"
        # A traceback segít a hiba pontos helyének megtalálásában.
        error_details = traceback.format_exc()
        error_message = (
            "Sajnáljuk, egy váratlan hiba történt a program futása közben.\n\n"
            f"Hiba típusa: {type(e).__name__}\n"
            f"Hiba üzenete: {e}\n\n"
            "Részletek (hibakereséshez):\n"
            f"{error_details}"
        )
        # Próbálunk egy hibaablakot mutatni.
        try:
            root_err = tk.Tk()
            root_err.withdraw()
            messagebox.showerror(error_title, error_message)
        except tk.TclError:
            # Végső esetben a konzolra írunk.
            print(f"KRITIKUS HIBA: {error_title}\n{error_message}")
        sys.exit(1)
