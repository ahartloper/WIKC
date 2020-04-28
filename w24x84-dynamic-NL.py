from src.reader import AbaqusInpReader
from src.abaqus_writer import AbaqusNonLinearCouplingWriter

inp_file = 'run_files/w24x84-dynamic-NL/test_alex_couple-NL.inp'
def_file = 'run_files/w24x84-dynamic-NL/w24x84-dynamic-NL-def.txt'
out_dir = 'run_files/w24x84-dynamic-NL/output/'

reader = AbaqusInpReader()
writer = AbaqusNonLinearCouplingWriter(out_dir)
couplings = reader.read(inp_file, def_file)
writer.write(couplings)
