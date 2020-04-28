import os


class AbaqusWriter:

    def __init__(self, output_dir):
        """ Constructor.
        :param str output_dir: Directory where files will be saved.

        Notes:
            - Implementations should overwrite self.KEYWFILE_BASE and self.DATAFILE_BASE to use these parameters.
        """
        self.output_dir = output_dir
        self.KEYWFILE_BASE = 'NOT IMPLEMENTED'
        self.DATAFILE_BASE = 'NOT IMPLEMENTED'
        return

    def write(self, couplings):
        """ Writes files for the provided couplings.
        :param list couplings: [Coupling] The couplings to be written to file.
        """
        raise NotImplementedError('write not implemented')
        return

    def _clear_output(self):
        # Clear any existing files written in the output directory
        file_list = os.listdir(self.output_dir)
        for f in file_list:
            # todo: make this clearing more robust - will raise an index error if have short file names
            if f[:len(self.DATAFILE_BASE)] == self.DATAFILE_BASE or f[:len(self.KEYWFILE_BASE)] == self.KEYWFILE_BASE:
                os.remove(os.path.join(self.output_dir, f))
        return


class AbaqusNonLinearCouplingWriter(AbaqusWriter):

    def __init__(self, output_dir):
        AbaqusWriter.__init__(self, output_dir)
        self.KEYWFILE_BASE = 'MPC_Field_Keywords.txt'
        self.JTYPE_DEFAULT = 0
        self._clear_output()
        return

    def write(self, couplings):
        """ Writes the nonlinear coupling to file for insertion to the input file. """
        # todo: these should be imported names from Coupling
        DISP_Z_NAME = 'disp-z'
        WARP_NAME = 'warping-term'
        SHELL_NAME = 'shell-term'
        field_strings = []
        mpc_strings = []
        for couple in couplings:
            jtype = self._gen_jtype(couple)
            beam_node = couple.beam_node
            shell_node_ids = couple.shell_nodes.keys()
            warping_values = dict()
            # Extract the value of the warping function from the constraints
            for constraint in couple.constraints:
                if constraint.constr_name == DISP_Z_NAME:
                    for term in constraint.terms:
                        if term.name == SHELL_NAME:
                            node = term.node
                        if term.name == WARP_NAME:
                            # Since the negative of the warping function is stored
                            w = -1.0 * term.coef
                    warping_values[node] = w
            field_strings += self._gen_field_strings(warping_values)
            mpc_strings += self._gen_mpc_strings(beam_node, shell_node_ids, jtype)
        # Write the strings
        amp_strings = self._gen_amp_strings()
        self._write_keyw_file(field_strings, mpc_strings, amp_strings)
        return

    def _gen_jtype(self, couple):
        """ Returns the JTYPE for the specified couple. """
        if couple.include_warping and couple.use_nonlinear:
            jtype = 27
        elif couple.include_warping and not couple.use_nonlinear:
            jtype = 17
        elif not couple.include_warping and couple.use_nonlinear:
            jtype = 26
        elif not couple.include_warping and not couple.use_nonlinear:
            jtype = 16
        return jtype

    def _write_keyw_file(self, field_strings, mpc_strings, amp_strings):
        """ Writes the file containing the keyword additions. """
        keyw_file = os.path.join(self.output_dir, self.KEYWFILE_BASE)
        with open(keyw_file, 'w') as file:
            file.write('** MPC Keywords\n** Copy these in the model definition\n')
            file.writelines(mpc_strings)
            file.write('\n\n** Amplitude Keyword\n** Copy these in the model definition\n')
            file.writelines(amp_strings)
            file.write('\n\n** Field Keywords\n** Copy these in the first step\n')
            file.writelines(field_strings)
        return

    def _gen_amp_strings(self):
        """ Returns the strings to define the amplitude for the warping function field. """
        strings = []
        MAX_TIME = '1.E6'
        strings.append(', '.join(['*Amplitude', 'name=warp_fun_amp\n']))
        strings.append(', '.join(['0.0', '1.0\n']))
        strings.append(', '.join([MAX_TIME, '1.0\n']))
        return strings

    def _gen_field_strings(self, warping_values):
        """ Returns the strings for the field keywords. """
        strings = []
        strings.append(', '.join(['*Field', 'variable=1', 'amplitude=warp_fun_amp\n']))
        # todo: move this to a datafile
        for node, val in warping_values.items():
            strings.append(', '.join([str(node), str(val) + '\n']))
        return strings

    def _gen_mpc_strings(self, beam_node, shell_nodes, jtype):
        """ Returns the strings for the MPC keywords. """
        strings = []
        for node in shell_nodes:
            s = ', '.join(['*MPC', 'MODE=NODE', 'USER\n'])
            s += ', '.join([str(jtype), str(node), str(beam_node) + '\n'])
            strings.append(s)
        return strings


class AbaqusLinearCouplingWriter(AbaqusWriter):
    """ Writes the constraints for using in an Abaqus input file. """

    def __init__(self, output_dir, input_path_prepend=''):
        """ Constructor.
        :param str output_dir: Directory where files will be saved.
        :param str input_path_prepend: String prepended to the input specification in the keyword line.

        Notes:
            - Writes one file containing all they keywords to be added to the input file.
            - Writes one file per keyword containing the data lines.
            - Deletes any previous data or keyword files in the output directory upon construction.
            - If input_path_prepend is not empty, then the keyword line is modified as follows:
                *Equation, input=<input_path_prepend><filename>
            E.g., if input_path_prepend='constr_files/', then the keyword line will be:
                *Equation, input=constr_files/<filename>
            This parameter is useful to specify the absolute path of the files or a relative path to the
            Abaqus working directory.
        """
        AbaqusWriter.__init__(self, output_dir)
        self.input_path_prepend = input_path_prepend
        self.DATAFILE_BASE = 'Constr_Eqn_Def_'
        self.KEYWFILE_BASE = 'Equation_Keywords.txt'
        self._clear_output()
        return

    def write(self, couplings):
        """ Writes datafiles for the provided couplings.
        :param list couplings: [Coupling] The couplings to be written to file.

        Notes:
            - The keywords that need to be added are written in a single file.
            - The written files contain the data lines used in the analysis are written to separate files.
        """
        file_list = []
        constraint_num = 0
        for couple in couplings:
            for constraint in couple.constraints:
                # todo: make the filename based on the node and DOF
                filename = self.DATAFILE_BASE + str(constraint_num) + '.txt'
                filepath = os.path.join(self.output_dir, filename)
                file_list.append(self.input_path_prepend + filename)
                self._constraint_file_writer(constraint, filepath)
                constraint_num += 1
        keyword_file = os.path.join(self.output_dir, self.KEYWFILE_BASE)
        self._keyword_file_writer(file_list, keyword_file)
        return

    def _constraint_file_writer(self, constraint, file):
        """ Writes the data lines for the *EQUATION keyword for a given constraint.
        :param Constraint constraint: The constraint to write.
        :param str file: Full path to the file to write.
        """
        def term_string(t):
            return ', '.join([str(t.node), str(t.dof), str(t.coef)]) + '\n'
        with open(file, 'w') as f:
            f.write(str(len(constraint.terms)) + '\n')
            for term in constraint.terms:
                f.write(term_string(term))
        return

    def _keyword_file_writer(self, constraint_files, file):
        """ Writes the keyword file. """
        def keyword_string(input):
            return '*Equation, input=' + input + '\n'
        with open(file, 'w') as f:
            for c in constraint_files:
                f.write(keyword_string(c))
        return
