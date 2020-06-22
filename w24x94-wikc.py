from src.reader import AbaqusInpReader
from src.abaqus_writer import AbaqusNonLinearCouplingWriter

inp_file = 'run_files/w24x94-5500/W24X94_Dynamic-WIKC-5500.inp'
def_file = 'run_files/w24x94-5500/w24x94-dynamic-wikc-def.txt'
out_dir = 'run_files/w24x94-5500/output/'

reader = AbaqusInpReader()
writer = AbaqusNonLinearCouplingWriter(out_dir)
couplings = reader.read(inp_file, def_file)
writer.write(couplings)
