from optparse import OptionParser
import commands
import os, sys
from pyne.material import Material

def h5m_Get_Mat(H5M_Path):
    command= "/home/zeineddine/cad_file/moab_tools/retag_mesh/retag_hdf5 "+ H5M_Path
    CL=commands.getstatusoutput(command);
    S="".join(CL[1])
    List= S.split('\n')
    Mat=List[List.index('OBB 2')+1:]
    return Mat

def XSDIR_Search(file1,searchPhrase,preferredLibsStr):
    preferredLibs=preferredLibsStr.split()
    searchfile = open(file1, "r")
    searchPhraseDot=searchPhrase + '.'
    Lib=[]

    for line in searchfile:
        if searchPhraseDot in line and line.find(searchPhraseDot)==1 or line.find(searchPhraseDot)==0:
      LineFound = line
	    Lib.append( LineFound[LineFound.find(".")+1:LineFound.find(" ",LineFound.find(".")+1 )] )
    print "Libraries for Isotope: ", searchPhrase, " found are: ", Lib
    Iso_Lib=[]

    if not Lib:
	print " Isotope: ", searchPhrase, " has no Libraries found."
	return 0
    elif preferredLibsStr== "None":
	Iso_Lib=[ searchPhrase, Lib[0]]
	print "No preferred Libary, first to find was chosen: ", Iso_Lib
	return Iso_Lib
    else:
    	for PLib in preferredLibs:
		if PLib in Lib:
			Iso_Lib=[ searchPhrase, PLib]
			break
	if not Iso_Lib:
		print "None of your preferred libraries was found for isotope: ", searchPhrase
		return 0
	else:
   		print "To MCNP: ", Iso_Lib
		return Iso_Lib
		
    searchfile.close()


def main( arguments = None ):

    #Instatiate options parser
    parser = OptionParser\
        (usage='%prog <flux mesh> [options]')

    parser.add_option('-w', dest='xsdir_Path', default=None,\
        help='Path to the XSDIR file, default=%default')

    parser.add_option('-o', dest='H5M_Path', default='None',\
        help='Path to the H5M file, default=%default')

    parser.add_option('-p', dest='preferredLibsStr', default='None',\
        help='string of preffered libraries white space separated. Example: "21c 22c 67c", default=%default')
    OPT, ARG = parser.parse_args()
    
    Mat_list= []
    Mat_list= h5m_Get_Mat(OPT.H5M_Path)
    Dictionary={}
    Mat_Comp_List=[]
    
    

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Reading '.h5' file to extract isotopes of the material
    #mat = Material()
    #mat.from_hdf5("/home/zeineddine/PYNE/Pyne/pyne-pyne-e14f89d/pyne/tests/mat.h5", "/mat", 1, protocol=0)
    #-------------------------------------------------------------------------------------------------------------------------

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ##### Or directly Read a text file of format: example: #####
    ##### Name    SomeMaterial
    ##### Mass    42
    ##### APerM   1
    ##### H1    0.04
    ##### U238    0.9
    ##### 6012	0.06
   




    ##### Both .txt or .h5 are compatible
    for Mat in Mat_list:

    	Path= "/home/zeineddine/Mat_Libs/" + Mat + ".txt"
	try:
    		mat = Material(Path)
	except:
		try :
			Path= "/home/zeineddine/Mat_Libs/" + Mat + ".h5"
			mat = Material()
			mat.from_hdf5(Path, "/mat", 1, protocol=0)
		except:
			print "The Material file '.h5' or '.txt' for material " , Mat, " was not found"
			continue
    	#print "Composition of tempate '.h5' or '.text' file: ", Mat, ": ", mat.comp
    	Isotopes=[]
    	for key in mat.comp.keys():
		Isotopes.append(str(key))
    	Isotopes.insert(0,Mat)
    
    	Mat_Comp_List.append(Isotopes)

    ####Example: Mat_Comp_list= [ [Mat1, iso1, iso2, iso3], [Mat2 , iso1, iso2 ,iso3], ...]
    print '\n', "list of 'Material,Composition' lists: ", Mat_Comp_List, '\n'





    for list in Mat_Comp_List:
	for iso in list:
		if iso !=list[0]:
			ResultDictElement=XSDIR_Search(OPT.xsdir_Path,iso,OPT.preferredLibsStr) 
			##### XSDIR_Search: RETURN example: ['6012', '90y'] if found, 0 if not found
			if ResultDictElement !=0:
				Dictionary.update({ResultDictElement[0]:ResultDictElement[1]})
    print '\n'
    print "Dictionary: ", Dictionary

if __name__ == '__main__':
    main()
