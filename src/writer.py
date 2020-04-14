import os


class AbaqusCouplingWriter:
    """ Writes the constraints for using in an Abaqus input file. """

    def __init__(self, output_dir, input_path_spec='filename'):
        """ Constructor.
        :param str output_dir: Directory where files will be saved.
        :param str input_path_spec: Use file name or full file path in input= optional parameter.

        Notes:
            - Deletes any previous data or keyword files in the output directory upon construction.
            - The values of input_path_spec are either: 'filename' or 'filepath'
                - 'filename' uses the name of the file (e.g., place the generated files in the working directory)
                - 'filepath' uses the full path (e.g., the files must be kept in the same location, but anywhere)
        """
        self.output_dir = output_dir
        self.input_path_spec = input_path_spec
        self.DATAFILE_BASE = 'Constr_Eqn_Def_'
        self.KEYWFILE_BASE = 'Equation_Keywords.txt'

        # Clear any existing files written
        file_list = os.listdir(self.output_dir)
        for f in file_list:
            if f[:len(self.DATAFILE_BASE)] == self.DATAFILE_BASE or f[:len(self.KEYWFILE_BASE)] == self.KEYWFILE_BASE:
                os.remove(os.path.join(self.output_dir, f))
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
                filename = self.DATAFILE_BASE + str(constraint_num) + '.txt'
                filepath = os.path.join(self.output_dir, filename)
                if self.input_path_spec == 'filename':
                    file_list.append(filename)
                elif self.input_path_spec == 'filepath':
                    file_list.append(filepath)
                else:
                    raise ValueError('Incorrect input_path_spec.')
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
