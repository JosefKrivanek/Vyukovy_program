import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pedalboard as pd
from pedalboard.io import AudioFile
import numpy as np
import sounddevice as sd



def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;"), ("All Files", "*.*")])  # Otevře dialog pro výběr souboru
    if file_path:  # Pokud byl vybrán soubor
        print(f"Načtený soubor: {file_path}")  # Debug výpis
        global loaded_file
        loaded_file = file_path  # Uložení cesty k souboru do globální proměnné

        # Získání pouze názvu souboru (bez cesty)
        file_name = os.path.basename(file_path)

def play_audio():
    if loaded_file:
        with AudioFile("output.wav") as f:
            audio = f.read(f.frames)  # Načte celé audio
            samplerate = f.samplerate
            channels = f.num_channels

    if channels == 1:
        audio = np.squeeze(audio)  # Odstranění zbytečných dimenzí
    elif channels == 2:
        audio = np.column_stack(audio)

        # Přehrání zvuku
        sd.play(audio, samplerate)

board = pd.Pedalboard([])

def process_audio():
    if loaded_file:
        with AudioFile(loaded_file) as f:  # Otevřeme soubor pro čtení
            print(f"Soubor '{loaded_file}' má {f.samplerate} Hz a {f.num_channels} kanálů")
            audio = f.read(f.frames)  # Načteme celý soubor
            
        # 🛠️ Zpracujeme audio efekty
        effected = board(audio, f.samplerate, reset=False)

        # Uložíme výstup
        with AudioFile('output.wav', 'w', f.samplerate, f.num_channels) as o:
            o.write(effected)
        print("✅ Export dokončen: output.wav")



def test_boardu ():
    print(f"Pedal board právě obsahuje: {board}")   #debug
        


#   Zobrazování framu na efekty   #
def on_tab_change(event):
    current_tab = hl_menu.index(hl_menu.select())  
    if current_tab in [0]:  
        effects_frame.pack_forget()
    else:  
        effects_frame.pack(anchor="s")  


                                    #  Přidání chorus do boardu #
def add_chorus():
    global chorus_frame, slider_rate, chorus_effect

    if "chorus_frame" not in globals():
        chorus_frame = tk.LabelFrame(effects_frame, text="Chorus")
        chorus_frame.pack(side="left")
        slider_rate = tk.Scale(chorus_frame, from_=100, to=0, label="Rate", command=lambda x: update_chorus())
        slider_rate.pack()

    if chorus_var.get() == 1:
        chorus_frame.pack(side="left")
        rate_chorus = int(slider_rate.get())
        chorus_effect = pd.Chorus(rate_hz=rate_chorus, depth=0, feedback=0)

        for effect in list(board):  # Použijeme kopii boardu, aby bylo bezpečné ho upravovat
            if isinstance(effect, pd.Chorus):
                board.remove(effect)  # Odebrání existujícího Chorus efektu

        board.append(chorus_effect)  # Přidání nového chorus efektu
    else:
        chorus_frame.pack_forget()
        # ❌ odebrání efektu
        for effect in list(board):  
            if isinstance(effect, pd.Chorus):
                board.remove(effect)  # Odstranění chorus efektu

    print(f"Pedalboard: {board}")  # Debug 

def update_chorus():
    global chorus_effect

    if chorus_effect in board:
        rate_chorus = int(slider_rate.get())
        chorus_effect.rate_hz = rate_chorus  # Aktualizace hodnoty chorus efektu
        print(f"🎚️ Aktualizován chorus efekt: rate_hz={rate_chorus}")  # Debug


                                    #  Přidání compressor do boardu #
def add_compressor():
    global Compressor_frame, slider_threshold, Compressor_effect

    if "Compressor_frame" not in globals():
        Compressor_frame = tk.LabelFrame(effects_frame, text="Compressor")
        Compressor_frame.pack(side="left")
        slider_threshold = tk.Scale(Compressor_frame, from_=100, to=0, label="Threshold", command=lambda x: update_Compressor())
        slider_threshold.pack()
    if compressor_var.get() == 1:
        Compressor_frame.pack(side="left")
        threshold_db_Compressor = int(slider_threshold.get())
        Compressor_effect = pd.Compressor(threshold_db=threshold_db_Compressor)
        for effect in list(board):  # Použijeme kopii boardu, aby bylo bezpečné ho upravovat
            if isinstance(effect, pd.Compressor):
                board.remove(effect)  # Odebrání existujícího Compressor efektu
        board.append(Compressor_effect)  # Přidání nového Compressor efektu
    else:
        Compressor_frame.pack_forget()
        for effect in list(board):  
            if isinstance(effect, pd.Compressor):
                board.remove(effect)  # Odstranění Compressor efektu
    print(f"Pedalboard: {board}")  # Debug výpis

