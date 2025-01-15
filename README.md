# Tutoriel_MD

## Séquences protéiques de NS4A, NS4B et du précurseur NS4A-2K-NS4B

### Séquence NS4A:
```
GAALGVMDALGTLPGHMTERFQEAIDNLAVLMRAETGSRPYKAAAAQLPETLETIMLLGLLGTVSLGIFFVLMRNKGIGKMGFGMVTLGASAWLMWLSEIEPARIACVLIVVFLLLVVLIPEPEKQR
```

### Séquence NS4B:
```
NELGWLERTKSDIAHLMGRKEEGTTIGFSMDIDLRPASAWAIYAALTTLITPAVQHAVTTSYNNYSLMAMATQAGVLFGMGKGMPFYAWDFGVPLLMIGCYSQLTPLTLIVAIILLVAHYMYLIPGLQAAAARAAQKRTAAGIMKNPVVDGIVVTDIDTMTIDPQVEKKMGQVLLIAVAVSSAVLLRTAWGWGEAGALITAATSTLWEGSPNKYWNSSTATSLCNIFRGSYLAGASLIYTVTRNAGLVKRR
```

### Séquence NS4A-2K-NS4B:
```
GAALGVMDALGTLPGHMTERFQEAIDNLAVLMRAETGSRPYKAAAAQLPETLETIMLLGLLGTVSLGIFFVLMRNKGIGKMGFGMVTLGASAWLMWLSEIEPARIACVLIVVFLLLVVLIPEPEKQRSPQDNQMAIIIMVAVGLLGLITANELGWLERTKSDIAHLMGRKEEGTTIGFSMDIDLRPASAWAIYAALTTLITPAVQHAVTTSYNNYSLMAMATQAGVLFGMGKGMPFYAWDFGVPLLMIGCYSQLTPLTLIVAIILLVAHYMYLIPGLQAAAARAAQKRTAAGIMKNPVVDGIVVTDIDTMTIDPQVEKKMGQVLLIAVAVSSAVLLRTAWGWGEAGALITAATSTLWEGSPNKYWNSSTATSLCNIFRGSYLAGASLIYTVTRNAGLVKRR
```

## Génération des protéines par Alpha Fold 2

Utilisation du Google Colab d'Alpha Fold 2 : [Lien vers ColabFold](https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb#scrollTo=ADDuaolKmjGW)

1. Entrer la séquence protéique souhaitée.
2. Suivre les étapes indiquées dans le Colab.

### Paramètres utilisés :
- **Num_relax**: 1
- **Template_mode**: none
- **Msa_mode**: mmseqs2_uniref_env
- **Pair_mode**: unpaired_paired
- **Model_type**: auto
- **Num_recycles**: auto
- **Recycle_early_stop_tolerance**: auto
- **relax_max_iterations**: 200
- **pairing_strategy**: greedy
- **max_msa**: auto
- **num_seeds**: 1

**Output principal :** Le fichier PDB `unrelaxed_rank_001`, représentant la structure protéique ayant le meilleur score.

## Modifications des structures générées par Alpha Fold 2

Pour NS4A et le précurseur, une étape supplémentaire a été appliquée aux structures protéiques générées par Alpha Fold avant de les intégrer dans une membrane lipidique. En effet, comme nous avions comme information que NS4A est censé posséder ses extrémités N-ter et C-ter du côté cytosol, nous avons ouvert NS4A et le précurseur dans le logiciel Pymol afin de modifier la torsion de la structure protéique générée par Alpha Fold pour qu’elle convienne à ce l’on attendait.

### Modification de NS4A et du précurseur

1. **Utilisation de PyMOL :**
   - Ouvrir le fichier PDB.
   - **Affichage** > Sequence > Sélectionner la séquence à modifier.
   - **Sele** > Action > Drag Coordinates > Ajuster la conformation.
   - **File** > Save Session As.

