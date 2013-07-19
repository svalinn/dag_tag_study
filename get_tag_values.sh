#!/usr/bin/python 

from itaps import iMesh,iBase
import string

datafile = "bllitebm01det21.h5m"

mesh = iMesh.Mesh()
mesh.load(datafile)

#ents = mesh.getEntities()
ents = mesh.getEntities(iBase.Type.all, iMesh.Topology.triangle)
print len(ents)
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
	    # the the string we are testing for is not in the list of found
	    # tag values, add to the list of tag_values
	    if not any(test in s for s in tag_values):
		    tag_values.append(test)
		    print test
		    # if the tag is called impl_complement, this is the 
		    # last tag we are done
		    if any('impl_complement' in s for s in tag_values):
			    found_all_tags=1
	

	     