def update_Compressor():
    global Compressor_effect
    if Compressor_effect in board:
        threshold_db_Compressor = int(slider_threshold.get())
        Compressor_effect.threshold_db = threshold_db_Compressor  # Aktualizace hodnoty Compressor efektu
        print(f"🎚️ Aktualizován Compressor efekt: rate_hz={threshold_db_Compressor}")  # Debug



                                    #  Přidání delay do boardu #
def add_delay():
    global Delay_frame, slider_s, Delay_effect

    if "Delay_frame" not in globals():
        Delay_frame = tk.LabelFrame(effects_frame, text="Delay")
        Delay_frame.pack(side="left")
        slider_s = tk.Scale(Delay_frame, from_=100, to=0, label="Threshold", command=lambda x: update_Delay())
        slider_s.pack()
    if delay_var.get() == 1:
        Delay_frame.pack(side="left")
        delay_in_seconds = int(slider_s.get())
        Delay_effect = pd.Delay(delay_seconds=delay_in_seconds)
        for effect in list(board):  # Použijeme kopii boardu, aby bylo bezpečné ho upravovat
            if isinstance(effect, pd.Delay):
                board.remove(effect)  # Odebrání existujícího Delay efektu
        board.append(Delay_effect)  # Přidání nového Delay efektu
    else:
        Delay_frame.pack_forget()
        for effect in list(board):  
            if isinstance(effect, pd.Delay):
                board.remove(effect)  # Odstranění Delay efektu
    print(f"Pedalboard: {board}")  # Debug výpis

def update_Delay():
    global Delay_effect
    if Delay_effect in board:
        delay_in_seconds = int(slider_s.get())
        Delay_effect.delay_seconds = delay_in_seconds  # Aktualizace hodnoty Delay efektu
        print(f"🎚️ Aktualizován Delay efekt: rate_hz={delay_in_seconds}")  # Debug



                                    #  Přidání distortion do boardu #
def add_distortion():
    global Distortion_frame, slider1, Distortion_effect

    if "Distortion_frame" not in globals():
        Distortion_frame = tk.LabelFrame(effects_frame, text="Distortion")
        Distortion_frame.pack(side="left")
        slider1 = tk.Scale(Distortion_frame, from_=100, to=0, label="Threshold", command=lambda x: update_Distortion())
        slider1.pack()
    if distortion_var.get() == 1:
        Distortion_frame.pack(side="left")
        Distortion_in_seconds = int(slider1.get())
        Distortion_effect = pd.Distortion(drive_db=Distortion_in_seconds)
        for effect in list(board):  # Použijeme kopii boardu, aby bylo bezpečné ho upravovat
            if isinstance(effect, pd.Distortion):
                board.remove(effect)  # Odebrání existujícího Distortion efektu
        board.append(Distortion_effect)  # Přidání nového Distortion efektu
    else:
        Distortion_frame.pack_forget()
        for effect in list(board):  
            if isinstance(effect, pd.Distortion):
                board.remove(effect)  # Odstranění Distortion efektu
    print(f"Pedalboard: {board}")  # Debug výpis

def update_Distortion():
    global Distortion_effect
    if Distortion_effect in board:
        Distortion_in_seconds = int(slider1.get())
        Distortion_effect.drive_db = Distortion_in_seconds  # Aktualizace hodnoty Distortion efektu
        print(f"🎚️ Aktualizován Distortion efekt: rate_hz={Distortion_in_seconds}")  # Debug

                                   #  Přidání Gain do boardu #
def add_Gain():
    global Gain_frame, slider_gai, Gain_effect

    if "Gain_frame" not in globals():
        Gain_frame = tk.LabelFrame(effects_frame, text="Gain")
        Gain_frame.pack(side="left")
        slider_gai = tk.Scale(Gain_frame, from_=100, to=0, label="Gain dB", command=lambda x: update_Gain())
        slider_gai.pack()
    if gain_var.get() == 1:
        Gain_frame.pack(side="left")
        Gain_in_dB = int(slider_gai.get())
        Gain_effect = pd.Gain(gain_db=Gain_in_dB)
        for effect in list(board):  
            if isinstance(effect, pd.Gain):
                board.remove(effect)  
        board.append(Gain_effect)  
    else:
        Gain_frame.pack_forget()
        for effect in list(board):  
            if isinstance(effect, pd.Gain):
                board.remove(effect)  
    print(f"Pedalboard: {board}")  

