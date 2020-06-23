import numpy as np
from .coupling import BSCoupling
from .component import IComponent, ISection, CoordSys, ICoupling

# definition file prototype:
# *coupling
# <beam_n_set_string>, <shell_n_set_string>, <local_coord_sys_string>
# repeat lines

NSET_KEYW = '*Nset'
NODE_KEYW = '*Node'
SYSTEM_KEYW = '*System'


def peek_line(f):
    """ Checks the next line, then goes back to the current line. """
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line


def line_lister(line):
    """ Returns a a list of stripped line split on ','. """
    return [li.strip() for li in line.split(',')]


class AbaqusInpToComponentReader:
    """ Reads an input file into Components. """

    def __init__(self):
        """ Constructor. """
        self.sections = dict()
        self.components = list()
        # Sets for all the node sets defined in any component
        self.beam_sets = dict()
        self.continuum_sets = dict()
        self.all_nodes = dict()
        self.all_beam_nodes = set()
        self.all_continuum_nodes = set()
        self.all_nodes_local = dict()
        # The global coord sys is denoted as system "0"
        self.coord_syss = {0: [0., 0., 0., 1., 0., 0., 0., 1., 0.]}
        self.node_systems = dict()
        self.cs_transforms = dict()

    def read(self, inp_file, definition_file):
        """ Returns the components defined. """
        self._read_def_file(definition_file)
        self._read_inp_file(inp_file)
        self._organize_beam_continuum_nodes()
        self._compute_component_local_coords()
        self._transform_nodes_to_local()
        self._define_component_domains()
        self._assign_component_coord_sys()
        self._assign_component_couplings()
        return self.components

    def _define_component_domains(self):
        """ Assigns all the nodes in the beam and continuum domains for each component. """
        for c in self.components:
            for node_set in c.beam_node_sets:
                for node_id in self.beam_sets[node_set]:
                    c.beam_nodes[node_id] = self.all_nodes_local[node_id]
            for node_set in c.continuum_node_sets:
                for node_id in self.continuum_sets[node_set]:
                    c.continuum_nodes[node_id] = self.all_nodes_local[node_id]

    def _assign_component_couplings(self):
        """ Parse and assign the couplings to the component. """
        for c in self.components:
            for ci in c.couplings_info:
                beam_id = self.beam_sets[ci['beam_set']][0]
                beam_node = {beam_id: self.all_nodes_local[beam_id]}
                cont_nodes = dict()
                for node_ids in self.continuum_sets[ci['continuum_set']]:
                    cont_nodes[node_ids] = self.all_nodes_local[node_ids]
                constr_def = self._parse_jtype(ci['jtype'])
                c.couplings.append(ICoupling(beam_node, cont_nodes, **constr_def))

    def _assign_component_coord_sys(self):
        """ Assign the component coord sys to global coord sys transformation for all components. """
        for c in self.components:
            # Use the first continuum node in the component since assumed to all have same orientation
            set1 = c.continuum_node_sets[0]
            node1 = self.continuum_sets[set1][0]
            cs1 = self.node_systems[node1]
            c.coord_sys = CoordSys(self.cs_transforms[cs1]['origin'], self.cs_transforms[cs1]['basis'])

    def _organize_beam_continuum_nodes(self):
        """ Organize all the nodes into either beam or continuum. """
        for set_names, set_nodes in self.beam_sets.items():
            self.all_beam_nodes = self.all_beam_nodes | set(set_nodes)
        for set_names, set_nodes in self.continuum_sets.items():
            self.all_continuum_nodes = self.all_continuum_nodes | set(set_nodes)

    def _read_def_file(self, def_file):
        """ Reads the information in coupling definition file. """

        def opt_extract(line_list):
            """ Gets the values after the equals sign. """
            options = dict()
            if len(line_list) > 1:
                for li in line_list[1:]:
                    opt = li.split('=')[0]
                    opt_val = li.split('=')[1]
                    options[opt] = opt_val
            return options

        with open(def_file, 'r') as file:
            line = file.readline()
            while line:
                l_list = line_lister(line)
                if l_list[0] == '*ISection':
                    section_options = opt_extract(l_list)
                    name = section_options['name']
                    line = file.readline()
                    fl = [float(li.strip()) for li in line.split(',')]
                    self.sections[name] = ISection(name, d=fl[0], bf=fl[1], tf=fl[2], tw=fl[3])

                if l_list[0] == '*Component':
                    component_options = opt_extract(l_list)
                    new_component = IComponent(component_options['name'], self.sections[component_options['section']])
                    # The active component will always be at the end of the list
                    self.components.append(new_component)

                elif l_list[0] == '*BeamNodes':
                    peeked_line = 'START'
                    while peeked_line[0] != '*':
                        line = file.readline()
                        l_list = [l.strip() for l in line.split(',')]
                        self.components[-1].beam_node_sets += l_list
                        for li in l_list:
                            self.beam_sets[li] = []
                        peeked_line = peek_line(file).strip()

                elif l_list[0] == '*ContinuumNodes':
                    peeked_line = 'START'
                    while peeked_line[0] != '*':
                        line = file.readline()
                        l_list = [l.strip() for l in line.split(',')]
                        self.components[-1].continuum_node_sets += l_list
                        for li in l_list:
                            self.continuum_sets[li] = []
                        peeked_line = peek_line(file).strip()

                elif l_list[0] == '*Coupling':
                    couple_options = opt_extract(l_list)
                    line = file.readline()
                    l_list = [l.strip() for l in line.split(',')]
                    couple_data = {'beam_set': l_list[0], 'continuum_set': l_list[1]}
                    self.beam_sets[couple_data['beam_set']] = []
                    self.continuum_sets[couple_data['continuum_set']] = []
                    couple_data = {**couple_data, **couple_options}
                    self.components[-1].couplings_info.append(couple_data)

                line = file.readline()
        return

    def _read_inp_file(self, inp_file):
        """ Reads the coupling information in the input file. """
        node_reading = False
        system_reading = False
        active_system = 0
        coord_sys_tag = 1

        with open(inp_file, 'r') as file:
            # Read the Nsets
            line = file.readline()
            while line:
                li = line.strip()
                if li[:len(NSET_KEYW)] == NSET_KEYW:
                    l_list = line_lister(line)
                    n_set_name = l_list[1].split('=')[1]
                    if len(l_list) > 2:
                        if l_list[2] == 'generate':
                            generate_option = True
                        else:
                            generate_option = False
                    else:
                        generate_option = False
                    if n_set_name in self.continuum_sets:
                        self.continuum_sets[n_set_name] = self._read_n_set(file, generate_option)
                    elif n_set_name in self.beam_sets:
                        self.beam_sets[n_set_name] = self._read_n_set(file, generate_option)
                line = file.readline()

            # Get coordinates of all registered nodes
            file.seek(0)
            line = file.readline()
            while line:
                l_list = [li.strip() for li in line.split(',')]
                if l_list[0][0] == '*':
                    # Stop at any keyword
                    node_reading = False
                    if system_reading:
                        system_reading = False
                        coord_sys_tag += 1
                # Read keywords
                if l_list[0] == SYSTEM_KEYW:
                    peeked_line = peek_line(file)
                    if peeked_line.strip()[0] == '*':
                        # Set to global coord sys and don't read
                        active_system = 0
                    else:
                        system_reading = True
                        active_system = coord_sys_tag
                        coord_sys_tag += 1

                elif l_list[0] == NODE_KEYW:
                    node_reading = True

                elif node_reading:
                    node_id = int(l_list[0])
                    if node_id in self.all_nodes:
                        coords = [float(c) for c in l_list[1:]]
                        self.all_nodes[node_id] = coords
                        self.node_systems[node_id] = active_system

                elif system_reading:
                    f_list = [float(li) for li in l_list]
                    if active_system in self.coord_syss:
                        self.coord_syss[active_system] += f_list
                    else:
                        self.coord_syss[active_system] = f_list
                line = file.readline()
        return

    def _parse_jtype(self, jtype):
        """ Returns the options from jtype. """
        val = int(jtype)
        if val == 16:
            constr_def = {'include_warping': False, 'use_nonlinear': False}
        elif val == 17:
            constr_def = {'include_warping': True, 'use_nonlinear': False}
        elif val == 26:
            constr_def = {'include_warping': False, 'use_nonlinear': True}
        elif val == 27:
            constr_def = {'include_warping': True, 'use_nonlinear': True}
        else:
            raise ValueError('Incorrect JTYPE provided.')
        return constr_def

    def _read_n_set(self, fp, use_generate):
        """ Returns the IDs of the nodes in the node set.
        :param FileObject fp: Pointer to the file being read.
        :param bool use_generate: If True, generate the node set.
        """
        if use_generate:
            line = fp.readline()
            l_list = line_lister(line)
            l_list = [int(li) for li in l_list]
            node_set = list(range(l_list[0], l_list[1] + 1, l_list[2]))
            for n in node_set:
                self.all_nodes[n] = []
        else:
            node_set = []
            peeked_line = 'START'
            while peeked_line[0] != '*':
                li = fp.readline().strip()
                nodes = li.split(',')
                for n in nodes:
                    if n != '':
                        node_set.append(int(n))
                        self.all_nodes[int(n)] = []
                peeked_line = peek_line(fp).strip()
        return node_set

    def _compute_component_local_coords(self):
        """ Compute the transformations implied by each coord. sys. """
        for cs_tag, cs_data in self.coord_syss.items():
            cs_data = np.array(cs_data)
            if len(cs_data) == 9:
                # The data defines o, p1, p2
                o = cs_data[[0, 1, 2]]
                n1 = cs_data[[3, 4, 5]] - o
                n1 = n1 / np.linalg.norm(n1)
                n2 = cs_data[[6, 7, 8]] - o
                n2 = n2 / np.linalg.norm(n2)
                n3 = np.cross(n1, n2)
                n3 = n3 / np.linalg.norm(n3)
                # Ensure right-handed system
                if np.linalg.det(np.column_stack((n1, n2, n3))) < 0:
                    n3 = -n3
                n_123 = np.column_stack((n1, n2, n3))
            self.cs_transforms[cs_tag] = {'origin': o, 'basis': n_123}
        pass

    def _transform_nodes_to_local(self):
        """ Transforms the nodes from model to component coordinate systems. """
        rmat_continuum = np.identity(3)
        rmat_beam = np.array([[0.,  0., -1.],
                              [0.,  1.,  0.],
                              [1.,  0.,  0.]])
        for node_id, coord in self.all_nodes.items():
            if node_id in self.all_beam_nodes:
                rmat = rmat_beam
            elif node_id in self.all_continuum_nodes:
                rmat = rmat_continuum
            else:
                raise ValueError('Node ID not found in beam or continuum domains.')
            c = np.array(coord)
            o = self.cs_transforms[self.node_systems[node_id]]['origin']
            transf_coord = np.dot(rmat, c) + o
            # Keep only 8 digits of precision (neglect values < 10^-8)
            transf_coord = transf_coord.round(8)
            self.all_nodes_local[node_id] = transf_coord
        pass
