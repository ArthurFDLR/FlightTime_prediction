## RESSOURCES
#Accees aux fonctions de calcules et créations graphiques
import Calculs_simu as calcsim
"La fonction graphique(info:list) prend en argument la liste des donnees du drone qui sont recolte dans la page InfoHelice. Elle renvoie [graphe :plt.Figure, temps de vol :float, rapport force/poids max :float, intensite en vol sationnaire :float"

import matplotlib.pyplot as plt
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib import style
from matplotlib.figure import Figure

LARGE_FONT= ("Verdana", 12)
UNITE_FONT= ("Helevtica", "8", "italic")

## CONSTRUCTION DE L'APPLI

class CalculateurApp(tk.Tk):    #Classe de l'application. Elle herite de tk.Tk

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)   #On intialise aussi tk.Tk avec les memes arguments
        self.resizable(0,0)     #Empeche la redimenssion des fenetres
        self.container = tk.Frame(self)  #On créer le cadre qui contiendra nos différentes pages. Elles sont empiler l'une sur l'autre. On met en avant celle qu'on veut.

        self.title("Calculateur Fendelair")
        tk.Tk.iconbitmap(self,default="LogoCalculateur.ico")

        self.container.pack(side="top", fill="both",expand = True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        ## BARRE MENU
        
        menubar = tk.Menu(self.container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Aide")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="Menu", menu=filemenu)

        tk.Tk.config(self, menu=menubar)

        ## CREATION PAGES
        self.frames = {} #Initialisation du dictionnaire contenant les differentes pages

        for F in (StartPage, PageOne, PageInfoDrone,PageAide): #remplie le dictionnaire et les ajouter a cotainer

            frame = F(self.container, self)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.montrer_page(StartPage)  #On commence par afficher la page d'acceuil

    def montrer_page(self, page):
        
        frame = self.frames[page]   #On cherche dans le dictionnaire la page...
        frame.tkraise() #... pour la mettre en avant
    
    def montrer_resultats(self,frameold):    #metode a utiliser UNIQUEMENT avec object de la classe InfoHelice
        
        info=[]
        for datanom in (frameold.poids_multirotor,frameold.nbrmoteur, frameold.courantvide_multirotor, frameold.capacite_multirotor, frameold.facteurdecharge_batterie, frameold.configuration_multirotor, frameold.courantcontinue_esc, frameold.courantmax_esc, frameold.kv_moteur, frameold.efficacite_moteur, frameold.pas_helice, frameold.diametre_helice): #Liste des informations recuperer dans frameold (i.e PageInfoDrone)
            
            info.append(datanom.get())
    
    
        #info=[general_poids,general_nbrmoteur]          
        frame = PageResultats(self.container, self, info)  #On creer une page de resultat
        frame.grid(row=0, column=0, sticky="nsew")
        
        frame.tkraise() #on l'affiche



## CONSTRUCTION DES PAGES CONSTITUTIVES 

class StartPage(tk.Frame):  #creation d'une page de depart

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Visit Page 1",
                            command=lambda: controller.montrer_page(PageOne))
        button.pack()
        
        button3 = tk.Button(self, text="Visit Page Info",
                            command=lambda: controller.montrer_page(PageInfoDrone))
        button3.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.montrer_page(StartPage))
        button1.pack()


