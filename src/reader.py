import numpy as np
from .coupling import BSCoupling

# definition file prototype:
# *coupling
# <beam_n_set_string>, <shell_n_set_string>, <local_coord_sys_string>
# repeat lines

# open def file
# save all nsets and coord sys to read
# close def file
# open inp file
# collect all the nodes in all the nsets
# reset file
# read all the necessary nodes
# read all the coord sys
# compute all the local coords
# create constraints

NSET_KEYW = '*Nset'
NODE_KEYW = '*Node'


class AbaqusInpReader:
    """ Returns a set of Coupling objects that define beam-shell coupling constraints. """

    def __init__(self):
        self.couplings = list()
        self.beam_sets = dict()
        self.shell_sets = dict()
        self.coord_syss = dict()
        self.all_nodes = dict()

    def _read_def_file(self, def_file):
        """ Reads the information in coupline definition file. """
        with open(def_file, 'r') as file:
            for line in file:
                l = line.strip()
                if l == '*coupling':
                    line = file.readline()
                    l_list = line.split(',')
                    l_list = [l.strip() for l in l_list]
                    self.couplings.append({'beam_set': l_list[0], 'shell_set': l_list[1], 'coord_sys': l_list[2]})
                    self.beam_sets[l_list[0]] = []
                    self.shell_sets[l_list[1]] = []
                    self.coord_syss[l_list[2]] = []
        return

    def _read_inp_file(self, inp_file):
        """ Reads the coupling information in the input file. """
        node_reading = False

        with open(inp_file, 'r') as file:
            # Using file.readline() is necessary because next(file) does not allow file.tell()
            line = file.readline()
            while line:
                l = line.strip()
                if l[:len(NSET_KEYW)] == NSET_KEYW:
                    n_set_name = l.split(',')[1].split('=')[1]
                    if n_set_name in self.shell_sets:
                        self.shell_sets[n_set_name] = self._read_n_set(file)
                    elif n_set_name in self.beam_sets:
                        self.beam_sets[n_set_name] = self._read_n_set(file)
                # todo: add reading for the coord systems
                line = file.readline()
            # Get coordinates of all registered nodes
            file.seek(0)
            for line in file:
                l = line.strip()
                if l[0] == '*':
                    node_reading = False
                if l[:len(NODE_KEYW)] == NODE_KEYW:
                    node_reading = True
                elif node_reading:
                    l_list = l.split(',')
                    node_id = int(l_list[0])
                    if node_id in self.all_nodes:
                        coords = [float(c) for c in l_list[1:]]
                        self.all_nodes[node_id] = coords
        return

    def read(self, inp_file, definition_file):
        """ Returns the beam-shell couplings defined. """
        self._read_def_file(definition_file)
        self._read_inp_file(inp_file)
        couples = []
        for c in self.couplings:
            coord_sys = c['coord_sys']
            shell_nodes = {}
            beam_node = {}
            for n in self.beam_sets[c['beam_set']]:
                beam_node[n] = self.all_nodes[n]
            beam_node_id = n
            # Get the local transformations
            # todo: handle other situations
            # translation = np.array(beam_node[beam_node_id])
            translation = np.array([0., 0., 0.])
            rotation = np.identity(3)
            for n in self.shell_sets[c['shell_set']]:
                shell_nodes[n] = np.matmul(rotation, np.array(self.all_nodes[n]) - translation)
            couples.append(BSCoupling(shell_nodes, beam_node_id, coord_sys))
        return couples

    def _read_n_set(self, fp):
        """ Returns the IDs of the nodes in the node set. 
        :param FilePointer fp: Pointer to the file being read.
        """
        # todo: add case of "generate" option in the Nset
        def peek_line(f):
            pos = f.tell()
            line = f.readline()
            f.seek(pos)
            return line

        node_set = []
        peeked_line = 'START'
        while peeked_line[0] != '*':
            l = fp.readline().strip()
            nodes = l.split(',')
            for n in nodes:
                if n != '':
                    node_set.append(int(n))
                    self.all_nodes[int(n)] = []
            peeked_line = peek_line(fp).strip()
        return node_set
