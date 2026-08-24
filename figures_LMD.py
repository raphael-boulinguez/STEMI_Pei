import os
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

FICHIER = "STEMI Péi - Base traitée n=268 (Boulinguez, 2026-08-16).xlsx"
FICHIER_BRUT = ("STEMI Péi - Extraction France-PCI ST+ 2024-11 à 2025-10 "
                "(VPC, 2026-06-30).xlsx")
DOSSIER = "figures"
HOPITAL_PCI = "CHU SITE FELIX GUYON (SAINT DENIS)"

# --- charte : 3 segments = 3 couleurs, tenues dans TOUT le memoire ---
C_PATIENT = "#4C72B0"      # bleu
C_PREHOSP = "#DD8452"      # orange
C_CARDIO  = "#55A868"      # vert
C_GRIS    = "#8C8C8C"
C_ALERTE  = "#C44E52"      # rouge : seuils et non-conformite

plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 300, "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 12.5, "axes.titleweight": "bold",
    "axes.grid": True, "grid.alpha": .25, "grid.linestyle": ":",
    "axes.axisbelow": True, "figure.autolayout": False,
})
os.makedirs(DOSSIER, exist_ok=True)


def enregistrer(fig, nom):
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(DOSSIER, f"{nom}.{ext}"), bbox_inches="tight")
    plt.close(fig)
    print(f"   ecrit : {DOSSIER}/{nom}.png et .pdf")


# ==========================================================================
# PREPARATION — identique au Script 3
# ==========================================================================
FICHIER = trouver(FICHIER, ["*Base trait*n=268*.xlsx", "*Base*268*.xlsx"])
df = pd.read_excel(FICHIER)
for c in ["symptomes", "appel", "FMC", "ECG", "fibrinolyse",
          "admission", "examen", "wire"]:
    df[c] = pd.to_datetime(df[c], errors="coerce")


def d(a, b):
    return ((df[b] - df[a]).dt.total_seconds() / 60.0).round(3)


for nom, (a, b) in {
        "d_sympto_appel": ("symptomes", "appel"), "d_appel_fmc": ("appel", "FMC"),
        "d_fmc_ecg": ("FMC", "ECG"), "d_ecg_admission": ("ECG", "admission"),
        "d_fmc_admission": ("FMC", "admission"),
        "d_admission_salle": ("admission", "examen"),
        "d_salle_wire": ("examen", "wire"), "d_admission_wire": ("admission", "wire"),
        "d_ecg_wire": ("ECG", "wire"), "d_ecg_lyse": ("ECG", "fibrinolyse"),
        "d_lyse_wire": ("fibrinolyse", "wire"), "d_fmc_wire": ("FMC", "wire"),
        "d_sympto_wire": ("symptomes", "wire")}.items():
    df[nom] = d(a, b)

CONTACT = {"appel": "appel", "appel_F": "appel", "medecin_ville": "FMC",
           "medecin_ville_F": "FMC", "selfPresenter_PCIcenter": "admission"}
df["d_systeme_esc"] = np.nan
for parc, col in CONTACT.items():
    m = df["categorie"] == parc
    df.loc[m, "d_systeme_esc"] = ((df.loc[m, "wire"] - df.loc[m, col])
                                  .dt.total_seconds() / 60).round(3)
df["S1"] = np.nan
df["S2"] = np.nan
for parc, col in CONTACT.items():
    m = df["categorie"] == parc
    df.loc[m, "S1"] = ((df.loc[m, col] - df.loc[m, "symptomes"])
                       .dt.total_seconds() / 60).round(3)
    df.loc[m, "S2"] = ((df.loc[m, "admission"] - df.loc[m, col])
                       .dt.total_seconds() / 60).round(3)
df["S3"] = df["d_admission_wire"]

P = df[~(df["d_sympto_wire"] > 24 * 60)].copy()      # analyse principale n=264
P["mode"] = P["categorie"].astype(str).str.replace("_F", "", regex=False)
P["lyse"] = P["categorie"].astype(str).str.endswith("_F")
LIB = {"appel": "Appel du 15", "medecin_ville": "Médecin de ville",
       "selfPresenter_PCIcenter": "Présentation spontanée\nau centre PCI",
       "selfPresenter_NonPCIcenter": "Présentation spontanée\nhôpital sans coro",
       "autre": "Autre"}
