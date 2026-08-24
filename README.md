# STEMI_Pei
Gestion, analyse et visualisation des données pour le projet de recherche STEMI_Pei



# Guide des figures du mémoire

## 1. La règle unique : une figure = un message, et le message est écrit dans le titre

C'est la seule chose à retenir. Une figure de mémoire ou de papier ne sert pas à « montrer les données » : elle sert à **faire passer une phrase**. Si tu ne peux pas écrire cette phrase avant de coder, la figure n'a pas encore de raison d'exister.

Le test, à faire sur chaque figure avant de l'insérer : **montre-la 5 secondes à quelqu'un qui ne connaît pas le sujet, puis demande-lui ce qu'il a compris.** S'il te répond « des barres avec des délais », la figure est ratée. S'il te répond « c'est le transport qui prend le plus de temps », elle est bonne.

Trois conséquences pratiques :

- **Le titre porte la conclusion, pas l'inventaire.** « Figure 2 — Où se perdent les minutes ? Décomposition en trois segments imputables » vaut mieux que « Figure 2 — Délais par catégorie ».
- **Une figure qui dit deux choses doit être coupée en deux**, ou en deux panneaux côte à côte avec un titre chacun.
- **Une figure qui ne dit rien devient un tableau.** Ce n'est pas une punition : un tableau bien fait est souvent plus honnête qu'un graphique décoratif.

---

## 2. Les sept règles de lisibilité, applicables partout

| # | Règle | Pourquoi |
|---|---|---|
| 1 | **Médiane et IQR, jamais moyenne ± écart-type** sur des délais | les délais sont très asymétriques ; une moyenne de délai est tirée par 3 patients |
| 2 | **Le `n` figure sur la figure**, pas seulement dans la légende | tes `n` changent d'une figure à l'autre (264, 258, 248, 226, 204, 192, 129, 68, 38, 22) : le lecteur doit voir lequel il regarde |
| 3 | **Jamais de camembert**, jamais de 3D, jamais d'axe tronqué sur des minutes | l'œil compare mal les angles, très bien les longueurs |
| 4 | **Barres horizontales** dès que les libellés de catégories sont longs | « Présentation spontanée au centre PCI » ne tient pas sous une barre verticale |
| 5 | **Les mêmes trois couleurs pour les trois segments dans tout le mémoire** | le lecteur apprend le code une fois ; ici bleu = patient, orange = préhospitalier, vert = cardiologue |
| 6 | **Chaque seuil affiché porte sa source sur la figure** | « cible ESC 120 min » et pas « objectif » ; un seuil sans source est indéfendable en soutenance |
| 7 | **Écrire la valeur sur la barre** quand il y a moins d'une dizaine de barres | la figure devient lisible sans revenir au texte |


**Deux pièges de ce mémoire en particulier :**

- **La somme des médianes n'est pas la médiane du total.** 45 + 104,5 + 30 = 179,5, mais la médiane du délai total des régulés est 215 min. Une barre empilée de médianes se lit **segment par segment**, jamais comme un total. C'est écrit en note sous la figure 2 — ne l'enlève pas.
- **Une médiane pile sur un seuil ne se commente pas avec une médiane.** Le door-to-balloon médian des régulés est exactement 30,0 min, mais **48,1 % dépassent 30 min** parce que 11 patients sont pile sur le seuil (19 sur l'ensemble des 248). Toujours le pourcentage, jamais « donc un sur deux dépasse ».
- **Les seuils s'affichent « ≤ », jamais « < ».** L'ESC les énonce comme des délais maximaux (« maximum time », « within 10 min »), et c'est ainsi qu'ils sont calculés. Sur cette base, écrire « < » au lieu de « ≤ » ferait passer FMC → ECG de 63,2 % à 49,2 % : 14 points, pour un symbole.

---

## 3. Message des figures

Pour chacune : le **message en une phrase** (c'est ce que tu écriras dans la légende), le **type de graphique et pourquoi celui-là**, et **ce qu'il faut vérifier** avant de l'insérer.

### Figure 1 — Diagramme de flux

**Message.** *De 287 procédures extraites à 264 analysées, en trois exclusions documentées.*
**Type.** Boîtes et flèches verticales, exclusions à droite. Format imposé par l'usage (STROBE) — ne pas inventer.
**À vérifier.** Que la somme des exclusions tombe juste : 287 − 14 − 3 − 2 = 268, puis − 4 = 264. Et que Vincent Piarrou-Cazala t'ait confirmé les trois motifs par écrit.
**Piège.** Les 4 patients > 24 h **sortent de l'analyse principale, ils ne sortent pas de l'étude** : ils sont comptés à part et ce sont eux le vivier du volet qualitatif. Deux flèches distinctes, deux libellés distincts.

### Figure 3 — Les trois segments imputables ⭐ **C'est LA figure du mémoire**

**Message.** *Chez les patients régulés, plus de la moitié du temps se perd en préhospitalier ; chez ceux qui passent par un médecin de ville, il se perd avant même le premier contact.*
**Type.** Deux panneaux : à gauche des **barres empilées horizontales** en minutes, à droite les **parts en %**. Empilé parce que les trois segments sont additifs et sans trou : c'est exactement ce que le lecteur doit voir.
**À vérifier.** Les trois parts ne somment pas à 100 % — ce sont trois médianes de parts individuelles. La note sous la figure le dit ; elle est obligatoire.
**Si tu ne devais garder qu'une figure, c'est celle-là.** Elle répond à la question du mémoire en une image.


---

## 4. La grille d'auto-vérification, à passer sur chaque figure avant de l'insérer

Coche les huit lignes. Une seule non cochée = la figure retourne à l'atelier.

1. Je peux écrire le message de la figure en **une phrase**, et cette phrase est dans le titre.
2. Le **`n`** est visible sur la figure, et c'est le bon `n` pour ce que je montre.
3. Tout **seuil affiché porte sa source** (ESC 2023, ESC QI 10, AHA…).
4. J'ai utilisé **médiane et IQR**, pas moyenne et écart-type.
5. Les **couleurs sont les mêmes** que dans les autres figures du mémoire.
6. La figure reste lisible **imprimée en noir et blanc** et **réduite à la moitié de sa taille**.
7. Aucun chiffre de la figure n'est saisi à la main : **tout vient du script**.
8. Le chiffre de la figure est **identique** au chiffre du même indicateur dans le texte et dans les tableaux. *(C'est le contrôle qui rattrape le plus d'erreurs.)*
