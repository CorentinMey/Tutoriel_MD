
﻿#########################################################################
#### Run this script in the terminal for an MD of a protein in membrane #
#########################################################################


######## You need ############
# - From Charmm-Gui: the file of your system called syst.gro (that you already equilibrated), itps from the protein chains, topol.top
# - prot.pdb, with all H and no missing atoms and clean, the same used to build the system in charmm-gui
# - MD files of this folder, with adapted mdp parameters, and itps of the lipids in syst.gro
# - If you have a phosphorylated residue: in the pdb file, rename by hand SER SP1 or SP2, THR THP1 or THP2, or TYR TP1 or TP2. (1 for protonated P, 2 for O-)
#	Then copy residuetypes.dat from the gromacs file (usually in usr/local/gromacs/share/gromacs/top/) into your working directory.
#	Add the following lines to the dat file: "SP1	Protein", "SP2	Protein", etc 
# - check the gmx make_ndx command and the following parameters

######## Parameters ############
topol="charmm-gui/gromacs/topol.top" #the topology file from Charmm Gui
itps_charmm="charmm-gui/gromacs/toppar/PROA.itp","charmm-gui/gromacs/toppar/PROB.itp" #names of itps for each protein chain, from Charmm Gui, separated with ","
lipids="POPC.itp","DOPC.itp","CHL1.itp" #names of lipids itp files, (in the same order as in system.gro), separated with ","
dimer=true #if protein is a dimer then = true

#to check after pdb2gmx command:
itps_gromacs="top_prot_Protein_chain_A.itp","top_prot_Protein_chain_B.itp" #names of itps for each protein chain, from gromacs (in the same order as in system.gro), separated with ","
posre_gromacs="posre_Protein_chain_A.itp","posre_Protein_chain_B.itp" #names of posre_itps for each protein chain, from gromacs, (in the same order as in itps_gromacs) separated with ","

### If you add the protein by hand in the membrane:
lipids=(POPC DOPC POPS SAPI) #names of the lipids in syst_charmm.pdb, in one string separated with one space
atom_number_lipid=(134 138 127 146) #number of beads for each lipid listed in "lipids", in the respective order
solute=(TIP3 CLA SOD) #names of the solvents in syst_charmm.pdb, in one string separated with " "
atom_number_sol=(3 1 1) #number of beads for each solute listed in "solute", in the respective order



######## Main ############

source /usr/local/gromacs/bin/GMXRC


#get topology of the protein
if [ "$dimer" = false ] ; then echo -e "8 \n 1 \n 0 \n 0 \n" | gmx pdb2gmx -f prot.pdb -o prot.gro -ter -ignh -p top_prot.top; else echo -e "8 \n 1 \n 0 \n 0 \n 0 \n 0 \n" | gmx pdb2gmx -f prot.pdb -o prot.gro -ter -ignh -p top_prot.top; fi
#CHARMM, TIP3P, NH3+, COO-, #NH2+ if Proline
#sometimes replace with: -e "8 \n 1 \n 1 \n 0 \n"
#or if dimer -e "8 \n 1 \n 1 \n 0 \n 1 \n 0 \n"

#make index:
echo -e "1 \n name 19 SOLU \n 13|14|15 \n name 20 MEMB \n 19|20 \n 16|17|18 \n name 22 SOLV \n q \n" | gmx make_ndx -f syst.gro -o index.ndx
#Protein = SOLU, DOPC_POPC_CHOL = MEMB, CLA_SOD_TIP3 = SOLV
#OR
#echo -e "1 \n name 18 SOLU \n 13|14 \n name 19 MEMB \n 18|19 \n 15|16|17 \n name 21 SOLV \n q \n" | gmx make_ndx -f syst.gro -o index.ndx
#DOPC_POPC=MEMB

#adapt topol.top, copy posres from PROA/PROB and rename atoms in syst.gro
python3 adapt_from_charmm.py $itps_charmm $posre_gromacs $topol "topol.top" $itps_gromacs $lipids
python3 rename_syst.py "syst.gro" $itps_gromacs

#OR do as in run_CG_mb.sh to add the protein in the membrane by hand 

#Minimization
gmx grompp -f em.mdp -o em.tpr -c syst.gro -r syst.gro -p topol.top -n index.ndx
gmx mdrun -v -deffnm em

#NVT and NPT equilibrations and production
gmx grompp -f eq1.mdp -o eq1.tpr -c em.gro -r syst.gro -p topol.top -n index.ndx
gmx mdrun -v -deffnm eq1
gmx grompp -f eq2.mdp -o eq2.tpr -c eq1.gro -r syst.gro -p topol.top -n index.ndx
gmx mdrun -v -deffnm eq2
gmx grompp -f eq3.mdp -o eq3.tpr -c eq2.gro -r syst.gro -p topol.top -n index.ndx
gmx mdrun -v -deffnm eq3
gmx grompp -f eq4.mdp -o eq4.tpr -c eq3.gro -r syst.gro -p topol.top -n index.ndx
gmx mdrun -v -deffnm eq4
gmx grompp -f eq5.mdp -o eq5.tpr -c eq4.gro -r syst.gro -p topol.top -n index.ndx
gmx mdrun -v -deffnm eq5
gmx grompp -f eq6.mdp -o eq6.tpr -c eq5.gro -r syst.gro -p topol.top -n index.ndx
gmx mdrun -v -deffnm eq6
gmx grompp -f md.mdp -o md.tpr -c eq6.gro -t eq6.cpt -p topol.top -n index.ndx


echo -e "Protein \n SOLU_MEMB \n" | gmx trjconv -s md.tpr -f eq6.gro -o eq6_centered_noWater.gro -pbc mol -center -n index.ndx

#Then run the production on an adapted GPU