print(f"Base {len(df)} · analyse principale {len(P)}\n")


# ==========================================================================
# FIGURE 1 — FLOW CHART
# Message : d'ou viennent les 264, exclusion par exclusion.
# ==========================================================================
print("Figure 1 — flow chart")
FICHIER_BRUT = trouver(FICHIER_BRUT, ["*Extraction France-PCI*.xlsx", "*Extraction*ST+*.xlsx"])
if os.path.exists(FICHIER_BRUT):
    brut = pd.read_excel(FICHIER_BRUT)
    ex = brut[~brut["Procédure N°"].astype(str).isin(set(df["Procedure"].astype(str)))]
    acr = (ex["Arrêt cardiaque"].astype(str).str.strip().str.lower() == "oui")
    chm = ex["1er hôpital d'accueil avec ou sans coro"].astype(str).str.upper().str.strip().eq("CHM") & ~acr
    n_brut, n_acr, n_chm = len(brut), int(acr.sum()), int(chm.sum())
    n_intra = len(ex) - n_acr - n_chm
else:
    n_brut, n_acr, n_chm, n_intra = 287, 14, 3, 2
    print("   (extraction brute absente : valeurs du 22/08 reprises en dur)")
n_24 = int((df["d_sympto_wire"] > 24 * 60).sum())

fig, ax = plt.subplots(figsize=(10.5, 7.6))
ax.set_xlim(0, 12); ax.set_ylim(0, 10); ax.axis("off"); ax.grid(False)
BX, BW = 0.4, 6.6
boites = [
    (7.9, f"Extraction France-PCI\nST+ < 24 h, CHU Nord, 01/11/2024 – 31/10/2025\nn = {n_brut}"),
    (5.3, f"Base traitée\nn = {n_brut - n_acr - n_chm - n_intra}"),
    (2.7, f"ANALYSE PRINCIPALE\nn = {n_brut - n_acr - n_chm - n_intra - n_24}"),
]
for y, txt in boites:
    ax.add_patch(FancyBboxPatch((BX, y - .60), BW, 1.20, boxstyle="round,pad=.10",
                                fc="white", ec="black", lw=1.4))
    ax.text(BX + BW / 2, y, txt, ha="center", va="center", fontsize=10.5)
for y0, y1 in [(7.26, 5.94), (4.66, 3.34)]:
    ax.add_patch(FancyArrowPatch((BX + BW / 2, y0), (BX + BW / 2, y1),
                                 arrowstyle="-|>", mutation_scale=17, lw=1.4,
                                 color="black"))
ax.add_patch(FancyBboxPatch((7.6, 5.90), 4.2, 1.55, boxstyle="round,pad=.10",
                            fc="#F2F2F2", ec=C_GRIS, lw=1.1))
ax.text(9.7, 6.68, f"Exclus (n = {n_acr + n_chm + n_intra})\n"
                   f"• arrêts cardiaques : {n_acr}\n"
                   f"• EVASAN Mayotte : {n_chm}\n"
                   f"• ST+ intra-hospitaliers du centre PCI : {n_intra}",
        ha="center", va="center", fontsize=9.5)
ax.plot([BX + BW / 2, 7.6], [6.6, 6.6], color=C_GRIS, lw=1.1)
ax.add_patch(FancyBboxPatch((7.6, 3.45), 4.2, 1.05, boxstyle="round,pad=.10",
                            fc="#F2F2F2", ec=C_GRIS, lw=1.1))
ax.text(9.7, 3.98, f"Sortis de l'analyse principale (n = {n_24})\n"
                   f"symptômes → guide > 24 h\n"
                   f"comptés à part, vivier du volet qualitatif",
        ha="center", va="center", fontsize=9.5)
ax.plot([BX + BW / 2, 7.6], [3.98, 3.98], color=C_GRIS, lw=1.1)
n_wire = int(P["wire"].notna().sum())
ax.text(BX + BW / 2, 1.5, f"dont passage du guide renseigné : n = {n_wire}\n"
                          f"({len(P) - n_wire} sans angioplastie : reperfusion "
                          f"spontanée, ATL non réalisée ou non propice)",
        ha="center", va="center", fontsize=9.3, color=C_GRIS, style="italic")
