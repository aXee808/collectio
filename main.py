import os,sys,shutil
import pickle
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk,Image
from tkinter.filedialog import askopenfilename,asksaveasfilename
from pathlib import Path

class Manufacturer:
    def __init__(self,name,foundation_year,foundation_country):
        self.name = name
        self.foundation_country = foundation_country
        self.foundation_year = foundation_year

class Platform:
    def __init__(self,name, manufacturer, architecture,creation_year,typeplatf):
        self.name = name
        self.architecture = architecture
        self.typeplat = typeplatf
        self.manufacturer = manufacturer
        self.creation_year = creation_year

class Game:
    def __init__(self,name,platform):
        self.name = name
        self.platform = platform
        self.id = None
        self.creation_year = None
        self.editor = None
        self.original_name = None
        self.nb_players = None
        self.type_support = None
        self.nb_supports = None
        self.status = None
        self.front_image = None
        self.images = None

    def add_images(self, image):
        self.list_images.append(image)

    def modify_status(self, status):
        self.status = status

    def modify_properties(self, creation_year,editor,original_name,nb_players,type_support,nb_supports,front_image):
        self.creation_year = creation_year
        self.editor = editor
        self.original_name = original_name
        self.nb_players = nb_players
        self.type_support = type_support
        self.nb_supports = nb_supports
        self.front_image = front_image

class GamesCompilation:
    def __init__(self,name,platform):
        self.name = name
        self.platform = platform
        self.creation_year = None
        self.editor = None
        self.type_support = None
        self.nb_supports = None
        self.front_image = None
        self.images = None
        self.list_games = []

    def add_game(self, game):
        self.list_games.append(game)

    def add_images(self, image):
        self.list_images.append(image)

    def modify_properties(self, creation_year,editor,type_support,nb_supports,front_image):
        self.creation_year = creation_year
        self.editor = editor
        self.type_support = type_support
        self.nb_supports = nb_supports
        self.front_image = front_image

class Collection:
    def __init__(self,name):
        self.idcounter = 0
        self.name = name
        self.list_games = []
    
    def add_game(self, game):
        #for g in self.list_games:
        #    if g.name==game.name:
        #        return False
        self.idcounter+=1
        game.id = self.idcounter
        self.list_games.append(game)
        return True
    
    def remove_game(self,id):
        for index, g in enumerate(self.list_games):
            if g.id==id:
                self.list_games.pop(index)

