import unittest
import numpy as np
from pywikc.reader import AbaqusInpReader
from pywikc.component_reader import AbaqusInpToComponentReader
from pywikc.imperfections.generate_imperfections import set_imperfection_properties, generate_component_imp

inp_file = 'testing/subassem.inp'
cdef_file = 'testing/subassem_cdef.txt'

out_dir = 'testing/output_subassem/'


class TestIImperfections(unittest.TestCase):

    def test_negative_amplitude(self):
        reader = AbaqusInpToComponentReader()
        reader.read(inp_file, cdef_file)
        for c in reader.components:
            set_imperfection_properties(c)
            generate_component_imp(c)
        beam_1_imp = reader.components[1].node_imperfections
        beam_2_imp = reader.components[2].node_imperfections
        beam_1_imp_amps = []
        for node_id, imp in beam_1_imp.items():
            beam_1_imp_amps.append(np.linalg.norm(np.array(imp)))
        beam_2_imp_amps = []
        for node_id, imp in beam_2_imp.items():
            beam_2_imp_amps.append(np.linalg.norm(np.array(imp)))
        self.assertAlmostEqual(max(beam_1_imp_amps), max(beam_2_imp_amps))
        pass