ax.set_title("Figure 1 — Diagramme de flux de la population d'étude", pad=14)
enregistrer(fig, "figure1")


# ==========================================================================
# FIGURE 2 — LES TROIS SEGMENTS  (LA figure du memoire)
# Message : chez les regules le temps se perd en prehospitalier ;
#           chez ceux qui passent par la ville, avant meme le contact.
# ==========================================================================
print("Figure 2 — les trois segments imputables")
groupes = [("appel", "Appel du 15"), ("medecin_ville", "Médecin de ville"),
           ("selfPresenter_PCIcenter", "Présentation spontanée\nau centre PCI")]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.2, 5.6),
                               gridspec_kw={"width_ratios": [1.25, 1]})
y = np.arange(len(groupes))[::-1]
med, ns = [], []
for mode, _ in groupes:
    g = P[P["mode"] == mode]
    med.append([g["S1"].median(), g["S2"].median(), g["S3"].median()])
    ns.append((int(g["S1"].notna().sum()), int(g["S2"].notna().sum()),
               int(g["S3"].notna().sum())))
med = np.array(med)
gauche = np.zeros(len(groupes))
for j, (c, lab) in enumerate([(C_PATIENT, "S1 patient\nsymptômes → contact"),
                              (C_PREHOSP, "S2 préhospitalier\ncontact → admission"),
                              (C_CARDIO, "S3 cardiologue\nadmission → guide")]):
    ax1.barh(y, med[:, j], left=gauche, color=c, label=lab, height=.55,
             edgecolor="white")
    for i, v in enumerate(med[:, j]):
        if v > 12:
            txt = f"{v:.0f}" if float(v).is_integer() else f"{v:.1f}".replace(".", ",")
            ax1.text(gauche[i] + v / 2, y[i], txt, ha="center", va="center",
                     color="white", fontweight="bold", fontsize=10.5)
    gauche += med[:, j]
# total = symptomes -> guide, exactement comme le tableau 4 du document Methodes
totaux = [P[P["mode"] == mode]["d_sympto_wire"].median() for mode, _ in groupes]
for i in range(len(groupes)):
    ax1.text(gauche[i] + 6, y[i], f"médiane du total\n{totaux[i]:.0f} min",
             va="center", fontsize=9.5, color="black")
ax1.set_yticks(y)
ax1.set_yticklabels([f"{lab}\n(n = {ns[i][0]})" for i, (_, lab) in enumerate(groupes)])
ax1.set_xlabel("Minutes (médianes de chaque segment)")
ax1.set_xlim(0, gauche.max() * 1.42)
ax1.set_title("Médianes des trois segments, par mode d'entrée")
ax1.legend(loc="upper center", bbox_to_anchor=(.5, -.16), ncol=3, fontsize=9,
           frameon=False)
ax1.text(0, -.42, "La somme des médianes n'est pas la médiane du total : les barres "
                  "se lisent segment par segment.",
         transform=ax1.transAxes, fontsize=9, color=C_GRIS, style="italic")

parts = []
for mode, _ in groupes:
    g = P[P["mode"] == mode].dropna(subset=["S1", "S2", "S3"])
    g = g[g["S1"] >= 0]
    tot = g["S1"] + g["S2"] + g["S3"]
    parts.append([(100 * g["S1"] / tot).median(), (100 * g["S2"] / tot).median(),
                  (100 * g["S3"] / tot).median(), len(g)])
parts = np.array(parts)
gauche = np.zeros(len(groupes))
for j, c in enumerate([C_PATIENT, C_PREHOSP, C_CARDIO]):
    ax2.barh(y, parts[:, j], left=gauche, color=c, height=.55, edgecolor="white")
    for i, v in enumerate(parts[:, j]):
        if v > 6:
            ax2.text(gauche[i] + v / 2, y[i], f"{v:.0f} %", ha="center", va="center",
                     color="white", fontweight="bold", fontsize=10.5)
    gauche += parts[:, j]
ax2.set_yticks(y)
ax2.set_yticklabels([f"n = {int(parts[i, 3])}" for i in range(len(groupes))])
ax2.set_xlabel("Part médiane de chaque segment dans le temps total (%)")
ax2.set_title("Part de chaque segment")
ax2.text(0, -.20, "Les trois parts ne somment pas à 100 % : ce sont trois médianes "
                  "de parts individuelles.", transform=ax2.transAxes,
         fontsize=9, color=C_GRIS, style="italic")
