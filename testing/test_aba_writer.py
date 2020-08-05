import unittest
import os
import errno
from pywikc.reader import AbaqusInpReader
from pywikc.component_reader import AbaqusInpToComponentReader
from pywikc.abaqus_equation_writer import AbaqusLinearCouplingWriter
from pywikc.abaqus_i_coupling_writer import AbaqusNonLinearCouplingWriter, AbaqusICouplingWriter


def dir_maker(directory):
    """ Makes directory if it doesn't exist, else does nothing. """
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return


inp_file = 'testing/Job-1.inp'
def_file = 'testing/def_file_1.txt'
cdef_file = 'testing/cdef_file_1.txt'

out_dir = 'testing/output/'
out_dir_nl = 'testing/output_nl/'
out_dir_comp = 'testing/output_component/'
dir_maker(out_dir)
dir_maker(out_dir_nl)
dir_maker(out_dir_comp)

class TestAbaqusWriter(unittest.TestCase):

    def test_read_def_file(self):
        reader = AbaqusInpReader()
        writer = AbaqusLinearCouplingWriter(out_dir)
        couplings = reader.read(inp_file, def_file)
        writer.write(couplings)
        pass

    def test_nl_writer(self):
        reader = AbaqusInpReader()
        writer = AbaqusNonLinearCouplingWriter(out_dir_nl)
        couplings = reader.read(inp_file, def_file)
        writer.write(couplings)
        pass


class TestAbaqusComponentWriter(unittest.TestCase):

    def test_component_writer(self):
        reader = AbaqusInpToComponentReader()
        components = reader.read(inp_file, cdef_file)
        couplings = []
        for c in components:
            couplings += c.couplings
        writer = AbaqusICouplingWriter(out_dir_comp)
        writer.write(couplings)
        pass
