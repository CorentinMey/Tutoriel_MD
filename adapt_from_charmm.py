# -*- coding: utf-8 -*-

###########################################################################
##### Adapts topology from gromacs with given system from Charmm #########
#### Adds the pos_res from proteins given by charmm to itps from gromacs #
##########################################################################


############## import ############
import sys
import os


############## Function #################

def posres(itp_charmm,posre_gromacs):
	'''itp = names of the itp files for each protein chain, from charmm, separated with ","
	posre_gromacs = names of the posre_itp files from gromacs, separated with ",", in the same order as the itps from charmm '''
	
	itp_c=itp_charmm.split(",")
	posre=posre_gromacs.split(",")
	
	#for each protein chain
	
	for i in range(0,len(itp_c)):
	
		itp=open(itp_c[i],"r")
		p=open(posre[i],"r")
		f=open("file2","w")
		
		#copy the beginning of the gromacs posre file
		tabs=[0,1]
		while tabs[1]!= "position_restraints":
			line=p.readline()
			f.write(line)
			tabs=line.split()
			if len(tabs)==0 or len(tabs)==1: #if empty line or with only one element
				tabs=[0,1]

		line=p.readline()
		f.write(line)

		#copy the posres from charmm
		
		#read the [ position_restraints ] part of the itp file 
		#read before part starts
		tabs=[0,1]
		while tabs[1]!= "position_restraints":
			line=itp.readline()
			tabs=line.split()
			if len(tabs)==0 or len(tabs)==1: #if empty line or with only one element
				tabs=[0,1]
				
		line=itp.readline()
		tabs=line.split()

		#copy [ position_restraints ] section
		while len(tabs)==5:	
			f.write(line)			
			line=itp.readline()
			tabs=line.split()
			
	
		os.rename("file2",posre[i])
				
		itp.close()
		p.close()
		f.close()



############## Function #################

def top_charmm(top_charmm,top_cop,itp_gro,lipids):
	'''topology from charmm and topology to copy
	itp_gro=names of the itps for each protein chain, from gromacs, separated with "," '''
	
	itp_g=itp_gro.split(",")
	lip=lipids.split(",")
	
	top_c=open(top_charmm,"r")
	top=open(top_cop,"r")
	f=open("file2","w")
		
	#copy the beginning of the top file
	tabs=[0,1,2]
	while tabs[1]!= "Include" or tabs[2]!= "protein":
		line=top.readline()
		f.write(line)
		tabs=line.split()
		if len(tabs)==0 or len(tabs)==1: #if empty line or with only one element
			tabs=[0,1,2]

	line=top.readline()
	
	#include the protein chain
	for prot in itp_g:
		f.write("#include \""+prot+"\"\n")
	
	f.write("\n")
	f.write("; Include lipids topology\n")
	
	for lipid in lip:
		f.write("#include \""+lipid+"\"\n")

	f.write("\n")
		
	#copy from #include water topology to [ molecules ]
	tabs=[0,1,2]
	while tabs[1]!= "Include" or tabs[2]!= "water":
		line=top.readline()
		tabs=line.split()
		if len(tabs)==0 or len(tabs)==1: #if empty line or with only one element
			tabs=[0,1,2]
				

	while tabs[1]!= "molecules":	
		f.write(line)			
		line=top.readline()
		tabs=line.split()
		if len(tabs)==0 or len(tabs)==1: #if empty line or with only one element
			tabs=[0,1]

	f.write(line)
	line=top.readline()
	f.write(line)

	#copy the molecule section from the charmm topology and modify the name of the chains
	tabs=[0,1]
	while tabs[1]!= "molecules":
		line=top_c.readline()
		tabs=line.split()
		if len(tabs)==0 or len(tabs)==1: #if empty line or with only one element
			tabs=[0,1]

	line=top_c.readline()
	
	#check where name of the chain starts in the title of top.top file
	for i in range (0,len(itp_g[0])):
		if itp_g[0][i]=="P" and itp_g[0][i+1]=="r" and itp_g[0][i+2]=="o" and itp_g[0][i+3]=="t" and itp_g[0][i+4]=="e" and itp_g[0][i+5]=="i" and itp_g[0][i+6]=="n": 
			s=i
			
	for prot in itp_g:
		line=top_c.readline()
		tabs=line.split()
		tabs[0]=prot[s:-4]
		line="	".join(tabs)
		f.write(line+"\n")
	
	for line in top_c.readlines():
		f.write(line)	
		

	os.rename("file2",top_cop)
				
	top_c.close()
	top.close()
	f.close()


############## Main #################
posres(sys.argv[1],sys.argv[2])
top_charmm(sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