2. **Minimisation avec GROMACS :**
Il faut ensuite minimiser la nouvelle structure protéique. Nous avons utiliser GROMACS sur un serveur distant pour ceci :
   - Charger GROMACS :
     ```bash
     source /usr/local/gromacs2023.5/bin/GMXRC
     ```
   - Création de la topologie :
     ```bash
     gmx pdb2gmx -f prot.pdb -o prot.gro -p prot.top -i prot.itp
     ```
     > Choisir CHARMM36 pour le champ de forces et TIP3P pour le modèle d'eau.
   - Créer une boîte :
     ```bash
     gmx editconf -f prot.gro -d 1.4 -o prot_box.gro
     ```
   - Ajouter des molécules d'eau :
     ```bash
     gmx solvate -cp prot_box.gro -cs spc216.gro -p prot.top -o prot_water.gro
     ```
   - Minimisation :
  Compilez et construisez le fichier .tpr (le fichier mini.mdp est disponible dans le dossier minimisation de ce répertoire)  :
     ```bash
     gmx grompp -f mini.mdp -c prot_water.gro -p prot.top -o mini.tpr
     gmx mdrun -v -deffnm mini
     ```

     Les nouvelles protéines ainsi créées ont été minimisées à l’aide de GROMACS pour qu’elles soient stables énergétiquement même après que leur structure aient été modifiées. Ainsi l’objectif était de voir si la torsion que l’on imposait se conservait au cours de la modélisation et si elle était dans un niveau favorable d’énergie.


## Utilisation de CHARMM-GUI
Lors de ce projet, nous avons utilisé CHARMM-GUI afin de générer des systèmes protéines-membranes sous format GROMACS. Pour ce faire, nous avons rentré les structures PDB des protéines NS4A et NS4B générées par Alpha Fold dans l’onglet “membrane builder” → “bilayer builder” de CHARMM-GUI.
### Génération d'un système protéine-membrane

1. **Structure PDB de NS4A et NS4B :**
   - Importée dans l'onglet **Membrane Builder**.
   - Paramètres :
     - **pH**: 7
     - **PPM**: 2.0
     - **Hauteur d'eau**: 40
     - Lipides :
       - 14 cholestérols
       - 14 POPS
       - 136 DOPC
       - 136 POPC
       - (pour chaque lipide, la quantité totale est répartie équitablement entre en dessous et au-dessus de la membrane). A noter que pour équilibrer la quantité de matière en dessous et au dessus de la membrane, il a fallu faire des ajustements en faisant passer des lipides au dessous ou au dessus de la membrane. Cette compensation de matière doit être faite lorsque la protéine prend plus de place d’un côté de la membrane que de l’autre.
     - Solvant : NaCl à 0.12 mmol/L.
     - Température : 310.5 K.

2. Pour mettre en place le système avec la membrane lipidique et le précurseur, une autre méthode de CHARMM-GUI a été employée. En effet, étant donné que le précurseur était trop volumineux pour que CHARMM-GUI arrive à créer un système protéine-membrane de lui même, nous avons dû générer la membrane toute seule avec l’aide de CHARMM-GUI, qui a ensuite été minimisé suivant le README contenu dans le dossier Membrane > Gromacs. Puis nous avons placé manuellement le précurseur dans la membrane toute faite, en prenant soin d’enlever tous les atomes et leur molécules correspondantes présents à moins de 3 Angstrom du précurseur nouvellement placé dans la membrane :
Mettre sur un pdb la membrane et la prot (appellée precurseur_mini).
select br. all within 1 of precurseur_mini
select sele and not precurseur_mini
Puis action --> remove atoms.
Regarder le nombre de lipides avec grep wordcount et diviser par le nombre d’atomes du lipide (à trouver dans la topologie) et ajuster dans la topologie.


Enfin, nous avons minimisé le système protéine - membrane grâce à GROMACS afin d’obtenir un système relativement stable (avec le même protocole que dans la partie 1 de ce README).

## Génération des fichiers de modélisation avec GROMACS

Pour générer les fichiers de modélisation, il faut avant tout générer les fichiers .tpr qui permettent de lancer la modélisation.
Protocole pour la préparation et la simulation MD avec GROMACS
1. Copie des fichiers nécessaires

