import unittest
from src.reader import AbaqusInpReader
from src.component_reader import AbaqusInpToComponentReader
from src.abaqus_equation_writer import AbaqusLinearCouplingWriter
from src.abaqus_i_coupling_writer import AbaqusNonLinearCouplingWriter, AbaqusICouplingWriter

inp_file = 'testing/Job-1.inp'
def_file = 'testing/def_file_1.txt'
cdef_file = 'testing/cdef_file_1.txt'

out_dir = 'testing/output/'
out_dir_nl = 'testing/output_nl/'
out_dir_comp = 'testing/output_component/'


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
