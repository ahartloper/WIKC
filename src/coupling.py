from .constraint import Constraint


class BSCoupling:
    """ Defines a beam-to-shell coupling. """

    def __init__(self, shell_nodes, beam_node, coord_sys):
        """ Constructor.
        :param dict shell_nodes: Tags and local coordinates of the shell nodes.
        :param int beam_node: Tag and coordinates of the beam node.
        :param int coord_sys: Transformation that relates the local and global coordinate systems.

        Creates the constraint equations for all the shell nodes.
        """
        # Data
        self.shell_nodes = shell_nodes
        self.beam_node = beam_node
        self.coord_sys = coord_sys

        self.constraints = list()

        # Parameters
        self.SHELL_COEF = 1.0
        self.BEAM_DISP_COEF = -1.0

        # Process constraints
        self._construct_constraint_equations()
        return

    def _construct_constraint_equations(self):
        """ Adds all the constraint equations to the set of constraints. """
        for shell_id in self.shell_nodes.keys():
            self._add_x_constraint(shell_id)
            self._add_y_constraint(shell_id)
            self._add_z_constraint(shell_id)
        return

    def _add_x_constraint(self, shell_id):
        """ Constraint for shell x displacement. """
        constr = Constraint()
        # Shell disp x
        constr.add_term(node=shell_id, dof=1, coef=self.SHELL_COEF)
        # Beam disp x
        constr.add_term(node=self.beam_node, dof=1, coef=self.BEAM_DISP_COEF)
        # Beam twist z
        constr.add_term(node=self.beam_node, dof=6, coef=self.shell_nodes[shell_id][1])
        self.constraints.append(constr)
        return

    def _add_y_constraint(self, shell_id):
        """ Constraint for shell y displacement. """
        constr = Constraint()
        # Shell disp y
        constr.add_term(node=shell_id, dof=2, coef=self.SHELL_COEF)
        # Beam disp y
        constr.add_term(node=self.beam_node, dof=2, coef=self.BEAM_DISP_COEF)
        # Beam twist z
        constr.add_term(node=self.beam_node, dof=6, coef=-self.shell_nodes[shell_id][0])
        self.constraints.append(constr)
        return

    def _add_z_constraint(self, shell_id):
        """ Constraint for shell y displacement. """
        constr = Constraint()
        # Shell disp z
        constr.add_term(node=shell_id, dof=3, coef=self.SHELL_COEF)
        # Beam disp z
        constr.add_term(node=self.beam_node, dof=3, coef=self.BEAM_DISP_COEF)
        # Beam rot x
        constr.add_term(node=self.beam_node, dof=4, coef=-self.shell_nodes[shell_id][1])
        # Beam rot y
        constr.add_term(node=self.beam_node, dof=5, coef=self.shell_nodes[shell_id][0])
        # Beam warping
        constr.add_term(node=self.beam_node, dof=7, coef=-self.shell_nodes[shell_id][0]*self.shell_nodes[shell_id][1])
        self.constraints.append(constr)
        return
