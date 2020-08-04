
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
inp_file = 'run_files/subassem_w27x235/SubAssem-W27X235-FS-Imp.inp'
cdef_file = 'run_files/subassem_w27x235/SubAssem-W27X235-FS-Imp-CDef.txt'
out_dir = 'run_files/subassem_w27x235/output/'
imp_file = os.path.join(out_dir, 'DBBW-SubAssem-W27X235-FS-Imp-Imp.txt')

# Read the .inp file
reader = AbaqusInpToComponentReader()
reader.read(inp_file, cdef_file)
imp_writer = AbaqusTxtWriter(reader.components)


# Generate the imperfections
for c in reader.components:
    set_imperfection_properties(c)
    generate_component_imp(c)
imp_writer.write_imperfections(imp_file)



# # Plot each of the components
# # Column
# # col_nodes = reader.components[0].continuum_nodes
# col_nodes = reader.components[0].get_imperfect_nodes()
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# for nid, coords in col_nodes.items():
#     ax.plot([coords[0]], [coords[1]], [coords[2]], 'ko')
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')
# plt.show()

# # Beam-1
# # col_nodes = reader.components[1].continuum_nodes
# col_nodes = reader.components[1].get_imperfect_nodes()
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# for nid, coords in col_nodes.items():
#     ax.plot([coords[0]], [coords[1]], [coords[2]], 'ko')
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')
# plt.show()

# # Beam-2
# col_nodes = reader.components[2].continuum_nodes
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# for nid, coords in col_nodes.items():
#     ax.plot([coords[0]], [coords[1]], [coords[2]], 'ko')
# ax.set_xlabel('x')
# ax.set_ylabel('y')
# ax.set_zlabel('z')
# plt.show()
