from src.reader import AbaqusInpReader
from src.abaqus_writer import AbaqusNonLinearCouplingWriter

inp_file = 'run_files/w24x146-dynamic/W24X146_Dynamic-WIKC-4500.inp'
def_file = 'run_files/w24x146-dynamic/w24x146-dynamic-wikc-def.txt'
out_dir = 'run_files/w24x146-dynamic/output/'

reader = AbaqusInpReader()
writer = AbaqusNonLinearCouplingWriter(out_dir)
couplings = reader.read(inp_file, def_file)
writer.write(couplings)
