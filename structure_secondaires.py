import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Chemin vers le fichier .dat
data_file = "resdssp_NS4A.dat"

# Chargement des données
data = []
with open(data_file, 'r') as f:
    for line in f:
        line = line.strip()  # Supprime les espaces ou sauts de ligne
        if line:  # Ignore les lignes vides
            data.append(list(line))  # Convertit chaque caractère en un élément de liste

# Création du DataFrame
df = pd.DataFrame(data)
print("Aperçu des données chargées :")
print(df.head())  # Vérifie les premières lignes

# Mappage des structures secondaires en valeurs numériques
structure_map = {
    'H': 1,  # Hélice
    'E': 2,  # Feuillet
    # Tout le reste sera regroupé dans "Autres"
}

# Fonction pour regrouper les autres structures
def map_structure(char):
    return structure_map.get(char, 3)  # 3 représente les "Autres"

# Conversion des caractères en valeurs numériques
df_numeric = df.applymap(map_structure)

from matplotlib.colors import ListedColormap

# Définir une palette personnalisée
colors = ['green', 'orange', 'yellow']  # Rouge pour H, bleu pour E, gris pour Autres
cmap = ListedColormap(colors)

# Création de la heatmap avec la palette personnalisée
plt.figure(figsize=(12, 8))
sns.heatmap(
    df_numeric,
    cmap=cmap,
    cbar_kws={'label': 'Structure secondaire (1: Hélice, 2: Feuillet, 3: Autres)'}
)
plt.xlabel("Résidus")
plt.ylabel("Frames")
plt.title("Suivi des structures secondaires (Hélices, Feuillets, Autres)")
plt.show()
