from src.reader import AbaqusInpReader
from src.abaqus_writer import AbaqusNonLinearCouplingWriter

inp_file = 'run_files/Ahmed_C5/C5-WIKC-TopRot.inp'
def_file = 'run_files/Ahmed_C5/C5-WIKC-Def.txt'
out_dir = 'run_files/Ahmed_C5/output/'

reader = AbaqusInpReader()
writer = AbaqusNonLinearCouplingWriter(out_dir)
couplings = reader.read(inp_file, def_file)
writer.write(couplings)