n_g = sum(len(P[P["mode"] == m]) for m, _ in groupes)
fig.suptitle(f"Figure 2 — Où se perdent les minutes ? Décomposition en trois "
             f"segments imputables (n = {n_g})", fontsize=13.5, fontweight="bold",
             y=1.02)
fig.tight_layout()
enregistrer(fig, "figure2")


# ==========================================================================
# FIGURE 3 — DELAIS PAR MODE D'ENTREE x FIBRINOLYSE
# Message : deux axes valent mieux que huit categories.
# ==========================================================================
print("Figure 3 — mode d'entrée x fibrinolyse")
modes = ["appel", "medecin_ville", "selfPresenter_NonPCIcenter",
         "selfPresenter_PCIcenter"]
fig, ax = plt.subplots(figsize=(11.5, 5.4))
x = np.arange(len(modes)); w = .36
for k, (lyse, c, lab) in enumerate([(False, C_CARDIO, "Angioplastie primaire"),
                                    (True, C_ALERTE, "Fibrinolyse")]):
    vals, nn = [], []
    for m in modes:
        s = P[(P["mode"] == m) & (P["lyse"] == lyse)]["d_ecg_wire"].dropna()
        vals.append(s.median() if len(s) else np.nan); nn.append(len(s))
    b = ax.bar(x + (k - .5) * w, vals, w, color=c, label=lab, edgecolor="white")
    for r, v, n in zip(b, vals, nn):
        if not np.isnan(v):
            ax.text(r.get_x() + r.get_width() / 2, v + 3, f"{v:.0f}\n(n={n})",
                    ha="center", va="bottom", fontsize=9.5)
ax.set_ylim(0, 232)
ax.set_xlim(-.65, len(modes) - 1 + 1.05)
xt = len(modes) - 1 + .48
ax.axhline(120, color=C_GRIS, ls="--", lw=1.3)
ax.text(xt, 120, "cible ESC\n≤ 120 min", ha="left", va="center", fontsize=9.5,
        color=C_GRIS)
ax.axhline(90, color=C_GRIS, ls=":", lw=1.3)
ax.text(xt, 88, "cible ESC ≤ 90 min\n(diagnostic hors\ncentre PCI)", ha="left",
        va="top", fontsize=9.5, color=C_GRIS)
ax.set_xticks(x); ax.set_xticklabels([LIB[m] for m in modes], fontsize=10)
ax.set_ylabel("ECG qualifiant → passage du guide (min, médiane)")
ax.set_title("Figure 3 — Horloge de stratégie ESC selon le mode d'entrée "
             "et la stratégie de reperfusion")
ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(.5, -.15),
          ncol=2, fontsize=10)
ax.text(0, -.28, "Chez les patients diagnostiqués AU centre de coronarographie "
                 "(dernier groupe), la cible ESC applicable est ≤ 60 min, pas ≤ 90.",
        transform=ax.transAxes, fontsize=9, color=C_GRIS, style="italic")
fig.tight_layout(); enregistrer(fig, "figure3")


# ==========================================================================
# FIGURE 4 — NOMBRE D'INTERVENANTS x DELAI SYSTEME
# Message : chaque intervenant supplementaire coute des minutes.
# ==========================================================================
print("Figure 4 — nb intervenants x délai système")
cols_int = [c for c in df.columns if c.startswith("intervenant_")]
P["nb_av_salle"] = P[cols_int].apply(
    lambda r: sum(1 for v in r if isinstance(v, str) and v.strip()
                  and "coro" not in v.lower()), axis=1)
niveaux = sorted(P["nb_av_salle"].unique())
donnees = [P[P["nb_av_salle"] == k]["d_systeme_esc"].dropna().values for k in niveaux]
niveaux = [k for k, dd in zip(niveaux, donnees) if len(dd) >= 3]
donnees = [dd for dd in donnees if len(dd) >= 3]
fig, ax = plt.subplots(figsize=(9, 5.2))
bp = ax.boxplot(donnees, patch_artist=True, widths=.55, showfliers=True,
                medianprops=dict(color="black", lw=2),
                flierprops=dict(marker="o", ms=3.5, alpha=.45, mfc=C_GRIS,
                                mec="none"))
