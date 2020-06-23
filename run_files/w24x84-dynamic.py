from src.reader import AbaqusInpReader
from src.abaqus_writer import AbaqusNonLinearCouplingWriter

inp_file = 'run_files/w24x84-dynamic/W24X84_Dynamic-LBIKC.inp'
def_file = 'run_files/w24x84-dynamic/w24x84-dynamic-def.txt'
out_dir = 'run_files/w24x84-dynamic/output/'

reader = AbaqusInpReader()
writer = AbaqusNonLinearCouplingWriter(out_dir)
couplings = reader.read(inp_file, def_file)
writer.write(couplings)
