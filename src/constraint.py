
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