class MainWindow:
    def __init__(self,master):
        # Initial settings
        self.master = master
        self.master.geometry("1600x820")
        self.master.title("Collectio")
        self.master.resizable(False,False)
        self.master.iconbitmap(APP_ICO)
        self.collection = None
        self.collection_name = None
        
        # Frames
        self.frameleft = tk.Frame(self.master)
        self.frameleft.place(x=10, y=10, width=600,height=780)
        self.frameright = tk.Frame(self.master, bg='red')
        self.frameright.place(x=620, y=10, width=970,height=780)

        # Menu
        self.create_menu_bar()

        # Frameleft --> Treeview
        self.coltree = ttk.Treeview(self.frameleft,columns=("Id","Plateforme","Nom","Statut"), show='headings',selectmode='browse')
        self.coltree.heading("Id",text="")
        self.coltree.heading("Plateforme",text="Plateforme")
        self.coltree.heading("Nom",text="Nom")
        self.coltree.heading("Statut",text="Statut")
        self.coltree.column("Id",width=0,stretch="no")
        self.coltree.column("Plateforme",width=120,stretch="no")
        self.coltree.column("Nom",width=400,stretch="no")
        self.coltree.column("Statut",width=40,stretch="no")
        self.coltree.pack()
        self.coltree.place(x=0, y=0, width=570, height=760)
        # Frameleft --> Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frameleft, orient=tk.VERTICAL, command=self.coltree.yview)
        self.coltree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack()
        self.scrollbar.place(x=570, y=0, width=20, height=760)
        # Frameleft --> bouttons
        self.addbutton = Button(self.frameleft, text="Ajouter",command=self.add_game_form)
        self.addbutton.place(x=0,y=760,width=60,height=20)
        self.addbutton.config(state=DISABLED)
        self.modbutton = Button(self.frameleft, text="Modifier",command=self.modify_game_form)
        self.modbutton.place(x=60,y=760,width=60,height=20)
        self.modbutton.config(state=DISABLED)
        self.delbutton = Button(self.frameleft, text="Retirer",command=self.remove_game)
        self.delbutton.place(x=120,y=760,width=60,height=20)
        self.delbutton.config(state=DISABLED)

    def create_menu_bar(self):
        menu_bar = Menu(self.master)

        menu_file = Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Nouvelle collection", command=self.new_collection_form)        
        menu_file.add_command(label="Ouvrir collection", command=self.open_collection)
        menu_file.add_command(label="Sauvegarder collection", command=self.save_collection)
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.master.quit)
        menu_bar.add_cascade(label="File", menu=menu_file)
        menu_help = Menu(menu_bar, tearoff=0)
        menu_help.add_command(label="A propos de...", command=self.do_about)
        menu_bar.add_cascade(label="?", menu=menu_help)

        self.master.config(menu=menu_bar)

    def open_collection(self):
        filepath = askopenfilename(initialdir=APP_DATA_DB_DIR,title="Choisir la collection à ouvrir",
                               filetypes=[("Collectio database", ".cdt")])
        if len(filepath)>0:
            try:
                with open(filepath,'rb') as pickle_file:
                    self.collection = pickle.load(pickle_file)
                    self.collection_name = self.collection.name
                    self.master.title(f"Collectio [{self.collection_name}]")
                    self.addbutton.config(state=NORMAL)
                    self.modbutton.config(state=NORMAL)
                    self.delbutton.config(state=NORMAL)
                    self.refresh_display()
            except Exception:
                messagebox.showerror("Erreur","Format de fichier incorrect")

    def save_collection(self):
        if self.collection is not None:
            filepath = asksaveasfilename(initialdir=APP_DATA_DB_DIR,title="Choisir le nom de la collection à sauvegarder",
                               filetypes=[("Collectio database", ".cdt")])
            try:
                if len(filepath)>0:
                    if '.cdt' not in filepath:
                        filepath = filepath + ".cdt"
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                    with open(filepath, 'wb') as pickle_file:
                        pickle.dump(self.collection,pickle_file)
            except Exception:
                messagebox.showerror("Erreur","Impossible de sauvegarder la collection.")      
        else:
            messagebox.showerror("Erreur","Pas de collection ouverte")

    def new_collection_form(self):
        self.top = tk.Toplevel()
        self.top.geometry("300x100")
        self.top.title("Entrer le nom de la nouvelle collection")
        self.top.resizable(False,False)    
        self.new_name = None
        
        self.inputnamebox = Entry(self.top)
        self.inputnamebox.place(x=20,y=20,width=260,height=20)
        self.cancelbutton = Button(self.top, text="Annuler",command=self.top.destroy)
        self.cancelbutton.place(x=80,y=60,width=60,height=20)
        self.newcollbutton = Button(self.top, text="Créer",command=self.set_new_collection)
        self.newcollbutton.place(x=180,y=60,width=60,height=20)

        self.top.wait_visibility()
        self.top.grab_set()
    
    def set_new_collection(self):
        temponame = ''.join(filter(str.isalnum, self.inputnamebox.get()))
        if len(temponame)>0:
            self.collection = Collection(temponame)
            self.collection_name = temponame
            self.master.title(f"Collectio [{self.collection_name}]")
            self.addbutton.config(state=NORMAL)
            self.modbutton.config(state=NORMAL)
            self.delbutton.config(state=NORMAL)
            self.refresh_display()
            self.top.grab_release()
            self.top.destroy()

    def add_game_form(self):
        self.top = tk.Toplevel()
        self.top.geometry("600x800")
        self.top.title("Ajouter un jeu")
        self.top.resizable(False,False)    
        
        # Name
        self.gamenamelabel = Label(self.top,text="Nom du jeu",anchor=W)
        self.gamenamelabel.place(x=10,y=20,width=100,height=20)
        self.gamenamebox = Entry(self.top)
        self.gamenamebox.place(x=100,y=20,width=300,height=20)

        # Manufacturer
        self.manufacturerlabel = Label(self.top,text="Constructeur",anchor=W)
        self.manufacturerlabel.place(x=10,y=60,width=100,height=20)
        selected_manufacturer = tk.StringVar()
        self.manufacturercbox = ttk.Combobox(self.top, textvariable=selected_manufacturer)
        self.manufacturercbox.place(x=100,y=60,width=300,height=20)
        manufacturers_name_list = []
        for m in manufacturers_list:
             manufacturers_name_list.append(m.name)
        self.manufacturercbox['values']= manufacturers_name_list
        self.manufacturercbox['state'] = 'readonly'
        self.manufacturercbox.bind("<<ComboboxSelected>>", self.manufacturercbox_select)

        # Platform
        self.platformlabel = Label(self.top,text="Plateforme",anchor=W)
        self.platformlabel.place(x=10,y=100,width=100,height=20)
        selected_platform = tk.StringVar()
        self.platformcbox = ttk.Combobox(self.top, textvariable=selected_platform)
        self.platformcbox['state'] = 'readonly'
        self.platformcbox.place(x=100,y=100,width=300,height=20)

        # Editor
        self.gameeditorlabel = Label(self.top,text="Editeur",anchor=W)
        self.gameeditorlabel.place(x=10,y=140,width=100,height=20)
        self.gameeditorbox = Entry(self.top)
        self.gameeditorbox.place(x=100,y=140,width=300,height=20)




        # Buttons
        self.cancelbutton = Button(self.top, text="Annuler",command=self.top.destroy)
        self.cancelbutton.place(x=80,y=760,width=60,height=20)
        self.newcollbutton = Button(self.top, text="Ajouter",command=self.add_game)
        self.newcollbutton.place(x=180,y=760,width=60,height=20)

        self.top.wait_visibility()
        self.top.grab_set()

    def manufacturercbox_select(self,event):
        game_platform = self.manufacturercbox.get()
        platforms_name_list = []
        for p in platforms_list:
             if p.manufacturer.name == game_platform: 
                platforms_name_list.append(p.name)
        self.platformcbox['values']= platforms_name_list
        self.platformcbox.current(0)

    def add_game(self):
        game_platform = self.platformcbox.get()
        game_name = self.gamenamebox.get()
        if len(game_name)>0:
            for p in platforms_list:
                if p.name == game_platform:
                    gameobj = Game(game_name,p)
                    gameobj.editor = self.gameeditorbox.get()
                    if self.collection.add_game(gameobj):
                        self.refresh_display()
                    self.top.destroy

    def remove_game(self):
        curGame = self.coltree.focus()
        game_selected = self.coltree.item(curGame)
        if messagebox.askquestion("Attention", f"Voulez vous supprimer le jeu {game_selected.get('values')[2]}")=='yes':
            self.collection.remove_game(game_selected.get('values')[0])
            self.refresh_display()

    def modify_game_form(self):
        print("modifier jeu")

    def modify_game(self):
        print("modifier jeu")
   
    def do_about(self):
        messagebox.showinfo("A propos de...", f"Collectio version {APP_VERSION}\n2025 GPL-3.0 license / Yannick Oréal")

    def refresh_display(self):
        for row in self.coltree.get_children():
            self.coltree.delete(row)
        i = 0
        for game in self.collection.list_games:
            self.coltree.insert(parent='',index='end',iid=i,text=game.platform.name,values=(game.id,game.platform.name,game.name,"acquis"))
            i=i+1
        #print(f"{game.platform.manufacturer.name} - {game.platform.name} - {game.name}")

