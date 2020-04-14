import unittest
from src.reader import AbaqusInpReader
from src.writer import AbaqusCouplingWriter

inp_file = 'testing/Job-1.inp'
def_file = 'testing/def_file_1.txt'
out_dir = 'testing/output/'


class TestAbaqusWriter(unittest.TestCase):

    def test_read_def_file(self):
        reader = AbaqusInpReader()
        writer = AbaqusCouplingWriter(out_dir)
        couplings = reader.read(inp_file, def_file)
        writer.write(couplings)
