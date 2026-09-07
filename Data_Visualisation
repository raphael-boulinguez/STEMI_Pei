###########################################################################
# Data visualisation
###########################################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.patches import Patch
import os

# Définition des chemins d'accès
FILE_PATH = "/Users/raphaelboulinguez/Desktop/STEMI_Pei/Code/"
DATA_FILE_NAME = os.path.join(FILE_PATH, "STEMI_Pei_Processed.xlsx")
STATS_FILE_NAME = os.path.join(FILE_PATH, "Results.xlsx")
OUTPUT_FILE_NAME = os.path.join(FILE_PATH, "Figures/")

###########################################################################
# Préparatifs communs

# Propriété des titres de graphiques
titre_graphs = {
    'family': 'Arial',
    'weight': 'bold',
    'size': 15
}

colors = ["#087549", "#E38753", "#D23535"]


# Création des DataFrame pour les figures
categories = ("tous", "appel", "appel_F", "selfPresenter_PCIcenter", "selfPresenter_NonPCIcenter", "selfPresenter_NonPCIcenter_F", "medecin_ville", "medecin_ville_F", "autre", "appel_tous", "selfPresenter_NonPCIcenter_tous", "medecin_ville_tous")
df_data = pd.read_excel(DATA_FILE_NAME)
df_stat_ = {}
for cat in categories:
    df_stat_[cat] = pd.read_excel(STATS_FILE_NAME, sheet_name = cat, index_col=0)


#Crée les dictionnaires avec les variables a utiliser pour chaque boxplots

def dictionnaire_statistiques (sous_type_delai, categorie):
    statistiques = {
        'med': df_stat_[categorie].loc['Mediane', sous_type_delai],
        'q1': df_stat_[categorie].loc['Q1', sous_type_delai],
        'q3': df_stat_[categorie].loc['Q3', sous_type_delai],
    }
    return(statistiques)

def n_statistiques (sous_type_delai, categorie):
    n_infos = {
        'n_total': df_stat_[categorie].loc['n_total', sous_type_delai],
        'n_analyse': df_stat_[categorie].loc['n_analyse', sous_type_delai],
        'n_absent': df_stat_[categorie].loc['n_absent_%', sous_type_delai],
        'n_erreur': df_stat_[categorie].loc['n_erreur_%', sous_type_delai],
        'n_outlier': df_stat_[categorie].loc['n_outlier_%', sous_type_delai],
    }
    return(n_infos)


###########################################################################
#region Figure 1 - FlowChart
###########################################################################

# Fonction qui crée les boîtes centrée sur coordonnes x,y (Ds repère 0 - 100)
def box(ax, x, y, texte, largeur=44, couleur='white', bordure='black', gras=False, taille=10, alignement='center'):
    return ax.text(
        x, y, texte,
        ha=alignement, va='center', # Point (x,y) au centre | Horizontal/VerticalAlignement texte
        fontsize=taille,
        fontweight='bold' if gras else 'normal',
        wrap=False,
        # bbox créer contour atour du texte
        bbox=dict(
            boxstyle='round, pad=0.6',  # coins arrondis + marge intérieure (en pourcent de taille de police)
            facecolor=couleur,
            edgecolor=bordure,
            linewidth=1.2
        )
    )

# Fonction qui crée les fleches : depart/arrivee = tuple(x, y) dans le repère
def fleche(ax, depart, arrivee, style='-|>', taille_tete=16, epaisseur=1.2, typeFleche='-'):
    ax.add_patch(FancyArrowPatch(
        depart, arrivee,
        arrowstyle=typeFleche, # -|> Tête pleine || -> Tête vide || -[ Barre || - trait
        mutation_scale=taille_tete, #Taille pointe flèche indépendant taille ligne. Prédéfinit à 16 mais modifiable à appel fonction
        linewidth=epaisseur, #Taille ligne indépendant taille tête. Prédéfinit à 1.2 mais modifiable à appel fonction
        color='black',
        shrinkA=0, shrinkB=0 #Raccourcir les extrémités
    ))


