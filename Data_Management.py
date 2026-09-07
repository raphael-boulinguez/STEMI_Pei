###########################################################################
# 4 etapes : Classification, Calcul délais, Analyse
# 1 - Préparation : Import des library | 
# 2 - Classification des prises en charge : Appel | SelfPresenter | Medecin
# 3 - Calcul des délais & Nb intervenant
# 4 - Analyse statistique
###########################################################################


###########################################################################
# 1 - Préparation
###########################################################################

import pandas as pd
import numpy as np
import os

# Definit le chemin d'acces/de sortie des fichier excel
FILE_PATH = "/Users/raphaelboulinguez/Desktop/STEMI_Pei/Code/"
INPUT_FILE_NAME = os.path.join(FILE_PATH, "STEMI_Pei.xlsx")
INTERMEDIATE_FILE_NAME = os.path.join(FILE_PATH, "STEMI_Pei_Processed.xlsx")
ANALYSIS_FILE_NAME = os.path.join(FILE_PATH, "Results.xlsx")

# Lit le fichier source, sur la bonne feuille et le met dans un dataframe
df = pd.read_excel(INPUT_FILE_NAME, sheet_name="Données")

# Fonction creation des colonnes
def creation_colonne(nom_colonne, index_colonne):
    df.insert(index_colonne, nom_colonne, np.nan)
    df[nom_colonne] = df[nom_colonne].astype('object')

# Fonction qui retourne la valeur arrondi
def safe_round(value):
    if pd.isna(value): return None
    return round(value, 0)


###########################################################################
# 2 - Classification des prises en charge
# Boucle qui passe sur chaque procédure pour repérer la catégorie :
#  - Appel ± F
#  - SelfPresenter ± PCI ± F
#  - Medecin ville ± F | Autre
###########################################################################

# Creation colonne 'categorie' au format String
creation_colonne("categorie", 1)


for i in range(len(df)):
    if (not pd.isna(df.loc[i, "appel"])
        and pd.isna(df.loc[i, "fibrinolyse"])):
        df.loc[i, "categorie"] = "appel"

    elif (not pd.isna(df.loc[i, "appel"])
    and not pd.isna(df.loc[i, "fibrinolyse"])):
        df.loc[i, "categorie"] = "appel_F"

    elif (pd.isna(df.loc[i, "appel"])
    and df.loc[i, "premier_hopital"] == "CHU SITE FELIX GUYON (SAINT DENIS)"
    and df.loc[i, "intervenant_1"] == "Service urgences"
    and pd.isna(df.loc[i, "fibrinolyse"])):
        df.loc[i, "categorie"] = "selfPresenter_PCIcenter"

    elif (pd.isna(df.loc[i, "appel"])
    and df.loc[i, "premier_hopital"] != "CHU SITE FELIX GUYON (SAINT DENIS)"
    and df.loc[i, "intervenant_1"] == "Service urgences"
    and pd.isna(df.loc[i, "fibrinolyse"])):
        df.loc[i, "categorie"] = "selfPresenter_NonPCIcenter"

    elif (pd.isna(df.loc[i, "appel"])
    and df.loc[i, "premier_hopital"] != "CHU SITE FELIX GUYON (SAINT DENIS)"
    and df.loc[i, "intervenant_1"] == "Service urgences"
    and not pd.isna(df.loc[i, "fibrinolyse"])):
        df.loc[i, "categorie"] = "selfPresenter_NonPCIcenter_F"

    elif (pd.isna(df.loc[i, "appel"])
    and (df.loc[i, "intervenant_1"] == "Médecin généraliste" or df.loc[i, "intervenant_1"] == "SOS médecin")
    and pd.isna(df.loc[i, "fibrinolyse"])):
        df.loc[i, "categorie"] = "medecin_ville"

    elif (pd.isna(df.loc[i, "appel"])
    and (df.loc[i, "intervenant_1"] == "Médecin généraliste" or df.loc[i, "intervenant_1"] == "SOS médecin")
    and not pd.isna(df.loc[i, "fibrinolyse"])):
        df.loc[i, "categorie"] = "medecin_ville_F"

    else: 
        df.loc[i, "categorie"] = "autre"


###########################################################################
# 3 - Calcul des délais
###########################################################################

# Creation des colonnes
colonnes = [
    "d_sympto_appel", "d_appel_fmc", "d_sympto_fmc", "d_fmc_ecg",
    "d_ecg_fibrynolyse", "d_ecg_admission",
    "d_patient", "d_pre_diagnostic", "d_system", "d_logistic_ESC", "d_delai_ECG", "d_logistic_extra_H", "d_logistic_intra_H", "d_puncture_2_balloon" , "d_revascularisation", "d_total",
    "d_pre_diagnostic_complet", "d_logistic_ESC_complet","d_revascularisation_complet", "d_total_complet",
    "nb_intervenant"]

