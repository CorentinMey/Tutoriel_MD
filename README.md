# Tutoriel_MD

## Séquences protéiques de NS4A, NS4B et du précurseur NS4A-2K-NS4B

### Séquence NS4A:
 
GAALGVMDALGTLPGHMTERFQEAIDNLAVLMRAETGSRPYKAAAAQLPETLETIMLLGLLGTVSLGIFFVLMRNKGIGKMGFGMVTLGASAWLMWLSEIEPARIACVLIVVFLLLVVLIPEPEKQR
 
### Séquence NS4B:
 
NELGWLERTKSDIAHLMGRKEEGTTIGFSMDIDLRPASAWAIYAALTTLITPAVQHAVTTSYNNYSLMAMATQAGVLFGMGKGMPFYAWDFGVPLLMIGCYSQLTPLTLIVAIILLVAHYMYLIPGLQAAAARAAQKRTAAGIMKNPVVDGIVVTDIDTMTIDPQVEKKMGQVLLIAVAVSSAVLLRTAWGWGEAGALITAATSTLWEGSPNKYWNSSTATSLCNIFRGSYLAGASLIYTVTRNAGLVKRR
 
### Séquence NS4A-2K-NS4B:
 
GAALGVMDALGTLPGHMTERFQEAIDNLAVLMRAETGSRPYKAAAAQLPETLETIMLLGLLGTVSLGIFFVLMRNKGIGKMGFGMVTLGASAWLMWLSEIEPARIACVLIVVFLLLVVLIPEPEKQRSPQDNQMAIIIMVAVGLLGLITANELGWLERTKSDIAHLMGRKEEGTTIGFSMDIDLRPASAWAIYAALTTLITPAVQHAVTTSYNNYSLMAMATQAGVLFGMGKGMPFYAWDFGVPLLMIGCYSQLTPLTLIVAIILLVAHYMYLIPGLQAAAARAAQKRTAAGIMKNPVVDGIVVTDIDTMTIDPQVEKKMGQVLLIAVAVSSAVLLRTAWGWGEAGALITAATSTLWEGSPNKYWNSSTATSLCNIFRGSYLAGASLIYTVTRNAGLVKRR


## Génération des protéines par Alpha Fold 2

Utilisation du google colab d'Alpha Fold 2 : https://colab.research.google.com/github/sokrypton/ColabFold/blob/main/AlphaFold2.ipynb#scrollTo=ADDuaolKmjGW

Rentrer la séquence protéique de la protéine dont on souhaite synthétiser la structure dans le colab, puis suivre les différentes étapes.

### Paramètres utilisés dans notre projet :
Num_relax=1
Template_mode=none
Msa_mode=mmseqs2_uniref_env
Pair_mode=unpaired_paired
Model_type=auto
Num_recycles=auto
Recycle_early_stop_tolerance=auto
relax_max_iterations:200
pairing_strategy:greedy
max_msa=auto
num_seeds=1

On obtient en output un ensemble de fichiers créés par Alpha Fold. Le fichier gardé pour la suite des analyses est le fichier PDB "unrelaxed_rank_001", qui correspond à la structure protéique générée avec le meilleur score.

## Modifications de la structure des protéines générées par Alpha Fold 2

Pour NS4A et le précurseur, une étape supplémentaire a été appliquée aux structures protéiques générées par Alpha Fold avant de les intégrer dans une membrane lipidique. En effet, comme nous avions comme information que NS4A est censé posséder ses extrémités N-ter et C-ter du côté cytosol, nous avons ouvert NS4A et le précurseur dans le logiciel Pymol afin de modifier la torsion de la structure protéique générée par Alpha Fold pour qu’elle convienne à ce l’on attendait.

Pour ce faire, ouvrir le fichier PDB de la protéine souhaitée, puis :
Display > Sequence > Sélectionner manuellement la séquence dont on veut changer la conformation > Sele > Action > Drag Coordinates > mouvoir la séquence pour l'agencer comme on le souhaite > File > Save Session As 

Il faut ensuite minimiser la nouvelle structure protéique. Nous avons utiliser GROMACS sur un serveur distant pour ceci :