# Les données | Flemme de récupérer dans le xlsx
n_source = 287
n_exclus_1 = 14
n_exclus_2 = 3
n_exclus_3 = 2
n_non_analysee = 4
n_exclus = n_exclus_1 + n_exclus_2 + n_exclus_3
n_inclus = n_source - n_exclus
n_analyse = n_inclus - n_non_analysee

periode = "1 novembre 2024 - 31 octobre 2025"

# Fonction qui contient le FLOWCHART complet ⚠️
def flowchart(save):

    # Creation canvas
    fig, ax = plt.subplots(figsize=(9, 11)) # En pouces -> 9x11
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off') # Axes, Graduations, Cadre masqué

    x_tronc = 50 # Axe vertical colonne principal
    x_droite = 85 #Bord gauche boite exclusion
    x_gauche = 15
    y_debut = 100 #Hauteur de début
    y_rang_05 = 83
    y_rang_1 = 70
    y_rang_15 = 60
    y_rang_2 = 47
    y_rang_25 = 50
    y_rang_3 = 40
    y_rang_4 = 30
    y_rang_fin = 30

    #1er box en haut
    box(ax, x_tronc, y_debut, 
        f"SCA ST+ traité par angioplastie \n"
        f"avec début des derniers symptômes < 24h \n"
        f"au CHU de la Réunion \n"
        f"{periode}\n"
        f"n = {n_source}")

    #1er flèche verticale
    fleche(ax, (x_tronc, y_debut), (x_tronc, y_rang_2))

    #1er flèche horizontale vers exclusion
    fleche(ax, (x_tronc, y_rang_05), (x_droite-25, y_rang_05))

    #box exclusion
    box(ax, x_droite-25, y_rang_05,
            f"Exclus (n = {n_exclus})\n"
            f"\n"
            f"•  Arrêt cardio-respiratoire : {n_exclus_1}\n"
            f"•  Évacuation sanitaire : {n_exclus_2}\n"
            f"•  SCA ST+ intra-hospitalier : {n_exclus_3}\n",
            alignement='left')

    #box traité
    box(ax, x_tronc, y_rang_1,
        f"Population éligible\n"
        f"n = {n_inclus}")

    #box non inclus
    box(ax, x_droite-25, y_rang_15,
        f"Exclus post calcul des délais (n = {n_non_analysee})\n"
        f"\n"
        f"•  Symptômes → Guide > 24h : {n_non_analysee}\n",
        alignement='left')

    #1er flèche horizontale vers non inclus
    fleche(ax, (x_tronc, y_rang_15), (x_droite-25, y_rang_15))

    #box analyse principale
    box(ax, x_tronc, y_rang_2,
        f"Population analysée\n"
        f"n = {n_analyse}")


    #2nd flèche verticale qui se divise en 3
    fleche(ax, (x_tronc, y_rang_2), (x_tronc, y_rang_2-10), typeFleche='-')
    fleche(ax, (x_droite,y_rang_2-10), (x_gauche, y_rang_2-10), typeFleche='-')

    # Crée les fleches verticales
    ecart_box_selon_nb = (x_droite - x_gauche) / 6
    x_tronc_droite = x_tronc + ecart_box_selon_nb
    x_tronc_gauche = x_tronc - ecart_box_selon_nb 
    nombre_fleche_verticale = [x_gauche, x_tronc_gauche, x_tronc_droite, x_droite]
    texte = [f"Appel 15 \nn = 136", f"Urgences \nn = 78", f"Medecin de ville \nn = 47", f"Autre \nn = 3"]
    for i, text in zip(nombre_fleche_verticale, texte):
        fleche(ax, (i, y_rang_2-10), (i, y_rang_fin))
        box(ax, i, y_rang_fin, text, alignement='center')

    plt.rcParams['font.family'] = 'Arial'
    plt.title("Diagramme de flux de la population d'étude", fontdict=titre_graphs, y=1.1)
    
    if save == False:
        plt.show()
    #   else: Faudrait que ca enregistre en PNG dans le fichier d'export, mais pour plus tard

#flowchart(False)
#endregion


###########################################################################
#region Figure 2 : WaterFall chart de l'aggrégat des données
###########################################################################

