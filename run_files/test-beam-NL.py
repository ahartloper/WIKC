from src.reader import AbaqusInpReader
from src.abaqus_writer import AbaqusNonLinearCouplingWriter

inp_file = 'run_files/test-beam-NL/Macro-EQN-Testing.inp'
def_file = 'run_files/test-beam-NL/Macro-EQN-Testing-def.txt'
out_dir = 'run_files/test-beam-NL/output/'

reader = AbaqusInpReader()
writer = AbaqusNonLinearCouplingWriter(out_dir)
couplings = reader.read(inp_file, def_file)
writer.write(couplings)
