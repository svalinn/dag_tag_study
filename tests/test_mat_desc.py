import nose 

from nose.tools import assert_equal, assert_not_equal, assert_raises, raises, assert_in

from pyne import nucname
from mat_desc import get_tag_values, xsdir_get_iso_lib

def test_get_tag_values1():
    assert_equal(get_tag_values('Form14.h5m'), ['m_2_rho_0.09', 'tally_0.cell.flux.n', 'm_1_rho_-8.8'])

def test_get_tag_values2():
    assert_equal(get_tag_values('Form20.h5m'), ['M_5_TorusPrism_9', 'imp_4Beryllium', '91_2Steel_3'])

def test_get_tag_values3():
    assert_equal(get_tag_values('Form10.h5m'), ['MAT_SphereCylinder', '31_2_6S_BORON^Steel', '91_2Steel_3', 'tally_<iit>_MAT.He', '.34Lithium', '31_2*6S*Water@Steel', '31_2Boron', 'M_5_TorusPrism_9'])

def test_xsdir_get_iso_lib1():
    assert_equal(xsdir_get_iso_lib('xsdirtemp', '922350',"None" ), ['922350', '67y'])

def test_xsdir_get_iso_lib2():
    assert_equal(xsdir_get_iso_lib('xsdirtemp', '922380',"None" ), ['922380', '22c'])

def test_xsdir_get_iso_lib3():
    assert_equal(xsdir_get_iso_lib('xsdirtemp', '2003',"None" ), ['2003', '21c'])

def test_xsdir_get_iso_lib4():
    assert_equal(xsdir_get_iso_lib('xsdirtemp', '922350',"21c 22c 67y" ), ['922350', '21c'])

def test_xsdir_get_iso_lib5():
    assert_equal(xsdir_get_iso_lib('xsdirtemp', '922380',"21c 22c 67y" ), ['922380', '21c'])

def test_xsdir_get_iso_lib6():
    assert_equal(xsdir_get_iso_lib('xsdirtemp', '2003',"24y 22c 67y" ), ['2003', '24y'])

def test_xsdir_get_iso_lib7():
    assert_equal(xsdir_get_iso_lib('xsdirtemp', '922350',"" ), 0)

def test_xsdir_get_iso_lib8():
    assert_equal(xsdir_get_iso_lib('xsdirtemp', '992233',"None" ), 0)


