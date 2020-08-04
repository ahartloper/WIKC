
import sys
import os
sys.path.append(os.path.join(sys.path[0], '..', '..'))
from src.imperfections.generate_imperfections import set_imperfection_properties, generate_component_imp
from src.imperfections.abaqus_txt_writer import AbaqusTxtWriter
from src.abaqus_i_coupling_writer import AbaqusICouplingWriter
from src.component_reader import AbaqusInpToComponentReader

# Locate the files to read
inp_file = 'run_files/test-beam-v2/WIKC-V2-Base.inp'
cdef_file = 'run_files/test-beam-v2/WIKC-V2-Base-CDef.txt'
out_dir = 'run_files/test-beam-v2/output/'

# Read the .inp file
reader = AbaqusInpToComponentReader()
reader.read(inp_file, cdef_file)

# Write the coupling defintions
couplings = []
for c in reader.components:
    couplings += c.couplings
couple_writer = AbaqusICouplingWriter(out_dir)
couple_writer.write(couplings)