dictionnaires_fig_2 = [dictionnaire_statistiques('d_total',"tous"),
     dictionnaire_statistiques('d_pre_diagnostic', "tous"),
     dictionnaire_statistiques('d_logistic_ESC', "tous"),
     dictionnaire_statistiques('d_revascularisation',"tous"),]

n_infos_fig_2 = [n_statistiques('d_total',"tous"),
     n_statistiques('d_pre_diagnostic', "tous"),
     n_statistiques('d_logistic_ESC', "tous"),
     n_statistiques('d_revascularisation', "tous"),]

def figure_2(save):
    # Paramètres pour le graphique de waterfall
    etapes = ['Temps total', 'Délai \npré-diagnostique', 'Délai transport', 'Délai \nrevascularisation']
    temps_total = dictionnaires_fig_2[0]['med']
    medianes = [d['med'] for d in dictionnaires_fig_2[1:]]
    q1s = [d['q1'] for d in dictionnaires_fig_2]
    q3s = [d['q3'] for d in dictionnaires_fig_2] 
    cumul = np.concatenate([[0], np.cumsum(medianes)[:-1]])
    n_effectifs = [round(n['n_analyse']) for n in n_infos_fig_2]

    fig, ax = plt.subplots(figsize=(12, 6))


    # Barres + Texte au milieux du temps total. Position 0 réservé
    pos_total = 0
    ax.barh(pos_total, temps_total, color='gray', alpha=1, edgecolor='black', height=0.6)
    ax.text(temps_total/2, pos_total - 0.04, f'{temps_total:.0f} min', ha='center', va='center', fontweight='bold', color='white', fontsize=8)
    ax.text(temps_total/2, pos_total + 0.10, f'[Q1: {q1s[0]:.0f} - Q3: {q3s[0]:.0f}]', ha='center', va='center', color='white', fontsize=6.5)

    # Les 3 étapes commencent maintenant à la position 1
    for i, (etape, med, base) in enumerate(zip(etapes[1:], medianes, cumul)):
        pos = i + 1  # décalage de 1 pour laisser la place à "Total time"
        ax.barh(pos, med, left=base, color=colors[i], edgecolor='black', height=0.6, label=etape)
        ax.text(base + med/2, pos - 0.04, f'{med:.0f} min', ha='center', va='center', fontweight='bold', color='white', fontsize=8)
        ax.text(base + med/2, pos + 0.10, f'[Q1: {q1s[i+1]:.0f} - Q3: {q3s[i+1]:.0f}]', ha='center', va='center', color='white', fontsize=6.5)

    # Barres reliant les colonnes (décalage de +1 aussi)
    for i in range(len(medianes) - 1):
        x = cumul[i] + medianes[i]
        pos = i + 1
        ax.plot([x, x], [pos + 0.3, pos + 1 - 0.3], color='lightgray', linestyle='--', linewidth=1)


    ax.grid(axis='x', linestyle='-', alpha=0.7, linewidth=0.4, color='lightgray')
    ax.set_axisbelow(True)

    ax.set_yticks(range(len(etapes)))
    ax.set_yticklabels(etapes, ha='right', ma='right', va='center')
    ax.set_xlabel("Temps en minutes")

    for i in range(len(etapes)):
        ax.annotate(f'n={n_effectifs[i]}',
                    xy=(0, i), xycoords=('axes fraction', 'data'),
                    xytext=(-10, -15), textcoords='offset points',
                    ha='right', va='top', fontsize=7, color='darkgray')

    ax.invert_yaxis()
    ax.spines[['top', 'right']].set_visible(False)
    fig.text(0.5, 0.01, "La barre \"Temps total\" représente la médiane du délai total directement mesuré et non la somme des médianes des trois sous-délais, qui peut différer en raison de la non-additivité de la médiane", ha='center', fontsize=8, style='italic', color='gray')
    plt.title("Figure 1 - Où perdons-nous du temps ? Analyse en cascade du délai symptôme-revascularisation selon l'intervenant", fontdict=titre_graphs, y=1.05)

    if save == False:
        plt.show()
    #   else: Faudrait que ca enregistre en PNG dans le fichier d'export, mais pour plus tard