for i in range(len(colonnes)):
    creation_colonne(colonnes[i], i + 10)

# Fonction qui calcule le délai
#  - Arg_input : df, index, column1 [1er temps], column2 [2nd temps], delay_colum [Nom colonne ou delai stocké]
#  - Nan si un des horodatage manquant
def calculate_delays(df, index, column1, column2, delay_column):

    if not pd.isna(df.loc[index, column1]) and not pd.isna(df.loc[index, column2]):
        df.loc[index, delay_column] = (df.loc[index, column2] - df.loc[index, column1]).total_seconds() / 60  # Convertir en minutes
    else:
        df.loc[index, delay_column] = np.nan  # Si un des horodatages est manquant, mettre NaN


# Nom des colonnes intervenant pour compter le nombre d'intervenant
colonnes_intervenants = ["intervenant_1", "intervenant_2", "intervenant_3", "intervenant_4", "intervenant_5"]

# Fonction qui calcule le nb intervenant dnans les colonnes_intervenants
def calculate_intervenant(df, index):
    count = -1 #On supprime le coronarographiste
    for col in colonnes_intervenants:
        valeur = df.loc[index, col]
        if pd.notna(valeur) and str(valeur).strip() != "":
            count +=1
    df.loc[index, "nb_intervenant"] = count


# Boucle for qui balaye l'excel et qui calcule l'ensemble des délais
for i in range(len(df)):
    calculate_delays(df, i, "symptomes", "appel", "d_sympto_appel")
    calculate_delays(df, i, "appel", "FMC", "d_appel_fmc")
    calculate_delays(df, i, "ECG", "fibrinolyse", "d_ecg_fibrynolyse")
    calculate_delays(df, i, "symptomes", "ECG", "d_pre_diagnostic")
    calculate_intervenant(df, i)

    if df.loc[i, "categorie"] == "selfPresenter_PCIcenter":
        calculate_delays(df, i, "symptomes", "admission", "d_sympto_fmc")
        calculate_delays(df, i, "symptomes", "admission", "d_patient")
        calculate_delays(df, i, "admission", "ECG", "d_fmc_ecg")
        calculate_delays(df, i, "ECG", "examen", "d_ecg_admission")
        calculate_delays(df, i, "ECG", "examen", "d_logistic_ESC")
        calculate_delays(df, i, "admission","ECG","d_delai_ECG")
        calculate_delays(df, i, "admission", "examen", "d_logistic_intra_H")
        calculate_delays(df, i, "examen", "wire", "d_puncture_2_balloon")
        calculate_delays(df, i, "admission", "wire", "d_system")
        calculate_delays(df, i, "admission", "wire", "d_revascularisation")
        calculate_delays(df, i, "symptomes", "wire", "d_total")
#       print(df.loc[i, "d_total"] - df.loc[i, "d_sympto_fmc"] - df.loc[i, "d_logistic_ESC"] - df.loc[i, "d_admission_wire"])

    elif df.loc[i, "categorie"] == "appel" or df.loc[i, "categorie"] == "appel_F":
        calculate_delays(df, i, "symptomes", "FMC", "d_sympto_fmc")
        calculate_delays(df, i, "symptomes", "appel", "d_patient")
        calculate_delays(df, i, "FMC", "ECG", "d_fmc_ecg")
        calculate_delays(df, i, "ECG", "admission", "d_ecg_admission")
        calculate_delays(df, i, "ECG", "admission", "d_logistic_ESC")
        calculate_delays(df, i, "appel", "ECG", "d_delai_ECG")
        calculate_delays(df, i, "appel", "admission", "d_logistic_extra_H")
        calculate_delays(df, i, "admission", "examen", "d_logistic_intra_H")
        calculate_delays(df, i, "examen", "wire", "d_puncture_2_balloon")
        calculate_delays(df, i, "FMC", "wire", "d_system")
        calculate_delays(df, i, "admission", "wire", "d_revascularisation")
        calculate_delays(df, i, "symptomes", "wire", "d_total")


    else:
        calculate_delays(df, i, "symptomes", "FMC", "d_sympto_fmc")
        calculate_delays(df, i, "symptomes", "FMC", "d_patient")
        calculate_delays(df, i, "FMC", "ECG", "d_fmc_ecg")
        calculate_delays(df, i, "ECG", "admission", "d_ecg_admission")
        calculate_delays(df, i, "ECG", "admission", "d_logistic_ESC")
        calculate_delays(df, i, "FMC","ECG","d_delai_ECG")
        calculate_delays(df, i, "FMC", "admission", "d_logistic_extra_H")
        calculate_delays(df, i, "admission", "examen", "d_logistic_intra_H")
        calculate_delays(df, i, "examen", "wire", "d_puncture_2_balloon")
        calculate_delays(df, i, "FMC", "wire", "d_system")
        calculate_delays(df, i, "admission", "wire", "d_revascularisation")
        calculate_delays(df, i, "symptomes", "wire", "d_total")


