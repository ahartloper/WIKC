import unittest
from src.reader import AbaqusInpReader
from src.abaqus_writer import AbaqusLinearCouplingWriter, AbaqusNonLinerCouplingWriter

inp_file = 'testing/Job-1.inp'
def_file = 'testing/def_file_1.txt'
out_dir = 'testing/output/'
out_dir_nl = 'testing/output_nl/'


class TestAbaqusWriter(unittest.TestCase):

    def test_read_def_file(self):
        reader = AbaqusInpReader()
        writer = AbaqusLinearCouplingWriter(out_dir)
        couplings = reader.read(inp_file, def_file)
        writer.write(couplings)

    def test_nl_writer(self):
        reader = AbaqusInpReader()
        writer = AbaqusNonLinerCouplingWriter(out_dir_nl)
        couplings = reader.read(inp_file, def_file)
        writer.write(couplings)