for b in bp["boxes"]:
    b.set(facecolor=C_PREHOSP, alpha=.65, edgecolor=C_GRIS)
for i, dd in enumerate(donnees, 1):
    ax.text(i, ax.get_ylim()[1] * .97, f"n = {len(dd)}\nmed {np.median(dd):.0f}",
            ha="center", va="top", fontsize=9.5)
ax.set_xticklabels([str(k) for k in niveaux])
ax.set_xlabel("Nombre d'intervenants AVANT la salle de coronarographie")
ax.set_ylabel("Délai système ESC : contact avec le système → guide (min)")
ax.set_title("Figure 4 — Délai système selon le nombre d'intervenants du parcours")
fig.tight_layout(); enregistrer(fig, "figure4")


# ==========================================================================
# FIGURE 4bis — TEMPS INTRA-HOSPITALIER : annonces vs presentation spontanee
# Message : le resultat le plus actionnable du memoire.
# ==========================================================================
print("Figure 4bis — temps intra-hospitalier")
gA = P[P["mode"] == "appel"]
gB = P[P["mode"] == "selfPresenter_PCIcenter"]
etiquettes = ["Admission → ECG", "Admission → salle", "Salle → guide",
              "Door-to-balloon\n(admission → guide)"]
colonnes = [None, "d_admission_salle", "d_salle_wire", "d_admission_wire"]
vA = [np.nan, gA["d_admission_salle"].median(), gA["d_salle_wire"].median(),
      gA["d_admission_wire"].median()]
vB = [gB["d_ecg_admission"].mul(-1).median(), gB["d_admission_salle"].median(),
      gB["d_salle_wire"].median(), gB["d_admission_wire"].median()]
fig, (axa, axb) = plt.subplots(1, 2, figsize=(13, 5.2),
                               gridspec_kw={"width_ratios": [1.4, 1]})
x = np.arange(len(etiquettes)); w = .36
axa.bar(x - w / 2, vA, w, color=C_CARDIO, label=f"Annoncés par le SAMU (n = {len(gA)})",
        edgecolor="white")
axa.bar(x + w / 2, vB, w, color=C_ALERTE,
        label=f"Présentation spontanée au centre PCI (n = {len(gB)})", edgecolor="white")
for xi, v in zip(x - w / 2, vA):
    if not np.isnan(v):
        axa.text(xi, v + 2, f"{v:.1f}", ha="center", va="bottom", fontsize=10)
for xi, v in zip(x + w / 2, vB):
    if not np.isnan(v):
        axa.text(xi, v + 2, f"{v:.1f}", ha="center", va="bottom", fontsize=10,
                 fontweight="bold")
axa.set_xticks(x); axa.set_xticklabels(etiquettes, fontsize=10)
axa.set_ylabel("Minutes (médiane)")
axa.set_ylim(0, 128)
axa.set_title("Temps écoulé APRÈS l'arrivée dans le même établissement")
axa.legend(fontsize=9.5, frameon=False, loc="upper center",
           bbox_to_anchor=(.5, -.12), ncol=2)
axa.text(0, -.34, "Chez les patients annoncés, l'ECG précède l'admission : "
                    "« admission → ECG » ne s'applique qu'aux présentations spontanées.",
         transform=axa.transAxes, fontsize=9, color=C_GRIS, style="italic")

dtb = P[P["categorie"].isin(["appel", "appel_F"])]["d_admission_wire"].dropna()
n_sup = int((dtb > 30).sum())
axb.bar([0, 1], [100 * (1 - n_sup / len(dtb)), 100 * n_sup / len(dtb)],
        color=[C_CARDIO, C_ALERTE], width=.55, edgecolor="white")
axb.text(0, 100 * (1 - n_sup / len(dtb)) + 1.5,
         f"{100 * (1 - n_sup / len(dtb)):.1f} %\n({len(dtb) - n_sup}/{len(dtb)})",
         ha="center", fontsize=10.5)
axb.text(1, 100 * n_sup / len(dtb) + 1.5,
         f"{100 * n_sup / len(dtb):.1f} %\n({n_sup}/{len(dtb)})", ha="center",
         fontsize=10.5, fontweight="bold")
