import tkinter as tk
import random

WIDTH = 300
HEIGHT = 300
VELIKOST_BUNKY = 30 

class Had:
    def __init__(self):
        self.telo = [(5, 5)]
        self.smer = (0, 1)  
        

    def pohyb(self):
        hlava = self.telo[0]
        nova_hlava = (hlava[0] + self.smer[0], hlava[1] + self.smer[1])
        self.telo = [nova_hlava] + self.telo[:-1]

    def zvetseni(self):
        self.telo.append(self.telo[-1])

    def kys(self):
        return self.telo[1:]  

    def kolize(self):
        if self.telo[0] in self.kys(): 
            exit()  

class Jidlo:
    def __init__(self):
        self.nove_jidlo()

    def nove_jidlo(self):
        self.pozice = (random.randint(0, (WIDTH // VELIKOST_BUNKY) - 1),
                       random.randint(0, (HEIGHT // VELIKOST_BUNKY) - 1))

class Hra:
    def __init__(self, root):
        self.root = root 
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#D1FFBD")
        self.canvas.pack() 

        self.had = Had()
        self.jidlo = Jidlo()
        self.pohyb_cekajici = False

        self.skore = 0

        self.root.bind("<KeyPress>", self.zmena_smeru)

        self.skorenapis = tk.Label(root, text = f"Skóre: {self.skore}", font=('Arial', 14)) #napise se to v te hre
        self.skorenapis.pack()
        
        self.vykresli_hraci_pole()

    def zmena_smeru(self, event): 
        if event.keysym == 'Up':
            self.had.smer = (0, -1)
        elif event.keysym == 'Down':
            self.had.smer = (0, 1)
        elif event.keysym == 'Left':
            self.had.smer = (-1, 0)
        elif event.keysym == 'Right':
            self.had.smer = (1, 0)

        if not self.pohyb_cekajici:
            self.aktualizuj_hru()

    def aktualizuj_hru(self):
        self.pohyb_cekajici = True  
        self.had.pohyb()

        self.had.kolize()

        if self.had.telo[0] == self.jidlo.pozice:
            self.had.zvetseni()
            self.jidlo.nove_jidlo()
            self.skore += 1

        self.vykresli_hraci_pole()

        self.skorenapis.config(text = f"Skóre: {self.skore}") #self.skore_label.config() -> aktualizuje text v labelu

        self.pohyb_cekajici = False

    def vykresli_hraci_pole(self):
        self.canvas.delete("all")

        for (x, y) in self.had.telo:
            x1 = x * VELIKOST_BUNKY 
            y1 = y * VELIKOST_BUNKY 
            x2 = x1 + VELIKOST_BUNKY 
            y2 = y1 + VELIKOST_BUNKY 
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")

        jidlo_x, jidlo_y = self.jidlo.pozice
        x1 = jidlo_x * VELIKOST_BUNKY
        y1 = jidlo_y * VELIKOST_BUNKY
        x2 = x1 + VELIKOST_BUNKY
        y2 = y1 + VELIKOST_BUNKY
        self.canvas.create_oval(x1, y1, x2, y2, fill="red")

root = tk.Tk() 
root.title("Had v Tkinteru")
hra = Hra(root)
root.mainloop()