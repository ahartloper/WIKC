from src.reader import AbaqusInpReader
from src.writer import AbaqusCouplingWriter

inp_file = 'run_files/test-beam/Macro-EQN-Testing.inp'
def_file = 'run_files/test-beam/Macro-EQN-Testing-def.txt'
out_dir = 'run_files/test-beam/output/'

reader = AbaqusInpReader()
writer = AbaqusCouplingWriter(out_dir, 'test-beam_constr_files/')
couplings = reader.read(inp_file, def_file)
writer.write(couplings)