axb.set_xticks([0, 1]); axb.set_xticklabels(["≤ 30 min", "> 30 min"])
axb.set_ylabel("% des patients régulés par le 15")
axb.set_ylim(0, 75)
axb.set_title("Door-to-balloon des patients régulés\n(seuil 30 min : origine AHA, "
              "pas une cible ESC)", fontsize=11)
n_pile = int((dtb == 30).sum())
axb.text(0, -.20, f"Médiane exactement à 30 min ; {n_pile} patients sont pile sur le "
                  f"seuil — d'où le pourcentage, et jamais la médiane, sur ce point.",
         transform=axb.transAxes, fontsize=9, color=C_GRIS, style="italic")
fig.suptitle("Figure 4bis — Le temps intra-hospitalier, seul segment que la distance "
             "au centre n'explique pas", fontsize=13.5, fontweight="bold", y=1.03)
fig.tight_layout(); enregistrer(fig, "figure4bis")


# ==========================================================================
# FIGURE 5 — LES FIBRINOLYSES
# Message : la lyse est rapide a decider, mais la cible des 10 min est
#           atteinte dans moins d'un cas sur deux.
# ==========================================================================
print("Figure 5 — fibrinolysés")
lyse = P[P["d_ecg_lyse"].notna()]
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 5),
                               gridspec_kw={"width_ratios": [1.3, 1]})
v = lyse["d_ecg_lyse"].dropna()
ax1.hist(v, bins=np.arange(0, max(60, v.max()) + 5, 5), color=C_PREHOSP,
         edgecolor="white")
ax1.set_ylim(0, ax1.get_ylim()[1] * 1.30)
ax1.axvline(10, color=C_ALERTE, ls="--", lw=2)
ax1.annotate("cible ESC ≤ 10 min", xy=(10, ax1.get_ylim()[1] * .93),
             xytext=(42, ax1.get_ylim()[1] * .93), color=C_ALERTE, fontsize=10,
             fontweight="bold", va="center",
             arrowprops=dict(arrowstyle="->", color=C_ALERTE, lw=1.4))
ax1.axvline(v.median(), color="black", ls="-", lw=1.6)
ax1.annotate(f"médiane {v.median():.0f} min", xy=(v.median(), ax1.get_ylim()[1] * .74),
             xytext=(52, ax1.get_ylim()[1] * .74), fontsize=10, va="center",
             arrowprops=dict(arrowstyle="->", color="black", lw=1.2))
ax1.set_xlabel("ECG qualifiant → bolus de fibrinolytique (min)")
ax1.set_ylabel(f"Nombre de patients (n = {len(v)})")
ax1.set_title("Délai de décision de la fibrinolyse")
pct = 100 * (v <= 10).mean()
ax2.bar([0, 1], [pct, 100 - pct], color=[C_CARDIO, C_ALERTE], width=.55,
        edgecolor="white")
for xi, val, nn in [(0, pct, int((v <= 10).sum())), (1, 100 - pct, int((v > 10).sum()))]:
    ax2.text(xi, val + 1.5, f"{val:.1f} %\n({nn}/{len(v)})", ha="center", fontsize=10.5)
ax2.set_xticks([0, 1]); ax2.set_xticklabels(["≤ 10 min", "> 10 min"])
ax2.set_ylabel("% des patients fibrinolysés"); ax2.set_ylim(0, 75)
ax2.set_title("Conformité à la cible ESC")
w2 = P["d_lyse_wire"].dropna()
fig.suptitle(f"Figure 5 — Fibrinolyse : {len(v)} patients, délai bolus → guide médian "
             f"{w2.median():.0f} min", fontsize=13.5, fontweight="bold", y=1.02)
fig.tight_layout(); enregistrer(fig, "figure5")


