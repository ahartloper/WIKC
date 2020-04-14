from src.reader import AbaqusInpReader
from src.writer import AbaqusCouplingWriter

inp_file = 'run_files/w24x84-dynamic/test_alex_couple.inp'
def_file = 'run_files/w24x84-dynamic/w24x84-dynamic-def.txt'
out_dir = 'run_files/w24x84-dynamic/output/'

reader = AbaqusInpReader()
writer = AbaqusCouplingWriter(out_dir)
couplings = reader.read(inp_file, def_file)
writer.write(couplings)
