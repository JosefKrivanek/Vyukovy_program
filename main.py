import os       # načítání a ukládání audia
import tkinter as tk    #GUI
from tkinter import ttk 
from tkinter import filedialog
import pedalboard as pd # efekty na audio
from pedalboard.io import AudioFile
import sounddevice as sd    #pčehrávání audia
import numpy as np  #práce s čísly
import matplotlib.pyplot as plt #vorba grafu
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    ## Barvy do stylů ##
BG_COLOR = "#1e1e1e"  # tmavá šedá pro pozadí
BTN_BG = "#3e3e3e"  # tmavá šedá pro tlačítka
BTN_FG = "#f5a623"  # oranžová pro text na tlačítkách
CHECK_FG = "#f5a623"  # oranžová pro text u checkboxů
GRAPH_COLOR = "#f5a623"  # oranžová pro křivky grafu

    ## Globální proměnné ##
loaded_file = None
waveform_canvas = None
board = pd.Pedalboard([])

    ## process audia ##
def process_audio():
    if loaded_file:
        with AudioFile(loaded_file) as f:  # Otevřeme soubor pro čtení
            print(f"Soubor '{loaded_file}' má {f.samplerate} Hz a {f.num_channels} kanálů") #debug
            audio = f.read(f.frames)  # Načteme celý soubor
            
        
        effected = board(audio, f.samplerate, reset=False)  # Zpracujeme audio efekty

        # Uložíme výstup
        with AudioFile('output.wav', 'w', f.samplerate, f.num_channels) as o:
            o.write(effected)   # Upraví audio podle boardu
        print(" Export dokončen: output.wav")   #debug
        plot_waveform("output.wav") # Aktualizace grafu
        
    ## Nahrání souboru ##
def load_file():
    global loaded_file
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav"), ("All Files", "*.*")])
    if file_path:
        print(f"Načtený soubor: {file_path}")   #debug
        loaded_file = file_path
        plot_waveform(loaded_file)  # Aktualizace grafu
        switch_tab()    # Přepne na kartu přehled

    ## Export a uložení audia ##
def save_audio():
    output_file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav"), ("All Files", "*.*")],title="Uložit jako")

    if output_file_path:  # Pokud uživatel zvolil cestu
        if loaded_file:  # Pokud je soubor načtený
            with AudioFile(loaded_file) as f:
                audio_data = f.read(f.frames)  # Načte všechny snímky zvuku
                processed_audio = board(audio_data, f.samplerate, reset=False)  # Aplikuje efekty na audio

                # Uložení upraveného zvuku do vybrané cesty
                with AudioFile(output_file_path, 'w', f.samplerate, f.num_channels) as o:
                    o.write(processed_audio)  # Uložení do souboru
                print(f"Upravené audio bylo uloženo do: {output_file_path}")

    ## Grafické zobrazení audia ##