# ==========================================================================
# FIGURE 6 — CONFORMITE AUX CIBLES
# Message : chaque barre porte sa source ; aucune cible maison.
# ==========================================================================
print("Figure 6 — conformité aux cibles")
pci = P["categorie"] == "selfPresenter_PCIcenter"
cibles = [
    ("FMC → ECG ≤ 10 min", P["d_fmc_ecg"].dropna(), 10, "ESC SCA 2023"),
    ("ECG → guide ≤ 120 min\n(seuil angioplastie vs lyse)", P["d_ecg_wire"].dropna(),
     120, "ESC SCA 2023"),
    ("ECG → guide ≤ 90 min\n(diagnostic hors centre PCI)",
     P[~pci]["d_ecg_wire"].dropna(), 90, "ESC QI 10"),
    ("ECG → guide ≤ 60 min\n(diagnostic au centre PCI)",
     P[pci]["d_ecg_wire"].dropna(), 60, "ESC QI 10"),
    ("ECG → bolus de lyse ≤ 10 min", P["d_ecg_lyse"].dropna(), 10, "ESC SCA 2023"),
]
fig, ax = plt.subplots(figsize=(10.5, 5.6))
y = np.arange(len(cibles))[::-1]
pcts = [100 * (s <= t).mean() for _, s, t, _ in cibles]
b = ax.barh(y, pcts, color=[C_CARDIO if p >= 50 else C_ALERTE for p in pcts],
            height=.55, edgecolor="white")
for yi, p, (lab, s, t, src) in zip(y, pcts, cibles):
    ax.text(p + 1.2, yi, f"{p:.1f} %   (n = {len(s)})", va="center", fontsize=10.5)
ax.set_yticks(y)
ax.set_yticklabels([f"{lab}\n{src}" for lab, _, _, src in cibles], fontsize=9.8)
ax.set_xlim(0, 100); ax.set_xlabel("% de patients atteignant la cible")
ax.set_title("Figure 6 — Conformité aux cibles ESC (recommandations 2023 et "
             "indicateurs de qualité 2025)")
ax.text(0, -.18, "Seuils évalués en inégalité large (≤), conformément à la "
                 "formulation ESC (« maximum time », « within »).\nLe door-to-balloon "
                 "n'apparaît pas : l'ESC ne fixe aucun seuil en minutes sur ce segment "
                 "(QI 13 : rapporter la médiane).",
        transform=ax.transAxes, fontsize=9, color=C_GRIS, style="italic")
fig.tight_layout(); enregistrer(fig, "figure6")


# ==========================================================================
# FIGURE 7 — VIOLIN PLOTS : toute la distribution, extremes compris
# ==========================================================================
print("Figure 7 — distributions")
series = [("Symptômes → contact\n(délai patient)", P["S1"].dropna(), C_PATIENT),
          ("Contact → admission\n(préhospitalier)", P["S2"].dropna(), C_PREHOSP),
          ("Admission → guide\n(door-to-balloon)", P["S3"].dropna(), C_CARDIO),
          ("ECG → guide\n(horloge ESC)", P["d_ecg_wire"].dropna(), C_GRIS)]
fig, ax = plt.subplots(figsize=(13, 6.2))
etiq = []
np.random.seed(0)
parts_v = ax.violinplot([s.values for _, s, _ in series], showextrema=False,
                        widths=.85)
for pc, (_, _, c) in zip(parts_v["bodies"], series):
    pc.set_facecolor(c); pc.set_alpha(.45); pc.set_edgecolor(c)
for i, (lab, s, c) in enumerate(series, 1):
    q1, med, q3 = s.quantile([.25, .5, .75])
    ax.vlines(i, q1, q3, color="black", lw=5, zorder=3)
    ax.plot(i, med, "o", color="white", ms=7, zorder=4, mec="black")
    seuil = q3 + 3 * (q3 - q1)
    out = s[s > seuil]
    ax.plot(np.full(len(out), i) + np.random.uniform(-.06, .06, len(out)), out,
            "o", ms=3.5, color=C_ALERTE, alpha=.8, zorder=5)
    etiq.append(f"{lab}\nn = {len(s)} · médiane {med:.0f} min\n{len(out)} valeurs extrêmes")
ax.set_yscale("symlog", linthresh=60)
ax.set_xticks(range(1, len(series) + 1))
ax.set_xticklabels(etiq, fontsize=9)
ax.set_ylabel("Minutes (échelle log au-delà de 60 min)")
ax.set_title("Figure 7 — Distribution complète des délais : les valeurs extrêmes sont "
             "montrées, jamais retirées")
ax.text(0, -.22, "Points rouges : valeurs > Q3 + 3 IQR. Elles sont réelles et restent "
                 "dans le calcul des médianes.", transform=ax.transAxes, fontsize=9,
        color=C_GRIS, style="italic")
fig.tight_layout(); enregistrer(fig, "figure7")

print("\nTerminé. Toutes les figures sont dans le dossier 'figures/'.")
