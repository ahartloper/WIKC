import pywikc


# Locate the files to read/write
# These paths assume that the run-directory is wikc/
inp_file = 'examples/DBBW/DBBW-Macro.inp'
cdef_file = 'examples/DBBW/DBBW-Macro-CDef.txt'
out_dir = 'examples/DBBW/output/'

# Generate the keyword and imperfection files
pywikc.gen_aba_couples_imperfections(inp_file, cdef_file, out_dir)
