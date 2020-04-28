from src.reader import AbaqusInpReader
from src.abaqus_writer import AbaqusNonLinearCouplingWriter

inp_file = 'run_files/galambos-beam-NL/Center_Tor_Macro-EQN-NL.inp'
def_file = 'run_files/galambos-beam-NL/galambos-beam-NL-def.txt'
out_dir = 'run_files/galambos-beam-NL/output/'

reader = AbaqusInpReader()
writer = AbaqusNonLinearCouplingWriter(out_dir)
couplings = reader.read(inp_file, def_file)
writer.write(couplings)