if __name__ == "__main__":
    """
    Description: Main routine
    """
    APP_PATH=Path(__file__).parent
    APP_VERSION="alpha 0.1"
    APP_DATA_DB_DIR=APP_PATH / "data/db"
    APP_ICO=APP_PATH / "data/assets/collectio.ico"

    # init manufacturers
    manufacturers_list=[Manufacturer("Nintendo",1889,"Japan"),
                        Manufacturer("Sega",1960,"Japan"),
                        Manufacturer("Nec",1899,"Japan"),
                        Manufacturer("Sony",1946,"Japan"),
                        Manufacturer("SNK",1973,"Japan"),
                        Manufacturer("Taito",1953,"Japan"),
                        Manufacturer("Capcom",1979,"Japan"),
                        Manufacturer("International Games System Co., Ltd.",1989,"Taiwan"),
                        Manufacturer("Sharp Corporation",1912,"Japan"),
                        Manufacturer("Atari",1972,"U.S.A"),
                        Manufacturer("Commodore",1954,"U.S.A"),
                        Manufacturer("Amstrad",1968,"England"),
                        Manufacturer("ASCII Corporation",1977,"Japan"),
                        Manufacturer("IBM",1911,"U.S.A")]

    # init platform
    platforms_list=[Platform("Famicom",manufacturers_list[0],"8-bits",1983,"console"),
                    Platform("Super Famicom",manufacturers_list[0],"16-bits",1990,"console"),
                    Platform("Twin Famicom",manufacturers_list[8],"8-bits",1986,"console"),
                    Platform("Gamecube",manufacturers_list[0],"128-bits",2001,"console"),
                    Platform("Master System",manufacturers_list[1],"8-bits",1986,"console"),
                    Platform("Megadrive",manufacturers_list[1],"16-bits",1988,"console"),
                    Platform("Saturn",manufacturers_list[1],"32-bits",1994,"console"),
                    Platform("PC Engine",manufacturers_list[2],"8-bits",1987,"console"),
                    Platform("MSX",manufacturers_list[12],"8-bits",1983,"micro-ordinateur"),
                    Platform("MSX2",manufacturers_list[12],"8-bits",1985,"micro-ordinateur"),
                    Platform("MSX2+",manufacturers_list[12],"8-bits",1988,"micro-ordinateur"),
                    Platform("Playstation",manufacturers_list[3],"64-bits",1994,"console"),
                    Platform("Playstation 2",manufacturers_list[3],"128-bits",2000,"console"),
                    Platform("Playstation 3",manufacturers_list[3],"Septieme gen",2006,"console"),
                    Platform("Playstation 4",manufacturers_list[3],"Huitieme gen",2013,"console"),
                    Platform("Playstation 5",manufacturers_list[3],"neuvieme gen",2020,"console"),
                    Platform("MVS",manufacturers_list[4],"16-bits",1990,"arcade"),
                    Platform("F3",manufacturers_list[5],"32-bits",1992,"arcade"),
                    Platform("Capcom System II",manufacturers_list[6],"16-bits",1993,"arcade"),
                    Platform("CPC 6128",manufacturers_list[11],"8-bits",1985,"micro-ordinateur"),
                    Platform("Atari ST",manufacturers_list[9],"16-bits",1985,"micro-ordinateur"),
                    Platform("Amiga 500",manufacturers_list[10],"16-bits",1987,"micro-ordinateur"),
                    Platform("Polygame Master",manufacturers_list[7],"16-bits",1997,"arcade"),
                    Platform("PC Compatible",manufacturers_list[13],"-",1981,"micro-ordinateur")]

    app = tk.Tk()
    window = MainWindow(app)
    app.mainloop()
