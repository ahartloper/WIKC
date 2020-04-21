from src.reader import AbaqusInpReader
from src.abaqus_writer import AbaqusLinearCouplingWriter

inp_file = 'run_files/w24x84-dynamic/test_alex_couple.inp'
def_file = 'run_files/w24x84-dynamic/w24x84-dynamic-def.txt'
out_dir = 'run_files/w24x84-dynamic/output/'

reader = AbaqusInpReader()
writer = AbaqusLinearCouplingWriter(out_dir, 'constr_files/')
couplings = reader.read(inp_file, def_file)
writer.write(couplings)
