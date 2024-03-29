import unittest
import numpy as np
from pywikc.reader import AbaqusInpReader
from pywikc.component_reader import AbaqusInpToComponentReader

inp_file = 'testing/Job-1.inp'
def_file = 'testing/def_file_1.txt'
def_file_jtype = 'testing/def_file_1_jtype.txt'
cdef_file = 'testing/cdef_file_1.txt'

macro_inp_file = 'testing/subassem-macro.inp'
macro_cdef_file = 'testing/subassem-macro_cdef.txt'


class TestAbaqusReader(unittest.TestCase):

    def test_read_def_file(self):
        reader = AbaqusInpReader()
        reader.read(inp_file, def_file)
        pass

    def test_read_def_file_with_jtype(self):
        reader = AbaqusInpReader()
        reader.read(inp_file, def_file_jtype)
        pass


class TestAbaqusComponentReader(unittest.TestCase):
    def test_read_component_def(self):
        reader = AbaqusInpToComponentReader()
        reader.read(inp_file, cdef_file)
        # Test reading the component sets
        self.assertTrue('Part-1-1_Set-4' in reader.beam_sets)
        self.assertTrue('Part-1-1_beam_node' in reader.beam_sets)
        self.assertTrue('Part-2-1_Set-14' in reader.continuum_sets)
        self.assertTrue('Part-2-1_interf_nodes_1' in reader.continuum_sets)
        # Test reading the node sets with generate
        self.assertEqual(len(reader.continuum_sets['Part-2-1_Set-14']), 538 - 6 + 1)
        # Test reading the component info
        self.assertEqual(len(reader.components), 1)
        self.assertEqual(reader.components[0].id, 'component-1')
        self.assertEqual(reader.components[0].section.name, 'w24x146')
        self.assertEqual(len(reader.components[0].couplings_info), 1)
        pass

    def test_read_component_inp(self):
        reader = AbaqusInpToComponentReader()
        reader.read(inp_file, cdef_file)
        # Test that reading all the nodes in the inp file
        nodes_in_sets = set()
        for set_names, set_nodes in reader.beam_sets.items():
            nodes_in_sets = nodes_in_sets | set(set_nodes)
        for set_names, set_nodes in reader.continuum_sets.items():
            nodes_in_sets = nodes_in_sets | set(set_nodes)
        self.assertEqual(len(reader.all_nodes), len(nodes_in_sets))
        # Test the coord sys
        self.assertEqual(len(reader.coord_syss), 2)
        self.assertEqual(len(reader.all_nodes), len(reader.node_systems))
        self.assertEqual(reader.coord_syss[0], [0., 0., 0., 1., 0., 0., 0., 1., 0.])
        self.assertEqual(reader.coord_syss[1], [0., 0., 1000., 6.12323399573677e-17, 0., 1001., 0., 1., 1000.])
        pass

    def test_local_transformation(self):
        reader = AbaqusInpToComponentReader()
        reader.read(inp_file, cdef_file)
        self.assertEqual(reader.all_nodes_local[5][2], 1000.)
        self.assertEqual(reader.all_nodes_local[240][0], 50.)
        self.assertEqual(reader.all_nodes_local[240][1], 50.)
        self.assertEqual(reader.all_nodes_local[240][2], 375.)
        pass

    def test_component_transformation(self):
        reader = AbaqusInpToComponentReader()
        reader.read(inp_file, cdef_file)
        c = reader.components[0]
        np.testing.assert_array_equal(c.coord_sys.pt, np.array([0., 0., 0.]))
        self.assertEqual(c.beam_nodes[5][2], 2000.)
        self.assertEqual(c.continuum_nodes[240][0], 50.)
        self.assertEqual(c.continuum_nodes[240][1], 50.)
        self.assertEqual(c.continuum_nodes[240][2], 375.)
        pass

    def test_component_couplings(self):
        reader = AbaqusInpToComponentReader()
        c = reader.read(inp_file, cdef_file)
        couple = c[0].couplings[0]
        self.assertEqual(list(couple.beam_node.keys())[0], 1)
        self.assertEqual(len(couple.continuum_nodes), 13)
        self.assertEqual(couple.use_nonlinear, True)
        self.assertEqual(couple.include_warping, True)
        n3 = np.array([0., 0., 1.])
        np.testing.assert_array_equal(couple.normal_direction, n3)
        pass

    def test_component_length(self):
        reader = AbaqusInpToComponentReader()
        c = reader.read(inp_file, cdef_file)
        c = reader.components[0]
        self.assertEqual(c.length, 2000.)
        pass

    def test_macro_component_length(self):
        reader = AbaqusInpToComponentReader()
        reader.read(macro_inp_file, macro_cdef_file)
        self.assertEqual(reader.components[0].length, 3708.)
        self.assertEqual(reader.components[1].length, 3962.)
        self.assertEqual(reader.components[2].length, 3962.)
        pass

    def test_macro_component_normals(self):
        reader = AbaqusInpToComponentReader()
        reader.read(macro_inp_file, macro_cdef_file)
        c = reader.components
        # column 1
        couple = c[0].couplings[0]
        n3 = np.array([0., 0., 1.])
        np.testing.assert_array_equal(couple.normal_direction, n3)
        # column 2
        couple = c[0].couplings[1]
        n3 = np.array([0., 0., 1.])
        np.testing.assert_array_equal(couple.normal_direction, n3)
        # beam1 2
        couple = c[1].couplings[0]
        n3 = np.array([0., -1., 0.])
        np.testing.assert_array_equal(couple.normal_direction, n3)
        # beam 2
        couple = c[2].couplings[0]
        n3 = np.array([0., 1., 0.])
        np.testing.assert_array_equal(couple.normal_direction, n3)
        pass

    def test_coupling_orientation_z_align(self):
        inp_file_1 = 'testing/WIKC-V2-Base.inp'
        cdef_file_1 = 'testing/WIKC-V2-Base-CDef.txt'
        reader = AbaqusInpToComponentReader()
        reader.read(inp_file_1, cdef_file_1)
        c = reader.components
        # Component 1
        couple = c[0].couplings[0]
        n3 = np.array([0., 0., 1.])
        np.testing.assert_array_equal(couple.normal_direction, n3)
        # Component 2
        couple = c[1].couplings[0]
        n3 = np.array([0., 0., 1.])
        np.testing.assert_array_equal(couple.normal_direction, n3)
        pass

    def test_coupling_orientation_y_align(self):
        inp_file_1 = 'testing/WIKC-V2-y-orient.inp'
        cdef_file_1 = 'testing/WIKC-V2-Base-CDef.txt'
        reader = AbaqusInpToComponentReader()
        reader.read(inp_file_1, cdef_file_1)
        c = reader.components
        # Component 1
        couple = c[0].couplings[0]
        n3 = np.array([0., 1., 0.])
        np.testing.assert_array_equal(couple.normal_direction, n3)
        # Component 2
        couple = c[1].couplings[0]
        n3 = np.array([0., 1., 0.])
        np.testing.assert_array_equal(couple.normal_direction, n3)
        pass
    