import tkinter as tk
from tkinter import ttk
import pedalboard as pd
from pedalboard.io import AudioFile


board = pd.Pedalboard([pd.Chorus(), pd.Compressor(threshold_db = -10, ratio= 2,attack_ms = 1,release_ms= 100), pd.Distortion(10), pd.Gain(100)])


with AudioFile('skibidi.wav') as f:
  
  with AudioFile('output.wav', 'w', f.samplerate, f.num_channels) as o:
  
    while f.tell() < f.frames:
      chunk = f.read(f.samplerate)
      effected = board(chunk, f.samplerate, reset=False)
      o.write(effected)

#   Zobrazování framu na efekty   #
def on_tab_change(event):
    current_tab = hl_menu.index(hl_menu.select())  
    if current_tab in [0]:  
        effects_frame.pack_forget()
    else:  
        effects_frame.pack(anchor="s")  

def add_chorus():
    global chorus_frame
    if "chorus_frame" not in globals():
        chorus_frame = tk.LabelFrame(effects_frame, text="Chorus")
        chorus_frame.pack(side="left")
        slider1 = tk.Scale(chorus_frame, from_=100, to=0, label="Nějaky parametr", command=1 )
        slider1.pack()
    if chorus_var.get() == 1:
        chorus_frame.pack(side="left")
    else:
        chorus_frame.pack_forget()

def add_compressor():
    global compressor_frame
    if "compressor_frame" not in globals():
        compressor_frame = tk.LabelFrame(effects_frame, text="Compressor")
        compressor_frame.pack(side="left")
        slider1 = tk.Scale(compressor_frame, from_=100, to=0, label="Nějaky parametr", command=1 )
        slider1.pack()
    if compressor_var.get() == 1:
        compressor_frame.pack(side="left")
    else:
        compressor_frame.pack_forget()

def add_delay():
    global delay_frame
    if "delay_frame" not in globals():
        delay_frame = tk.LabelFrame(effects_frame, text="Delay")
        delay_frame.pack(side="left")
        slider1 = tk.Scale(delay_frame, from_=100, to=0, label="Nějaky parametr", command=1 )
        slider1.pack()
    if delay_var.get() == 1:
        delay_frame.pack(side="left")
    else:
        delay_frame.pack_forget()

def add_distortion():
    global distortion_frame
    if "distortion_frame" not in globals():
        distortion_frame = tk.LabelFrame(effects_frame, text="Distortion")
        distortion_frame.pack(side="left")
        slider1 = tk.Scale(distortion_frame, from_=100, to=0, label="Nějaky parametr", command=1 )
        slider1.pack()
    if distortion_var.get() == 1:
        distortion_frame.pack(side="left")
    else:
        distortion_frame.pack_forget()

def add_gain():
    global gain_frame
    if "gain_frame" not in globals():
        gain_frame = tk.LabelFrame(effects_frame, text="Gain")
        gain_frame.pack(side="left")
        slider1 = tk.Scale(gain_frame, from_=100, to=0, label="Nějaky parametr", command=1 )
        slider1.pack()
    if gain_var.get() == 1:
        gain_frame.pack(side="left")
    else:
        gain_frame.pack_forget()

def add_reverb():
    global reverb_frame
    if "reverb_frame" not in globals():
        reverb_frame = tk.LabelFrame(effects_frame, text="Reverb")
        reverb_frame.pack(side="left")
        slider1 = tk.Scale(reverb_frame, from_=100, to=0, label="Nějaky parametr", command=1 )
        slider1.pack()
    if reverb_var.get() == 1:
        reverb_frame.pack(side="left")
    else:
        reverb_frame.pack_forget()



#   Hlavní okno   #
root = tk.Tk()
root.title("AudioApp v2")
root.minsize(620,500)

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
load_btn = tk.Button(karta_soubor, text="Load", command=1)
load_btn.pack()

save_btn = tk.Button(karta_soubor, text="Save", command=1)
save_btn.pack()

help_btn = tk.Button(karta_soubor, text="help", command=1)
help_btn.pack()

##  Přehled  ##
play_btn = tk.Button(karta_prehled, text="Play", command=1)
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
gain_btn = tk.Checkbutton(karta_efekty, text="gain", variable=gain_var, command=add_gain)
gain_btn.grid(row=1, column=5)

reverb_var = tk.IntVar()
reverb_var.set(0)
reverb_btn = tk.Checkbutton(karta_efekty, text="reverb", variable=reverb_var, command=add_reverb)
reverb_btn.grid(row=1, column=6)


hl_menu.bind("<<NotebookTabChanged>>", on_tab_change)


root.mainloop()



