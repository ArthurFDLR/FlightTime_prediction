import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib import colors
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg

import numpy as np
import copy
import tkinter as tk
from graph.label_lines import *

style.use('ggplot')


def fonction_utiles(info):
    poids_multirotor,nbrmoteur, courantvide_multirotor, capacite_batterie, facteurdecharge_batterie, configuration_batterie, courantcontinue_esc, courantmax_esc, kv_moteur, efficacite_moteur, pas_helice, diametre_helice = info
    
    #capacite de la batterie en mAh
    #renvoie le temps de vol en minutes
    capacite_batterie_reelle=(0.7* float(capacite_batterie))*(10**(-3))
    f= float(poids_multirotor) / int(nbrmoteur)
    
    tension_nominale = int(configuration_batterie) * 3.9
    
    intensite_moy = calcul_intensite_force(f,float(pas_helice) , float(diametre_helice) , float(kv_moteur) , float(courantvide_multirotor) , float(efficacite_moteur)/100 ) #Pour 1 moteur
    intensite_max = min(float(courantmax_esc),(float(capacite_batterie)*(10**(-3))*float(facteurdecharge_batterie))/float(nbrmoteur))
    
    force_max_continue=calcul_force_intensite(intensite_max*0.9, float(pas_helice),  float(diametre_helice), float(kv_moteur), float(courantvide_multirotor),float(efficacite_moteur)/100)
    
    tps_vol = (capacite_batterie_reelle*60) / (intensite_moy*int(nbrmoteur) + float(courantvide_multirotor))
    
    pui_moyenne = tension_nominale*((intensite_moy*int(nbrmoteur))+float(courantvide_multirotor))
    
    rapport_poidsforce = force_max_continue/f
    
    return tps_vol, pui_moyenne, rapport_poidsforce

def calcul_intensite_force(force,pas,diametre,kv,courant_vide,eff_moteur): #force en gramme; pas et diametre en Inch
    
    c1,c2 = 7.84,0.725
    inch_meter = 0.0254    
    efficacite = eff_moteur
    Kv = int(kv)
    Io = 0.3
    Kc = 1/Kv
    g = 9.81
    
    F = force
    coeff_correction = (pas/diametre) * c1
    puissance_correction=(diametre/pas) * c2
    I = ((F * g * (pas*inch_meter)*coeff_correction) / (efficacite*Kv)) ** puissance_correction
    return I + Io     #http://learningrc.com/motor-kv/

    
def calcul_force_intensite(intensite,pas,diametre,kv,courant_vide,eff_moteur): #force en gramme

    c1,c2 = 7.84,0.725
    inch_meter = 0.0254    
    efficacite = eff_moteur
    Kv = int(kv)
    Kc = 1/Kv
    g = 9.81
    
    I = intensite
    coeff_correction = (pas/diametre) * c1
    puissance_correction=(diametre/pas) * c2
    
    F = ((I ** (1/puissance_correction)) * (efficacite*Kv)) / (g * (pas*inch_meter)*coeff_correction) #A verifier
    return F