def plot_waveform(output_file_path, max_samples=10_000, chunk_size=1024):
    global waveform_canvas

    with AudioFile(output_file_path) as f:
        samplerate = f.samplerate / 1000  # Vzorkování
        total_frames = f.frames # Délka audia
        num_channels = f.num_channels   # Mono/Stereo
        step = max(1, total_frames // max_samples) #Velikost kroku
        samples = []
        # Načte celé audio po chunk_size
        for _ in range(0, total_frames, chunk_size):
            audio_chunk = f.read(chunk_size)
            if audio_chunk is None:
                break
            if num_channels > 1:
                audio_chunk = np.mean(audio_chunk, axis=0)

            samples.append(audio_chunk[::step]) # Přidáme jen každý n-tý vzorek
        audio_data = np.concatenate(samples, axis=0) if samples else np.array([])   # 
    time = np.linspace(0, len(audio_data) * step / samplerate, num=len(audio_data)) # Čas naose x

    # Zničíme starý graf, pokud existuje
    if waveform_canvas is not None:
        waveform_canvas.get_tk_widget().destroy()
        waveform_canvas = None

    #  Nový graf
    fig = Figure(figsize=(6, 2), dpi=150)
    ax = fig.add_subplot(111)
    ax.plot(time, audio_data, color=GRAPH_COLOR, linewidth=0.8)

    waveform_canvas = FigureCanvasTkAgg(fig, master=visual_frame)
    waveform_canvas.get_tk_widget().pack(fill="x", expand=True)
    waveform_canvas.draw()

    ## Přehrávání audia ##
def play_audio():
    if loaded_file:
        with AudioFile("output.wav") as f:
            audio = f.read(f.frames)  # Načte celé audio
            samplerate = f.samplerate   # Vzorkování
            channels = f.num_channels   # Mono/Stereo
    # Komrese stereo na mono
    if channels == 1:
        audio = np.squeeze(audio)
    elif channels == 2:
        audio = np.column_stack(audio)
        sd.play(audio, samplerate)  # Přehrání zvuku

    ## Zastavení audia
def stop_audio():
    sd.stop()

def test_boardu ():
    print(f"Pedal board právě obsahuje: {board}")   #debug        
    ## Přepnutí na kartu přehled
def switch_tab():
    hl_menu.select(karta_prehled)

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
        chorus_frame = tk.LabelFrame(effects_frame, text="Chorus", bg=BG_COLOR, fg=BTN_FG)  # Frame na chorus efekt
        chorus_frame.pack(side="left")  # Vytvoření framu
        slider_rate = tk.Scale(chorus_frame, from_=15, to=0, resolution=0.5, label="Rate", command=lambda x: update_chorus(), bg=BG_COLOR, fg=BTN_FG) # Slider na efekt
        slider_rate.pack()  # Zobrazení slideru

    if chorus_var.get() == 1:   # Pokud stlačíme chorus btn
        chorus_frame.pack(side="left") # Zobrazení frame chorus
        rate_chorus = int(slider_rate.get())    # Získání hodnoty slideru
        chorus_effect = pd.Chorus(rate_hz=rate_chorus, depth=0, feedback=0) # Upravení hodnot chorus efektu

        for effect in list(board):  # Použijeme kopii boardu, aby bylo bezpečné ho upravovat
            if isinstance(effect, pd.Chorus): # Když najde efekt, který patří Chorusu
                board.remove(effect)  # Odebrání Chorus efektu
        board.append(chorus_effect)  # Přidání nového chorus efektu
    else:
        chorus_frame.pack_forget()
        # odebrání efektu
        for effect in list(board):  
            if isinstance(effect, pd.Chorus):
                board.remove(effect)  # Odstranění chorus efektu

    print(f"Pedalboard: {board}")  # Debug 

def update_chorus():
    global chorus_effect
    if chorus_effect in board: # Když je chorus v boardu
        rate_chorus = int(slider_rate.get())    # Zíkání hodnoty slideru
        chorus_effect.rate_hz = rate_chorus  # Aktualizace hodnoty chorus efektu
        print(f" Aktualizován chorus efekt: rate_hz={rate_chorus}")  # Debug


                                    #  Přidání compressor do boardu #
def add_compressor():
    global Compressor_frame, slider_threshold, Compressor_effect

    if "Compressor_frame" not in globals():
        Compressor_frame = tk.LabelFrame(effects_frame, text="Compressor", bg=BG_COLOR, fg=BTN_FG)
        Compressor_frame.pack(side="left")
        slider_threshold = tk.Scale(Compressor_frame, from_=6, to=-30, label="Threshold dB", command=lambda x: update_Compressor(), bg=BG_COLOR, fg=BTN_FG)
        slider_threshold.pack()
    if compressor_var.get() == 1:
        Compressor_frame.pack(side="left")
        threshold_db_Compressor = int(slider_threshold.get())
        Compressor_effect = pd.Compressor(threshold_db=threshold_db_Compressor)
        for effect in list(board): 
            if isinstance(effect, pd.Compressor):
                board.remove(effect)
        board.append(Compressor_effect)  
    else:
        Compressor_frame.pack_forget()
        for effect in list(board):  
            if isinstance(effect, pd.Compressor):
                board.remove(effect)  
    print(f"Pedalboard: {board}")  

def update_Compressor():
    global Compressor_effect
    if Compressor_effect in board:
        threshold_db_Compressor = int(slider_threshold.get())
        Compressor_effect.threshold_db = threshold_db_Compressor  
        print(f" Aktualizován Compressor efekt: threshold dB={threshold_db_Compressor}")  



                                    #  Přidání delay do boardu #
def add_delay():
    global Delay_frame, slider_s, Delay_effect

    if "Delay_frame" not in globals():
        Delay_frame = tk.LabelFrame(effects_frame, text="Delay", bg=BG_COLOR, fg=BTN_FG)
        Delay_frame.pack(side="left")
        slider_s = tk.Scale(Delay_frame, from_=30, to=0,resolution=0.2, label="Delay ms", command=lambda x: update_Delay(), bg=BG_COLOR, fg=BTN_FG)
        slider_s.pack()
    if delay_var.get() == 1:
        Delay_frame.pack(side="left")
        delay_in_seconds = int(slider_s.get())
        Delay_effect = pd.Delay(delay_seconds=delay_in_seconds)
        for effect in list(board):  
            if isinstance(effect, pd.Delay):
                board.remove(effect)  
        board.append(Delay_effect)  
    else:
        Delay_frame.pack_forget()
        for effect in list(board):  
            if isinstance(effect, pd.Delay):
                board.remove(effect)  
    print(f"Pedalboard: {board}")  

def update_Delay():
    global Delay_effect
    if Delay_effect in board:
        delay_in_seconds = int(slider_s.get())
        Delay_effect.delay_seconds = delay_in_seconds  
        print(f" Aktualizován Delay efekt: delay ms={delay_in_seconds}")  



                                    #  Přidání distortion do boardu #
def add_distortion():
    global Distortion_frame, slider_dis, Distortion_effect

    if "Distortion_frame" not in globals():
        Distortion_frame = tk.LabelFrame(effects_frame, text="Distortion", bg=BG_COLOR, fg=BTN_FG)
        Distortion_frame.pack(side="left")
        slider_dis = tk.Scale(Distortion_frame, from_=30, to=0, resolution=0.5, label="Drive dB", command=lambda x: update_Distortion(), bg=BG_COLOR, fg=BTN_FG)
        slider_dis.pack()
    if distortion_var.get() == 1:
        Distortion_frame.pack(side="left")
        Distortion_in_seconds = int(slider_dis.get())
        Distortion_effect = pd.Distortion(drive_db=Distortion_in_seconds)
        for effect in list(board):  
            if isinstance(effect, pd.Distortion):
                board.remove(effect)  
        board.append(Distortion_effect)  
    else:
        Distortion_frame.pack_forget()
        for effect in list(board):  
            if isinstance(effect, pd.Distortion):
                board.remove(effect)  
    print(f"Pedalboard: {board}")  

def update_Distortion():
    global Distortion_effect
    if Distortion_effect in board:
        Distortion_in_seconds = int(slider_dis.get())
        Distortion_effect.drive_db = Distortion_in_seconds  
        print(f" Aktualizován Distortion efekt: drive dB={Distortion_in_seconds}")  



                                    #  Přidání Gain do boardu #
def add_Gain():
    global Gain_frame, slider_gai, Gain_effect

    if "Gain_frame" not in globals():
        Gain_frame = tk.LabelFrame(effects_frame, text="Gain", bg=BG_COLOR, fg=BTN_FG)
        Gain_frame.pack(side="left")
        slider_gai = tk.Scale(Gain_frame, from_=30, to=0, resolution=0.5, label="Gain dB", command=lambda x: update_Gain(), bg=BG_COLOR, fg=BTN_FG)
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
        print(f" Aktualizován Gain efekt: dB={Gain_in_dB}")



                                    #  Přidání Reverb do boardu #
def add_Reverb():
    global Reverb_frame, slider_room, Reverb_effect

    if "Reverb_frame" not in globals():
        Reverb_frame = tk.LabelFrame(effects_frame, text="Reverb", bg=BG_COLOR, fg=BTN_FG)
        Reverb_frame.pack(side="left")
        slider_room = tk.Scale(Reverb_frame, from_=100, to=0, label="Room size", command=lambda x: update_Reverb(), bg=BG_COLOR, fg=BTN_FG)
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
        print(f" Aktualizován Reverb efekt: room size={Reverb_room_size}")



#   Hlavní okno   #
root = tk.Tk()
root.title("AudioApp v2")
root.minsize(900,450)
root.maxsize(900,600)
root.configure(bg=BG_COLOR)

# Nastavení ttk stylu pro barevné schéma
style = ttk.Style()
style.configure("TFrame", background=BG_COLOR)
style.configure("TButton", background=BTN_BG, foreground=BTN_FG)
style.configure("TCheckbutton", background=BG_COLOR, foreground=CHECK_FG)

#   Effects bar #
effects_frame = tk.LabelFrame(root, relief="sunken", height=100, width=620, bg=BG_COLOR, fg=BTN_FG)
effects_frame.pack(anchor="s", fill="x")


#   Karty   #
hl_menu = ttk.Notebook(root)
hl_menu.pack(expand=True, fill="both")

karta_soubor = ttk.Frame(hl_menu, style="TFrame")
karta_prehled = ttk.Frame(hl_menu, style="TFrame")
karta_efekty = ttk.Frame(hl_menu, style="TFrame")

hl_menu.add(karta_soubor, text="Soubor")
hl_menu.add(karta_prehled, text="Přehled")
hl_menu.add(karta_efekty, text="Efekty")


##  Soubor  ##
load_btn = tk.Button(karta_soubor, text="Load",font=("Bahnschrift", 12,"bold"), padx=5, pady=5, bd=8, command=load_file, bg=BTN_BG, fg=BTN_FG)
load_btn.pack(pady=10)

save_btn = tk.Button(karta_soubor, text="Save",font=("Bahnschrift", 12,"bold"), padx=5, pady=5, bd=8, command=save_audio, bg=BTN_BG, fg=BTN_FG)
save_btn.pack( pady=10)

#help_btn = tk.Button(karta_soubor, text="help",font=("Bahnschrift", 12,"bold"), padx=5, pady=5, bd=8, command=1, bg=BTN_BG, fg=BTN_FG)
#help_btn.pack( pady=10)

##  Přehled  ##
play_btn = tk.Button(karta_prehled, text="Play",font=("Bahnschrift", 12,"bold"), padx=5, pady=5, bd=8, command=lambda: (process_audio(), play_audio()), bg=BTN_BG, fg=BTN_FG)
play_btn.grid(row=1, column=1)

stop_btn = tk.Button(karta_prehled, text="Stop",font=("Bahnschrift", 12,"bold"), padx=5, pady=5, bd=8, command=stop_audio, bg=BTN_BG, fg=BTN_FG)
stop_btn.grid(row=1, column=2)

visual_frame = tk.LabelFrame(karta_prehled, relief="sunken",  bg=BG_COLOR)
visual_frame.grid(row=3, column=1, columnspan=2)



##  Efekty  ##

chorus_var = tk.IntVar()
chorus_var.set(0)
chorus_btn = tk.Checkbutton(karta_efekty, text="Chorus", font=("Bahnschrift", 12,"bold"), padx=5, pady=5, bd=8, variable=chorus_var, command=add_chorus, bg=BG_COLOR, fg=CHECK_FG)
chorus_btn.grid(row=1, column=1)

compressor_var = tk.IntVar()
compressor_var.set(0)
compressor_btn = tk.Checkbutton(karta_efekty, text="Compressor", font=("Bahnschrift", 12,"bold"), padx=5, pady=5, bd=8, variable=compressor_var, command=add_compressor, bg=BG_COLOR, fg=CHECK_FG)
compressor_btn.grid(row=1, column=2)

delay_var = tk.IntVar()
delay_var.set(0)
delay_btn = tk.Checkbutton(karta_efekty, text="Delay", font=("Bahnschrift", 12,"bold"), padx=5, pady=5, bd=8, variable=delay_var, command=add_delay, bg=BG_COLOR, fg=CHECK_FG)
delay_btn.grid(row=1, column=3)

distortion_var = tk.IntVar()
distortion_var.set(0)
distortion_btn = tk.Checkbutton(karta_efekty, text="Distortion", font=("Bahnschrift", 12,"bold"), padx=5, pady=5, bd=8, variable=distortion_var, command=add_distortion, bg=BG_COLOR, fg=CHECK_FG)
distortion_btn.grid(row=1, column=4)

gain_var = tk.IntVar()
gain_var.set(0)
gain_btn = tk.Checkbutton(karta_efekty, text="Gain", font=("Bahnschrift", 12,"bold"), padx=5, pady=5, bd=8, variable=gain_var, command=add_Gain, bg=BG_COLOR, fg=CHECK_FG)
gain_btn.grid(row=1, column=5)

reverb_var = tk.IntVar()
reverb_var.set(0)
reverb_btn = tk.Checkbutton(karta_efekty, text="Reverb", font=("Bahnschrift", 12,"bold"), padx=5, pady=5, bd=8, variable=reverb_var, command=add_Reverb, bg=BG_COLOR, fg=CHECK_FG)
reverb_btn.grid(row=1, column=6)

hl_menu.bind("<<NotebookTabChanged>>", on_tab_change)

root.mainloop()