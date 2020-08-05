# Example to use pywikc to generate the keyword file and the imperfections
#
# See the doc/ directory for information on the definition file
#
# 1) Run this example from the wikc/ directory using a command-line tool as follows:
#    $ python examples/DBBW/DBBW-macro-processing.py
# 2) The input file can be modified using the keywords and imperfections
# 3) The modified input file can be ran using Abaqus
#
# Note: the DBBW-Macro.inp file has already been edited with the keywords and imperfections.
#
# ----- File start -----
import pywikc


# Locate the files to read/write
inp_file = 'examples/DBBW/DBBW-Macro.inp'
cdef_file = 'examples/DBBW/DBBW-Macro-CDef.txt'
out_dir = 'examples/DBBW/output/'
# Create the output directory if it doesn't already exist
pywikc.dir_maker(out_dir)

# Generate the keyword and imperfection files in the output directory
pywikc.gen_aba_couples_imperfections(inp_file, cdef_file, out_dir)
