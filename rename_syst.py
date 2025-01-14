# -*- coding: utf-8 -*-

#####################################################################################
##### Rename the atoms of a protein in a system.gro file, as in an itp file #########
##### When the atoms in the gro file are in the same order as in the itp file #######
#####################################################################################



############## import ############
import sys
import os


############## Function #################

def rename_syst(original_gro,litp):
	'''itp = names of the itp files for each protein chain, in the same order as in gro, separated with ","'''

	i=open(original_gro,"r")
	f=open("file2","w")

	
	#make a list with the atoms of each itp file
	atoms=[]
	
	litp=litp.split(",")

	for fitp in litp:
	
		j=open(fitp,"r")

		#read the [ atoms ] part of the itp file 
		#read before [ atoms ] starts
		tabs=[0,1]
		while tabs[1]!= "atoms":
			line=j.readline()
			tabs=line.split()
			if len(tabs)==0 or len(tabs)==1: #if empty line or with only one element
				tabs=[0,1]

		j.readline()
		line=j.readline()
		tabs=line.split()
		
		#read [ atoms ] section
		n=1 #to read only lines with atoms
		while len(tabs)!=0:
			if tabs[0]==str(n):
				atoms.append(tabs[4])
				n+=1
				
			line=j.readline()
			tabs=line.split()

        
	#rename gro file
	n=0
	for line in i.readlines():
		tabs=line.split()
		if tabs[0][-3:] in ('VAL', 'ILE', 'LEU', 'GLU', 'GLN', 'GLY', 'PRO', 'ASP', 'ASN', 'HIS', 'TRP', 'PHE', 'TYR', 'CYS','ARG', 'LYS', 'SER', 'THR', 'MET', 'ALA','HSD','HSE','HIE','HID'):
			tabs[1]=atoms[n]
			
			#.gro file format: for each row, 8,7, 5, 8, 8 and 8 characters
			#adds the number of spaces needed to respect the format
			spaces1=" "*(8-len(tabs[0]))
			spaces2=" "*(7-len(tabs[1]))
			spaces3=" "*(5-len(tabs[2]))
			spaces4=" "*(8-len(tabs[3]))
			spaces5=" "*(8-len(tabs[4]))
			spaces6=" "*(8-len(tabs[5]))

			#writes the line with the new compound name and right number of spaces
			new_line=spaces1+tabs[0]+spaces2+tabs[1]+spaces3+tabs[2]+spaces4+tabs[3]+spaces5+tabs[4]+spaces6+tabs[5]+"\n"
			f.write(new_line)
			n+=1
			
		else:
			f.write(line)
			
			
			
			
	os.rename("file2",original_gro)
				
	
	i.close()
	j.close()
	f.close()


############## Main #################
rename_syst(sys.argv[1],sys.argv[2])