figure_2(False)

#endregion


###########################################################################
#region Figure 3 : Délais selon porte d'entrée dans la maladie
###########################################################################

mode_entree = ["appel_tous", "selfPresenter_PCIcenter", "selfPresenter_NonPCIcenter_tous", "medecin_ville_tous"]
nom_mode_entree = ["Appel SAMU\nCentre 15", "Présentation\ncentre PCI", "Présentation\ncentre non PCI", "Médecin de\nville"]
nom_delai = ["d_patient", "d_logistic_large", "d_revascularisation"]
noms_legende = [
    "Patient\nsymptômes → Contact",
    "Logistique\nContact → Admission",
    "Revascularisation\nAdmission → Guide"
]

colors_fig_3 = ["#087549", "#82A000", "#FF5500", "#D23535"]

# Fonction qui appelle les données selon mode d'entree, delais concerné et renvois mediane, Q1, Q3, n_infos
def delai_data(entree, delais):
    data = dictionnaire_statistiques(delais, entree)
    return(data)

def n_data(entree, delais):
    data = n_statistiques(delais, entree)
    return(data)





mode_entree = ["appel_tous", "selfPresenter_PCIcenter", "selfPresenter_NonPCIcenter_tous", "medecin_ville_tous"]
nom_mode_entree = ["Appel SAMU\nCentre 15", "Présentation\ncentre PCI", "Présentation\ncentre non PCI", "Médecin de\nville"]

nom_delai = ["d_patient", "d_logistic_extra_H", "d_logistic_intra_H", "d_puncture_2_balloon"]
noms_legende = [
    "Patient\nSymptômes → Contact : Appel ou Admission",
    "Logistique extra-hospitalière\nContact → Admission centre-PCI",
    "Logistique intra-hospitalière\nAdmission → Salle de cathétérisme",
    "Revascularisation\nSalle de cathétérisme → Passage du guide"
]

colors_fig_3 = ["#087549", "#E38753", "#D23535", "#111010"]  # 4 couleurs pour 4 segments

# Modes concernés par le transfert inter-hôpital (donc avec le segment extra-hospitalier)
modes_avec_transfert = ["appel_tous", "selfPresenter_NonPCIcenter_tous", "medecin_ville_tous"]


def delai_data(entree, delais):
    data = dictionnaire_statistiques(delais, entree)
    return(data)

def n_data(entree, delais):
    data = n_statistiques(delais, entree)
    return(data)


def figure_3(save):

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))


    #Partie de gauche
    labels_y = []
    n_list = []
    max_cumul = 0

    for (y_pos, mode), segment in zip(enumerate(mode_entree), nom_mode_entree):

        # Construction dynamique des segments selon le mode d'entrée
        if mode in modes_avec_transfert:
            valeurs_delais = ["d_patient", "d_logistic_extra_H", "d_logistic_intra_H", "d_puncture_2_balloon"]
        else:
            # Pas de segment extra-hospitalier pour les self-presenters en centre PCI
            valeurs_delais = ["d_patient", "d_logistic_intra_H", "d_puncture_2_balloon"]

        medianes = [delai_data(mode, d)['med'] for d in valeurs_delais]
        couleurs_utilisees = colors_fig_3 if mode in modes_avec_transfert else [colors_fig_3[0], colors_fig_3[2], colors_fig_3[3]]

        cumul = 0
        for valeur, couleur in zip(medianes, couleurs_utilisees):
            ax1.barh(y_pos, valeur, left=cumul, color=couleur, edgecolor='black', linewidth=0.5, height=0.5)
            ax1.text(cumul + valeur/2, y_pos, f'{valeur:g}', ha='center', va='center',
                      fontsize=8, fontweight='bold', color='white')
            cumul += valeur

        # Position ECG
        delai_ecg = delai_data(mode, "d_delai_ECG")['med']
        position_ecg = medianes[0] + delai_ecg  # patient + délai jusqu'à l'ECG
        ax1.plot([position_ecg, position_ecg], [y_pos - 0.24, y_pos + 0.24],
                  linestyle='--', color='black', linewidth=1.5, zorder=5)
        # Petit label au-dessus de la barre pour identifier le repère ECG
        ax1.text(position_ecg, y_pos - 0.32, 'ECG', ha='center', va='bottom', fontsize=6, fontweight='bold', color='black')

        total = delai_data(mode, "d_total")['med']
        ax1.text(cumul + 5, y_pos, f'Médiane\n{total:g}min', ha='left', va='center', fontsize=9)

        n = n_data(mode, "d_patient")['n_analyse']
        n_list.append(n)
        labels_y.append(f'{segment}')
        max_cumul = max(max_cumul, cumul)

    ax1.set_yticks(range(len(mode_entree)))
    ax1.set_yticklabels(labels_y, ha='right', ma='right', va='center')
    for i in range(len(mode_entree)):
        ax1.annotate(f'n={n_list[i]}', xy=(0, i), xycoords=('axes fraction', 'data'), xytext=(-10, -15), textcoords='offset points', ha='right', va='top', fontsize=7, color='gray')
    ax1.invert_yaxis()

    ax1.set_xlabel('Temps en minutes')
    ax1.set_title('Décomposition du délai symptôme-revascularisation')
    ax1.set_xlim(0, max_cumul * 1.2)
    ax1.spines[['top', 'right']].set_visible(False)

