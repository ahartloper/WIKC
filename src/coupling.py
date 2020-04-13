
class ConstraintTerm:
    """ A single term in a linear constraint equation. """

    def __init__(self, node, dof, coef):
        """ Constructor.
        :param int node: Tag of the node.
        :param int dof: Degree of freedom at the node.
        :param float coef: Coefficient in the constraint.
        """
        self.node = node
        self.dof = dof
        self.coef = coef
        return


class Constraint:
    """ Defines a linear constraint equation in standard form.

    Standard form is:
        \\sum_i \\sum_j c^j_i u^j_i = 0,
    where i is the node ID, j indicates the DOF, c^j_i is the coefficient,
    and u^j_i is the DOF specified by i and j.
    The user needs to specify the node, DOF, and coefficient for all the terms in the equation.
    """

    def __init__(self):
        self.terms = []
        return

    def add_term(self, node, dof, coef):
        self.terms.append(ConstraintTerm(node, dof, coef))
        return


class BSCoupling:
    """ Defines a beam-to-shell coupling. """

    def __init__(self, shell_nodes, beam_node, coord_sys_id):
        """ Constructor.
        :param dict shell_nodes: Tags and local coordinates of the shell nodes.
        :param int beam_node: Tag of the beam node.
        :param int coord_sys_id: Tag of the coordinate system that relates the local and global coordinate systems.

        Creates the constraint equations for all the shell nodes.
        """
        # Data
        self.shell_nodes = shell_nodes
        self.beam_node = beam_node
        self.coord_sys_id = coords_id

        self.constraints = list()

        # Parameters
        self.SHELL_COEF = 1.0
        self.BEAM_DISP_COEF = -1.0

        # Process constraints
        self._construct_constraint_equations()
        return

    def _construct_constraint_equations(self):
        """ Adds all the constraint equations to the set of constraints. """
        for shell_id in shell_nodes.keys:
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
        constr.add_term(node=self.beam_node, dof=1, coef=-self.BEAM_DISP_COEF)
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
        constr.add_term(node=self.beam_node, dof=2, coef=-self.BEAM_DISP_COEF)
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
        constr.add_term(node=self.beam_node, dof=3, coef=-self.BEAM_DISP_COEF)
        # Beam rot x
        constr.add_term(node=self.beam_node, dof=4, coef=-self.shell_nodes[shell_id][1])
        # Beam rot y
        constr.add_term(node=self.beam_node, dof=5, coef=self.shell_nodes[shell_id][0])
        # Beam warping
        constr.add_term(node=self.beam_node, dof=7, coef=-self.shell_nodes[shell_id][0]*self.shell_nodes[shell_id][1])
        self.constraints.append(constr)
        return