Copier les fichiers nécessaires du répertoire Generate_MD (présent dans ce GitHub) vers le répertoire de travail actuel.
2. Chargement de GROMACS

Charger GROMACS dans l'environnement en exécutant la commande suivante :

source /usr/local/gromacs/bin/GMXRC

3. Génération de la topologie de la protéine

Générer la topologie pour la protéine uniquement à partir du fichier prot.pdb :

gmx pdb2gmx -f prot.pdb -o prot.gro -ter -ignh -p top_prot.top

Sélectionner les options suivantes :

    Topologie CHARMM (option 8).
    Eau TIP3P (option 1).
    Terminaisons NH3+ pour l'extrémité N-terminale et COO- pour l'extrémité C-terminale.

4. Préparation du système dans PyMOL

    Charger le système CHARMM dans PyMOL.
    Remplacer la protéine d'origine (CHARMM) dans la membrane par la structure générée prot.gro.
    Sauvegarder le système complet sous le nom syst.pdb.

5. Conversion du système en fichier .gro

Convertir le fichier syst.pdb en fichier .gro :

gmx editconf -f syst.pdb -o syst.gro

6. Ajustement des dimensions de la boîte

    Supprimer la dernière ligne du fichier syst.gro contenant les dimensions de la boîte.
    Ajouter les dimensions de la boîte provenant du fichier step5_input.gro généré par CHARMM-GUI.

7. Création des index

Créer un fichier d'index pour le système :

gmx make_ndx -n index.ndx -o index.ndx -f syst.gro

Dans l'interface GROMACS, entrer les commandes suivantes :

1  
name 20 SOLU  
13|14|15|16  
name 21 MEMB  
20|21  
17|18|19  
name 22 SOLV  
q  

Note : Adapter les numéros en fonction du système :

    1 correspond à la protéine.
    13/14/15/16 correspond aux lipides (CHL1, DOPC, POPC, POPS).
    17/18/19 correspond aux ions et solvants (SOD, CLA, TIP3).

8. Mise à jour des fichiers de topologie

    Copier le nombre de molécules depuis charmm-gui/topol.top dans le fichier topol.top.
    Copier les contraintes de position (posres) depuis les fichiers CHARMM-GUI vers le fichier topol.top.

9. Minimisation d'énergie et simulations d'équilibrage

    Minimisation d'énergie :

gmx grompp -f em.mdp -o em.tpr -c syst.gro -r syst.gro -p topol.top -n index.ndx  
gmx mdrun -v -deffnm em

    Équilibrages successifs :
    Pour chaque étape d'équilibrage (eq1 à eq6), exécuter les commandes suivantes :

gmx grompp -f eqX.mdp -o eqX.tpr -c prev_eq.gro -r syst.gro -p topol.top -n index.ndx  
gmx mdrun -v -deffnm eqX

    Remplacer eqX par eq1, eq2, ..., eq6.
    Remplacer prev_eq.gro par le fichier .gro généré à l'étape précédente (em.gro, eq1.gro, ...).

10. Production de la dynamique moléculaire

Préparer et exécuter la production de la dynamique moléculaire :

gmx grompp -f md.mdp -o md.tpr -c eq6.gro -t eq6.cpt -p topol.top -n index.ndx  
gmx mdrun -v -deffnm md

Notes importantes

    Vérifier à chaque étape que les fichiers générés sont cohérents.
    Adapter les noms de fichiers et les paramètres en fonction du système et des fichiers .mdp utilisés.
    S'assurer que tous les fichiers nécessaires sont présents dans le répertoire de travail avant de commencer.

Fichiers générés après exécution

    md.tpr : fichier de lancement de la MD contenant les topologies et paramètres.
    index.ndx : fichier d'index par groupes (Protein, SOL, Ion, etc.).
    syst.gro : fichier .gro du système après équilibrage (fichier de départ pour la MD).
    md.edr : fichier contenant les variables thermodynamiques (énergies, température, pression).
    md.xtc : fichier de trajectoire contenant toutes les positions de tous les atomes.
    md.log : fichier de log pour vérifier le déroulement de la MD.

