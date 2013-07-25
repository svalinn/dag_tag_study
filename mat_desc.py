import string
import os
import sys
from pyne.material import Material
from itaps import iMesh,iBase
from optparse import OptionParser
from pyne.mcnp import Xsdir




def get_tag_values(H5M_Path):
    datafile = H5M_Path

    mesh = iMesh.Mesh()
    mesh.load(datafile)

    ents = mesh.getEntities(iBase.Type.all, iMesh.Topology.triangle)
    #print len(ents)
    mesh_set = mesh.getEntSets()

    tag_values=[]
    found_all_tags=0
    for i in mesh_set:
        if found_all_tags == 1:
	    break

    	# get all the tags
    	tags = mesh.getAllTags(i)
    	# loop over the tags checking for name
    	for t in tags:
            # if we find name
            if t.name == 'NAME':
	        # the handle is the tag name
	        t_handle = mesh.getTagHandle(t.name)
	        # get the data for the tag, with taghandle in element i
	        tag = t_handle[i]
	        a=[]
	        # since we have a byte type tag loop over the 32 elements
	        for part in tag:
	            # if the byte char code is non 0
       	            if (part != 0 ):
	                # convert to ascii
	                a.append(str(unichr(part)))
	                # join to end string
                        test=''.join(a)
			#the the string we are testing for is not in the list of found
			# tag values, add to the list of tag_values
		if not any(test in s for s in tag_values):
	                tag_values.append(test)
			#print test
			# if the tag is called impl_complement, this is the
			# last tag we are done
			if any('impl_complement' in s for s in tag_values):
			        found_all_tags=1
    return tag_values


#def h5m_Get_Mat(H5M_Path):
    #command= "/home/zeineddine/cad_file/moab_tools/retag_mesh/retag_hdf5 "+ H5M_Path
    #CL=commands.getstatusoutput(command);
    #S="".join(CL[1])
    #List= S.split('\n')
    #Mat=List[List.index('OBB 2')+1:]
    #return Mat

    
    
def xsdir_get_iso_lib(xsdirFile,searchIsotope,preferredLibsStr):
    
    # get preferred libraries from input string
    preferredLibs=preferredLibsStr.split()

    
    lib=[]
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Old code to output 'Lib'

    #searchfile = open(file1, "r")
    #searchPhraseDot=searchPhrase + '.'
    

    #for line in searchfile:
        #if searchPhraseDot in line and line.find(searchPhraseDot)==1 or line.find(searchPhraseDot)==0:
	    #LineFound = line
	    #Lib.append(LineFound[LineFound.find(".")+1: LineFound.find(" ",LineFound.find(".")+1 )])
    #------------------------------------------------------------------------------------------------------------




    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # New code using mcnp.Xsdir

    # initialize Xsdir object with iput xsdirFile
    xsFile= Xsdir(xsdirFile)
    # get table of libraries corresponding to search Isotope
    tables=xsFile.find_table(searchIsotope);
    for isoLibValues in tables:
        # extract library from "<XsDirTable: isotope.library>"
	lib.append(isoLibValues.name.split( '.' )[1])
    #------------------------------------------------------------------------------------------------------------ 
    print "Libraries for Isotope: ", searchIsotope, " found are: ", lib

    iso_lib=[]
    if not lib:
        print " Isotope: ", searchIsotope, " has no Libraries found."
	return 0
    elif preferredLibsStr== "None":
	iso_lib=[ searchIsotope, lib[0]]
	print "No preferred Libary, first to find was chosen: ", iso_lib
	return iso_lib
    else:
    	for pLib in preferredLibs:
	    if pLib in lib:
	        iso_lib=[ searchIsotope, pLib]
	        break
	if not iso_lib:
	    print "None of your preferred libraries was found for isotope: ", searchIsotope
	    return 0
	else:
   	    print "To MCNP: ", iso_lib
	    return iso_lib
		
    #searchfile.close()


def main( arguments = None ):

    # Instatiate options parser
    parser = OptionParser\
        (usage='%prog <material description> [options]')

    parser.add_option('-w', dest='xsdir_Path', default=None,\
        help='Path to the XSDIR file, default=%default')

    parser.add_option('-o', dest='H5M_Path', default='None',\
        help='Path to the H5M file, default=%default')

    parser.add_option('-p', dest='preferredLibsStr', default='None',\
        help='string of preffered libraries white space separated. Example: "21c 22c 67c", default=%default')
    OPT, ARG = parser.parse_args()
    
    #XS=XSDIR_Search2(OPT.xsdir_Path)
    mat_list= []
    # get the material list from the '.h5m' file
    mat_list= get_tag_values(OPT.H5M_Path)
    dictionary={}
    mat_comp_list=[]
    
    

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ##### text material file of format: example: #####
    ##### Name    SomeMaterial
    ##### Mass    42
    ##### APerM   1
    ##### H1    0.04
    ##### U238    0.9
    ##### 6012	0.06
   



    # Both .txt or .h5 material files are compatible
    for Mat in mat_list:

    	Path= "tests/Mat_Libs/" + Mat + ".txt"
	try:
    	    mat = Material(Path)
	except:
	    try :
	        Path= "tests/Mat_Libs/" + Mat + ".h5"
	        mat = Material()
	        mat.from_hdf5(Path, "/mat", 1, protocol=0)
	    except:
	        print "The Material file '.h5' or '.txt' for material " , Mat, " was not found"
	        continue
    	# print "Composition of tempate '.h5' or '.text' file: ", Mat, ": ", mat.comp
    	isotopes=[]
	# get isotopes from mat.comp dictionary
    	for key in mat.comp.keys():
	    isotopes.append(str(key))
	# preppend the isotopes with their corresponding material tag in the list
    	isotopes.insert(0, Mat)
    
	# append the new list of Isotopes to Mat_Comp_list
    	mat_comp_list.append(isotopes)

    ####Example: Mat_Comp_list= [ [Mat1, iso1, iso2, iso3], [Mat2 , iso1, iso2 ,iso3], ...]
    print '\n', "list of 'Material,Composition' lists: ", mat_comp_list, '\n'

    for list in mat_comp_list:
	for iso in list:
	    if iso !=list[0]:
	        # get dictionary element for the current isotope in the list
	        resultDictElement=xsdir_get_iso_lib(OPT.xsdir_Path,iso,OPT.preferredLibsStr) 
	        ##### xsdir_get_iso_lib: RETURN example: ['6012', '90y'] if found, 0 if not found
	        print ' '
	        if resultDictElement !=0:
		    dictionary.update({resultDictElement[0]: resultDictElement[1]})
    print ' '
    print "Dictionary: ", dictionary

if __name__ == '__main__':
    main()
