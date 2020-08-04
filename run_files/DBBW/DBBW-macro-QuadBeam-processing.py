
import sys
import os
sys.path.append(os.path.join(sys.path[0], '..', '..'))
from src.imperfections.generate_imperfections import set_imperfection_properties, generate_component_imp
from src.imperfections.abaqus_txt_writer import AbaqusTxtWriter
from src.abaqus_i_coupling_writer import AbaqusICouplingWriter
from src.component_reader import AbaqusInpToComponentReader
# Import matplotlib 3D
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Locate the files to read
inp_file = 'run_files/DBBW/DBBW-Macro-KC-QuadBeam.inp'
cdef_file = 'run_files/DBBW/DBBW-Macro-KC-NoParts-CDef.txt'
out_dir = 'run_files/DBBW/output/'
imp_file = os.path.join(out_dir, 'DBBW-Macro-KC-QuadBeam-Imp.txt')

# Read the .inp file
reader = AbaqusInpToComponentReader()
reader.read(inp_file, cdef_file)
imp_writer = AbaqusTxtWriter(reader.components)

# Generate the imperfections
for c in reader.components:
    set_imperfection_properties(c)
    generate_component_imp(c)
imp_writer.write_imperfections(imp_file)

# Write the coupling defintions
# couplings = []
# for c in reader.components:
#     couplings += c.couplings
# couple_writer = AbaqusICouplingWriter(out_dir)
# couple_writer.write(couplings)
