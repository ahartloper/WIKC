from src.reader import AbaqusInpReader
from src.abaqus_writer import AbaqusNonLinearCouplingWriter

inp_file = 'run_files/NIST_A/NIST_A-WIKC.inp'
def_file = 'run_files/NIST_A/NIST_A-def.txt'
out_dir = 'run_files/NIST_A/output/'

reader = AbaqusInpReader()
writer = AbaqusNonLinearCouplingWriter(out_dir)
couplings = reader.read(inp_file, def_file)
writer.write(couplings)