source /usr/local/gromacs2023.5/bin/GMXRC 
### 1.1 Création de la topologie
Créez une topologie (qui contient l’ensemble des paramètres pour calculer l’énergie) avec la commande
suivante :
gmx pdb2gmx -f prot.pdb -o prot.gro -p prot.top -i prot.itp
Entrez le numéro correspondant au champ de forces (CHARMM36) lorsque le programme vous le
demande, puis entrez le choix du modèle d’eau (TIP3P).

### 1.2 Élargissement de la boite
gmx editconf -f prot.gro -d 1.4 -o prot_box.gro

### 1.3 Solvatation de la protéine
Dans un premier temps, remplissez l’espace vide de la boite de simulation avec des molécules d’eau :
gmx solvate -cp prot_box.gro -cs spc216.gro -p prot.top -o prot_water.gro
Le programme genbox ajoute des molécules d’eau explicites autour de la protéine. Vérifiez à la fin du
nouveau fichier .top que le choix du champ de forces (CHARMM36) et du modèle d’eau (TIP3P) ont bien
été pris en compte et que votre système contient maintenant la protéine et un certain nombre de
molécules d’eau (notez le nombre de molécules d’eau).

### 1.4 Minimisation
Compilez et construisez le fichier .tpr (le fichier mini.mdp est disponible dans le dossier minimisation de ce répertoire)  :
gmx grompp -f mini.mdp -c prot_water.gro -p prot.top -o mini.tpr
Lancez la minimisation (à partir du fichier mini.tpr généré précédemment) :
gmx mdrun -v -deffnm mini

Les nouvelles protéines ainsi créées ont été minimisées à l’aide de GROMACS pour qu’elles soient stables énergétiquement même après que leur structure aient été modifiées. Ainsi l’objectif était de voir si la torsion que l’on imposait se conservait au cours de la modélisation et si elle était dans un niveau favorable d’énergie.

## Utilisation de CHARMM-GUI

Lors de ce projet, nous avons utilisé CHARMM-GUI afin de générer des systèmes protéines-membranes sous format GROMACS. Pour ce faire, nous avons rentré les structures PDB des protéines NS4A et NS4B générées par Alpha Fold dans l’onglet “membrane builder” → “bilayer builder” de CHARMM-GUI. Nous avons ensuite suivi les étapes proposées par la plateforme Web, tout en spécifiant les paramètres suivants : 
pH 7
PPM 2.0
Hauteur de l’eau au dessus de la membrane : 40
14 cholestérols, 14 de POPS (lipide anionique), 136 de DOPC et 136 de POPC. (pour chaque lipide, la quantité totale est répartie équitablement entre en dessous et au-dessus de la membrane). A noter que pour équilibrer la quantité de matière en dessous et au dessus de la membrane, il a fallu faire des ajustements en faisant passer des lipides au dessous ou au dessus de la membrane. Cette compensation de matière doit être faite lorsque la protéine prend plus de place d’un côté de la membrane que de l’autre.
Solvant : NaCl à 0.12 mmol/L
Température du système: 310.5 Kelvin.
Pour mettre en place le système avec la membrane lipidique et le précurseur, une autre méthode de CHARMM-GUI a été employée. En effet, étant donné que le précurseur était trop volumineux pour que CHARMM-GUI arrive à créer un système protéine-membrane de lui même, nous avons dû générer la membrane toute seule avec l’aide de CHARMM-GUI, qui a ensuite été minimisé suivant le README contenu dans le dossier Membrane > Gromacs. Puis nous avons placé manuellement le précurseur dans la membrane toute faite, en prenant soin d’enlever tous les atomes et leur molécules correspondantes présents à moins de 3 Angstrom du précurseur nouvellement placé dans la membrane :
Mettre sur un pdb la membrane et la prot.
select br. all within 1 of precurseur_mini
select sele and not precurseur_mini
Puis action --> remove atoms.
Regarder le nombre de lipides avec grep wordcount et diviser par le nombre d’atomes du lipide (à trouver dans la topologie) et ajuster dans la topologie.


Enfin, nous avons minimisé le système protéine - membrane grâce à GROMACS afin d’obtenir un système relativement stable (avec le même protocole que dans la partie 1 de ce README).

## Génération des fichiers de modélisation grâce à GROMACS