def update_Gain():
    global Gain_effect
    if Gain_effect in board:
        Gain_in_dB = int(slider_gai.get())
        Gain_effect.gain_db = Gain_in_dB  
        print(f"🎚️ Aktualizován Gain efekt: dB={Gain_in_dB}")



                                    #  Přidání Reverb do boardu #
def add_Reverb():
    global Reverb_frame, slider_room, Reverb_effect

    if "Reverb_frame" not in globals():
        Reverb_frame = tk.LabelFrame(effects_frame, text="Reverb")
        Reverb_frame.pack(side="left")
        slider_room = tk.Scale(Reverb_frame, from_=100, to=0, label="Reverb", command=lambda x: update_Reverb())
        slider_room.pack()
    if reverb_var.get() == 1:
        Reverb_frame.pack(side="left")
        Reverb_room_size = int(slider_room.get())
        Reverb_effect = pd.Reverb(room_size=Reverb_room_size)
        for effect in list(board):  
            if isinstance(effect, pd.Reverb):
                board.remove(effect)  
        board.append(Reverb_effect)  
    else:
        Reverb_frame.pack_forget()
        for effect in list(board):  
            if isinstance(effect, pd.Reverb):
                board.remove(effect)  
    print(f"Pedalboard: {board}")  

def update_Reverb():
    global Reverb_effect
    if Reverb_effect in board:
        Reverb_room_size = int(slider_room.get())
        Reverb_effect.room_size = Reverb_room_size/100  
        print(f"🎚️ Aktualizován Reverb efekt: room size={Reverb_room_size}")



#   Hlavní okno   #
root = tk.Tk()
root.title("AudioApp v2")
root.minsize(1080,600)

#   Effects bar ##
effects_frame = tk.LabelFrame(root, relief="sunken", height=100, width=620)
effects_frame.pack(anchor="s", fill="x")


#   Karty   #
hl_menu = ttk.Notebook(root)
hl_menu.pack(expand=True, fill="both")

karta_soubor = ttk.Frame(hl_menu)
karta_prehled = ttk.Frame(hl_menu)
karta_efekty = ttk.Frame(hl_menu)

hl_menu.add(karta_soubor, text="Soubor")
hl_menu.add(karta_prehled, text="Přehled")
hl_menu.add(karta_efekty, text="Efekty")


##  Soubor  ##
load_btn = tk.Button(karta_soubor, text="Load", command=load_file)
load_btn.pack()

save_btn = tk.Button(karta_soubor, text="Save", command=process_audio)
save_btn.pack()

help_btn = tk.Button(karta_soubor, text="help", command=play_audio)
help_btn.pack()

def ooooo():
    process_audio()
    play_audio()

##  Přehled  ##
play_btn = tk.Button(karta_prehled, text="Play", command=ooooo)
play_btn.grid(row=1, column=1)

stop_btn = tk.Button(karta_prehled, text="Stop", command=1)
stop_btn.grid(row=1, column=2)

visual_frame = tk.LabelFrame(karta_prehled, relief="sunken", height=100, width=620)
visual_frame.grid(row=2, column=1, columnspan=2)



##  Efekty  ##

chorus_var = tk.IntVar()
chorus_var.set(0)
chorus_btn = tk.Checkbutton(karta_efekty, text="Chorus", variable=chorus_var, command=add_chorus)
chorus_btn.grid(row=1, column=1)

compressor_var = tk.IntVar()
compressor_var.set(0)
compressor_btn = tk.Checkbutton(karta_efekty, text="compressor", variable=compressor_var, command=add_compressor)
compressor_btn.grid(row=1, column=2)

delay_var = tk.IntVar()
delay_var.set(0)
delay_btn = tk.Checkbutton(karta_efekty, text="delay", variable=delay_var, command=add_delay)
delay_btn.grid(row=1, column=3)

distortion_var = tk.IntVar()
distortion_var.set(0)
distortion_btn = tk.Checkbutton(karta_efekty, text="distortion", variable=distortion_var, command=add_distortion)
distortion_btn.grid(row=1, column=4)

gain_var = tk.IntVar()
gain_var.set(0)
gain_btn = tk.Checkbutton(karta_efekty, text="gain", variable=gain_var, command=add_Gain)
gain_btn.grid(row=1, column=5)

reverb_var = tk.IntVar()
reverb_var.set(0)
reverb_btn = tk.Checkbutton(karta_efekty, text="reverb", variable=reverb_var, command=add_Reverb)
reverb_btn.grid(row=1, column=6)


hl_menu.bind("<<NotebookTabChanged>>", on_tab_change)


root.mainloop()


