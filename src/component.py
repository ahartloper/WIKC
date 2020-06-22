import numpy as np


class ICoupling:
    """ Warping-Inclusive Kinematic Coupling for I-shaped cross-sections. """

    def __init__(self, beam_node, continuum_nodes, normal_dir, nonlinear_def, warping_def):
        """ Constructor.
        :param dict beam_node: {int: [float, float]} Beam node in the coupling in local coords.
        :param dict continuum_nodes: {int: [float, float]} Continuum nodes in the coupling in local coords.
        :param list normal_dir: [float, float, float] Vector defining the cross-section normal direction.
        :param bool nonlinear_def: If True, then nonlinear version of coupling used.
        :param bool warping_def: If True, then use warping-inclusive coupling.
        """
        self.beam_node = beam_node
        self.continuum_nodes = continuum_nodes
        self.normal_dir = normal_dir
        self.use_nonlinear = nonlinear_def
        self.include_warping = warping_def

        self.warping_fun = self._compute_warping_fun()

    def _compute_warping_fun(self):
        """ Returns the warping function evaluated at each node. """
        wfun = dict()
        for node_id, coords in self.continuum_nodes.items():
            wfun[node_id] = coords[0] * coords[1]
        return wfun


class CoordSys:
    """ Defines the local coordinate system in R^3 for a component. """

    def __init__(self, point, n1, n3):
        """ Constructor.
        :param np.ndarray point: Origin of the coord sys wrt the global coord sys.
        :param np.ndarray n1: Vector defining orientation of strong axis.
        :param np.ndarray n3: Vector defining orientation of the component centerline.
        """
        self.pt = point
        self.n1 = np.array(n1)
        self.n3 = np.array(n3)
        self.n2 = np.cross(self.n1, self.n3)


class IComponent:
    """ Defines the origin, nodes, and couplings for a component with an I-shaped cross-section. """

    def __init__(self, section, coord_sys, beam_nodes, continuum_nodes, couplings):
        """ Constructor.
        :param ISection section: Defines the geometry of the cross-section.
        :param CoordSys coord_sys: Origin and orientation of the component.
        :param dict beam_nodes: {int: [float, float]} Defines all the beam nodes.
        :param dict continuum_nodes: {int: [float, float]} Defines all the continuum nodes.
        :param list couplings: [Coupling] Defines the couplings in the component.
        """
        self.section = section
        self.coord_sys = coord_sys
        self.beam_domains = beam_domains
        self.continuum_domains = continuum_domains
        self.couplings = couplings