def graphique(data):
    
    poids_multirotor,nbrmoteur, courantvide_multirotor, capacite_batterie, facteurdecharge_batterie, configuration_batterie, courantcontinue_esc, courantmax_esc, kv_moteur, efficacite_moteur, pas_helice, diametre_helice = data
    
    fig = Figure(figsize=(11, 4), dpi=100)
    
    ax_for = fig.add_subplot(121)

    intensite_max = min(float(courantmax_esc),(float(capacite_batterie)*(10**(-3))*float(facteurdecharge_batterie))/float(nbrmoteur))

    force_max_continue=calcul_force_intensite(float(courantcontinue_esc), float(pas_helice),  float(diametre_helice), float(kv_moteur), float(courantvide_multirotor),float(efficacite_moteur)/100)
    force_max = calcul_force_intensite(intensite_max, float(pas_helice),  float(diametre_helice), float(kv_moteur), float(courantvide_multirotor),float(efficacite_moteur)/100)
    
    force_fonctionnement = float(poids_multirotor)/float(nbrmoteur) #gramme
    intensite_fonctionnement = calcul_intensite_force(force_fonctionnement, float(pas_helice),  float(diametre_helice), float(kv_moteur), float(courantvide_multirotor), float(efficacite_moteur)/100)

    # Courbe I(f)
    axe_force=[]
    axe_intensite=[]

    for force_g in range(1,int(force_max)+200,10):

        intensite = calcul_intensite_force(force_g,float(pas_helice), float(diametre_helice),float(kv_moteur),float(courantvide_multirotor),float(efficacite_moteur)/100)
        axe_force.append(force_g)
        axe_intensite.append(intensite)
        
    ax_for.plot(axe_force,axe_intensite)
    
    # Droites caracteristiques

    ax_for.plot([force_fonctionnement,force_fonctionnement],[0,intensite_fonctionnement],'k--')
    ax_for.plot([0,force_fonctionnement],[intensite_fonctionnement,intensite_fonctionnement],'k--')
    ax_for.plot([0,force_max],[intensite_max,intensite_max],'r--')
    ax_for.plot([0,force_max_continue],[float(courantcontinue_esc),float(courantcontinue_esc)],'r--')

    # Configuration
    ax_for.set_title ("Point de fonctionnement en vol stationnaire", fontsize=13)
    ax_for.set_xlabel(r'Force $ [gf] $',fontsize=10)
    ax_for.set_ylabel(r'Intensité $ [A] $',fontsize=10)
    
    #ax_for.set_xlim([0,force_max + 100])
    ax_for.set_ylim(bottom=0)
    
    # Annotation
    intensite_str = str(intensite_fonctionnement)
    intensite_annotation = intensite_str[0:4]
    force_str = str(force_fonctionnement)
    force_annotation = force_str[0:5]
    
    extraticks_x = [force_fonctionnement]
    ax_for.set_xticks(list(ax_for.get_xticks()) + extraticks_x)
    extraticks_y = [intensite_fonctionnement]
    ax_for.set_yticks(list(ax_for.get_yticks()) + extraticks_y)

    ax_for.annotate(r'$( {} A ; {} gf )$'.format(intensite_annotation,force_annotation),
        xy=(force_fonctionnement, intensite_fonctionnement), xycoords='data',
        xytext=(35, 0), textcoords='offset points',
        arrowprops=dict(facecolor='black', shrink=0.02),
        horizontalalignment='left', verticalalignment='bottom')

    ax_for.axvspan(force_max_continue, force_max, facecolor='darkorange', alpha=0.25)
    ax_for.axvspan(force_max, force_max + 200, facecolor='r', alpha=0.25)

    
     #Courbe efficacite
    
    ax_eff = fig.add_subplot(122)
    axe_efficacite= [] # force/intensite
    
    for i in range( len(axe_force) ):
        axe_efficacite.append(axe_force[i] / axe_intensite[i])
    
    ax_eff.plot(axe_force,axe_efficacite)

    ax_eff.plot([force_fonctionnement,force_fonctionnement],[0,force_fonctionnement/intensite_fonctionnement],'k--')
    ax_eff.plot([0,force_fonctionnement],[force_fonctionnement/intensite_fonctionnement,force_fonctionnement/intensite_fonctionnement],'k--')
    
    ax_eff.annotate(r'Point de fonctionnement',
        xy=(force_fonctionnement, force_fonctionnement/intensite_fonctionnement), xycoords='data',
        xytext=(30, 30), textcoords='offset points',
        arrowprops=dict(facecolor='black', shrink=0.02),
        horizontalalignment='left', verticalalignment='bottom')
    
    # Configuration
    ax_eff.set_title ("Efficacité du systeme propulsif", fontsize=13)
    ax_eff.set_ylabel(r'Force/Intensité $ [gf/A] $',fontsize=10)
    ax_eff.set_xlabel(r'Force $ [gf] $',fontsize=10)
    
    
    return fig