class PageInfoDrone(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Informations multirotor", font=LARGE_FONT) #Titre
        label.grid(row=0, column=0, pady=10,padx=10)

        ##FENETRE INFO GENERAL
        FenetreInfoGlobal = tk.LabelFrame(self, text="Information général", padx=20, pady=20)  #Cadre
        FenetreInfoGlobal.grid(row=1, column=0,sticky='NSWE', padx=10, pady=10)
        
        self.poids_multirotor = tk.StringVar(self,value="1600")         #Entree de poids
        entree_poids = tk.Entry(FenetreInfoGlobal, textvariable=self.poids_multirotor, width=10)
        label_poids = tk.Label(FenetreInfoGlobal, text ="Poids :")
        label_poids_unite = tk.Label(FenetreInfoGlobal, text ="g", font=UNITE_FONT)
        
        entree_poids.grid(row = 0, column = 1, columnspan=3, sticky = "E")
        label_poids.grid(row = 0, column = 0, sticky = "E")
        label_poids_unite.grid(row = 0, column = 4, sticky = "W")
        
        self.courantvide_multirotor = tk.StringVar(self,value="0.00")         #Entree de courant a vide 
        entree_courantvide = tk.Entry(FenetreInfoGlobal, textvariable=self.courantvide_multirotor, width=10)
        label_courantvide = tk.Label(FenetreInfoGlobal, text ="Courant à vide :")
        label_courantvide_unite = tk.Label(FenetreInfoGlobal, text ="A", font=UNITE_FONT)
        
        entree_courantvide.grid(row = 1, column = 1, columnspan=3, sticky = "E")
        label_courantvide.grid(row = 1, column = 0, sticky = "E")
        label_courantvide_unite.grid(row = 1, column = 4, sticky = "W")
        
        self.nbrmoteur = tk.StringVar(self)
        entree_nbrmoteur = tk.Spinbox(FenetreInfoGlobal, from_=3, to=8, width=9, textvariable=self.nbrmoteur)  #Entree nombre moteurs
        label_nbrmoteur = tk.Label(FenetreInfoGlobal, text ="Nombre de moteurs :")

        entree_nbrmoteur.grid(row = 2, column = 1, columnspan=3, sticky = "E")
        label_nbrmoteur.grid(row = 2, column = 0, sticky = "E")
        
        ##FENETRE INFO BATTERIE
        FenetreInfoBatterie = tk.LabelFrame(self, text="Information batterie", padx=20, pady=20)  #Cadre
        FenetreInfoBatterie.grid(row=2, column=0,sticky='NSWE', padx=10, pady=10, rowspan=3)
        
        self.capacite_multirotor = tk.StringVar(self,value="5000")         #Entree batterie 
        entree_capacite = tk.Entry(FenetreInfoBatterie, textvariable=self.capacite_multirotor, width=10)
        label_capacite = tk.Label(FenetreInfoBatterie, text ="Batterie - Capacité :")
        label_capacite_unite = tk.Label(FenetreInfoBatterie, text ="mAh", font=UNITE_FONT)
        
        entree_capacite.grid(row = 0, column = 1, sticky = "E") 
        label_capacite.grid(row = 0, column = 0, sticky = "E")
        label_capacite_unite.grid(row = 0, column = 2, sticky = "W")
        
        self.facteurdecharge_batterie = tk.StringVar(self,value="30")         #Entree batterie 
        entree_facteurdecharge = tk.Entry(FenetreInfoBatterie, textvariable=self.facteurdecharge_batterie, width=10)
        label_facteurdecharge = tk.Label(FenetreInfoBatterie, text ="facteur de decharge (C) :")
        
        entree_facteurdecharge.grid(row = 1, column = 1, sticky = "E") 
        label_facteurdecharge.grid(row = 1, column = 0, sticky = "E")
        
        self.configuration_multirotor  = tk.StringVar() #Entree configuration batterie
        bouton1 = tk.Radiobutton(FenetreInfoBatterie, text="2S1P ~ 7.4V", variable=self.configuration_multirotor , value =2)
        bouton2 = tk.Radiobutton(FenetreInfoBatterie, text="3S1P ~ 11.1V", variable=self.configuration_multirotor , value =3)
        bouton3 = tk.Radiobutton(FenetreInfoBatterie, text="4S1P ~ 14.8V", variable=self.configuration_multirotor , value =4)
        bouton1.grid(row = 2, column = 1, columnspan=2)
        bouton2.grid(row = 3,column = 1, columnspan=2)
        bouton3.grid(row = 4,column = 1, columnspan=2)
        label_configuration = tk.Label(FenetreInfoBatterie, text ="Configuration :")
        label_configuration.grid(row = 2, column = 0, sticky = "E")


        
        ## FENETRE INFO MOTEUR-ESC
        
        FenetreSysProp = tk.LabelFrame(self, text="Information système propulsif électronique", padx=20, pady=20)  #Cadre
        FenetreSysProp.grid(row=1, column=1,sticky='NSWE',padx=10, pady=10)
        
        label_courant_esc = tk.Label(FenetreSysProp, text ="Intensité des ESCs :")         #Entree de courant ESC 
        label_courant_esc.grid(row = 0, column = 0, sticky = "E")


        self.courantcontinue_esc = tk.StringVar(self,value="20.00") # ESC en continue
        entree_courantcontinue_esc = tk.Entry(FenetreSysProp, textvariable=self.courantcontinue_esc, width=10)
        label_courantcontinue_esc_unite = tk.Label(FenetreSysProp, text ="A en continue" , font=UNITE_FONT)
        
        entree_courantcontinue_esc.grid(row = 0, column = 1)
        label_courantcontinue_esc_unite.grid(row = 0, column = 2, sticky = "W")


        self.courantmax_esc = tk.StringVar(self,value="30.00")         # ESC en max
        entree_courantmax_esc = tk.Entry(FenetreSysProp, textvariable=self.courantmax_esc, width=10)
        label_courantmax_esc_unite = tk.Label(FenetreSysProp, text ="A maximal" , font=UNITE_FONT)
        
        entree_courantmax_esc.grid(row = 1, column = 1)
        label_courantmax_esc_unite.grid(row = 1, column = 2, sticky = "W")
        

        self.kv_moteur = tk.StringVar(self,value="980")         #Entree KV Moteur 
        entree_kv_moteur = tk.Entry(FenetreSysProp, textvariable=self.kv_moteur, width=10)
        label_kv_moteur = tk.Label(FenetreSysProp, text ="KV moteur :")
        label_kv_moteur_unite = tk.Label(FenetreSysProp, text ="(tr/min)/V" , font=UNITE_FONT)
        
        entree_kv_moteur.grid(row = 2, column = 1)
        label_kv_moteur.grid(row = 2, column = 0, sticky = "E")
        label_kv_moteur_unite.grid(row = 2, column = 2, sticky = "W")


        self.efficacite_moteur = tk.StringVar(self,value="74")         #Entree efficacite Moteur 
        entree_efficacite_moteur = tk.Entry(FenetreSysProp, textvariable=self.efficacite_moteur, width=10)
        label_efficacite_moteur = tk.Label(FenetreSysProp, text ="Efficacité moteur :")
        label_efficacite_moteur_unite = tk.Label(FenetreSysProp, text ="%" , font=UNITE_FONT)
        
        entree_efficacite_moteur.grid(row = 3, column = 1)
        label_efficacite_moteur.grid(row = 3, column = 0, sticky = "E")
        label_efficacite_moteur_unite.grid(row = 3, column = 2, sticky = "W")


        ## FENETRE INFO HELICES
        
        FenetreHelice = tk.LabelFrame(self, text="Hélice", padx=20, pady=20)  #Cadre
        FenetreHelice.grid(row=2, column=1,sticky='NSWE',padx=10, pady=10)
        
        self.pas_helice = tk.StringVar(self,value="4.5")         #Entree pas 
        entree_pas_helice = tk.Entry(FenetreHelice, textvariable=self.pas_helice, width=10)
        label_pas_helice = tk.Label(FenetreHelice, text ="Pas :")
        label_pas_helice_unite = tk.Label(FenetreHelice, text ="inch" , font=UNITE_FONT)
        
        entree_pas_helice.grid(row = 0, column = 1)
        label_pas_helice.grid(row = 0, column = 0, sticky = "E")
        label_pas_helice_unite.grid(row = 0, column = 2, sticky = "W")

        self.diametre_helice = tk.StringVar(self,value="10")         #Entree diametre 
        entree_diametre_helice = tk.Entry(FenetreHelice, textvariable=self.diametre_helice, width=10)
        label_diametre_helice = tk.Label(FenetreHelice, text ="Diametre :")
        label_diametre_helice_unite = tk.Label(FenetreHelice, text ="inch" , font=UNITE_FONT)
        
        entree_diametre_helice.grid(row = 1, column = 1)
        label_diametre_helice.grid(row = 1, column = 0, sticky = "E")
        label_diametre_helice_unite.grid(row = 1, column = 2, sticky = "W")

        ## BOUTONS COMMANDES
        buttonBTH = tk.Button(self, text="Retour page d'acceuil",
                            command=lambda: controller.montrer_page(StartPage))
        buttonBTH.grid(row=3, column=1, sticky='WE')
        
        
        buttonGraph = tk.Button(self, text="Afficher resultats",
                            command=lambda: controller.montrer_resultats(self))  #Bouton pour creer et afficher une page de resultat
        buttonGraph.grid(row=4, column=1, sticky='WE')
        
        buttonGraph = tk.Button(self, text="Aide",
                            command=lambda: controller.montrer_page(PageAide))  #Bouton afficher la page d'aide
        buttonGraph.grid(row=5, column=1, sticky='WE')


class PageResultats(tk.Frame):

    def __init__(self, parent, controller,info):
        tk.Frame.__init__(self, parent)
        
        Titre = tk.Label(self, text="Resultats de simulation", font=LARGE_FONT)
        Titre.grid(row=0, column=0, pady=10,padx=10)
        
        buttonClose = tk.Button(self, text="Close",
                            command=lambda: self.quitto(PageInfoDrone))    #Quitter et supprimer la page
        buttonClose.grid(row=0, column=1, pady=10,padx=10)

        
        ## GRAPHIQUE
        
        FenetreGraph = tk.LabelFrame(self, text="Graphique efficacite", padx=20, pady=20)  #Cadre
        FenetreGraph.grid(row=1, column=0, pady=10,padx=10)
        
        fig = calcsim.graphique(info)   #recupere le graph du fichier de Vincent
        graph = FigureCanvasTkAgg(fig, FenetreGraph)
        canvas = graph.get_tk_widget()
        canvas.pack()   #afficher le graph
        
        toolbar = NavigationToolbar2TkAgg(graph, FenetreGraph)  #ajouter la barre de controle du graph
        toolbar.update()
        graph._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        ## DONNEE 
        tps_vol, pui_moyenne, rapport_poidsforce = calcsim.fonction_utiles(info) # renvoie temps de vol ; puissance moyenne ; rapport poids/force
        
        tps_vol_str=str(tps_vol)
        pui_moyenne_str=str(pui_moyenne)
        rapport_poidsforce_str=str(rapport_poidsforce)
        
        FenetreResult = tk.LabelFrame(self, text="Donnée de vol", padx=20, pady=20)  #Cadre
        FenetreResult.grid(row=2, column=0,padx=10, pady=10)
        
        Fenetretempsvol = tk.LabelFrame(FenetreResult, text="Temps de vol", padx=10, pady=10)  #temps de vol
        Fenetretempsvol.grid(row=0, column=0)
        label_tempsvol = tk.Label(Fenetretempsvol, text="{} minutes".format(tps_vol_str[:4]))
        label_tempsvol.grid(row=0, column=0)
        
        Fenetre_puimoy = tk.LabelFrame(FenetreResult, text="Puissance moyenne", padx=10, pady=10)  #Puissance moyenne
        Fenetre_puimoy.grid(row=0, column=1)
        label_puimoy = tk.Label(Fenetre_puimoy, text="{} Watt".format(pui_moyenne_str[:3]))
        label_puimoy.grid(row=0, column=0)
        
        Fenetre_rapport_forcepoids = tk.LabelFrame(FenetreResult, text="Rapport force/poids", padx=10, pady=10)  #Rapport poids puissance
        Fenetre_rapport_forcepoids.grid(row=0, column=2)
        label_rapport_forcepoids = tk.Label(Fenetre_rapport_forcepoids, text="{}".format(rapport_poidsforce_str[:3]))
        label_rapport_forcepoids.grid(row=0, column=0)

    def quitto(self,page):  #suicide et affiche "page"
        lambda: controller.montrer_page(page)
        self.destroy()


class PageAide(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        titre = tk.Label(self, text="Description des champs d'information", font=LARGE_FONT)
        titre.grid(row=0, column=0, pady=10,padx=10)

        poidstitre = tk.Label(self, text="poids :")
        poidstitre.grid(row=1, column=0)
        poidsinfo = tk.Label(self, text="Poids total du drone en vol dont le poids de la batterie")
        poidsinfo.grid(row=1, column=1)
        
        button1 = tk.Button(self, text="Retour",
                            command=lambda: controller.montrer_page(PageInfoDrone))
        button1.grid(row=4,column=0, sticky='EW')


## PROCESS

app = CalculateurApp()  #Creation de l'objet
app.mainloop()  #Loop d'affichage