# Calcul délais total uniquement si l'ensemble des sous délais sont complets
    if pd.notna(df.loc[i,"d_sympto_fmc"]) and pd.notna(df.loc[i,"d_logistic_ESC"]) and pd.notna(df.loc[i,"d_revascularisation"]):
        if df.loc[i, "categorie"] == "selfPresenter_PCIcenter":
            calculate_delays(df, i, "symptomes", "ECG", "d_pre_diagnostic_complet")
            calculate_delays(df, i, "ECG", "examen", "d_logistic_ESC_complet")
            calculate_delays(df, i, "examen", "wire", "d_revascularisation_complet")
        else: 
            calculate_delays(df, i, "symptomes", "ECG", "d_pre_diagnostic_complet")
            calculate_delays(df, i, "ECG", "admission", "d_logistic_ESC_complet")
            calculate_delays(df, i, "admission", "wire", "d_revascularisation_complet")
        calculate_delays(df, i, "symptomes", "wire", "d_total_complet")


###########################################################################
# x - Point d'arrêt
# Crée un excel avec le df travaillé pour contrôle -> STEMI_Pei_processed
###########################################################################

df.to_excel(INTERMEDIATE_FILE_NAME, sheet_name="Données", index=False)


###########################################################################
# 3 - Analyse des délais : Médiane, IQR, P10/90, n, n absent/errur, n outlier
###########################################################################

def calculate_statistics(categories, delays):
    # Filtre le dataframe pour la catégorie donnée
    if categories == "tous": df_category = df
    elif categories == "appel_tous": df_category = df[df["categorie"].isin(["appel", "appel_F"])] # Rassemble les catégorie avec les fibrynolysés dedans
    elif categories == "selfPresenter_NonPCIcenter_tous": df_category = df[df["categorie"].isin(["selfPresenter_NonPCIcenter", "selfPresenter_NonPCIcenter_F"])]
    elif categories == "medecin_ville_tous": df_category = df[df["categorie"].isin(["medecin_ville", "medecin_ville_F"])] 
    else: df_category = df[df["categorie"] == categories]

    results = []
    n = len(df_category)

    for delay in delays:
        serie = df_category[delay]

        n_absent = int(serie.isna().sum())
        n_absent_percent = round((n_absent / n) * 100, 2) if n > 0 else 0
        n_erreur = int((serie <= 0).sum())
        n_erreur_percent = round((n_erreur / n) * 100, 2) if n > 0 else 0
        n_analyse = n - n_absent - n_erreur

        serie_valide = serie[serie.notna() & (serie >= 0)]


        if len(serie_valide) <= 0 or delay == "nb_intervenant":
            median = q1 = q3 = iqr = p10 = p90 = None
            n_outlier = n_outlier_percent = None
            if delay == "nb_intervenant":
                median = round(serie_valide.mean(),2)
                n_absent = n_absent_percent = n_erreur = n_erreur_percent = None
        else: 
            median = safe_round(serie_valide.median())
            q1 = safe_round(serie_valide.quantile(0.25))
            q3 = safe_round(serie_valide.quantile(0.75))
            iqr = q3 - q1
            p10 = safe_round(serie_valide.quantile(0.10))
            p90 = safe_round(serie_valide.quantile(0.90))

            if iqr is not None: n_outlier = int((serie_valide > (q3 + 3 * iqr)).sum())
            else: n_outlier = 0

            n_outlier_percent = round((n_outlier / len(serie_valide)) * 100, 2) if n > 0 else 0

        results.append({ "Delai": delay, "Mediane": median, "Q1": q1, "Q3": q3, "IQR": iqr, "P10": p10, "P90": p90,
                        "n_total": n, "n_analyse": n_analyse, "n_absent": n_absent, "n_absent_%": n_absent_percent,
                        "n_erreur": n_erreur, "n_erreur_%": n_erreur_percent, "n_outlier": n_outlier,"n_outlier_%": n_outlier_percent})

    # Transpose les données d'un diactionnaire ) un data frame en mettant en colonne les délais et en index les médiane, q10, ...
    df_intermediaire = pd.DataFrame(results)
    df_intermediaire = df_intermediaire.set_index("Delai")
    df_intermediaire = df_intermediaire.T
    return df_intermediaire

# Nécessité de définir l'ensemble des catégories !
categories = ("tous", "appel", "appel_F", "selfPresenter_PCIcenter", "selfPresenter_NonPCIcenter", "selfPresenter_NonPCIcenter_F", "medecin_ville", "medecin_ville_F", "autre", "appel_tous", "selfPresenter_NonPCIcenter_tous", "medecin_ville_tous")

with pd.ExcelWriter(ANALYSIS_FILE_NAME, engine='openpyxl', mode='w') as writer:
    for category in categories:
        df_results = calculate_statistics(category, colonnes)
        df_results.to_excel(writer, sheet_name=category, index=True)