#Partie de droite
    for (y_pos, mode), segment in zip(enumerate(mode_entree), nom_mode_entree):
        if mode in modes_avec_transfert:
            valeurs_delais = ["d_patient", "d_logistic_extra_H", "d_logistic_intra_H", "d_puncture_2_balloon"]
        else:
            # Pas de segment extra-hospitalier pour les self-presenters en centre PCI
            valeurs_delais = ["d_patient", "d_logistic_intra_H", "d_puncture_2_balloon"]

        medianes = [delai_data(mode, d)['med'] for d in valeurs_delais]
        total = sum(medianes)
        pourcentages = [round(v / total * 100, 0) for v in medianes]

        print(total)
        print(medianes)

        couleurs_utilisees = colors_fig_3 if mode in modes_avec_transfert else [colors_fig_3[0], colors_fig_3[2], colors_fig_3[3]]

        cumul = 0
        for valeur, couleur in zip(pourcentages, couleurs_utilisees):
            ax2.barh(y_pos, valeur, left=cumul, color=couleur, edgecolor='black', linewidth=0.5, height=0.5)
            ax2.text(cumul + valeur/2, y_pos, f'{valeur:g}', ha='center', va='center',fontsize=8, fontweight='bold', color='white')
            cumul += valeur


    ax2.set_yticks(range(len(mode_entree)))
    ax2.set_yticklabels("")
    ax2.tick_params(axis='y', length=0)
    ax2.invert_yaxis()

    ax2.set_xlabel('Temps relatifs en pourcent')
    ax2.set_title('Part de chaque segment')
    ax2.set_xlim(0, 100)
    ax2.spines[['top', 'right']].set_visible(False)

    ax2.text(0.5, -0.15, "Pourcentages calculés à partir de la somme des médianes des sous-délais", transform=ax2.transAxes, ha='center', va='top', fontsize=7, style='italic', color='gray')

    # Légende en bas
    legend_elements = [
        Patch(facecolor=couleur, edgecolor='black', label=nom)
        for nom, couleur in zip(noms_legende, colors_fig_3)
    ]

    fig.legend(handles=legend_elements, loc='lower center', ncol=4, bbox_to_anchor=(0.5, 0.05), frameon=False, fontsize=9, handlelength=1.5, handleheight=1.5, columnspacing=2)

    # Ajuster l'espace en bas pour laisser de la place à la légende
    plt.subplots_adjust(bottom=0.25, top=0.80)
    fig.suptitle("Figure 2 - Où pouvons-nous gagner des minutes ? Analyse des temps médians selon le mode d'entrée", fontfamily=titre_graphs['family'], fontweight=titre_graphs['weight'], fontsize=titre_graphs['size'], y=0.98)

    if save == False:
        plt.show()

figure_3(False)

#endregion