## Analyse de différentes données lors de la modélisation grâce à GROMACS

Au cours des différentes modélisations, plusieurs types de données ont été recueillies pour analyse, en plus de la visualisation de la trajectoire.
1. Écart quadratique moyen (RMSD)

Le RMSD mesure l'écart entre chaque structure de la trajectoire et une structure de référence (la structure initiale ici). Les carbones alpha ont été choisis pour le groupe d’atomes utilisé à la fois pour l'alignement et le calcul.
Commande :

gmx rms -f NS4A.xtc -s NS4A.tpr -o rmsd_NS4A.xvg

2. Fluctuations atomiques (RMSF)

Les fluctuations atomiques renseignent sur la mobilité des atomes autour de leur position d'équilibre. Ici, seule la mobilité des carbones alpha a été calculée.
Commande :

gmx rmsf -f NS4A.xtc -s NS4A.tpr -o rmsf_NS4A.xvg -res

3. Rayon de giration

Le rayon de giration mesure la compacité de la protéine.
Commande :

gmx gyrate -f NS4A.xtc -s NS4A.tpr -o gyrate_NS4A.xvg

4. Carte des structures secondaires au cours de la simulation

Cette étape utilise un fichier au format .dat, qui assigne pour chaque frame les structures secondaires de la protéine (E pour feuillet, H pour hélice, T pour tournant).
À partir de ce fichier et d’un script Python (structure_secondaire.py, présent dans ce GitHub), une carte des structures secondaires a été générée.

Commande pour générer le fichier .dat :

gmx dssp -f NS4A.xtc -s NS4A.tpr -o resdssp -tu ns -hmode dssp

5. Informations thermodynamiques

Ces données permettent d'analyser l'énergie cinétique, potentielle, totale, ainsi que la température et la pression au cours de la modélisation.
Commandes :

    Température :

gmx energy -f NS4A.edr -o temp_NS4A.xvg

Pression :

gmx energy -f NS4A.edr -o pression_NS4A.xvg

Énergie cinétique, potentielle et totale :

    gmx energy -f NS4A.edr -o energy_NS4A.xvg

Visualisation des fichiers générés

Pour ouvrir les fichiers .xvg générés, utiliser la commande suivante dans le terminal :

xmgrace -nxy nom_fichier.xvg

Pré-requis :

    xmgrace doit être installé.
    SSH en mode display (mode X) doit être activé.

Utilisation de VMD
1. Réduction de la trajectoire pour une meilleure manipulation

Pour alléger le temps de chargement de la vidéo, générer une sous-partie de la simulation où seule 1 frame sur 30 est affichée :
Commande :

gmx trjconv -s md.tpr -f md.xtc -o subset -skip 30

2. Chargement dans VMD

Ouvrir le répertoire contenant les fichiers de modélisation avec la commande :

vmd

Note :

    vmd doit être installé.
    SSH en mode display (mode X) doit être activé.

Dans VMD :

    Charger les fichiers :
        File > New Molecule > Browse > Sélectionner votre fichier prot.gro > Load.
        Load Files For > 0:prot.gro > Browse > Sélectionner votre fichier de trajectoire md.xtc > Load.
    Améliorer le chargement :
        Graphics > Representations > Delete Rep.
    Visualisation de la protéine :
        Create Rep > Selected Atoms : protein, Drawing Method : Cartoon.
        Orienter la protéine comme souhaité.
    Visualisation des lipides :
        Create Rep > Selected Atoms : resname POPC, Material : Glass 1, Drawing Method : VDW.

Création d'un film

    Lancer Movie Maker :
    Extensions > Visualization > Movie Maker.

    Configurer les paramètres :
        Movie settings > Trajectory.
        Si la vidéo est trop longue, ajuster le trajectory step size (10-20 secondes est une durée optimale).

    Générer la vidéo :
    Cliquer sur Make Movie.














