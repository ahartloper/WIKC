import unittest
from src.reader import AbaqusInpReader

inp_file = 'testing/Job-1.inp'
def_file = 'testing/def_file_1.txt'
def_file_jtype = 'testing/def_file_1_jtype.txt'


class TestAbaqusReader(unittest.TestCase):

    def test_read_def_file(self):
        reader = AbaqusInpReader()
        reader.read(inp_file, def_file)
        pass

    def test_read_def_file_with_jtype(self):
        reader = AbaqusInpReader()
        reader.read(inp_file, def_file_jtype)
        pass
